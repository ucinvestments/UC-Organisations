"""
Flask web application for orchestrating UCOP organization scrapers.
"""

import os
import sys
import threading
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, jsonify, request, send_file
import click

from config import ORGANIZATIONS, FLASK_CONFIG
from common.utils import (
    get_all_scrapers,
    load_organization_data,
    get_scrape_statistics,
    load_scraper_module
)


app = Flask(__name__)
app.config.update(FLASK_CONFIG)

# Track running scrapers
running_scrapers = {}
scraper_results = {}


@app.route('/')
def index():
    """Dashboard showing all organizations."""
    scrapers = get_all_scrapers()

    org_stats = []
    for scraper in scrapers:
        stats = get_scrape_statistics(scraper['org_dir'])
        stats['display_name'] = scraper['name']
        org_stats.append(stats)

    return render_template('index.html', organizations=org_stats)


@app.route('/organization/<org_dir>')
def organization_detail(org_dir):
    """Show details for a specific organization."""
    org_data = load_organization_data(org_dir)
    stats = get_scrape_statistics(org_dir)

    if not org_data:
        return f"Organization data not found for: {org_dir}", 404

    # Get staff list
    staff_files = list(Path(org_dir).rglob('staff/**/*.json'))
    staff_list = []

    for staff_file in staff_files:
        try:
            import json
            with open(staff_file, 'r') as f:
                staff_data = json.load(f)
                staff_data['file_path'] = str(staff_file)
                staff_list.append(staff_data)
        except Exception:
            pass

    return render_template(
        'organization.html',
        org_data=org_data,
        stats=stats,
        staff_list=staff_list,
        org_dir=org_dir
    )


@app.route('/api/status')
def api_status():
    """Get status of all organizations as JSON."""
    scrapers = get_all_scrapers()
    org_stats = []

    for scraper in scrapers:
        stats = get_scrape_statistics(scraper['org_dir'])
        stats['display_name'] = scraper['name']
        stats['is_running'] = scraper['org_dir'] in running_scrapers
        org_stats.append(stats)

    return jsonify(org_stats)


@app.route('/api/organization/<org_dir>')
def api_organization(org_dir):
    """Get organization data as JSON."""
    org_data = load_organization_data(org_dir)
    if not org_data:
        return jsonify({'error': 'Organization not found'}), 404

    return jsonify(org_data)


@app.route('/scrape/<org_dir>', methods=['POST'])
def scrape_organization(org_dir):
    """Trigger scraping for a specific organization."""
    if org_dir in running_scrapers:
        return jsonify({'error': 'Scraper already running for this organization'}), 400

    # Load the scraper module
    module = load_scraper_module(org_dir)
    if not module:
        return jsonify({'error': f'Scraper not found for {org_dir}'}), 404

    # Find the scraper class
    scraper_class = None
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (isinstance(attr, type) and
            hasattr(attr, '__bases__') and
            any('BaseScraper' in str(base) for base in attr.__bases__)):
            scraper_class = attr
            break

    if not scraper_class:
        return jsonify({'error': 'Scraper class not found in module'}), 500

    # Run scraper in background thread
    def run_scraper():
        try:
            running_scrapers[org_dir] = {
                'start_time': datetime.now().isoformat(),
                'status': 'running'
            }

            scraper = scraper_class()
            scraper.run()

            scraper_results[org_dir] = {
                'status': 'completed',
                'end_time': datetime.now().isoformat(),
                'stats': scraper.stats
            }
        except Exception as e:
            scraper_results[org_dir] = {
                'status': 'failed',
                'end_time': datetime.now().isoformat(),
                'error': str(e)
            }
        finally:
            if org_dir in running_scrapers:
                del running_scrapers[org_dir]

    thread = threading.Thread(target=run_scraper)
    thread.start()

    return jsonify({
        'message': f'Started scraping for {org_dir}',
        'org_dir': org_dir
    })


@app.route('/scrape/all', methods=['POST'])
def scrape_all():
    """Trigger scraping for all organizations."""
    scrapers = get_all_scrapers()

    triggered = []
    skipped = []

    for scraper in scrapers:
        org_dir = scraper['org_dir']
        if org_dir in running_scrapers:
            skipped.append(org_dir)
        else:
            # Trigger scrape (simplified - in production, use task queue)
            triggered.append(org_dir)

    return jsonify({
        'message': f'Triggered {len(triggered)} scrapers',
        'triggered': triggered,
        'skipped': skipped
    })


@app.route('/logs')
def view_logs():
    """View scraping logs."""
    log_dir = Path('logs')
    log_files = []

    if log_dir.exists():
        for log_file in log_dir.glob('*.log'):
            log_files.append({
                'name': log_file.name,
                'path': str(log_file),
                'size': log_file.stat().st_size,
                'modified': datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            })

    return render_template('logs.html', log_files=log_files)


@app.route('/logs/<log_file>')
def view_log_file(log_file):
    """View specific log file."""
    log_path = Path('logs') / log_file

    if not log_path.exists() or not log_path.is_file():
        return "Log file not found", 404

    # Read last 1000 lines
    with open(log_path, 'r') as f:
        lines = f.readlines()
        content = ''.join(lines[-1000:])

    return f"<pre>{content}</pre>"


# CLI commands
@app.cli.command()
@click.argument('org_dir')
def scrape(org_dir):
    """Run scraper for a specific organization from CLI."""
    click.echo(f"Starting scraper for {org_dir}...")

    module = load_scraper_module(org_dir)
    if not module:
        click.echo(f"Error: Scraper not found for {org_dir}", err=True)
        return

    # Find and run scraper class
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (isinstance(attr, type) and
            hasattr(attr, '__bases__') and
            any('BaseScraper' in str(base) for base in attr.__bases__)):
            scraper = attr()
            scraper.run()
            click.echo(f"Completed scraping for {org_dir}")
            return

    click.echo("Error: Scraper class not found", err=True)


@app.cli.command()
def scrape_all_cli():
    """Run all scrapers from CLI."""
    scrapers = get_all_scrapers()
    click.echo(f"Found {len(scrapers)} scrapers")

    for scraper_info in scrapers:
        org_dir = scraper_info['org_dir']
        click.echo(f"\n{'='*50}")
        click.echo(f"Scraping: {scraper_info['name']}")
        click.echo(f"{'='*50}\n")

        module = load_scraper_module(org_dir)
        if module:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    hasattr(attr, '__bases__') and
                    any('BaseScraper' in str(base) for base in attr.__bases__)):
                    try:
                        scraper = attr()
                        scraper.run()
                    except Exception as e:
                        click.echo(f"Error: {e}", err=True)
                    break


if __name__ == '__main__':
    app.run(
        host=FLASK_CONFIG['HOST'],
        port=FLASK_CONFIG['PORT'],
        debug=FLASK_CONFIG['DEBUG']
    )
