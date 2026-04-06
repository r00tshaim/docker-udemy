# FastAPI CRUD Example

A simple FastAPI project using an in-memory Python dictionary as data storage.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
uv run uvicorn app.main:app --reload
```

## Endpoints

- `GET /items`
- `GET /items/{item_id}`
- `POST /items`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`

## Docker Lessons

### Lession 1: Build docker image of fastapi project using UBUNTU as base image

**Command:**

```bash
docker build -t fastapi-ubuntu .
```

**Explaination of Flags:**

*   `-t fastapi-ubuntu`: Tags the image with the name `fastapi-ubuntu`. This makes it easier to refer to the image later.
*   `.`: Specifies the build context, which is the current directory containing the Dockerfile.

**Output:**

```
[+] Building 0.6s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/ubuntu:latest
 => [auth] library/ubuntu:pull token for registry-1.docker.io
 => [internal] load build context
 => [1/5] FROM docker.io/library/ubuntu:latest@sha256:8b47c030d93026a79883651121d5565389659b8be4366533722b513364214f08
 => [2/5] WORKDIR /app
 => [3/5] COPY ./requirements.txt .
 => [4/5] RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install -r requirements.txt
 => [5/5] COPY .
 => exporting to image
 => => exporting layers
 => => writing image sha256:sha256_hash_here
 => => naming to docker.io/library/fastapi-ubuntu
```

### Lession 2: Creating a container from generated docker image

**Command:**

```bash
docker run fastapi-ubuntu
```

**Explaination of Flags:**

*   `fastapi-ubuntu`: The name of the Docker image to create a container from.

**Output:**

```
INFO:     Will watch for changes in these directories: ['/app']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [1] using statreload
INFO:     Started server process [8] using uvicorn.workers.UvicornWorker
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Lession 3: Reduce the docker image size using python:3.11-slim as base image

*   **Dockerfile Change:** Modify your `Dockerfile` to use `FROM python:3.11-slim` instead of `FROM ubuntu` to create a smaller image.

**Command:**

```bash
docker build -t fastapi-slim .
```

**Explaination of Flags:**

*   `-t fastapi-slim`: Tags the image with the name `fastapi-slim`, indicating it's the slim version.
*   `.`: Specifies the build context.

**Output:**

```
[+] Building 0.7s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [auth] library/python:pull token for registry-1.docker.io
 => [internal] load build context
 => [1/6] FROM docker.io/library/python:3.11-slim@sha256:sha256_hash_here
 => [2/6] WORKDIR /app
 => [3/6] COPY ./requirements.txt .
 => [4/6] RUN pip install -r requirements.txt
 => [5/6] COPY .
 => [6/6] EXPOSE 8000
 => exporting to image
 => => exporting layers
 => => writing image sha256:sha256_hash_here
 => => naming to docker.io/library/fastapi-slim
```

### Lession 4: Mapping the ports

**Command (Specific Port Mapping):**

```bash
docker run -p 5000:8000 fastapi-slim
```

**Explaination of Flags:**

*   `-p 5000:8000`: Maps port `5000` on the host machine to port `8000` inside the container. This allows you to access the FastAPI application from your host's port 5000.

**Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1] using uvicorn.workers.UvicornWorker
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Command (Automatic Port Mapping):**

```bash
docker run -P fastapi-slim
```

**Explaination of Flags:**

*   `-P`: (Capital P) Automatically maps all `EXPOSE`d ports in the container to random available high-numbered ports on the host machine.

**Output (showing port mapping):**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1] using uvicorn.workers.UvicornWorker
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

To see the mapped port, run `docker ps` in another terminal:

```bash
docker ps
```

Output of `docker ps`:

```
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                     NAMES
<container_id>   fastapi-slim   "uvicorn app.main:ap…"   5 seconds ago   Up 4 seconds   0.0.0.0:32768->8000/tcp   vigilant_goldberg
```

### Lession 5: Removing the conatiner as soon docker process exits (using --rm flag)

**Command:**

```bash
docker run --rm fastapi-slim
```

**Explaination of Flags:**

*   `--rm`: Automatically removes the container and its file system when the container exits. This helps keep your system clean by not leaving stopped containers.

**Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1] using uvicorn.workers.UvicornWorker
INFO:     Waiting for application startup.
INFO:     Application startup complete.
^CINFO:     Stopping reloader process [1]
INFO:     Stopped reloader process [1] using statreload
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
```

After the container exits (e.g., by pressing `CTRL+C`), if you run `docker ps -a`, you will not see this container in the list.

### Lession 6: detach mode (using -d)

**Command:**

```bash
docker run -d -p 5000:8000 fastapi-slim
```

**Explaination of Flags:**

*   `-d`: Runs the container in detached mode, meaning it runs in the background and prints the container ID.
