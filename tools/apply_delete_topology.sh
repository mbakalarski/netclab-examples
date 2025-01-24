#!/bin/bash
BASE_DIR=$(git rev-parse --show-toplevel)
TOPOLOGY_DIR="${BASE_DIR}/manifests/${2}"
OPERATION="${1}"

export HTTP_SERVER_IP=$(docker network inspect kind | jq -r .[].IPAM.Config[].Gateway | grep -v ':')

if [ ${OPERATION} == "apply" ]; then
  kubectl kustomize "$TOPOLOGY_DIR" | envsubst '$HTTP_SERVER_IP' | kubectl "$OPERATION" -f -
fi

if [ ${OPERATION} == "delete" ]; then
  kubectl "$OPERATION" -k "$TOPOLOGY_DIR"
fi
