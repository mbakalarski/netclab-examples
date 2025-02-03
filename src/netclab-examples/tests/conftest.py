from pathlib import Path

import pytest
import snappi
from dotenv import dotenv_values
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config
from pyats.topology.device import Device


def svc_ext_ip_and_ports(k8s_svc: str, k8s_namespace: str):
    k8s_config.load_kube_config()
    v1 = k8s_client.CoreV1Api()
    ret = v1.read_namespaced_service(k8s_svc, k8s_namespace)
    ext_ip = ret.status.load_balancer.ingress[0].ip
    ports = {i.name: i.port for i in ret.spec.ports}
    return ext_ip, ports


def ext_ip(k8s_svc: str, k8s_namespace: str) -> str:
    ip, _ = svc_ext_ip_and_ports(k8s_svc, k8s_namespace)
    return ip


def csr(k8s_name: str) -> Device:
    env = dotenv_values()
    csr_ip = ext_ip(k8s_name, env.get("K8S_NAMESPACE"))
    csr = Device(
        k8s_name,
        os="iosxe",
        connections={
            "cli": {
                "protocol": "ssh",
                "ip": csr_ip,
                "ssh_options": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
            },
        },
        credentials={
            "default": dict(
                username=env.get("CSR_USER"),
                password=env.get("CSR_PASS"),
            )
        },
    )
    return csr


def configure_csr(csr: Device, filepath: Path) -> Device:
    with open(filepath) as f:
        csr.configure(f.readlines())


def unconfigure_csr(csr: Device):
    csr.cli.execute("configure replace nvram:startup-config force")


def otg_api(k8s_svc: str, port_name, transport):
    env = dotenv_values()
    ip, ports = svc_ext_ip_and_ports(
        k8s_svc,
        env.get("K8S_NAMESPACE"),
    )
    otg_api: snappi.Api = snappi.api(
        location=f"https://{ip}:{ports.get(port_name)}",
        transport=transport,
        verify=False,
    )
    return otg_api


def otg_http_api(k8s_svc: str):
    api = otg_api(k8s_svc, "https", snappi.Transport.HTTP)
    return api


def otg_grpc_api(k8s_svc: str):
    return otg_api(k8s_svc, "grpc", snappi.Transport.GRPC)


def configure_otg(otg_api: snappi.Api, filepath: Path):
    config: snappi.Config = otg_api.config()
    with open(filepath) as f:
        payload = config.deserialize(f.read())
    otg_api.set_config(payload)


def unconfigure_otg(otg_api: snappi.Api):
    config: snappi.Config = otg_api.config()
    payload = config.deserialize("{}")
    otg_api.set_config(payload)


# @pytest.fixture
# def b2b_config(otg_api: snappi.Api):
#     config: snappi.Config = otg_api.config()
#     config.options.port_options.location_preemption = True

#     tx_port = config.ports.port(name="tx_port", location="eth1")[-1]
#     rx_port = config.ports.port(name="rx_port", location="eth2")[-1]

#     f1 = config.flows.add(name="f1")
#     f1.duration.fixed_packets.packets = 10
#     f1.tx_rx.port.tx_name = tx_port.name
#     f1.metrics.enable = True
#     f1.tx_rx.port.rx_names = [rx_port.name]

#     eth, ip, udp = f1.packet.ethernet().ipv4().udp()
#     eth.dst.value = "00:00:00:00:00:11"
#     ip.dst.value = "192.168.1.1"
#     udp.dst_port.value = 5000

#     return config


# @pytest.fixture
# def b2b_device_config(otg_api: snappi.Api):
#     config: snappi.Config = otg_api.config()
#     config.options.port_options.location_preemption = True

#     tx_port = config.ports.add(name="tx_port", location="eth1")
#     rx_port = config.ports.add(name="rx_port", location="eth2")

#     tx_dev = config.devices.add(name="Tx Dev")
#     rx_dev = config.devices.add(name="Rx Dev")

#     tx_eth = tx_dev.ethernets.add(name="Tx Eth", mac="00:00:01:00:00:01")
#     tx_eth.connection.port_name = tx_port.name

#     rx_eth = rx_dev.ethernets.add(name="Rx Eth", mac="00:00:01:00:00:02")
#     rx_eth.connection.port_name = rx_port.name

#     tx_ip = tx_eth.ipv4_addresses.ipv4(
#         gateway="1.1.1.2",
#         address="1.1.1.1",
#         name="tx_ip",
#     )[-1]

#     rx_ip = rx_eth.ipv4_addresses.ipv4(
#         gateway="1.1.1.1",
#         address="1.1.1.2",
#         name="rx_ip",
#     )[-1]

#     f1 = config.flows.add(name="f1")
#     f1.duration.fixed_packets.packets = 10
#     f1.tx_rx.device.tx_names = [tx_ip.name]
#     f1.tx_rx.device.rx_names = [rx_ip.name]
#     f1.metrics.enable = True

#     return config
