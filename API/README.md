# UC Organizations Scraper System

A Flask-based web scraping orchestrator for all University of California organizations. This system provides a distributed scraper architecture where each organization has its own scraper module, orchestrated through a central Flask web application.

Organizations include:
- **UCOP** (UC Office of the President) organizations
- **Academic Senate**
- **Board of Regents**
- **UC Campuses** (Berkeley, Davis, Irvine, Los Angeles, Merced, Riverside, San Diego, San Francisco, Santa Barbara, Santa Cruz)
- **National Laboratories** (Lawrence Berkeley, Lawrence Livermore, Los Alamos)

## Features

- **Distributed Architecture**: Each organization directory contains its own `scraper.py` file
- **Web Dashboard**: Flask-powered web interface for managing and monitoring scrapers
- **CLI Support**: Run scrapers individually or in batch via command-line
- **Comprehensive Logging**: Per-organization logging with detailed statistics
- **Modular Design**: Shared base class and utilities prevent code duplication
- **REST API**: JSON API endpoints for programmatic access
- **Auto-discovery**: Automatically detects and loads all scraper modules

## Directory Structure

```
API/
├── app.py                          # Flask orchestrator application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Docker container definition
├── docker-run.sh                   # Docker run script
├── common/                         # Shared modules
│   ├── __init__.py
│   ├── base_scraper.py            # Abstract base scraper class
│   └── utils.py                   # Utility functions
├── templates/                      # Flask HTML templates
│   ├── index.html                 # Dashboard
│   ├── organization.html          # Organization detail view
│   └── logs.html                  # Logs viewer
├── static/
│   └── style.css                  # CSS styling
├── logs/                          # Scraping logs (auto-created)
│
├── ucop/                          # UCOP organizations
│   ├── academic_affairs/
│   │   ├── scraper.py             # Organization-specific scraper
│   │   ├── organization.json      # (created by scraper)
│   │   └── staff/                 # (created by scraper)
│   ├── ethics_compliance_audit_services/
│   ├── external_relations_communications/
│   ├── uc_finance/
│   ├── uc_investments/
│   ├── uc_legal/
│   ├── uc_national_laboratories/
│   ├── uc_operations/
│   ├── university_of_california_health/
│   └── systemwide_office_of_civil_rights/
│
├── academic_senate/               # UC Academic Senate
│   └── scraper.py                 # (to be implemented)
│
├── board_of_regents/              # UC Board of Regents
│   └── scraper.py                 # (to be implemented)
│
├── campuses/                      # UC Campuses
│   ├── berkeley/
│   │   └── scraper.py             # (to be implemented)
│   ├── davis/
│   ├── irvine/
│   ├── los_angeles/
│   ├── merced/
│   ├── riverside/
│   ├── san_diego/
│   ├── san_francisco/
│   ├── santa_cruz/
│   └── santa_barbara/
│
└── labs/                          # National Laboratories
    ├── lawrence_berkeley_national_laboratory/
    │   └── scraper.py             # (to be implemented)
    ├── lawrence_livermore_national_laboratory/
    └── los_alamos_national_laboratory/
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Verify installation:**

```bash
python -m flask --version
```

## Usage

### Web Interface

#### Start the Flask App

```bash
python app.py
```

Or using Flask CLI:

```bash
export FLASK_APP=app.py
flask run
```

The web dashboard will be available at `http://localhost:5000`

#### Web Features

- **Dashboard** (`/`): View all organizations, staff counts, and scraping status
- **Organization Detail** (`/organization/<org_dir>`): Detailed view of organization data and staff
- **Logs** (`/logs`): View scraping logs for debugging
- **API Endpoints**: JSON endpoints for programmatic access

### Command-Line Interface

#### Run Individual Scraper

Run a specific organization's scraper:

```bash
python <org_directory>/scraper.py
```

Example:

```bash
# UCOP organization
python ucop/ethics_compliance_audit_services/scraper.py

# Campus (when implemented)
python campuses/berkeley/scraper.py
```

#### Using Flask CLI

```bash
# Scrape a specific UCOP organization
flask scrape ucop/ethics_compliance_audit_services

# Scrape a campus (when implemented)
flask scrape campuses/berkeley

# Scrape all organizations
flask scrape-all-cli
```

### API Endpoints

#### Get Status of All Organizations

```bash
curl http://localhost:5000/api/status
```

#### Get Organization Data

```bash
# UCOP organization
curl http://localhost:5000/api/organization/ucop/academic_affairs

# Campus (when implemented)
curl http://localhost:5000/api/organization/campuses/berkeley
```

#### Trigger Scraping

```bash
# Scrape specific UCOP organization
curl -X POST http://localhost:5000/scrape/ucop/ethics_compliance_audit_services

# Scrape a campus (when implemented)
curl -X POST http://localhost:5000/scrape/campuses/berkeley

# Scrape all organizations
curl -X POST http://localhost:5000/scrape/all
```

## Configuration

Edit `config.py` to modify:

- Organization URLs
- Scraper settings (delays, retries, timeouts)
- Flask server settings

Example:

```python
SCRAPER_SETTINGS = {
    "user_agent": "UCOP-Scraper/1.0 (Educational Research)",
    "delay_between_requests": 2,  # seconds
    "max_retries": 3,
    "timeout": 10  # seconds
}
```

## Creating New Scrapers

To add a new organization scraper:

### For UCOP Organizations

1. **Create organization directory:**

```bash
mkdir ucop/new_organization
```

2. **Add to config.py (UCOP_ORGANIZATIONS):**

```python
UCOP_ORGANIZATIONS = {
    "ucop/new_organization": {
        "name": "New Organization",
        "main_url": "https://www.ucop.edu/new-org/index.html",
        "staff_urls": {
            "main": "https://www.ucop.edu/new-org/staff/index.html"
        }
    }
}
```

3. **Create scraper.py:** (use existing UCOP scrapers as template)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from common.base_scraper import BaseScraper
from config import ORGANIZATIONS

class NewOrgScraper(BaseScraper):
    def __init__(self):
        org_config = ORGANIZATIONS['ucop/new_organization']
        super().__init__(
            org_name=org_config['name'],
            org_dir='ucop/new_organization',
            base_url=org_config['main_url']
        )
        self.staff_urls = org_config['staff_urls']

    def scrape_organization(self):
        # Implementation here
        pass

    def scrape_staff(self):
        # Implementation here
        pass

if __name__ == '__main__':
    scraper = NewOrgScraper()
    scraper.run()
```

### For Campuses, Labs, etc.

Follow the same pattern but place the scraper in the appropriate directory:
- `campuses/campus_name/scraper.py`
- `labs/lab_name/scraper.py`
- `academic_senate/scraper.py`
- `board_of_regents/scraper.py`

The Flask app will automatically discover scrapers in these locations.

## Output Format

### Organization JSON

```json
{
  "name": "Organization Name",
  "data_source": "https://...",
  "description": "...",
  "leadership": [...],
  "sub_departments": [...],
  "contact": {...},
  "scraped_at": "2025-10-25T12:00:00"
}
```

### Staff JSON

```json
{
  "name": "John Doe",
  "title": "Director",
  "department": "Leadership",
  "organization": "Organization Name",
  "contact": {
    "phone": "(510) 123-4567",
    "email": "john.doe@ucop.edu"
  },
  "data_source": "https://..."
}
```

## Troubleshooting

### Scraper not found

Make sure the scraper file exists and contains a class inheriting from `BaseScraper`:

```bash
ls -la <org_directory>/scraper.py
```

### Import errors

Ensure you're running from the API base directory and dependencies are installed:

```bash
cd /path/to/API
pip install -r requirements.txt
```

### View logs

Check the logs directory for detailed error information:

```bash
cat logs/<org_directory>.log
```

Or use the web interface at `http://localhost:5000/logs`

## Organizations Included

### UCOP Organizations (Implemented)
1. Academic Affairs
2. Ethics, Compliance and Audit Services
3. External Relations and Communications
4. UC Finance
5. UC Investments
6. UC Legal - Office of the General Counsel
7. UC National Laboratories
8. UC Operations
9. University of California Health
10. Systemwide Office of Civil Rights

### Other Organizations (Structure Ready)
- Academic Senate
- Board of Regents
- 10 UC Campuses (Berkeley, Davis, Irvine, LA, Merced, Riverside, San Diego, San Francisco, Santa Barbara, Santa Cruz)
- 3 National Laboratories (Lawrence Berkeley, Lawrence Livermore, Los Alamos)

## Technical Details

### Base Scraper Class

All scrapers inherit from `BaseScraper` which provides:

- HTTP fetching with retry logic and rate limiting
- HTML parsing with BeautifulSoup
- JSON file management
- Directory structure creation
- Comprehensive logging
- Statistics tracking

### Utilities Module

Common functions for:

- Name normalization
- Text cleaning
- Phone number formatting
- Email validation
- Scraper discovery
- Data loading

## Best Practices

1. **Rate Limiting**: Default 2-second delay between requests
2. **Error Handling**: All errors logged, scraping continues
3. **Incremental Updates**: Re-run scrapers to update data
4. **Logging**: Check logs for debugging
5. **Testing**: Test individual scrapers before batch runs

## License

Educational use only. Respect UC website terms of service and robots.txt.

## Support

For issues or questions, check the logs directory or review scraper implementation.
