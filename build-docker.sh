#!/bin/bash
# GOK:AI Docker Build Script
# Purpose: Build and push Docker images to container registry

set -e

echo "=========================================="
echo "GOK:AI Docker Build Pipeline"
echo "=========================================="

# Configuration
IMAGE_NAME=${1:-"gok-ai"}
IMAGE_TAG=${2:-"latest"}
REGISTRY=${3:-"local"}
GCP_PROJECT=${GCP_PROJECT:-"meta-geniusz-gok-turbo"}

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  Image Name: $IMAGE_NAME"
echo "  Image Tag: $IMAGE_TAG"
echo "  Registry: $REGISTRY"
echo "  GCP Project: $GCP_PROJECT"
echo ""

# Step 1: Build main image
echo -e "${BLUE}[1/4]${NC} Building main GOK:AI image..."
docker build \
  --tag ${IMAGE_NAME}:${IMAGE_TAG} \
  --tag ${IMAGE_NAME}:latest \
  --label "version=${IMAGE_TAG}" \
  --label "project=gok-ai" \
  -f Dockerfile \
  .

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ Main image built successfully${NC}"
else
  echo -e "${RED}✗ Failed to build main image${NC}"
  exit 1
fi

# Step 2: Build MTaQuest image
echo -e "${BLUE}[2/4]${NC} Building MTaQuest service image..."
docker build \
  --tag ${IMAGE_NAME}-mtaquest:${IMAGE_TAG} \
  --label "version=${IMAGE_TAG}" \
  --label "service=mtaquest" \
  -f INFRA/Dockerfile.mtaquest \
  .

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ MTaQuest image built successfully${NC}"
else
  echo -e "${RED}✗ Failed to build MTaQuest image${NC}"
  exit 1
fi

# Step 3: Build API image
echo -e "${BLUE}[3/4]${NC} Building API Gateway image..."
docker build \
  --tag ${IMAGE_NAME}-api:${IMAGE_TAG} \
  --label "version=${IMAGE_TAG}" \
  --label "service=api-gateway" \
  -f INFRA/Dockerfile.api \
  .

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓ API image built successfully${NC}"
else
  echo -e "${RED}✗ Failed to build API image${NC}"
  exit 1
fi

# Step 4: Push images (if not local registry)
if [ "$REGISTRY" != "local" ]; then
  echo -e "${BLUE}[4/4]${NC} Pushing images to ${REGISTRY}..."
  
  case $REGISTRY in
    gcr)
      echo "Pushing to Google Container Registry..."
      docker tag ${IMAGE_NAME}:${IMAGE_TAG} gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}
      docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}
      echo -e "${GREEN}✓ Pushed to gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}${NC}"
      ;;
    ar)
      echo "Pushing to Google Artifact Registry..."
      REGION=${4:-us-central1}
      docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGION}-docker.pkg.dev/${GCP_PROJECT}/gok-ai/${IMAGE_NAME}:${IMAGE_TAG}
      docker push ${REGION}-docker.pkg.dev/${GCP_PROJECT}/gok-ai/${IMAGE_NAME}:${IMAGE_TAG}
      echo -e "${GREEN}✓ Pushed to ${REGION}-docker.pkg.dev${NC}"
      ;;
    dockerhub)
      echo "Pushing to Docker Hub..."
      docker push ${IMAGE_NAME}:${IMAGE_TAG}
      echo -e "${GREEN}✓ Pushed to Docker Hub${NC}"
      ;;
    *)
      echo -e "${YELLOW}Unknown registry: $REGISTRY (skipping push)${NC}"
      ;;
  esac
else
  echo -e "${BLUE}[4/4]${NC} Local registry mode (skipping push)"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Build Pipeline Complete!"
echo "==========================================${NC}"
echo ""
echo "Built images:"
echo "  - ${IMAGE_NAME}:${IMAGE_TAG}"
echo "  - ${IMAGE_NAME}-mtaquest:${IMAGE_TAG}"
echo "  - ${IMAGE_NAME}-api:${IMAGE_TAG}"
echo ""
echo "To run locally with Docker Compose:"
echo -e "${BLUE}docker-compose up${NC}"
echo ""
