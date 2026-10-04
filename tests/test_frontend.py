from frontend.app import ApiError, api_request


def test_api_request_builds_url_and_parses_json(monkeypatch):
    import frontend.app as frontend

    class FakeResponse:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {"status": "healthy"}

    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, kwargs=kwargs)
        return FakeResponse()

    monkeypatch.setattr(frontend.requests, "request", fake_request)
    assert api_request("GET", "/health") == {"status": "healthy"}
    assert captured["url"] == f"{frontend.API_URL}/health"
    assert captured["kwargs"]["timeout"] == frontend.REQUEST_TIMEOUT


def test_api_request_reports_connection_errors(monkeypatch):
    import requests
    import frontend.app as frontend

    def fake_request(*args, **kwargs):
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(frontend.requests, "request", fake_request)
    try:
        api_request("GET", "/tasks")
    except ApiError as exc:
        assert "Could not reach the To-Do API" in str(exc)
    else:
        raise AssertionError("ApiError should be raised")
