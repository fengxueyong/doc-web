#!/bin/bash

set -e

IMAGE_NAME="doc-web-backend"
IMAGE_TAG="1.0.0"

usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -t, --tag <tag>       Image tag (default: 1.0.0)"
    echo "  -p, --push <repo>     Push image to registry after build"
    echo "  --no-cache            Build without Docker cache"
    echo "  -h, --help            Show this help message"
    exit 1
}

PUSH_REPO=""
NO_CACHE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        -p|--push)
            PUSH_REPO="$2"
            shift 2
            ;;
        --no-cache)
            NO_CACHE="--no-cache"
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo " Building doc-web-backend Docker Image"
echo "========================================"
echo "Project dir : $SCRIPT_DIR"
echo "Image       : $IMAGE_NAME:$IMAGE_TAG"
echo "========================================"

cd "$SCRIPT_DIR"

docker build $NO_CACHE \
    -t "$IMAGE_NAME:$IMAGE_TAG" \
    .

if [ -n "$PUSH_REPO" ]; then
    echo ""
    echo "Pushing image to $PUSH_REPO..."
    docker tag "$IMAGE_NAME:$IMAGE_TAG" "$PUSH_REPO/$IMAGE_NAME:$IMAGE_TAG"
    docker push "$PUSH_REPO/$IMAGE_NAME:$IMAGE_TAG"
fi

echo ""
echo "Build complete: $IMAGE_NAME:$IMAGE_TAG"
