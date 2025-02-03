import pytest
from snappi import Config

pytestmark = pytest.mark.filterwarnings(
    "ignore::urllib3.exceptions.InsecureRequestWarning"
)


def test_before_configured_otg(otg01_api):
    config = otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) == 0


def test_configured_otg(configured_otg01_api):
    config = configured_otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) != 0


def test_after_configured_otg(otg01_api):
    config = otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) == 0
