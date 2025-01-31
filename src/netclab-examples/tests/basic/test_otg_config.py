import datetime
import time
from pprint import pprint

import pytest
import snappi

# @pytest.fixture  # fixture overriding
# def b2b_config(b2b_device_config):
#     return b2b_device_config


def test_config_send(api: snappi.Api, b2b_config: snappi.Config):
    config_to_send_dict = b2b_config.serialize(encoding=snappi.Config.DICT)

    api.set_config(b2b_config)

    config: snappi.Config = api.get_config()
    config_from_ixia_dict = config.serialize(encoding=snappi.Config.DICT)

    print(config)

    assert config_to_send_dict["ports"] == config_from_ixia_dict["ports"]


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_port_metrics(api: snappi.Api, b2b_config: snappi.Config):
    api.set_config(b2b_config)

    ts = api.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    warning: snappi.Warning = api.set_control_state(ts)

    print(warning)
    assert len(warning.warnings) == 0

    metrics_req: snappi.MetricsRequest = api.metrics_request()

    start = datetime.datetime.now()
    while True:
        metrics_resp: snappi.MetricsResponse = api.get_metrics(metrics_req)
        if (datetime.datetime.now() - start).seconds > 10:
            raise Exception("deadline exceeded")
        if (
            metrics_resp.port_metrics[0].transmit
            == metrics_resp.port_metrics[0].STOPPED
        ):
            break
        time.sleep(0.1)

    pprint(metrics_resp.serialize(encoding="dict"))

    assert (
        metrics_resp.port_metrics[0].frames_tx == metrics_resp.port_metrics[1].frames_rx
        and metrics_resp.port_metrics[0].frames_rx
        == metrics_resp.port_metrics[1].frames_tx
    )


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_flow_metrics(api: snappi.Api, b2b_device_config: snappi.Config):
    api.set_config(b2b_device_config)

    ts = api.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    warning: snappi.Warning = api.set_control_state(ts)

    print(warning)
    assert len(warning.warnings) == 0

    metrics_req: snappi.MetricsRequest = api.metrics_request()
    metrics_req.flow.flow_names = ["f1"]

    start = datetime.datetime.now()
    while True:
        metrics_resp: snappi.MetricsResponse = api.get_metrics(metrics_req)
        if (datetime.datetime.now() - start).seconds > 10:
            raise Exception("deadline exceeded")
        if (
            metrics_resp.flow_metrics[0].transmit
            == metrics_resp.flow_metrics[0].STOPPED
        ):
            break
        time.sleep(0.1)

    pprint(metrics_resp.serialize(encoding="dict"))

    assert (
        metrics_resp.flow_metrics[0].frames_tx == metrics_resp.flow_metrics[0].frames_rx
    )
