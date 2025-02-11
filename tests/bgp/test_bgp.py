import pytest
from snappi import Config

pytestmark = pytest.mark.filterwarnings(
    "ignore::urllib3.exceptions.InsecureRequestWarning"
)


def test_bgp_0a(unconfigured_csr01):
    out = unconfigured_csr01.cli.execute("show run | in router")
    assert "router bgp" not in out


def test_bgp_0b(unconfigured_otg01):
    otg_config = unconfigured_otg01.get_config().serialize(encoding=Config.DICT)
    assert len(otg_config) == 0


def test_bgp_1a(configured_csr01):
    out = configured_csr01.cli.execute("show run | in router")
    assert "router bgp" in out


def test_bgp_1b(configured_otg01):
    otg_config = configured_otg01.get_config().serialize(encoding=Config.DICT)
    assert len(otg_config) != 0


def test_bgp_1c(configured_csr01, configured_otg01):
    out = configured_csr01.cli.execute("show run | in router")
    otg_config = configured_otg01.get_config().serialize(encoding=Config.DICT)
    assert len(otg_config) != 0 and "router bgp" in out


def test_bgp_2(
    configured_csr01,
    configured_otg01,
    otg01_protocol_started,
    otg01_traffic_started,
):
    assert True


# from pathlib import Path
#
# import pytest
#
#
# @pytest.mark.otg_and_file(
#     "otg-controller",
#     Path.resolve(Path(__file__).parent / "otg_config.yaml"),
# )
# @pytest.mark.csr_and_file(
#     "csr01",
#     Path.resolve(Path(__file__).parent / "bgp_config.txt"),
# )
# def test_bgp(configured_csr, configured_otg):
#     out = configured_csr.cli.execute("show run | in router")
#     assert "router bgp 6501" in out

#     otg_config = configured_otg.get_config().serialize(encoding=Config.DICT)
#     assert len(otg_config) != 0
