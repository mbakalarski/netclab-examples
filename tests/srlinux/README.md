## BGP on CSR

### Topology:

[topo-01](/manifests/topo-01/topology.md)


### Run with OTG:
```
ip=$(kubectl get svc/otg-controller -o json | jq -r .status.loadBalancer.ingress[].ip)
export OTG_API="https://${ip}:8443"

otg_cfg="tests/srlinux/otg_bgpv4.yaml"

otgen run --insecure --file "$otg_cfg" --rxbgp 2x --metrics flow | otgen transform --metrics flow | otgen display --mode table
```

### Get state of BGP
```
watch -n 1 "curl -sk \"${OTG_API}/monitor/metrics\" \
    -X POST \
    -H  'Content-Type: application/json' \
    -d '{ \"choice\": \"bgpv4\" }'"
```


