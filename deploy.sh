#!/bin/bash
# Production Deployment Script for Sentiment Analysis System

set -e  # Exit on any error

echo "🚀 Starting Production Deployment of Sentiment Analysis System"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.production .env
        print_warning "Please edit .env file with your configuration before continuing."
        read -p "Press Enter to continue after editing .env file..."
    fi
    
    print_success "Prerequisites check completed"
}

# Setup directories
setup_directories() {
    print_status "Setting up directories..."
    
    mkdir -p logs cache data ssl
    chmod 755 logs cache data
    
    print_success "Directories created"
}

# Build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Stop existing services
    docker-compose down --remove-orphans
    
    # Build and start services
    docker-compose build --no-cache
    docker-compose up -d
    
    print_success "Services deployed"
}

# Wait for services to be healthy
wait_for_services() {
    print_status "Waiting for services to be healthy..."
    
    # Wait for main app
    for i in {1..30}; do
        if curl -f http://localhost:5000/api/health >/dev/null 2>&1; then
            print_success "Main application is healthy"
            break
        fi
        
        if [ $i -eq 30 ]; then
            print_error "Main application failed to start within 5 minutes"
            docker-compose logs sentiment-app
            exit 1
        fi
        
        print_status "Waiting for main application... ($i/30)"
        sleep 10
    done
    
    # Wait for Redis
    if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
        print_success "Redis is healthy"
    else
        print_warning "Redis health check failed"
    fi
}

# Run tests
run_tests() {
    print_status "Running production tests..."
    
    # API health check
    if curl -f http://localhost:5000/api/health >/dev/null 2>&1; then
        print_success "API health check passed"
    else
        print_error "API health check failed"
        return 1
    fi
    
    # Test sentiment analysis endpoint
    response=$(curl -s -X POST http://localhost:5000/api/analyze \
        -H "Content-Type: application/json" \
        -d '{"text":"This is a great test!"}')
    
    if echo "$response" | grep -q '"success": true'; then
        print_success "Sentiment analysis endpoint test passed"
    else
        print_error "Sentiment analysis endpoint test failed"
        echo "Response: $response"
        return 1
    fi
    
    # Test news endpoint
    if curl -f http://localhost:5000/api/news >/dev/null 2>&1; then
        print_success "News endpoint test passed"
    else
        print_warning "News endpoint test failed (may be expected if no news data)"
    fi
    
    print_success "All tests passed"
}

# Show deployment information
show_deployment_info() {
    print_success "🎉 Deployment completed successfully!"
    echo
    echo "==================== DEPLOYMENT INFO ===================="
    echo "Dashboard URL:     http://localhost"
    echo "API Base URL:      http://localhost/api"
    echo "Health Check:      http://localhost/api/health"
    echo "Prometheus:        http://localhost:9090"
    echo "Grafana:           http://localhost:3000"
    echo
    echo "==================== USEFUL COMMANDS ===================="
    echo "View logs:         docker-compose logs -f"
    echo "Check status:      docker-compose ps"
    echo "Stop services:     docker-compose down"
    echo "Restart app:       docker-compose restart sentiment-app"
    echo "Update app:        ./deploy.sh"
    echo
    echo "==================== MONITORING ===================="
    echo "Container Stats:   docker stats"
    echo "App Logs:          docker-compose logs sentiment-app"
    echo "Nginx Logs:        docker-compose logs nginx"
    echo "System Resources:  docker system df"
    echo
    echo "🔧 For configuration changes, edit .env and run: docker-compose restart"
    echo "📖 For documentation, see README.md"
}

# Cleanup function
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Deployment failed. Cleaning up..."
        docker-compose down --remove-orphans
    fi
}

# Set trap for cleanup
trap cleanup EXIT

# Main deployment flow
main() {
    echo "📊 Sentiment Analysis System - Production Deployment"
    echo "===================================================="
    
    check_prerequisites
    setup_directories
    deploy_services
    wait_for_services
    run_tests
    show_deployment_info
    
    print_success "🚀 Production deployment completed successfully!"
}

# Parse command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "test")
        run_tests
        ;;
    "stop")
        print_status "Stopping services..."
        docker-compose down
        print_success "Services stopped"
        ;;
    "restart")
        print_status "Restarting services..."
        docker-compose restart
        print_success "Services restarted"
        ;;
    "logs")
        docker-compose logs -f "${2:-sentiment-app}"
        ;;
    "status")
        docker-compose ps
        ;;
    "update")
        print_status "Updating application..."
        docker-compose build --no-cache sentiment-app
        docker-compose up -d sentiment-app
        wait_for_services
        run_tests
        print_success "Application updated"
        ;;
    *)
        echo "Usage: $0 {deploy|test|stop|restart|logs|status|update}"
        echo
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  test    - Run production tests"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  logs    - Show logs (specify service name as second arg)"
        echo "  status  - Show service status"
        echo "  update  - Update application only"
        exit 1
        ;;
esac
