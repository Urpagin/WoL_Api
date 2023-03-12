from wakeonlan import send_magic_packet
# from getmac import get_mac_address

ips = {
    "192.168.1.40": "e4:5f:01:24:bf:8b",  # Raspberry Pi
    "192.168.1.45": "a8:a1:59:66:7a:ba",  # MiniPc
    "192.168.1.10": "80:61:5f:10:f5:f0"   # Main Pc
}


def wake_machine(ip: str):
    if ip not in ips:
        raise Exception("ip does not correspond to any mac address.")
    else:
        send_magic_packet(ips[ip])
