#!/bin/bash

set -e

BASE_DIR=$(git rev-parse --show-toplevel)
TOPOLOGY_DIR="${BASE_DIR}/manifests/${2}"
OPERATION="${1}"

docker network ls | grep kind 1>/dev/null && NETWORK="kind"

for gw in $(docker network inspect "${NETWORK}" | jq -r .[].IPAM.Config[].Gateway);
do
  echo $gw | grep -v ':' 1>/dev/null && export HTTP_SERVER_IP="${gw}" && break
done

if [ ${OPERATION} == "apply" ]; then
  kubectl kustomize "$TOPOLOGY_DIR" | envsubst '$HTTP_SERVER_IP' | kubectl "$OPERATION" -f -
fi

if [ ${OPERATION} == "delete" ]; then
  kubectl "$OPERATION" -k "$TOPOLOGY_DIR"
fi
