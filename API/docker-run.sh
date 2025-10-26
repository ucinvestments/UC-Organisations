#!/bin/bash

# Docker helper script for UCOP Scraper

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Function to build the image
build() {
    print_info "Building Docker image..."
    docker-compose build
    print_info "Build complete!"
}

# Function to start the containers
start() {
    print_info "Starting UCOP Scraper..."
    docker-compose up -d
    print_info "Container started!"
    print_info "Web interface available at: http://localhost:5000"
}

# Function to stop the containers
stop() {
    print_info "Stopping UCOP Scraper..."
    docker-compose down
    print_info "Container stopped!"
}

# Function to view logs
logs() {
    docker-compose logs -f
}

# Function to restart
restart() {
    stop
    start
}

# Function to run a scraper
scrape() {
    if [ -z "$1" ]; then
        print_error "Please specify an organization to scrape"
        print_info "Usage: $0 scrape <organization_name>"
        exit 1
    fi

    print_info "Running scraper for: $1"
    docker-compose exec ucop-scraper python "$1/scraper.py"
}

# Function to run all scrapers
scrape_all() {
    print_info "Running all scrapers..."
    docker-compose exec ucop-scraper flask scrape-all-cli
}

# Function to show status
status() {
    print_info "Container status:"
    docker-compose ps
    echo ""
    print_info "Health status:"
    docker inspect ucop-scraper --format='{{.State.Health.Status}}' 2>/dev/null || echo "Not running"
}

# Function to open shell in container
shell() {
    print_info "Opening shell in container..."
    docker-compose exec ucop-scraper /bin/bash
}

# Function to clean up
clean() {
    print_warn "This will remove all containers and images. Continue? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_info "Cleaning up..."
        docker-compose down --rmi all --volumes
        print_info "Cleanup complete!"
    else
        print_info "Cleanup cancelled."
    fi
}

# Main script
case "$1" in
    build)
        check_docker
        build
        ;;
    start)
        check_docker
        start
        ;;
    stop)
        check_docker
        stop
        ;;
    restart)
        check_docker
        restart
        ;;
    logs)
        check_docker
        logs
        ;;
    scrape)
        check_docker
        scrape "$2"
        ;;
    scrape-all)
        check_docker
        scrape_all
        ;;
    status)
        check_docker
        status
        ;;
    shell)
        check_docker
        shell
        ;;
    clean)
        check_docker
        clean
        ;;
    *)
        echo "UCOP Scraper Docker Helper"
        echo ""
        echo "Usage: $0 {build|start|stop|restart|logs|scrape|scrape-all|status|shell|clean}"
        echo ""
        echo "Commands:"
        echo "  build       - Build the Docker image"
        echo "  start       - Start the containers"
        echo "  stop        - Stop the containers"
        echo "  restart     - Restart the containers"
        echo "  logs        - View container logs (follow mode)"
        echo "  scrape      - Run a specific scraper (e.g., ./docker-run.sh scrape academic_affairs)"
        echo "  scrape-all  - Run all scrapers"
        echo "  status      - Show container status"
        echo "  shell       - Open a shell in the container"
        echo "  clean       - Remove all containers and images"
        echo ""
        exit 1
        ;;
esac
