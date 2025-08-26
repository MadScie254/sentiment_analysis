#!/usr/bin/env python3
"""
Production deployment script for the sentiment analysis system
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def create_docker_file():
    """Create Dockerfile for containerization"""
    dockerfile_content = """# Sentiment Analysis API Docker Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "api_server.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created Dockerfile")

def create_docker_compose():
    """Create docker-compose.yml for easy deployment"""
    compose_content = """version: '3.8'

services:
  sentiment-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - sentiment-api
    restart: unless-stopped

volumes:
  logs:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("✅ Created docker-compose.yml")

def create_nginx_config():
    """Create nginx configuration"""
    nginx_content = """events {
    worker_connections 1024;
}

http {
    upstream sentiment_api {
        server sentiment-api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://sentiment_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://sentiment_api/health;
            access_log off;
        }
    }
}
"""
    
    with open("nginx.conf", "w") as f:
        f.write(nginx_content)
    print("✅ Created nginx.conf")

def create_systemd_service():
    """Create systemd service file for Linux deployment"""
    service_content = """[Unit]
Description=Sentiment Analysis API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/sentiment-analysis
Environment=PATH=/opt/sentiment-analysis/venv/bin
ExecStart=/opt/sentiment-analysis/venv/bin/python api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open("sentiment-analysis.service", "w") as f:
        f.write(service_content)
    print("✅ Created systemd service file")

def create_kubernetes_manifests():
    """Create Kubernetes deployment manifests"""
    
    # Deployment
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": "sentiment-analysis", "labels": {"app": "sentiment-analysis"}},
        "spec": {
            "replicas": 3,
            "selector": {"matchLabels": {"app": "sentiment-analysis"}},
            "template": {
                "metadata": {"labels": {"app": "sentiment-analysis"}},
                "spec": {
                    "containers": [{
                        "name": "sentiment-api",
                        "image": "sentiment-analysis:latest",
                        "ports": [{"containerPort": 8000}],
                        "env": [
                            {"name": "ENVIRONMENT", "value": "production"},
                            {"name": "API_HOST", "value": "0.0.0.0"},
                            {"name": "API_PORT", "value": "8000"}
                        ],
                        "resources": {
                            "requests": {"cpu": "100m", "memory": "256Mi"},
                            "limits": {"cpu": "500m", "memory": "512Mi"}
                        },
                        "livenessProbe": {
                            "httpGet": {"path": "/health", "port": 8000},
                            "initialDelaySeconds": 30,
                            "periodSeconds": 10
                        },
                        "readinessProbe": {
                            "httpGet": {"path": "/health", "port": 8000},
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5
                        }
                    }]
                }
            }
        }
    }
    
    # Service
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "sentiment-analysis-service"},
        "spec": {
            "selector": {"app": "sentiment-analysis"},
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": 8000}],
            "type": "LoadBalancer"
        }
    }
    
    # Ingress
    ingress = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": "sentiment-analysis-ingress",
            "annotations": {
                "kubernetes.io/ingress.class": "nginx",
                "cert-manager.io/cluster-issuer": "letsencrypt-prod"
            }
        },
        "spec": {
            "tls": [{"hosts": ["sentiment-api.yourdomain.com"], "secretName": "sentiment-tls"}],
            "rules": [{
                "host": "sentiment-api.yourdomain.com",
                "http": {
                    "paths": [{
                        "path": "/",
                        "pathType": "Prefix",
                        "backend": {
                            "service": {"name": "sentiment-analysis-service", "port": {"number": 80}}
                        }
                    }]
                }
            }]
        }
    }
    
    os.makedirs("k8s", exist_ok=True)
    
    with open("k8s/deployment.yaml", "w") as f:
        json.dump(deployment, f, indent=2)
    
    with open("k8s/service.yaml", "w") as f:
        json.dump(service, f, indent=2)
    
    with open("k8s/ingress.yaml", "w") as f:
        json.dump(ingress, f, indent=2)
    
    print("✅ Created Kubernetes manifests in k8s/ directory")

def create_deployment_scripts():
    """Create deployment scripts"""
    
    # Docker deployment script
    docker_deploy = """#!/bin/bash
set -e

echo "🚀 Deploying Sentiment Analysis API with Docker"

# Build the image
echo "📦 Building Docker image..."
docker build -t sentiment-analysis:latest .

# Stop existing container if running
echo "🛑 Stopping existing container..."
docker stop sentiment-api 2>/dev/null || true
docker rm sentiment-api 2>/dev/null || true

# Run the new container
echo "▶️  Starting new container..."
docker run -d \\
    --name sentiment-api \\
    -p 8000:8000 \\
    --restart unless-stopped \\
    sentiment-analysis:latest

echo "✅ Deployment completed!"
echo "🌐 API available at: http://localhost:8000"
echo "📖 Documentation at: http://localhost:8000/docs"
"""
    
    with open("deploy_docker.sh", "w") as f:
        f.write(docker_deploy)
    
    # Kubernetes deployment script
    k8s_deploy = """#!/bin/bash
set -e

echo "🚀 Deploying Sentiment Analysis API to Kubernetes"

# Apply manifests
echo "📦 Applying Kubernetes manifests..."
kubectl apply -f k8s/

# Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl rollout status deployment/sentiment-analysis

# Get service info
echo "📋 Service information:"
kubectl get services sentiment-analysis-service

echo "✅ Kubernetes deployment completed!"
"""
    
    with open("deploy_k8s.sh", "w") as f:
        f.write(k8s_deploy)
    
    # Make scripts executable on Unix systems
    try:
        os.chmod("deploy_docker.sh", 0o755)
        os.chmod("deploy_k8s.sh", 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    print("✅ Created deployment scripts")

def create_monitoring_config():
    """Create monitoring and logging configuration"""
    
    # Prometheus configuration
    prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'sentiment-analysis'
    static_configs:
      - targets: ['sentiment-api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
"""
    
    # Grafana dashboard
    grafana_dashboard = {
        "dashboard": {
            "title": "Sentiment Analysis API",
            "panels": [
                {
                    "title": "Request Rate",
                    "type": "graph",
                    "targets": [{"expr": "rate(http_requests_total[5m])"}]
                },
                {
                    "title": "Response Time",
                    "type": "graph", 
                    "targets": [{"expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"}]
                },
                {
                    "title": "Error Rate",
                    "type": "graph",
                    "targets": [{"expr": "rate(http_requests_total{status=~\"5..\"}[5m])"}]
                }
            ]
        }
    }
    
    os.makedirs("monitoring", exist_ok=True)
    
    with open("monitoring/prometheus.yml", "w") as f:
        f.write(prometheus_config)
    
    with open("monitoring/grafana-dashboard.json", "w") as f:
        json.dump(grafana_dashboard, f, indent=2)
    
    print("✅ Created monitoring configuration")

def main():
    """Main deployment preparation function"""
    print("🚀 Sentiment Analysis System - Deployment Setup")
    print("=" * 60)
    print("Creating deployment files and configurations...")
    print()
    
    try:
        create_docker_file()
        create_docker_compose()
        create_nginx_config()
        create_systemd_service()
        create_kubernetes_manifests()
        create_deployment_scripts()
        create_monitoring_config()
        
        print("\n" + "=" * 60)
        print("🎉 Deployment setup completed successfully!")
        print()
        print("📁 Created files:")
        print("   • Dockerfile - Container image definition")
        print("   • docker-compose.yml - Multi-container setup")
        print("   • nginx.conf - Reverse proxy configuration")
        print("   • sentiment-analysis.service - Systemd service")
        print("   • k8s/ - Kubernetes manifests")
        print("   • deploy_docker.sh - Docker deployment script")
        print("   • deploy_k8s.sh - Kubernetes deployment script")
        print("   • monitoring/ - Monitoring configuration")
        print()
        print("🚀 Deployment Options:")
        print("   1. Docker: ./deploy_docker.sh")
        print("   2. Docker Compose: docker-compose up -d")
        print("   3. Kubernetes: ./deploy_k8s.sh")
        print("   4. Systemd: sudo systemctl enable sentiment-analysis")
        print()
        print("📊 Monitoring:")
        print("   • Prometheus: monitoring/prometheus.yml")
        print("   • Grafana: monitoring/grafana-dashboard.json")
        print("   • Health check: /health endpoint")
        print()
        print("🔧 Next Steps:")
        print("   1. Test the system: python test_system.py")
        print("   2. Build Docker image: docker build -t sentiment-analysis .")
        print("   3. Deploy using your preferred method")
        print("   4. Monitor the application")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
