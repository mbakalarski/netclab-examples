from kubernetes import client, config


def svc_ext_ip_and_ports(k8s_svc: str, k8s_namespace: str):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.read_namespaced_service(k8s_svc, k8s_namespace)
    ext_ip = ret.status.load_balancer.ingress[0].ip
    ports = {i.name: i.port for i in ret.spec.ports}
    return ext_ip, ports


def ext_ip(k8s_svc: str, k8s_namespace: str) -> str:
    ip, _ = svc_ext_ip_and_ports(k8s_svc, k8s_namespace)
    return ip
