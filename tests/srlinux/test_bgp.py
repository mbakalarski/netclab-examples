import pytest

otg_cfg_fname = "otg_bgpv4.yaml"

pytestmark = [pytest.mark.topo_01, pytest.mark.otgcfg(otg_cfg_fname)]


def test_otg01_unconfigured(otg01_unconfigured):
    otg_config = otg01_unconfigured.get_config().serialize(encoding="dict")
    assert len(otg_config) == 0


def test_otg01_configured(otg01_configured):
    otg_config = otg01_configured.get_config().serialize(encoding="dict")
    assert len(otg_config) != 0


def test_otg01_with_bgpv4_converged(otg01_with_bgpv4_converged):
    assert True


def test_traffic(otg01_with_bgpv4_converged, otg01_with_traffic_stopped):
    mreq = otg01_with_traffic_stopped.metrics_request()
    mreq.flow.flow_names = ["f1"]
    mresp = otg01_with_traffic_stopped.get_metrics(mreq)
    assert (
        mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_tx"]
        == mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_rx"]
    )
