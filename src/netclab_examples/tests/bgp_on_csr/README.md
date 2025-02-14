## BGP on CSR

### Topology:

[topo-02](/manifests/topo-02/topology.md)

### States:
```
            otg01_unconfigured
                \
                otg01_configured -------
                /                       \
    otg01_with_protocol_started     otg01_with_traffic_started
        |                                  \
        |                                  otg01_with_metrics_ready
        |
        |
        |   csr01_unconfigured
        |       \
        |       csr01_configured
        |           /
    csr01_with_bgp_sessions_up
```
