from pathlib import Path

import pytest

from ..conftest import configure_otg, otg_http_api, unconfigure_otg


@pytest.fixture(scope="session")
def otg01():
    otg01 = otg_http_api("otg-controller")
    yield otg01


@pytest.fixture
def configured_otg01(otg01):
    configure_otg(otg01, Path(__file__).parent / "otg01_config.yaml")
    yield otg01
    unconfigure_otg(otg01)
