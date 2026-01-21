╔══════════════════════════════════════╗
║           ZERO2CLOUD // LOCK-IN      ║
║          DOCKER CHEAT SHEET          ║
╚══════════════════════════════════════╝

Purpose: Daily Docker reps for Zero2Cloud
Last Updated: 2026-01-20

=========================================
WHAT IS DOCKER? (1-LINER)
=========================================
Docker lets you run apps in isolated containers:
- same app, same setup, same behavior anywhere

=========================================
CORE WORDS
=========================================
Image     = template (blueprint)
Container = running instance of an image
Dockerfile= recipe to build an image
Volume    = storage that persists
Network   = container communication layer

=========================================
CHECK DOCKER
=========================================
docker --version
docker ps                # running containers
docker ps -a             # all containers
docker images            # list images
docker info              # system info

=========================================
RUN CONTAINERS
=========================================
docker run hello-world

docker run -it ubuntu bash
# -i interactive, -t terminal

docker run -it --rm ubuntu bash
# --rm deletes container when you exit

docker run -d nginx
# -d runs in background

=========================================
STOP / REMOVE
=========================================
docker stop <container>
docker start <container>
docker restart <container>

docker rm <container>
docker rmi <image>

=========================================
LOGS + INSPECT
=========================================
docker logs <container>
docker logs -f <container>        # follow logs live

docker inspect <container>
docker exec -it <container> bash  # enter a running container

=========================================
PORTS
=========================================
docker run -p 8080:80 nginx
# host:container

Then open:
http://localhost:8080

=========================================
VOLUMES (SAVE DATA)
=========================================
docker volume ls
docker volume create mydata

docker run -it -v mydata:/data ubuntu bash
# volume_name:/path/in/container

Bind mount (map a folder from your PC):
docker run -it -v "$PWD":/work ubuntu bash

=========================================
BUILD IMAGES (DOCKERFILE)
=========================================
docker build -t myapp:1 .

Run it:
docker run --rm myapp:1

=========================================
CLEANUP (KEEP SYSTEM FAST)
=========================================
docker system df
docker system prune
# WARNING: removes unused stuff

More aggressive:
docker system prune -a

=========================================
DOCKER COMPOSE (MULTI-CONTAINER)
=========================================
docker compose version
docker compose up -d
docker compose down
docker compose logs -f

=========================================
ZERO2CLOUD DOCKER GOLDEN RULES
=========================================
- Images are READ-ONLY
- Containers are disposable
- Volumes persist your important data
- Use --rm when practicing to keep it clean
=========================================

