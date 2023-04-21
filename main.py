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
HASHED_KEY = os.getenv('HASHED_KEY')
MACHINES_FILENAME = 'machines.db'

if not HASHED_KEY:
    raise Exception('HASHED_PASSWORD is empty.')


async def verify_key(key: str) -> None:
    if hashlib.sha384(key.encode('utf-8')).hexdigest() != HASHED_KEY:
        raise HTTPException(detail='Error, key invalid',
                            status_code=status.HTTP_401_UNAUTHORIZED)


async def verify_ip(ip: str) -> None:
    if not ip:
        raise HTTPException(detail='Error, ip is null',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if not ip.isascii():
        raise HTTPException(detail='Error, ip is not ASCII',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if len(ip) > 15:
        raise HTTPException(detail='Error, ip too long (15 chars max)',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    if len(ip) < 7:
        raise HTTPException(detail='Error, ip too short (7 chars min)',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    ip_segments: list[str, ...] = ip.split('.')
    if len(ip_segments) != 4:
        raise HTTPException(detail='Error, ip must have 4 segments',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        ip_segments: list[int, int, int, int] = [int(seg) for seg in ip_segments]
    except ValueError:
        raise HTTPException(detail='Error, ip not made of integers',
                            status_code=status.HTTP_401_UNAUTHORIZED)

    for seg in ip_segments:
        if seg > 255 or seg < 0:
            raise HTTPException(detail='Error, ip malformed',
                                status_code=status.HTTP_401_UNAUTHORIZED)


@app.get('/')
async def root():
    with open('index.html', 'r') as f:
        data = f.read()
    return HTMLResponse(content=data, media_type="text/html", status_code=status.HTTP_200_OK)


@app.post('/wake')
async def wake(ip: str, key: str):
    await verify_key(key)
    await verify_ip(ip)
    try:
        await wake_machine(ip, MACHINES_FILENAME)
    except Exception as e:
        raise HTTPException(detail=str(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return {'detail': f'Magic packet sent to {ip}'}


@app.get('/ping')
async def ping(ip: str, key: str):
    await verify_key(key)
    await verify_ip(ip)
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
    await verify_key(key)
    await verify_ip(ip)
    add_machine_obj = AddMachine(MACHINES_FILENAME)

    mac = getmac.get_mac_address(ip=ip)
    if not mac:
        return {'detail': 'Could not fetch the mac address'}
    try:
        add_machine_obj.add_machine(ip, mac)
    except Exception as e:
        return {'detail': f'Error: {e}'}
    else:
        return {'detail': f'Successfully added {ip} in database'}


@app.get('/database')
async def database(key: str):
    await verify_key(key)
    add_machine_obj = AddMachine(MACHINES_FILENAME)
    return {'detail': add_machine_obj.get_all_rows()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5545, log_level="info")
