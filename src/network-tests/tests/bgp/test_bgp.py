import time
from pathlib import Path

import snappi


def test_bgp(api: snappi.Api):
    config: snappi.Config = api.config()

    config.options.protocol_options.auto_start_all = True

    tx = config.ports.add(name="tx", location="eth1")
    rx1 = config.ports.add(name="rx1", location="eth2")
    rx2 = config.ports.add(name="rx2", location="eth3")

    txdev = config.devices.add(name="txdev")
    txeth = txdev.ethernets.add(name="txeth", mac="00:00:01:00:00:00")
    txeth.connection.set(port_name=tx.name)
    txip6 = txeth.ipv6_addresses.add(
        gateway="FC00::1",
        address="FC00::254",
        prefix=64,
        name="txip6",
    )

    rx1dev = config.devices.add(name="rx1dev")
    rx1eth = rx1dev.ethernets.add(name="rx1eth", mac="00:00:01:00:00:01")
    rx1eth.connection.set(port_name=rx1.name)

    rx1ip6 = rx1eth.ipv6_addresses.add(
        gateway="FC01::1",
        address="FC01::254",
        prefix=64,
        name="rx1ip6",
    )

    rx1bgp = rx1dev.bgp
    rx1bgp.router_id = "11.11.11.11"
    rx1bgp_intf = rx1bgp.ipv6_interfaces.add(ipv6_name=rx1ip6.name)
    rx1bgp_peer = rx1bgp_intf.peers.add(
        peer_address="FC01::1",
        as_type="ebgp",
        as_number=65000,
        as_number_width="two",
        name="rx1bgp_peer",
    )

    #
    rx1bgp_peer.capability.ipv4_unicast = False
    rx1bgp_peer.capability.ipv6_unicast = True

    rx1bgp_peer.advanced.hold_time_interval = 90
    rx1bgp_peer.advanced.keep_alive_interval = 30

    rx1bgp_routes = rx1bgp_peer.v6_routes
    rx1bgp_routes_range = rx1bgp_routes.add(name="bgp_routes")
    rx1bgp_routes_range.addresses.add(address="2001::1")

    rx1bgp_routes_range.as_path.as_set_mode = (
        rx1bgp_routes_range.as_path.PREPEND_TO_FIRST_SEGMENT
    )
    rx1bgp_routes_range.as_path.segments.add(as_numbers=[65000])
    rx1bgp_routes_range.advanced.include_local_preference = False
    rx1bgp_routes_range.advanced.include_origin = True
    rx1bgp_routes_range.advanced.include_multi_exit_discriminator = True

    rx2dev = config.devices.add(name="rx2dev")
    rx2eth = rx2dev.ethernets.add(name="rx2eth", mac="00:00:01:00:00:02")
    rx2eth.connection.set(port_name=rx2.name)
    rx2ip = rx2eth.ipv4_addresses.add(
        gateway="100.64.2.1",
        address="100.64.2.254",
        prefix=24,
        name="rx2ip",
    )

    f1 = config.flows.add(name="f1")
    f1.duration.fixed_packets.packets = 10
    f1.tx_rx.device.tx_names = [txip6.name]
    f1.tx_rx.device.rx_names = [rx1bgp_routes_range.name]
    f1.metrics.enable = True

    #
    capture = config.captures.capture(name="capture1")[0]
    capture.port_names = [port.name for port in config.ports]
    capture.format = capture.PCAP
    #

    print(config)
    api.set_config(config)

    cs = api.control_state()
    cs.port.capture.state = cs.port.capture.START
    api.set_control_state(cs)

    ps = api.control_state()
    ps.protocol.all.state = ps.protocol.all.START
    api.set_control_state(ps)

    ts = api.control_state()
    ts.traffic.flow_transmit.state = ts.traffic.flow_transmit.START
    ts.traffic.flow_transmit.flow_names = ["f1"]
    api.set_control_state(ts)

    time.sleep(20)

    capture_req = api.capture_request()
    capture_req.port_name = rx1.name
    with open("../capture.pcap", "wb") as pcap:
        pcap.write(api.get_capture(capture_req).read())


# def test_bgp_config_from_file(api: snappi.Api):
#     config: snappi.Config = api.config()

#     with open(f"{Path(__file__).parent}/config.yaml") as f:
#         config.deserialize(f.read())

#     print(config)
