#!/bin/bash
BASE_DIR=$(git rev-parse --show-toplevel)
TOPOLOGY_DIR="${BASE_DIR}/manifests/${2}"
OPERATION="${1}"

docker network ls | grep netclab 1>/dev/null && NETWORK="netclab"
docker network ls | grep kind 1>/dev/null && NETWORK="kind"

export HTTP_SERVER_IP=$(docker network inspect "${NETWORK}" | jq -r .[].IPAM.Config[].Gateway | grep -v ':')

if [ ${OPERATION} == "apply" ]; then
  kubectl kustomize "$TOPOLOGY_DIR" | envsubst '$HTTP_SERVER_IP' | kubectl "$OPERATION" -f -
fi

if [ ${OPERATION} == "delete" ]; then
  kubectl "$OPERATION" -k "$TOPOLOGY_DIR"
fi
