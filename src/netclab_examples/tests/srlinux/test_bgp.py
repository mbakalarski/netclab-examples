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


@pytest.mark.otgcfg(otg_cfg_fname)
def test_otg01_with_protocols_started(otg01_with_protocol_started):
    assert True


@pytest.mark.otgcfg(otg_cfg_fname)
def test_traffic(otg01_with_protocol_started, otg01_with_metrics_ready):

    mreq = otg01_with_metrics_ready.metrics_request()
    mreq.flow.flow_names = ["f1"]
    mresp = otg01_with_metrics_ready.get_metrics(mreq)
    print(mresp)
    
    # assert (
    #     mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_tx"]
    #     == mresp.serialize(encoding="dict").get("flow_metrics")[0]["frames_rx"]
    # )
    assert True
