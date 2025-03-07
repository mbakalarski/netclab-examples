#!/bin/bash

set -e

BASE_DIR=$(git rev-parse --show-toplevel)
source "${BASE_DIR}/.env"

docker run --name www -dt --mount "type=bind,source=${IMAGES_DIR},target=/usr/share/nginx/html" -p 8080:80 nginx:latest
