ip=$(kubectl get svc/otg-controller -o json | jq -r .status.loadBalancer.ingress[].ip)
export OTG_API="https://${ip}:8443"
export OTG_LOCATION_P1="eth1"
export OTG_LOCATION_P2="eth2"
export OTG_LOCATION_P3="eth3"

otg_yaml="$1"
otgen run --insecure --file $otg_yaml --yaml --metrics flow | \
otgen transform --metrics flow | \
otgen display --mode table
