import pytest

pytestmark = pytest.mark.topo_01

otg_cfg_fname = "otg_bgpv4.yaml"


# def test_otg01_unconfigured(otg01_unconfigured):
#     otg_config = otg01_unconfigured.get_config().serialize(encoding="dict")
#     assert len(otg_config) == 0


@pytest.mark.otgcfg(otg_cfg_fname)
def test_otg01_configured(otg01_configured):
    otg_config = otg01_configured.get_config().serialize(encoding="dict")
    assert len(otg_config) != 0
