# Website (Nginx + Docker)

A simple Nginx-based web server running in Docker that displays a Hello, World (Christmas edition) page and is access on port 8080.

## Project Structure

.
├── Dockerfile
├── index.html
└── README.md

## Requirements

- Docker installed

Check Docker installation:
```docker --version```

## Build the Image

```docker build -t website-img .```

Verify the image:
```docker images```

## Run the Container

Remove existing container if needed:
```docker rm -website-img```

Run the container:
```docker run -d --name website-container -p 8080:80 website-img```

## Test the Application

Open in browser:
http://localhost:8080

Or via terminal:
```curl http://localhost:8080```

## View Logs

```docker logs website-container```

## Stop and Remove the Container

```docker stop website-container```
```docker rm website-container```
docker tag website-img titankir/website-img:1.0

## Push on Docker Hub
```docker tag website-img <username>/website-img:1.0```
```docker push <username>/website-img:1.0```