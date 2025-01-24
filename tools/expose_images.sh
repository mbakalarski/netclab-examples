#!/bin/bash
if [ -z "${IMAGES_DIR}" ]; then
  IMAGES_DIR="${HOME}/images"
fi

docker run --name www -dt --mount "type=bind,source=${IMAGES_DIR},target=/usr/share/nginx/html" -p 8080:80 nginx:latest
