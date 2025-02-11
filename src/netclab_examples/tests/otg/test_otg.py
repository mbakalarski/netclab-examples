import pytest
from snappi import Config

pytestmark = pytest.mark.filterwarnings(
    "ignore::urllib3.exceptions.InsecureRequestWarning"
)


def test_configured_otg(configured_otg01):
    config = configured_otg01.get_config().serialize(encoding=Config.DICT)
    assert len(config) != 0


def test_not_configured_otg(otg01):
    config = otg01.get_config().serialize(encoding=Config.DICT)
    assert len(config) == 0
