#!/usr/bin/env bash

PROJECT_NAME="fastapi"

echo "Running: docker build \
    --no-cache=true \
    -t $PROJECT_NAME \
    . \
    || exit
    "

docker buildx build  \
    -t "$PROJECT_NAME" \
    . \
    || exit
