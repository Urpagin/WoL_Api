import hashlib
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status

from wol import wake_machine, _ping

app = FastAPI()

load_dotenv()
HASHED_PASSWORD = os.getenv('HASHED_PASSWORD')
if not HASHED_PASSWORD:
    raise Exception('HASHED_PASSWORD is empty.')


async def test_ip_pass_for_errors(ip: str, password: str) -> None:
    if hashlib.sha384(password.encode('utf-8')).hexdigest() != HASHED_PASSWORD:
        print(password)
        raise HTTPException(detail='Error, password is invalid',
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
    html = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <META NAME="robots" CONTENT="noindex,nofollow">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WoL API</title>
</head>
<body style="background-color:bisque"></body>
<body>
    <h1 style="font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif">
    Congratulations, you are here!</h1>
    
</body>
</html>
    """
    return HTMLResponse(html, status_code=200)


@app.post('/wake')
async def wake(ip: str, password: str):
    await test_ip_pass_for_errors(ip, password)
    try:
        await wake_machine(ip)
    except Exception as e:
        raise HTTPException(detail=str(e),
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return {'detail': f'Magic packet sent to {ip}'}


@app.get('/ping')
async def ping(ip: str, password: str):
    await test_ip_pass_for_errors(ip, password)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=53562, log_level="info")
