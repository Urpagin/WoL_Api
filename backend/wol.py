from pythonping import ping
from wakeonlan import send_magic_packet

from add_machine import AddMachine


async def wake_machine(ip: str, filename: str) -> None:
    add_machine_obj = AddMachine(filename)
    data: list[tuple[str, str], ...] | list[None] = add_machine_obj.contains_ip(ip)
    if not data:
        raise Exception("Could not find mac address in database")
    mac: str = data[0][1]
    if mac == "00:00:00:00:00:00":
        raise Exception("Cannot wake the machine, mac is 00:00:00:00:00:00")
    send_magic_packet(mac)


async def _ping(ip: str) -> bool:
    return ping(target=ip, timeout=1).success()
