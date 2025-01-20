import datetime
import time
from pprint import pprint

import pytest
import snappi

# @pytest.fixture                       # fixture overriding
# def b2b_config(b2b_device_config):
#     return b2b_device_config


def test_config_send(api: snappi.Api, b2b_config: snappi.Config):
    config_to_send_dict = b2b_config.serialize(encoding=snappi.Config.DICT)

    api.set_config(b2b_config)

    config: snappi.Config = api.get_config()
    config_from_ixia_dict = config.serialize(encoding=snappi.Config.DICT)

    pprint(config_from_ixia_dict)

    assert config_to_send_dict["ports"] == config_from_ixia_dict["ports"]


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_flow(api: snappi.Api, b2b_config: snappi.Config):
    api.set_config(b2b_config)

    ts = api.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    warning: snappi.Warning = api.set_control_state(ts)

    pprint(f"\nwarning:\n\t{warning}")
    assert len(warning.warnings) == 0

    # port metrics

    metric_req: snappi.MetricsRequest = api.metrics_request()
    metric_req.port.port_names = ["tx_port", "rx_port"]
    metric_req.port.column_names = [
        metric_req.port.FRAMES_TX,
        metric_req.port.FRAMES_RX,
    ]
    metric_resp: snappi.MetricsResponse = api.get_metrics(metric_req)
    pprint(f"\nmetric_resp:\n{metric_resp}")

    assert (
        metric_resp.port_metrics[0].frames_tx == metric_resp.port_metrics[1].frames_rx
        and metric_resp.port_metrics[0].frames_rx
        == metric_resp.port_metrics[1].frames_tx
    )

    # # flow metrics

    # metric_req: snappi.MetricsRequest = api.metrics_request()
    # metric_req.flow.flow_names = ["f1"]
    # start = datetime.datetime.now()
    # while True:
    #     metrics: snappi.MetricsResponse = api.get_metrics(metric_req)
    #     if (datetime.datetime.now() - start).seconds > 10:
    #         raise Exception("deadline exceeded")
    #     pprint(metrics)
    #     if metrics.flow_metrics[0].transmit == metrics.flow_metrics[0].STOPPED:
    #         break
    #     time.sleep(0.1)


# @pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
# def test_link_up(api: snappi.Api):
#     ps = api.control_state()
#     ps.port.link.state = ps.port.link.UP
#     api.set_control_state(ps)
