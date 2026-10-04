# To-Do List Application

A small full-stack task manager with a Streamlit UI, FastAPI REST API, and SQLite persistence.

## Requirements

- Python 3.10 or newer
- pip

## Setup

From the project root, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you need to customize the configuration. The defaults work locally. Relative SQLite database paths are resolved from this project directory, not the current shell directory. Do not commit `.env`.

## Run the application

Open two terminals in the project root and activate the virtual environment in each.

Start the API:

```powershell
python -m uvicorn backend.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive documentation is at `http://127.0.0.1:8000/docs`.

Start the Streamlit UI:

```powershell
python -m streamlit run frontend/app.py
```

The UI is normally available at `http://localhost:8501`. The SQLite database (`todo.db` by default) and its parent directory are created automatically when the API starts.

## Features

- Create tasks with optional descriptions
- View all tasks and filter pending or completed tasks
- Mark tasks complete or pending and delete them
- Persistent SQLite storage
- FastAPI validation and interactive API documentation
- Configurable API and database URLs through environment variables

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | API status |
| `GET` | `/health` | Health check |
| `GET` | `/tasks` | List tasks |
| `POST` | `/tasks` | Create a task |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

Task titles are trimmed and must contain 1–200 characters. Create-task JSON may include `title`, `description`, and `completed`; updates may include any subset of those fields.

## Tests

Install root requirements, then run:

```powershell
python -m pytest
```

The API tests use a temporary in-memory SQLite database and do not rely on the runtime database.

## Deployment and workflow

See [DEPLOYMENT.md](DEPLOYMENT.md) for Render and Streamlit Community Cloud setup, and [WORKFLOW.md](WORKFLOW.md) for the request flow and GitHub Actions workflow.
