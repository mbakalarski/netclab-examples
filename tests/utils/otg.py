from pathlib import Path

import snappi
from dotenv import dotenv_values

from .k8s import svc_ext_ip_and_ports


def api(k8s_svc: str, port_name, transport):
    env = dotenv_values()
    ip, ports = svc_ext_ip_and_ports(
        k8s_svc,
        env.get("K8S_NAMESPACE"),
    )
    api: snappi.Api = snappi.api(
        location=f"https://{ip}:{ports.get(port_name)}",
        transport=transport,
        verify=False,
    )
    return api


def http_api(k8s_svc: str):
    return api(k8s_svc, "https", snappi.Transport.HTTP)


def grpc_api(k8s_svc: str):
    return api(k8s_svc, "grpc", snappi.Transport.GRPC)


def configure(api: snappi.Api, filepath: Path):
    config: snappi.Config = api.config()
    with open(filepath) as f:
        payload = config.deserialize(f.read())
    api.set_config(payload)


def unconfigure(api: snappi.Api):
    config: snappi.Config = api.config()
    payload = config.deserialize("{}")
    api.set_config(payload)


def start_all_protocols(api: snappi.Api):
    ps = api.control_state()
    ps.protocol.all.state = ps.protocol.all.START
    api.set_control_state(ps)


def start_traffic_flow(api: snappi.Api, flow_name: str):
    ts = api.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = [flow_name]
    api.set_control_state(ts)


def is_transmit_stopped(api: snappi.Api, flow_names: list):
    mreq = api.metrics_request()
    mreq.flow.flow_names = flow_names
    mres: snappi.MetricsResponse = api.get_metrics(mreq)
    miter: snappi.FlowMetricIter = mres.flow_metrics[0]
    print("FLOW METRICS", miter, sep="\n")
    return True if miter.transmit == miter.STOPPED else False


def is_bgpv4_converged(otg) -> bool:
    mreq = otg.metrics_request()
    mreq.bgpv4.column_names = [
        "routes_advertised",
        "routes_received",
        "end_of_rib_received",
    ]
    mresp = otg.get_metrics(mreq).serialize(encoding="dict")

    return (
        True
        if (
            mresp.get("bgpv4_metrics")[0].get("end_of_rib_received") == "1"
            and mresp.get("bgpv4_metrics")[1].get("end_of_rib_received") == "1"
            and (
                mresp.get("bgpv4_metrics")[0].get("routes_advertised")
                == mresp.get("bgpv4_metrics")[1].get("routes_received")
            )  # fmt: skip
        )
        else False
    )
