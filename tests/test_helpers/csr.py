from pathlib import Path

from dotenv import dotenv_values
from pyats.topology.device import Device

from .k8s import ext_ip


def csr_device(k8s_name: str) -> Device:
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
        csr.cli.configure(f.readlines())


def unconfigure_csr(csr: Device):
    csr.cli.execute("configure replace nvram:startup-config force")


def bgp_sessions_up(csr: Device):
    out = csr.cli.execute("show bgp all neighbors | in state =")
    return True if "down" not in out and "Established" in out else False
