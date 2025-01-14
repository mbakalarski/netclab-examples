import pytest
import snappi
from snappi import Api, Config
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config


def otg_controller_location(svc_name: str, namespace: str) -> str:
    k8s_config.load_kube_config()
    v1 = k8s_client.CoreV1Api()
    ret = v1.read_namespaced_service(svc_name, namespace)
    for i in ret.spec.ports:
        if i.name == "https":
            port = i.port
            break
    return ret.status.load_balancer.ingress[0].ip, port


@pytest.fixture(scope="session")
def api():
    ip, port = otg_controller_location("otg-controller", "default")
    api: Api = snappi.api(location=f"https://{ip}:{port}", verify=False)
    yield api
    del api


@pytest.fixture
def b2b_config(api: Api):
    config: Config = api.config()
    config.ports.port(name="tx", location="p1").port(name="rx", location="p2")
    return config
