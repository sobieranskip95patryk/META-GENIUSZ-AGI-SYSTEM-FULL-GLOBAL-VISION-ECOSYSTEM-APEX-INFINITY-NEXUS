# GOK:AI Repository Structure & Architecture Guide

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2026  

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Repository Structure](#repository-structure)
3. [Module Descriptions](#module-descriptions)
4. [Setup Instructions](#setup-instructions)
5. [Docker Deployment](#docker-deployment)
6. [Development Workflow](#development-workflow)
7. [Deployment Pipeline](#deployment-pipeline)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Local Development (Python)
```bash
# Setup
bash setup-dev.sh           # Linux/macOS
setup-dev.bat              # Windows

# Run
python main.py

# Test
make test
```

### Docker (Recommended)
```bash
# Start full stack
bash docker-start.sh up

# Access services
# Main App:    http://localhost:8080
# MTaQuest:    http://localhost:5000
# API:         http://localhost:8000
# Neo4j:       http://localhost:7474
```

### Google Cloud (Production)
```bash
# Deploy
bash deploy-gcp.sh

# Access via Cloud Run URL
```

---

## 📁 Repository Structure

```
AGI_GOK/
├── CORE/                          # Central inference engine
│   ├── Inference/                 # Inference engines & reasoning
│   │   ├── t_causality_orchestrator.py
│   │   ├── global_vision_analyzer.py
│   │   ├── causal_inference_engine.py
│   │   └── ... (20+ inference modules)
│   ├── Memory/                    # Memory systems
│   │   ├── long_term_graph.py
│   │   ├── sensory_buffer.py
│   │   ├── attention_mechanism.py
│   │   └── ... (Memory manifests & axioms)
│   ├── Structures/                # Data structures
│   └── spiral_pipeline.py         # Main orchestrator
│
├── INFRA/                         # Infrastructure & Services
│   ├── Services/                  # Microservices
│   │   ├── api_server.py          # REST API Gateway
│   │   ├── mtaquest_bridge.py     # MTaQuest bridge
│   │   └── neuronal_bridge_server.py
│   ├── Environment/               # Environment management
│   ├── Diagnostics/               # Health checks
│   ├── scaling_manager_v3.py      # GCP scaling
│   └── requirements.txt
│
├── MTAQUEST/                      # Hybrid Dialog Platform
│   ├── hybrid_dialog_protocol.py  # Core protocol
│   ├── intent_quantization.py     # IQE module
│   ├── vector_synchronization.py  # VSE module
│   ├── README.md                  # Complete guide
│   ├── INTEGRATION_GUIDE.md
│   └── requirements.txt
│
├── ECONOMY/                       # Application Layer
│   ├── ESG_Scoring_Kernel.py      # ESG scoring system
│   ├── Drift_Money_Kernel/        # Economic models
│   └── Only_Together_System/      # Cooperative economics
│
├── META/                          # Self-Optimization
│   ├── Ethics_Alignment/          # Ethical reasoning
│   └── Self_Optimization/         # Hyperparameter evolution
│
├── PERCEPTION/                    # Data Integration
│   ├── Language/                  # NLP & linguistic analysis
│   └── Sensors/                   # Data acquisition
│
├── SECURE/                        # Security Layer
│   └── Anonymous_Firewall/        # Privacy protection
│
├── CONFIG/                        # Configuration
│   ├── config.yaml                # Main configuration
│   ├── gcp_project_config.yaml    # GCP settings
│   └── .env.example               # Template
│
├── PAPERS/                        # Publications
│   └── (T_Causality WhitePaper, etc.)
│
├── FRONTEND/                      # Web Interface
│   └── index.html                 # Dashboard
│
├── tests/                         # Test Suite
│   ├── test_ags_gcp.py            # AGS autonomy tests
│   ├── test_global_vision.py
│   └── test_t_causality.py
│
├── Docker Configuration
│   ├── Dockerfile                 # Production image
│   ├── Dockerfile.mtaquest        # MTaQuest service
│   ├── Dockerfile.api             # API gateway
│   ├── docker-compose.yml         # Dev environment
│   ├── docker-compose.mtaquest.yml
│   ├── docker-compose.prod.yml    # Production
│   └── .dockerignore
│
├── Scripts
│   ├── setup-dev.sh               # Dev setup (Linux/macOS)
│   ├── setup-dev.bat              # Dev setup (Windows)
│   ├── build-docker.sh            # Docker build
│   ├── docker-start.sh            # Quick Docker start
│   └── deploy-gcp.sh              # GCP deployment
│
├── Configuration Files
│   ├── main.py                    # Main entry point
│   ├── requirements.txt           # Python dependencies
│   ├── Makefile                   # Make commands
│   ├── Procfile                   # Heroku deployment
│   ├── netlify.toml               # Netlify config
│   ├── vercel.json                # Vercel config
│   ├── LICENSE
│   └── README.md
│
└── Documentation (.md files)
    ├── ACTION_PLAN.md
    ├── IMPLEMENTATION_STATUS.md
    ├── BUILD_REPORT.md
    ├── DIRECTIVE_II_*.md (8 files)
    └── ... (40+ documentation files)
```

---

## 🔧 Module Descriptions

### CORE/ - Central Intelligence Engine
**Purpose:** Main reasoning, inference, and knowledge processing

**Key Components:**
- **t_causality_orchestrator.py** - Causal reasoning orchestration
- **global_vision_analyzer.py** - System-wide vision analysis
- **causal_inference_engine.py** - Causal inference
- **knowledge_fusion.py** - Knowledge integration
- **free_will_codification.py** - Autonomy & decision-making
- **long_term_graph.py** - Persistent knowledge graph

**Usage:**
```python
from CORE.spiral_pipeline import ASQK_Orchestrator
orchestrator = ASQK_Orchestrator()
result = orchestrator.process(query)
```

---

### INFRA/ - Infrastructure & Services
**Purpose:** API, service orchestration, and cloud integration

**Key Components:**
- **api_server.py** - REST API with Gemini integration
- **mtaquest_bridge.py** - MTaQuest protocol bridge
- **scaling_manager_v3.py** - GCP auto-scaling
- **neuronal_bridge_server.py** - Neural service bridge

**Services:**
- REST API (Port 8080)
- MTaQuest Server (Port 5000)
- Neuronal Bridge (Port 9000+)

---

### MTAQUEST/ - Hybrid Dialog Platform
**Purpose:** Advanced dialog protocol with intent quantization

**Key Components:**
- **hybrid_dialog_protocol.py** - HDP core protocol
- **intent_quantization.py** - IQE intent engine
- **vector_synchronization.py** - VSE vector engine

**Capabilities:**
- Multi-turn conversations
- Intent quantization
- Vector synchronization with Neo4j
- Real-time response generation

---

### ECONOMY/ - Application Layer
**Purpose:** Business applications and use cases

**Key Systems:**
- **ESG_Scoring_Kernel.py** - Environmental, Social, Governance scoring
- **Drift_Money_Kernel/** - Economic modeling
- **Only_Together_System/** - Cooperative economics

---

### META/ - Self-Optimization
**Purpose:** System improvement and alignment

**Subsystems:**
- **Ethics_Alignment/** - Ethical constraints & reasoning
- **Self_Optimization/** - Hyperparameter evolution & learning

---

---

## 🔨 Setup Instructions

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (recommended)
- Google Cloud SDK (for GCP deployment)
- 4GB RAM minimum (8GB recommended)

### Local Setup (Python)

**Linux/macOS:**
```bash
# Clone repository (if using git)
git clone <repo-url>
cd AGI_GOK

# Run setup script
bash setup-dev.sh

# Activate environment
source .venv/bin/activate

# Run application
python main.py
```

**Windows:**
```batch
# Clone repository
git clone <repo-url>
cd AGI_GOK

# Run setup script
setup-dev.bat

# Run application (venv already activated)
python main.py
```

### Verify Installation
```bash
# Test imports
python -c "from CORE.spiral_pipeline import *; print('✓ CORE loaded')"
python -c "from INFRA.Services.api_server import *; print('✓ INFRA loaded')"

# Run tests
pytest tests/ -v
```

---

## 🐳 Docker Deployment

### Quick Start
```bash
# One-command start (Linux/macOS)
bash docker-start.sh up

# Or use Docker Compose directly
docker-compose up -d

# Verify services
docker-compose ps
```

### Services Configuration

**docker-compose.yml** includes:
- **gok-app** - Main application (Port 8080)
- **mtaquest-server** - MTaQuest service (Port 5000)
- **neo4j** - Graph database (Port 7474)
- **redis** - Cache layer (Port 6379)
- **api-gateway** - API service (Port 8000)

### Building Custom Images
```bash
# Build all images
bash build-docker.sh

# Build specific image
docker build -f Dockerfile -t gok-ai:custom .

# Push to registry
docker tag gok-ai:custom gcr.io/PROJECT/gok-ai:custom
docker push gcr.io/PROJECT/gok-ai:custom
```

### Production Docker Setup
```bash
# Use production compose
docker-compose -f docker-compose.prod.yml up -d

# With environment variables
export GCP_PROJECT=meta-geniusz-gok-turbo
export GCP_REGION=us-central1
export APP_VERSION=1.0.0
docker-compose -f docker-compose.prod.yml up -d
```

---

## 👨‍💻 Development Workflow

### Using Make Commands
```bash
# Available commands
make help

# Development setup
make dev

# Run application
make run

# Testing
make test                 # Run tests
make test-cov            # With coverage

# Code quality
make lint                # Run linters
make format              # Format code

# Docker
make docker-build        # Build images
make docker-up           # Start stack
make docker-down         # Stop stack
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and test
python main.py
pytest tests/

# Commit
git add .
git commit -m "feat: new feature description"

# Push
git push origin feature/new-feature
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_ags_gcp.py -v

# Run with coverage
pytest tests/ --cov=CORE --cov=INFRA --cov-report=html

# Run specific test
pytest tests/test_ags_gcp.py::TestAGS::test_autonomy -v
```

---

## 🚀 Deployment Pipeline

### Local → Docker → Cloud

**Step 1: Local Testing**
```bash
make test
make lint
```

**Step 2: Docker Build**
```bash
bash build-docker.sh gok-ai latest
```

**Step 3: Push to Registry**
```bash
docker push gcr.io/PROJECT/gok-ai:latest
```

**Step 4: Deploy to Cloud Run**
```bash
bash deploy-gcp.sh
```

### CI/CD Integration

**GitHub Actions Example:**
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and Deploy
        run: bash deploy-gcp.sh
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# API Configuration
API_KEY=your-gemini-api-key
API_HOST=0.0.0.0
API_PORT=8080

# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Cache
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=password

# GCP
GCP_PROJECT=meta-geniusz-gok-turbo
GCP_REGION=us-central1

# Logging
LOG_LEVEL=INFO
DEBUG=False
```

### Config Files
- **CONFIG/config.yaml** - Main system configuration
- **CONFIG/gcp_project_config.yaml** - GCP-specific settings
- **.env.example** - Environment template
- **Makefile** - Development commands

---

## 🆘 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs gok-app

# Rebuild without cache
docker-compose build --no-cache

# Reset volumes
docker-compose down -v
docker-compose up -d
```

**Port conflicts:**
```bash
# Find process using port 8080
lsof -i :8080

# Use different port
docker-compose -f docker-compose.yml -e PORT=9090 up
```

### Python Issues

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.10+

# Clear cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

**Module not found:**
```bash
# Add to PYTHONPATH
export PYTHONPATH=$PWD:$PYTHONPATH

# Or run from repo root
cd /path/to/AGI_GOK
python -c "from CORE import *"
```

### Database Issues

**Neo4j connection failed:**
```bash
# Check if Neo4j is running
docker-compose ps | grep neo4j

# Restart Neo4j
docker-compose restart neo4j

# Check logs
docker-compose logs neo4j
```

**Redis connection failed:**
```bash
# Check Redis status
redis-cli ping

# Or via Docker
docker-compose exec redis redis-cli ping
```

### API Issues

**API Server not responding:**
```bash
# Check if service is running
curl http://localhost:8080/health

# Check logs
docker-compose logs api-gateway

# Restart service
docker-compose restart api-gateway
```

---

## 📚 Additional Resources

- **T_CAUSALITY_WHITEPAPER.md** - Technical whitepaper
- **MTAQUEST/README.md** - MTaQuest platform guide
- **DIRECTIVE_II_EXECUTION_PLAN.md** - Execution roadmap
- **BUILD_REPORT.md** - System build details
- **REPOSITORY_ENCYCLOPEDIA.md** - Complete reference

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review relevant documentation files
3. Check logs: `docker-compose logs`
4. Run tests: `pytest tests/ -v`

---

**Status:** ✅ Production Ready  
**Last Updated:** 2026  
**Maintainer:** GOK:AI Development Team
