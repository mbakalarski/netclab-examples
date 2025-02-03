from pathlib import Path

import pytest

from ..conftest import configure_otg, otg_http_api, unconfigure_otg


@pytest.fixture(scope="session")
def otg01_api():
    otg01_api = otg_http_api("otg-controller")
    yield otg01_api


@pytest.fixture
def configured_otg01_api(otg01_api):
    configure_otg(otg01_api, Path(__file__).parent / "otg01_config.yaml")
    yield otg01_api
    unconfigure_otg(otg01_api)
