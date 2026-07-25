# Videoflix API

## Overview
Videoflix is a video streaming application built with the Django REST Framework. Users can browse and watch videos directly within the application.
The platform supports multiple video resolutions, allowing users to watch videos in 480p, 720p, or 1080p, depending on their preferred video quality and available bandwidth.
Authentication is handled using JWT (JSON Web Tokens) and HTTP-only cookies to ensure secure management of user data.

---

## Features
- User registration, login, and logout
- Object-level permissions
- JWT-based authentication
- Video upload and management through the Django Admin Panel
- Video streaming and playback
- Support for multiple video resolutions: 480p, 720p, 1080p
- Automatic video transcoding into different resolutions
- Protected API endpoints

---

## Installation

### Requirements
- Python 3.12
- pip 26.1.1
- ffmpeg
- hls

## 1. Clone the repository
  ```bash
    git clone https://github.com/Pradi8/project.Quizly-backend  
  ```  
  ```bash 
    cd project.Quizly-backend
  ```

## 2. Create a virtual environment
  ```bash 
    python -m venv env
  ```

## 3. Activate the virtual environment
### <b>Linux/Mac</b>
```bash
  source env/bin/activate  
```
### <b>Windows</b>
```bash
  env\Scripts\activate      
```

## 4. Install Python dependencies
```bash
  python -m pip install -r requirements.txt
```

## 5. Install system dependencies

### WSL / Linux (Ubuntu)

#### Install FFmpeg

```bash
  sudo apt update
  sudo apt install ffmpeg
```

#### Install Deno

```bash
    curl -fsSL https://deno.land/install.sh | sh
```

### Windows

#### Install FFmpeg

Download a Windows build from the official website:

```bash
  https://ffmpeg.org/download.html
```

or use a trusted build provider:

```bash
  https://www.gyan.dev/ffmpeg/builds/
```
Extract the downloaded archive

Move it to a location such as:

```bash
  C:\ffmpeg
```

After extraction, your folder should look like:

```bash
  C:\ffmpeg\bin
```

Add FFmpeg to PATH

Add the following path to your Windows environment variables:

```bash
  C:\ffmpeg\bin
```

Steps:

1. Open System Environment Variables
2. Click Environment Variables
3. Select Path under System Variables
4. Click Edit
5. Add:

```bash
  C:\ffmpeg\bin
```
6. Save and close all dialogs
7. Verify Installation
   Open a new terminal and run:
```bash
  ffmpeg -version
```


####  Docker Installation

Docker is installed differently depending on the operating system. This document describes how to install Docker on **Windows**, **macOS**, and **Ubuntu/Debian Linux**.

## Windows

### 1. Download Docker Desktop

Download Docker Desktop from the official Docker website:

[Download Docker Desktop](https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com)

### 2. Start the Installation

Run the downloaded installer and follow the installation instructions.

If required, restart Windows after the installation.

### 3. Start Docker Desktop

Open Docker Desktop and wait until Docker has fully started.

### 4. Verify the Installation

Open **PowerShell** and run the following command:

```powershell
docker --version
```

You can then test whether Docker is working correctly with:

```powershell
docker run hello-world
```

---

## macOS

### 1. Download Docker Desktop

Download Docker Desktop from the official Docker website:

[Download Docker Desktop](https://www.docker.com/products/docker-desktop/?utm_source=chatgpt.com)

### 2. Select the Correct Version

Choose the appropriate version for your Mac:

* **Apple Silicon** (e.g., M1, M2, M3, M4)
* **Intel**

### 3. Install Docker Desktop

Install Docker Desktop and start the application.

### 4. Verify the Installation

Open the Terminal and run:

```bash
docker --version
```

You can then test Docker with:

```bash
docker run hello-world
```

---

## Ubuntu / Debian Linux

On Ubuntu and Debian, Docker can be installed using the official Docker repository.

### 1. Update Package Lists

```bash
sudo apt update
```

### 2. Install Docker

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 3. Verify the Installation

Test the Docker installation with:

```bash
sudo docker run hello-world
```

If the test runs successfully, Docker has been installed correctly.

---

## Check the Docker Version

You can check the installed Docker version at any time by running:

```bash
docker --version
```

## Check Docker Compose

If Docker Compose is installed, you can check its version with:

```bash
docker compose version
```

## Summary

| Operating System | Installation                          |
| ---------------- | ------------------------------------- |
| Windows          | Docker Desktop                        |
| macOS            | Docker Desktop                        |
| Ubuntu / Debian  | Docker Engine + Docker Compose Plugin |

After successfully installing Docker, you can use it to create, run, and manage containers.


### 2. Create your .env file

### Linux / macOS / Git Bash

```
cp .env.example .env
```
### Windows (CMD)

```
copy .env.example .env
```

### Windows (PowerShell)

```
Copy-Item .env.example .env
```

### 3. Configure your .env

Open the .env file and fill in your value:

GEMINI_API_KEY=your-api-key-here

## Notes

Make sure your `.env` file is not committed to Git. Add it to `.gitignore`:

```
gitignore.env
```

If the API key is missing or invalid, the application will not be able to connect to the Gemini API.

## 6. Create database migrations
```bash
  python manage.py makemigrations
```

## 7. Apply database migrations
```bash
  python manage.py migrate
```

## 8. Create a superuser (admin account)
```bash
  python manage.py createsuperuser
```

## 9. Start the development server
```bash
  python manage.py runserver  
```
  The project will be running at http://127.0.0.1:8000/


# Project Structure
```
auth_app/
├── api/
│   ├── authentication.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
videoflix/
├── api/
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── services/
│   └──hls.py 
├── models.py
├── signals.py
├── tasks.py
core/
├── settings.py

manage.py <br>
requirements.txt <br>
README.md

```