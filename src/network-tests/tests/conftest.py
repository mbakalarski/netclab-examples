import pytest
import snappi
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config


def otg_controller_location(svc_name: str, namespace: str):
    k8s_config.load_kube_config()
    v1 = k8s_client.CoreV1Api()
    ret = v1.read_namespaced_service(svc_name, namespace)
    for i in ret.spec.ports:
        if i.name == "https":
            port = i.port
            break
    for i in ret.spec.ports:
        if i.name == "grpc":
            grpc_port = i.port
            break
    return ret.status.load_balancer.ingress[0].ip, port, grpc_port


@pytest.fixture(scope="session")
def api():
    ip, port, _ = otg_controller_location("otg-controller", "default")
    api: snappi.Api = snappi.api(location=f"https://{ip}:{port}", verify=False)
    yield api


@pytest.fixture(scope="session")
def grpc_api():
    ip, _, grpc_port = otg_controller_location("otg-controller", "default")
    grpc_api: snappi.Api = snappi.api(
        location=f"https://{ip}:{grpc_port}",
        transport=snappi.Transport.GRPC,
        verify=False,
    )
    yield grpc_api


@pytest.fixture
def b2b_config(api: snappi.Api):
    config: snappi.Config = api.config()
    config.options.port_options.location_preemption = True

    tx_port = config.ports.port(name="tx_port", location="eth1")[-1]
    rx_port = config.ports.port(name="rx_port", location="eth2")[-1]

    f1 = config.flows.add(name="f1")
    f1.tx_rx.port.tx_name = tx_port.name
    f1.metrics.enable = True
    f1.tx_rx.port.rx_names = [rx_port.name]

    eth, ip, udp = f1.packet.ethernet().ipv4().udp()
    eth.dst.value = "00:00:00:00:00:11"
    ip.dst.value = "192.168.1.1"
    udp.dst_port.value = 5000

    return config


@pytest.fixture
def b2b_device_config(api: snappi.Api):
    config: snappi.Config = api.config()
    config.options.port_options.location_preemption = True

    tx_port = config.ports.add(name="tx_port", location="eth1")
    rx_port = config.ports.add(name="rx_port", location="eth2")

    tx_dev = config.devices.add(name="Tx Dev")
    rx_dev = config.devices.add(name="Rx Dev")

    tx_eth = tx_dev.ethernets.add(name="Tx Eth", mac="00:00:01:00:00:01")
    tx_eth.connection.port_name = tx_port.name

    rx_eth = rx_dev.ethernets.add(name="Rx Eth", mac="00:00:01:00:00:02")
    rx_eth.connection.port_name = rx_port.name

    # tx_eth.mac = "00:00:01:00:00:01"
    # rx_eth.mac = "00:00:01:00:00:02"

    return config
