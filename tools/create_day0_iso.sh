#!/bin/bash
BASE_DIR=$(git rev-parse --show-toplevel)

if [ -z "${IMAGES_DIR}" ]; then
  IMAGES_DIR="${HOME}/images"
fi

mkisofs -l -o "${IMAGES_DIR}/csr_config.iso" "${BASE_DIR}/tools/iosxe_config.txt"
