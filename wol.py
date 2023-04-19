import polars
from pythonping import ping
from wakeonlan import send_magic_packet

from add_machine import AddMachine


async def wake_machine(ip: str, filename: str) -> None:
    add_machine_obj = AddMachine(filename)
    data: polars.Series = add_machine_obj.read_csv().to_dict()

    for i, file_ip in enumerate(data['IP']):
        if file_ip == ip:
            send_magic_packet(data['MAC'][i])
            return

    raise Exception("Could not find the machine's mac address in database")


async def _ping(ip: str) -> bool:
    return ping(target=ip, timeout=1).success()
