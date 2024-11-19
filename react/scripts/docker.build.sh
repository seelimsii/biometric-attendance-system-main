#!/bin/sh

build_type="local"
PROJECT_NAME="react"

cp ./../deploy/$build_type/environments/.env.react .env
echo "Running: docker build -t $PROJECT_NAME . \
    || exit
    "

docker build -t "$PROJECT_NAME" . \
    || exit