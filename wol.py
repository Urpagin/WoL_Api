from wakeonlan import send_magic_packet
from pythonping import ping
from getmac import get_mac_address


async def wake_machine(ip: str) -> None:
    try:
        send_magic_packet(get_mac_address(ip=ip))
    except Exception:
        raise Exception("Could not fetch the machine's mac address")


async def _ping(ip: str) -> bool:
    return ping(target=ip, timeout=1).success()
