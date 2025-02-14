from pathlib import Path

import pytest
from waiting import wait

from netclab_examples.test_helpers.csr import (
    bgp_sessions_up,
    configure_csr,
    csr_device,
    unconfigure_csr,
)
from netclab_examples.test_helpers.otg import (
    configure_otg,
    otg_http_api,
    otg_transmit_stopped,
    unconfigure_otg,
)


@pytest.fixture(scope="session")
def csr01():
    csr01 = csr_device("csr01")
    csr01.connect()
    yield csr01
    # csr01.destroy()  # takes time, c.a. 20s


@pytest.fixture
def csr01_unconfigured(csr01):
    unconfigure_csr(csr01)
    return csr01


@pytest.fixture
def csr01_configured(csr01, request):
    fname = request.node.get_closest_marker("csrcfg").args[0]
    configure_csr(csr01, Path(__file__).parent / fname)
    yield csr01
    unconfigure_csr(csr01)


@pytest.fixture
def csr01_with_bgp_sessions_up(csr01_configured, otg01_with_protocol_started):
    wait(
        lambda: bgp_sessions_up(csr01_configured),
        timeout_seconds=60,
        waiting_for="bgp sessions up",
    )
    return csr01_configured


@pytest.fixture(scope="session")
def otg01():
    otg01 = otg_http_api("otg-controller")
    return otg01


@pytest.fixture
def otg01_unconfigured(otg01):
    unconfigure_otg(otg01)
    return otg01


@pytest.fixture
def otg01_configured(otg01, request):
    cfg = request.node.get_closest_marker("otgcfg").args[0]
    configure_otg(otg01, Path(__file__).parent / cfg)
    yield otg01
    # unconfigure_otg(otg01)


@pytest.fixture
def otg01_with_protocol_started(otg01_configured):
    ps = otg01_configured.control_state()
    ps.protocol.all.state = ps.protocol.all.START
    otg01_configured.set_control_state(ps)
    return otg01_configured


@pytest.fixture
def otg01_with_traffic_started(otg01_configured):
    ts = otg01_configured.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    otg01_configured.set_control_state(ts)
    return otg01_configured


@pytest.fixture
def otg01_with_metrics_ready(otg01_with_traffic_started):
    wait(
        lambda: otg_transmit_stopped(otg01_with_traffic_started, ["f1"]),
        timeout_seconds=60,
        waiting_for="otg transmit stopped",
    )
    return otg01_with_traffic_started
