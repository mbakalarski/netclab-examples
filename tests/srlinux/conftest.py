from pathlib import Path

import pytest
from snappi import Api as SnappiApi
from waiting import wait

import tests.utils.otg as otg


@pytest.fixture(scope="session")
def otg01() -> SnappiApi:
    otg01 = otg.http_api("otg-controller")
    return otg01


@pytest.fixture
def otg01_unconfigured(otg01: SnappiApi) -> SnappiApi:
    otg.unconfigure(otg01)
    yield otg01
    otg.unconfigure(otg01)


@pytest.fixture
def otg01_configured(otg01_unconfigured: SnappiApi, request) -> SnappiApi:
    cfg = request.node.get_closest_marker("otgcfg").args[0]
    otg.configure(otg01_unconfigured, Path(__file__).parent / cfg)
    otg01_configured = otg01_unconfigured
    return otg01_configured


@pytest.fixture
def otg01_with_protocol_started(otg01_configured: SnappiApi) -> SnappiApi:
    otg.start_all_protocols(otg01_configured)
    otg01_with_protocol_started = otg01_configured
    return otg01_with_protocol_started


@pytest.fixture
def otg01_with_bgpv4_converged(otg01_with_protocol_started: SnappiApi) -> SnappiApi:
    wait(
        lambda: otg.is_bgpv4_converged(otg01_with_protocol_started),
        timeout_seconds=30,
        waiting_for="bgp convergence",
    )
    otg01_with_bgpv4_converged = otg01_with_protocol_started
    return otg01_with_bgpv4_converged


@pytest.fixture
def otg01_with_traffic_started(otg01_configured: SnappiApi) -> SnappiApi:
    otg.start_traffic_flow(otg01_configured, "f1")
    otg01_with_traffic_started = otg01_configured
    return otg01_with_traffic_started


@pytest.fixture
def otg01_with_traffic_stopped(otg01_with_traffic_started: SnappiApi) -> SnappiApi:
    wait(
        lambda: otg.is_transmit_stopped(otg01_with_traffic_started, ["f1"]),
        timeout_seconds=60,
        waiting_for="otg transmit stopped",
    )
    otg01_with_traffic_stopped = otg01_with_traffic_started
    return otg01_with_traffic_stopped
