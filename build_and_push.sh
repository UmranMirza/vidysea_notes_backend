#!/bin/bash

if [ -z "$1" ]
then
    echo "Error: Please pass environment name (e.g., dev, staging, production)"
    exit 1
fi

# Automatically detect service name from current folder
CURRENT_DIR=${PWD##*/}
SERVICE_NAME=${CURRENT_DIR//-/_}   # Replace "-" with "_" if needed
DOCKER_REPO="mohitsymb/symb_build"

echo "Building and Pushing for environment: $1"
echo "Service Name Detected: $SERVICE_NAME"

docker buildx build --platform linux/amd64 -t "${DOCKER_REPO}:${SERVICE_NAME}_$1" . --push --load

echo "✅ Successfully built and pushed: ${DOCKER_REPO}:${SERVICE_NAME}_$1"