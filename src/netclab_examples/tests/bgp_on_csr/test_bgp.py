import pytest
import snappi

csr_cfg_fname = "csr_bgpv6.cfg"
otg_cfg_fname = "otg_bgpv6.yaml"


def test_bgp_0a(csr01_unconfigured):
    out = csr01_unconfigured.cli.execute("show run | in router")
    assert "router bgp" not in out


def test_bgp_0b(otg01_unconfigured):
    otg_config = otg01_unconfigured.get_config().serialize(encoding=snappi.Config.DICT)
    assert len(otg_config) == 0


@pytest.mark.csrcfg(csr_cfg_fname)
def test_bgp_1a(csr01_configured):
    out = csr01_configured.cli.execute("show run | in router")
    assert "router bgp" in out


@pytest.mark.otgcfg(otg_cfg_fname)
def test_bgp_1b(otg01_configured):
    otg_config = otg01_configured.get_config().serialize(encoding=snappi.Config.DICT)
    assert len(otg_config) != 0


@pytest.mark.csrcfg(csr_cfg_fname)
@pytest.mark.otgcfg(otg_cfg_fname)
def test_bgp_1c(
    csr01_configured,
    otg01_configured,
    otg01_with_protocol_started,
    csr01_with_bgp_sessions_up,
):
    out = csr01_configured.cli.execute("show run | in router")
    otg_config = otg01_configured.get_config().serialize(encoding=snappi.Config.DICT)
    assert len(otg_config) != 0 and "router bgp" in out


@pytest.mark.csrcfg(csr_cfg_fname)
@pytest.mark.otgcfg(otg_cfg_fname)
def test_bgp_2(
    csr01_configured,
    otg01_configured,
    otg01_with_protocol_started,
    csr01_with_bgp_sessions_up,
    otg01_with_traffic_started,
    otg01_with_metrics_ready: snappi.Api,
):
    mreq: snappi.MetricsRequest = otg01_with_metrics_ready.metrics_request()
    mreq.flow.flow_names = ["f1"]
    mresp: snappi.MetricsResponse = otg01_with_metrics_ready.get_metrics(mreq)
    print(mresp.serialize(encoding="dict"))

    assert True
