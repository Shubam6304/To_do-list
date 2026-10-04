import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 5


class ApiError(Exception):
    """An API request failed or returned an unexpected response."""


def api_request(method: str, path: str, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ApiError(f"Could not reach the To-Do API at {API_URL}: {exc}") from exc

    if response.status_code == 204:
        return None
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise ApiError("The To-Do API returned an invalid response.") from exc


def render_app():
    st.set_page_config(
        page_title="To-Do List",
        page_icon="✅",
        layout="centered",
    )
    st.title("✅ To-Do List")
    st.caption("Streamlit frontend • FastAPI backend • SQLite database")

    with st.form("add_task", clear_on_submit=True):
        st.subheader("Add a task")
        title = st.text_input("Task", max_chars=200)
        description = st.text_area("Description (optional)")
        submitted = st.form_submit_button("➕ Add task", use_container_width=True)
        if submitted:
            if not title.strip():
                st.warning("Enter a task title.")
            else:
                try:
                    api_request(
                        "POST",
                        "/tasks",
                        json={
                            "title": title,
                            "description": description or None,
                            "completed": False,
                        },
                    )
                except ApiError as exc:
                    st.error(str(exc))
                else:
                    st.rerun()

    try:
        tasks = api_request("GET", "/tasks")
    except ApiError as exc:
        st.error(str(exc))
        st.info("Start the backend with `uvicorn backend.main:app --reload`.")
        return

    total = len(tasks)
    completed_count = sum(task["completed"] for task in tasks)
    pending_count = total - completed_count
    columns = st.columns(3)
    columns[0].metric("Total", total)
    columns[1].metric("Pending", pending_count)
    columns[2].metric("Completed", completed_count)
    st.divider()

    selected_filter = st.radio(
        "Filter tasks",
        ("All", "Pending", "Completed"),
        horizontal=True,
    )
    if selected_filter == "Pending":
        tasks = [task for task in tasks if not task["completed"]]
    elif selected_filter == "Completed":
        tasks = [task for task in tasks if task["completed"]]

    if not tasks:
        st.info("No tasks yet." if total == 0 else "No tasks match this filter.")
    else:
        for task in tasks:
            with st.container(border=True):
                task_columns = st.columns([0.08, 0.72, 0.20])
                completed = task_columns[0].checkbox(
                    "Done",
                    value=task["completed"],
                    key=f"completed_{task['id']}",
                    label_visibility="collapsed",
                )

                if task["completed"]:
                    task_columns[1].markdown(f"### ~~{task['title']}~~")
                else:
                    task_columns[1].markdown(f"### {task['title']}")
                if task.get("description"):
                    task_columns[1].write(task["description"])

                if task_columns[2].button(
                    "🗑️ Delete",
                    key=f"delete_{task['id']}",
                    use_container_width=True,
                ):
                    try:
                        api_request("DELETE", f"/tasks/{task['id']}")
                    except ApiError as exc:
                        st.error(str(exc))
                    else:
                        st.rerun()

                if completed != task["completed"]:
                    try:
                        api_request(
                            "PUT",
                            f"/tasks/{task['id']}",
                            json={"completed": completed},
                        )
                    except ApiError as exc:
                        st.error(str(exc))
                    else:
                        st.rerun()

    with st.sidebar:
        st.header("Settings")
        st.write(f"Backend: `{API_URL}`")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
        st.divider()
        st.write("API documentation:")
        st.code(f"{API_URL}/docs")


if __name__ == "__main__":
    render_app()
