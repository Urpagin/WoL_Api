# 🌐 Wake on LAN API

Python REST API that wakes a machine (that supports WoL) from outside the local network.

## 📦 Installation

> [!NOTE]
> We currently bake the `backend/.env` file into the Docker image, which is considered bad practice. This might be fixed in future updates.

### 🐳 Docker Compose (recommended)

Clone the repository:

```bash
git clone https://github.com/Urpagin/WoL_Api/
```

Navigate to the repository:

```bash
cd WoL_Api
```

Create and populate your `.env` file:

```bash
vim .env
```

Add the following to `.env`:

```env
HASHED_KEY=<HASHEDKEY>
```

Use [this tool](https://emn178.github.io/online-tools/sha384.html) to hash your password with **SHA384**.

Launch the Docker Compose setup:

```bash
sudo docker compose up -d
```

### 🐳 Docker

Follow the steps in [Docker Compose](#-docker-compose-recommended) up to and including the `.env` setup.

Then build the Docker image:

```bash
docker build -t urpagin/wol-api:0.0.1 .
```

Check the image ID:

```bash
docker images
```

Run the Docker container (replace `<IMAGEID>` with the actual image ID):

```bash
docker run -d --restart=always --network host --name wol-api <IMAGEID>
```

### 🐍 Python

Follow the steps in [Docker Compose](#-docker-compose-recommended) up to and including the `.env` setup.

Install the dependencies:

```bash
pip install -r backend/requirements.txt
```

Run the application from the root directory (not from inside `backend`):

```bash
python backend/main.py
```

---

✅ It's Saul Goodman! Execute `docker ps` to list running containers or `docker ps -a` to view both running and stopped containers, useful if `wol-api` crashes.

## ⚙️ API Specifications

* `/` (**GET**): Simple static HTTP endpoint to check API status.
* `/wake` (**POST**): Accepts `key` and `ip`; wakes a machine using a magic packet.
* `/ping` (**GET**): Accepts `key` and `ip`; returns the ping response from the machine.
* `/add-machine` (**PUT**): Accepts `key` and `ip`; retrieves the MAC address of `ip` and stores the tuple `(ip, mac)` in the database.
* `/database` (**GET**): Accepts `key`; returns the database content as a list.

**Note**: All responses are JSON formatted: `{"detail": <RESPONSE>}`.

**Note**: Before using `/wake`, ensure you've added the machine's MAC address to the database using `/add-machine`.

---

![programming-background](https://user-images.githubusercontent.com/72459611/233224334-12f22cf9-489b-4838-96ae-3dfb699e1a4f.jpg)

![Hero-Wodaabe-nomads-in-Chad](https://user-images.githubusercontent.com/72459611/232763128-d5a71109-091f-45da-af54-b923ab919c3f.jpg)

![flag-india](https://user-images.githubusercontent.com/72459611/233224416-2acf770f-5706-4983-bbc2-fb2e78d30cd6.jpg)

**Image Credits**: [Image by www.slon.pics](https://www.freepik.com/free-photo/flag-india_1179373.htm#query=india&position=16&from_view=search&track=sph) on Freepik.
