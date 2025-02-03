def test_before_configured_bgp(csr01):
    out = csr01.cli.execute("show run | in router")
    assert "router bgp 6500" not in out


def test_configured_bgp(configured_csr01):
    out = configured_csr01.cli.execute("show run | in router")
    assert "router bgp 6500" in out


def test_after_configured_bgp(csr01):
    out = csr01.cli.execute("show run | in router")
    assert "router bgp 6500" not in out
