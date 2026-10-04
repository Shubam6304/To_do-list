# Deployment Notes

## Backend on Render

Create a Web Service and connect the GitHub repository.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

After deployment, copy the backend URL.

Example:

```text
https://your-backend.onrender.com
```

## Frontend on Streamlit Community Cloud

Connect the same GitHub repository.

Main file:

```text
frontend/app.py
```

Set the environment variable:

```text
API_URL=https://your-backend.onrender.com
```

The frontend will then communicate with the deployed FastAPI backend.

## Important

SQLite is suitable for learning/local projects. For a production application with multiple users, use PostgreSQL or another hosted database. Render's local filesystem may be ephemeral; use a persistent disk or a hosted database if deployed data must survive service restarts or redeployments.
