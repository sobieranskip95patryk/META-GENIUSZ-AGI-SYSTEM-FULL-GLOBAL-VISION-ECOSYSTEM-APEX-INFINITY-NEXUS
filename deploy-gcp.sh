#!/bin/bash
# GOK:AI Deployment Script for Google Cloud
# Purpose: Deploy GOK:AI to Google Cloud Run, Cloud Build, or GKE

set -e

# Configuration
GCP_PROJECT=${GCP_PROJECT:-"meta-geniusz-gok-turbo"}
GCP_REGION=${GCP_REGION:-"us-central1"}
IMAGE_REPO=${IMAGE_REPO:-"gok-ai"}
APP_VERSION=${APP_VERSION:-"1.0.0"}

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}=========================================="
echo "GOK:AI Google Cloud Deployment"
echo "==========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Verify prerequisites
echo -e "${BLUE}[1/8]${NC} Verifying prerequisites..."

if ! command_exists gcloud; then
    echo -e "${RED}✗ Google Cloud SDK not found${NC}"
    echo "Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! command_exists docker; then
    echo -e "${RED}✗ Docker not found${NC}"
    echo "Please install Docker first"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Step 2: Authenticate with GCP
echo -e "${BLUE}[2/8]${NC} Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $GCP_PROJECT
echo -e "${GREEN}✓ Authenticated with GCP${NC}"

# Step 3: Enable required APIs
echo -e "${BLUE}[3/8]${NC} Enabling required Google Cloud APIs..."
gcloud services enable \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    cloudresourcemanager.googleapis.com

echo -e "${GREEN}✓ APIs enabled${NC}"

# Step 4: Create Artifact Registry repository (if needed)
echo -e "${BLUE}[4/8]${NC} Setting up Artifact Registry..."
if gcloud artifacts repositories describe $IMAGE_REPO \
    --location=$GCP_REGION \
    --project=$GCP_PROJECT >/dev/null 2>&1; then
    echo "Repository already exists"
else
    echo "Creating repository..."
    gcloud artifacts repositories create $IMAGE_REPO \
        --repository-format=docker \
        --location=$GCP_REGION \
        --project=$GCP_PROJECT
fi
echo -e "${GREEN}✓ Artifact Registry configured${NC}"

# Step 5: Configure Docker authentication
echo -e "${BLUE}[5/8]${NC} Configuring Docker authentication..."
gcloud auth configure-docker ${GCP_REGION}-docker.pkg.dev
echo -e "${GREEN}✓ Docker authenticated${NC}"

# Step 6: Build and push images
echo -e "${BLUE}[6/8]${NC} Building and pushing Docker images..."

REGISTRY="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${IMAGE_REPO}"

echo "Building main image..."
docker build \
    --tag ${REGISTRY}/gok-ai:${APP_VERSION} \
    --tag ${REGISTRY}/gok-ai:latest \
    -f Dockerfile \
    .

echo "Pushing main image..."
docker push ${REGISTRY}/gok-ai:${APP_VERSION}
docker push ${REGISTRY}/gok-ai:latest

echo "Building MTaQuest image..."
docker build \
    --tag ${REGISTRY}/gok-ai-mtaquest:${APP_VERSION} \
    -f INFRA/Dockerfile.mtaquest \
    .
docker push ${REGISTRY}/gok-ai-mtaquest:${APP_VERSION}

echo "Building API image..."
docker build \
    --tag ${REGISTRY}/gok-ai-api:${APP_VERSION} \
    -f INFRA/Dockerfile.api \
    .
docker push ${REGISTRY}/gok-ai-api:${APP_VERSION}

echo -e "${GREEN}✓ Images built and pushed${NC}"

# Step 7: Deploy to Cloud Run
echo -e "${BLUE}[7/8]${NC} Deploying to Cloud Run..."

gcloud run deploy gok-ai \
    --image ${REGISTRY}/gok-ai:latest \
    --platform managed \
    --region $GCP_REGION \
    --memory 2Gi \
    --cpu 1 \
    --timeout 3600 \
    --allow-unauthenticated \
    --set-env-vars "GCP_PROJECT=${GCP_PROJECT},ENVIRONMENT=production" \
    --project $GCP_PROJECT

echo -e "${GREEN}✓ Deployed to Cloud Run${NC}"

# Step 8: Display deployment information
echo -e "${BLUE}[8/8]${NC} Gathering deployment information..."

SERVICE_URL=$(gcloud run services describe gok-ai \
    --platform managed \
    --region $GCP_REGION \
    --format='value(status.url)' \
    --project $GCP_PROJECT)

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Service Details:"
echo -e "  ${BLUE}Service URL:${NC} $SERVICE_URL"
echo -e "  ${BLUE}Project:${NC} $GCP_PROJECT"
echo -e "  ${BLUE}Region:${NC} $GCP_REGION"
echo -e "  ${BLUE}Version:${NC} $APP_VERSION"
echo ""
echo "Images pushed to:"
echo "  - ${REGISTRY}/gok-ai:${APP_VERSION}"
echo "  - ${REGISTRY}/gok-ai-mtaquest:${APP_VERSION}"
echo "  - ${REGISTRY}/gok-ai-api:${APP_VERSION}"
echo ""
echo "Next steps:"
echo "  1. Test the service: curl $SERVICE_URL/health"
echo "  2. View logs: gcloud run logs read gok-ai --limit 50"
echo "  3. Monitor: https://console.cloud.google.com/run"
echo ""
