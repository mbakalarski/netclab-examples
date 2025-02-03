#!/bin/bash

set -e

BASE_DIR=$(git rev-parse --show-toplevel)
export $(cat ${BASE_DIR}/.env | xargs)

TMP_DIR=$(mktemp -d)
cat $BASE_DIR/tools/iosxe_config.txt | envsubst > "${TMP_DIR}/iosxe_config.txt"

mkisofs -l -o "${IMAGES_DIR}/csr_config.iso" "${TMP_DIR}/iosxe_config.txt"

rm -rf $TMP_DIR
