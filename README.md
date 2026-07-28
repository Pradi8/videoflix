# Videoflix API

## Overview

Videoflix is a video streaming application built with the **Django REST Framework**. Users can browse and watch videos directly within the application.

The platform supports multiple video resolutions, allowing users to watch videos in **480p, 720p, or 1080p**, depending on their preferred video quality and available bandwidth.

Authentication is handled using **JWT (JSON Web Tokens)** and **HTTP-only cookies** to ensure secure management of user data.

---

## Features

- User registration, login, and logout
- Object-level permissions
- JWT-based authentication
- HTTP-only cookies for secure token management
- Video upload and management through the **Django Admin Panel**
- Video streaming and playback
- Support for multiple video resolutions:
  - 480p
  - 720p
  - 1080p
- Automatic video transcoding into different resolutions
- HLS-based video streaming
- Protected API endpoints

---

## Development

The application is fully containerized using Docker and Docker Compose.

The project consists of the following main components:

- **Django** version 6.0.3 as the web framework
- **Python** version 3.12.7 as the programming language
- **Django REST Framework** for the REST API
- **PostgreSQL** for database management
- **Redis** for background job queuing
- **Django RQ** for managing background tasks
- **RQ Worker** for processing asynchronous jobs
- **FFmpeg** for video processing and transcoding
- **HLS** for video streaming
- **Gunicorn** for running the Django application
- **WhiteNoise** for serving static files
- **Docker** for containerization

FFmpeg is installed automatically inside the Docker container during the image build.

Python dependencies are installed automatically from `requirements.txt` during the Docker image build.

PostgreSQL and Redis are started automatically as Docker containers using Docker Compose.


## Requirements

Before running the project, make sure the following software is installed:

- Docker
- Docker Compose

Docker Desktop includes Docker Engine and Docker Compose.

Download Docker Desktop:

https://www.docker.com/products/docker-desktop/

Verify the installation:

```bash
docker --version
docker compose version
```

### Docker Installation

Download and install Docker Desktop for your operating system:

[Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

Docker Desktop includes Docker Engine and Docker Compose.

After installation, verify that Docker is working correctly:

```bash
docker --version
```

## Installation

### 1. Clone the Repository

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/Pradi8/videoflix
cd videoflix
```

### 2. Create the `.env` File

Create a `.env` file based on the provided `.env.template` file.

#### Linux / macOS / Git Bash

```bash
cp .env.template .env
```

#### Windows CMD

```cmd
copy .env.template .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.template .env
```

### 3. Configure the `.env` File

Open the `.env` file and configure the required environment variables.

Make sure your `.env` file is not committed to Git. Add it to your `.gitignore` file:

```gitignore
.env
```

### 4. Build and Start the Application

Build the Docker image and start all required containers:

```bash
docker compose up --build
```

To run the containers in the background:

```bash
docker compose up --build -d
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

Follow the instructions in the terminal to enter the username, email address, and password.

The Django Admin Panel will be available at:

```text
http://127.0.0.1:8000/admin/
```

### 5. Upload Videos

Videos can be uploaded and managed through the **Django Admin Panel**.

1. Open:

   ```text
   http://127.0.0.1:8000/admin/
   ```

2. Log in with your superuser credentials.
3. Upload and manage videos through the admin interface.

The uploaded videos are processed and made available for streaming in different resolutions.

---

## Docker Commands

### Start the Application

```bash
docker compose up
```

### Start in the Background

```bash
docker compose up -d
```

### Apply Database Migrations

If database migrations are not applied automatically, run:

```bash
docker compose exec web python manage.py migrate
```

> **Note:** The Django service is named `web` in the `docker-compose.yml`.

### Create a Superuser

To create a Django superuser for accessing the Django Admin Panel, run:

```bash
docker compose exec web python manage.py createsuperuser
```

### Rebuild the Containers

```bash
docker compose up --build
```

### Stop the Application

```bash
docker compose down
```

### Stop Containers and Remove Volumes

```bash
docker compose down -v
```

### View Container Logs

```bash
docker compose logs
```

### View Logs in Real Time

```bash
docker compose logs -f
```

---

## Project Structure

```text
auth_app/
├── api/
│   ├── authentication.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py

core/
├──  settings.py

videoflix/
├── api/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── services/
│   └── hls.py
├── models.py
├── signals.py
├── tasks.py

templates/
├── emails/
│   ├── confirm.html
│   ├── password_reset.html

utils/
└──email.py

manage.py
requirements.txt
docker-compose.yml
backend.Dockerfile
backend.entrypoint.sh
.env.template
README.md
```

---