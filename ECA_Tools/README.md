# ECA Tools

ECA Tools is a Flask + SageMath web application for elliptic curve computations.

It currently includes:
- Curve order calculations from user input
- Listing elliptic curve points and point orders
- A simple web UI with calculator and credits pages

Live deployment (Render):
- https://eca-tools.onrender.com

## Project Structure

- `WebApp/app.py` - Flask routes and form handling
- `WebApp/webapp_helpers.py` - validation and helper utilities
- `WebApp/scripts/find_Curve_Order.py` - curve order computation script
- `WebApp/scripts/List_Elliptic_Curve_Pts_N_Ordrs.py` - point and order listing script
- `WebApp/scripts/Point_Add.py` - elliptic curve point addition
- `WebApp/scripts/Point_Substract.py` - elliptic curve point subtraction
- `WebApp/scripts/Point_Multiply.py` - scalar multiplication on elliptic curves
- `WebApp/scripts/Point_Divide.py` - finds points whose scalar multiple equals a given point
- `WebApp/templates/` - HTML templates and CSS
- `WebApp/requirements.txt` - Python dependencies
- `WebApp/Dockerfile` - container image definition
- `WebApp/docker-compose.yml` - local container orchestration

## Prerequisites

For local development with Docker:
- Docker Desktop installed

For deployment:
- A GitHub repository containing this project
- A Render account

## Run Locally (Docker Compose)

From `2026/ECA_Tools/WebApp`:

```bash
docker compose up -d --build
```

Open:
- http://localhost:8080

Stop the app:

```bash
docker compose down
```

Optional logs:

```bash
docker compose logs -f web
```

## Deploy on Render

### 1. Push code to GitHub
- Create a repository (or use an existing one).
- Push the `BE_Projects/2026/ECA_Tools/WebApp` code (or the whole project).

### 2. Create a new Web Service on Render
- Sign in to Render.
- Click **New +** -> **Web Service**.
- Connect your GitHub account and select your repository.

### 3. Configure service settings
Use these settings:
- Runtime: **Docker**
- Root Directory:
  - If your repo root is `BE_Projects`, set: `2026/ECA_Tools/WebApp`
  - If `WebApp` is at repo root, leave blank

### 4. Deploy
- Click **Create Web Service**.
- Wait for build and deploy to finish.
- Open the generated Render URL.

## Notes
- The app runs Sage scripts through subprocess calls with a 120-second timeout.
- The container starts with Gunicorn on port `8080`.
- Render can override `PORT`; local Docker Compose already maps `8080:8080`.
