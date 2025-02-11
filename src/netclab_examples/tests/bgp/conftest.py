import time
from pathlib import Path

import pytest

from netclab_examples.test_helpers.csr import (
    configure_csr,
    csr,
    unconfigure_csr,
)
from netclab_examples.test_helpers.otg import (
    configure_otg,
    otg_http_api,
    unconfigure_otg,
)


@pytest.fixture(scope="session")
def csr01():
    csr01 = csr("csr01")
    csr01.connect()
    yield csr01
    csr01.destroy()


@pytest.fixture
def configured_csr01(csr01):
    configure_csr(csr01, Path(__file__).parent / "csr01_config.txt")
    time.sleep(20) # TODO: wait for ints and bgp to be UP
    yield csr01
    unconfigure_csr(csr01)


@pytest.fixture
def unconfigured_csr01(csr01):
    unconfigure_csr(csr01)
    return csr01


@pytest.fixture(scope="session")
def otg01():
    otg01 = otg_http_api("otg-controller")
    yield otg01


@pytest.fixture
def configured_otg01(otg01):
    configure_otg(otg01, Path(__file__).parent / "otg01_config.yaml")
    yield otg01
    unconfigure_otg(otg01)


@pytest.fixture
def unconfigured_otg01(otg01):
    unconfigure_otg(otg01)
    return otg01


@pytest.fixture
def otg01_protocol_started(configured_otg01):
    ps = configured_otg01.control_state()
    ps.protocol.all.state = ps.protocol.all.START
    configured_otg01.set_control_state(ps)


@pytest.fixture
def otg01_traffic_started(configured_otg01):
    ts = configured_otg01.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    configured_otg01.set_control_state(ts)
