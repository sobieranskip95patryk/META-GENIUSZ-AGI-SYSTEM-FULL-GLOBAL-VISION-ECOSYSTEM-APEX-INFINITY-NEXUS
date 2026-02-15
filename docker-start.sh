#!/bin/bash
# GOK:AI Docker Quick Start Script
# Purpose: Simple one-command startup for Docker environment

set -e

echo "=========================================="
echo "GOK:AI Docker Quick Start"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from https://www.docker.com/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/"
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Parse command
COMMAND=${1:-up}

case $COMMAND in
    up)
        echo "🚀 Starting GOK:AI Docker environment..."
        docker-compose build --no-cache
        docker-compose up -d
        echo ""
        echo "✅ Environment started!"
        echo ""
        echo "Services running:"
        docker-compose ps
        echo ""
        echo "Access points:"
        echo "  Main App:    http://localhost:8080"
        echo "  MTaQuest:    http://localhost:5000"
        echo "  API Gateway: http://localhost:8000"
        echo "  Neo4j:       http://localhost:7474"
        echo "  Redis:       localhost:6379"
        echo ""
        ;;
    
    down)
        echo "🛑 Stopping GOK:AI Docker environment..."
        docker-compose down
        echo "✅ Environment stopped"
        ;;
    
    logs)
        echo "📋 Displaying logs..."
        docker-compose logs -f
        ;;
    
    restart)
        echo "🔄 Restarting GOK:AI Docker environment..."
        docker-compose restart
        docker-compose ps
        ;;
    
    shell)
        SERVICE=${2:-gok-app}
        echo "🐚 Entering shell in $SERVICE container..."
        docker-compose exec $SERVICE bash
        ;;
    
    status)
        echo "📊 GOK:AI Docker environment status:"
        docker-compose ps
        echo ""
        docker-compose logs --tail=20
        ;;
    
    clean)
        echo "🧹 Cleaning up Docker resources..."
        docker-compose down -v
        docker system prune -f
        echo "✅ Cleanup complete"
        ;;
    
    *)
        echo "Usage: $0 {up|down|logs|restart|shell|status|clean}"
        echo ""
        echo "Commands:"
        echo "  up       - Start Docker environment (default)"
        echo "  down     - Stop Docker environment"
        echo "  logs     - View container logs"
        echo "  restart  - Restart containers"
        echo "  shell    - Enter shell in a container"
        echo "  status   - Check environment status"
        echo "  clean    - Remove all Docker resources"
        exit 1
        ;;
esac

echo ""
