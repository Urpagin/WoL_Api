# Wake on Lan API

Python REST API that wakes a machine (that supports wol) from outside the local network.

## Installation

### 🐳 Docker Compose (recommended)

```bash
git clone https://github.com/Urpagin/WoL_Api/
```
```bash
cd WoL_Api
```
```bash
vim .env
```
Then populate `.env` with `HASHED_KEY=<HASHEDKEY>`   
Use [this webpage](https://emn178.github.io/online-tools/sha384.html) to hash your password using the **SHA384** hashing algorithm.

```bash
sudo docker compose up -d
```


### 🐳 Docker

Follow steps in the [Docker Compose](#-docker-compose-recommended) section up to and including the `.env`.

Then you can:

```bash
docker build -t urpagin/wol-api:0.0.1 .
```
```bash
docker images
```
Then copy image ID
```bash
docker run -d --restart=always --network host --name wol-api <IMAGEID>
```

### 🐍 Python

Follow steps in the [Docker Compose](#-docker-compose-recommended) section up to and including the `.env`.

Then you can:

Install the dependencies.
```bash
pip install -r backend/requirements.txt
```

Run the program; make sure to run it from the root level, **not** inside `backend`
```bash
python backend/main.py
```




It's Saul Goodman. Now you can execute `docker ps` to show all running containers or `docker ps -a` to show all running and exited containers in case wol-api crashed.

## ⚙️ API Specs
      
`/`(GET): simple static HTTP to check the API   
`/wake`(POST): takes `key` and `ip` wakes a machine with pagic packet       
`/ping`(GET): takes `key` and `ip` returns the ping response of the machine   
`/add-machine`(PUT): takes `key` and `ip` gets the mac address of `ip` and ands the tuple (ip, mac) into database   
`/database`(GET): takes `key` returns the database content in the form of a list.   

Note: all responses are json `{"detail": <RESPONSE>}`   
Note X2: before using `/wake` make sure you added the machine's mac address to the database with `/add-machine`


![programming-background-with-person-working-with-codes-computer (1)](https://user-images.githubusercontent.com/72459611/233224334-12f22cf9-489b-4838-96ae-3dfb699e1a4f.jpg)

![Hero-Wodaabe-nomads-in-Chad-Photo-credit-Tariq-Zaidi-Zuma-Press-01](https://user-images.githubusercontent.com/72459611/232763128-d5a71109-091f-45da-af54-b923ab919c3f.jpg)

![flag-india](https://user-images.githubusercontent.com/72459611/233224416-2acf770f-5706-4983-bbc2-fb2e78d30cd6.jpg)

Image Credits: <a href="https://www.freepik.com/free-photo/flag-india_1179373.htm#query=india&position=16&from_view=search&track=sph">Image by www.slon.pics</a> on Freepik
