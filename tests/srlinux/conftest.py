from pathlib import Path

import pytest
from waiting import wait

from tests.utils.otg import (
    configure_otg,
    otg_http_api,
    otg_transmit_stopped,
    unconfigure_otg,
)


@pytest.fixture(scope="session")
def otg01():
    otg01 = otg_http_api("otg-controller")
    return otg01


@pytest.fixture
def otg01_unconfigured(otg01):
    # unconfigure_otg(otg01)
    return otg01


@pytest.fixture
def otg01_configured(otg01_unconfigured, request):
    cfg = request.node.get_closest_marker("otgcfg").args[0]
    configure_otg(otg01_unconfigured, Path(__file__).parent / cfg)
    otg01_configured = otg01_unconfigured
    return otg01_configured


@pytest.fixture
def otg01_with_protocol_started(otg01_configured):
    ps = otg01_configured.control_state()
    ps.protocol.all.state = ps.protocol.all.START
    otg01_configured.set_control_state(ps)
    otg01_with_protocol_started = otg01_configured
    return otg01_with_protocol_started


@pytest.fixture
def otg01_with_traffic_started(otg01_configured):
    ts = otg01_configured.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    otg01_configured.set_control_state(ts)
    otg01_with_traffic_started = otg01_configured
    return otg01_with_traffic_started


@pytest.fixture
def otg01_with_metrics_ready(otg01_with_traffic_started):
    wait(
        lambda: otg_transmit_stopped(otg01_with_traffic_started, ["f1"]),
        timeout_seconds=60,
        waiting_for="otg transmit stopped",
    )

    import time

    time.sleep(10)

    otg01_with_metrics_ready = otg01_with_traffic_started
    return otg01_with_metrics_ready
