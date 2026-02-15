# Dockerfile for GOK:AI ESG Scoring Kernel (Directive II MVP)
# Stage: Production deployment on Google Cloud Run
# Base: Python 3.10

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project structure
COPY CORE/ CORE/
COPY INFRA/ INFRA/
COPY ECONOMY/ ECONOMY/
COPY MTAQUEST/ MTAQUEST/
COPY META/ META/
COPY PERCEPTION/ PERCEPTION/
COPY CONFIG/ CONFIG/

# Copy main execution files
COPY main.py .
COPY main_directive_i.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:${PORT}/health')" || exit 1

# Run the application
CMD exec gunicorn \
    --bind :${PORT} \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    ECONOMY.ESG_Scoring_Kernel:app
