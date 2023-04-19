import hashlib
import os

import getmac
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

from add_machine import AddMachine
from wol import wake_machine, _ping

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()
HASHED_PASSWORD = os.getenv('HASHED_PASSWORD')
MACHINES_FILENAME = 'machines.db'

if not HASHED_PASSWORD:
    raise Exception('HASHED_PASSWORD is empty.')


async def check_ip_key(ip: str, key: str) -> None:
    if hashlib.sha384(key.encode('utf-8')).hexdigest() != HASHED_PASSWORD:
        raise HTTPException(detail='Error, key is invalid',
                            status_code=status.HTTP_401_UNAUTHORIZED)
    elif not ip.isascii():
        raise HTTPException(detail='Error, ip is invalid - not ascii',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif not ip:
        raise HTTPException(detail='Error, ip is null',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif len(ip) > 15:
        raise HTTPException(detail='Error, ip is too long (15 chars max)',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get('/')
async def read_root():
    with open('index.html', 'r') as f:
        data = f.read()
    return HTMLResponse(content=data, media_type="text/html", status_code=status.HTTP_200_OK)


@app.post('/wake')
async def wake(ip: str, key: str):
    await check_ip_key(ip, key)
    try:
        await wake_machine(ip, MACHINES_FILENAME)
    except Exception as e:
        raise HTTPException(detail=str(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return {'detail': f'Magic packet sent to {ip}'}


@app.get('/ping')
async def ping(ip: str, key: str):
    await check_ip_key(ip, key)
    try:
        ping_resp = await _ping(ip)
    except Exception as e:
        raise HTTPException(detail=str(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if ping_resp:
            return {'detail': f'{ip} successfully responded!'}

        else:
            return {'detail': f'{ip} did not respond!'}


@app.put('/add-machine')
async def add_machine(ip: str, key: str):
    await check_ip_key(ip, key)
    add_machine_obj = AddMachine(MACHINES_FILENAME)
    print(add_machine_obj.get_all_rows())

    mac = getmac.get_mac_address(ip=ip)
    if not mac:
        return {'detail': 'Could not fetch the mac address'}
    try:
        add_machine_obj.add_machine(ip, mac)
    except Exception as e:
        return {'detail': f'Error: {e}'}
    else:
        return {'detail': f'Successfully added {ip} in database'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=53562, log_level="info")
