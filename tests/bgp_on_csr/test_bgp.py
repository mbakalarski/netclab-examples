import pytest

pytestmark = pytest.mark.topo_02

csr_cfg_fname = "csr_bgpv6.cfg"
otg_cfg_fname = "otg_bgpv6.yaml"


def test_csr01_unconfigured(csr01_unconfigured):
    out = csr01_unconfigured.cli.execute("show run | in router")
    assert "router bgp" not in out


def test_otg01_unconfigured(otg01_unconfigured):
    otg_config = otg01_unconfigured.get_config().serialize(encoding="dict")
    assert len(otg_config) == 0


@pytest.mark.csrcfg(csr_cfg_fname)
def test_csr01_configured(csr01_configured):
    out = csr01_configured.cli.execute("show run | in router")
    assert "router bgp" in out


@pytest.mark.otgcfg(otg_cfg_fname)
def test_otg01_configured(otg01_configured):
    otg_config = otg01_configured.get_config().serialize(encoding="dict")
    assert len(otg_config) != 0


@pytest.mark.csrcfg(csr_cfg_fname)
@pytest.mark.otgcfg(otg_cfg_fname)
def test_csr01_and_otg01_configured(csr01_configured, otg01_configured):
    out = csr01_configured.cli.execute("show run | in router")
    otg_config = otg01_configured.get_config().serialize(encoding="dict")
    assert len(otg_config) != 0 and "router bgp" in out


@pytest.mark.csrcfg(csr_cfg_fname)
@pytest.mark.otgcfg(otg_cfg_fname)
def test_csr01_bgp_sessions_up(csr01_with_bgp_sessions_up):
    assert True


@pytest.mark.csrcfg(csr_cfg_fname)
@pytest.mark.otgcfg(otg_cfg_fname)
def test_traffic_metrics_ok(csr01_with_bgp_sessions_up, otg01_with_metrics_ready):
    mreq = otg01_with_metrics_ready.metrics_request()
    mreq.flow.flow_names = ["f1"]
    mresp = otg01_with_metrics_ready.get_metrics(mreq)
    assert (
        mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_tx"]
        == mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_rx"]
    )
