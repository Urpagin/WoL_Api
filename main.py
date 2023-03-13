from fastapi import FastAPI, HTTPException
from starlette import status

from wake_on_lan import wake_machine, _ping

app = FastAPI()
PASSWORD = 'Uqv6VRd5MOUlGj3Vcavt1Zkid65OfntIAUcb9NgdnmFPRGU24O'


async def test_ip_pass_for_errors(ip: str, password: str) -> None:
    if password != PASSWORD:
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
            return {'detail': 'Ping successful!'}

        else:
            return {'detail': 'Ping failed'}
