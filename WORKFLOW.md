# Application Workflow

## User workflow

```text
User
  |
  v
Streamlit Frontend
  |
  | HTTP requests
  v
FastAPI Backend
  |
  v
SQLAlchemy
  |
  v
SQLite Database
```

## Add Task

```text
User enters title/description
        |
        v
Streamlit POST /tasks
        |
        v
FastAPI validates request
        |
        v
SQLAlchemy inserts Task
        |
        v
SQLite stores task
        |
        v
API returns created task
        |
        v
Streamlit refreshes UI
```

## Complete Task

```text
Checkbox changed
      |
      v
PUT /tasks/{id}
      |
      v
FastAPI updates completed field
      |
      v
SQLite
      |
      v
Updated task returned
```

## Delete Task

```text
Delete button
      |
      v
DELETE /tasks/{id}
      |
      v
FastAPI finds task
      |
      v
SQLAlchemy deletes task
      |
      v
SQLite updated
      |
      v
Streamlit refreshes UI
```

## GitHub workflow

```text
Local Project
     |
     v
git init
     |
     v
git add .
     |
     v
git commit
     |
     v
git push
     |
     v
GitHub Repository
     |
     v
GitHub Actions
     |
     +--> Install dependencies
     |
     +--> Compile Python
     |
     +--> Import backend
     |
     +--> Run tests
```
