def test_configured_csr(configured_csr01):
    out = configured_csr01.cli.execute("show run | in router")
    assert "router bgp 6500" in out


def test_not_configured_csr(csr01):
    out = csr01.cli.execute("show run | in router")
    assert "router bgp 6500" not in out
