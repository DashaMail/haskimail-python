from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from haskimail import AccountClient, ServerClient


def _make_response(status_code: int = 200, body: dict | list | None = None) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = json.dumps(body).encode() if body is not None else b""
    resp.json.return_value = body
    return resp


@pytest.fixture
def mock_session():
    with patch("haskimail.client.requests.Session") as mock_cls:
        session = MagicMock()
        mock_cls.return_value = session
        yield session


@pytest.fixture
def server_client(mock_session) -> ServerClient:
    return ServerClient("test-server-token")


@pytest.fixture
def account_client(mock_session) -> AccountClient:
    return AccountClient("test-account-token")


@pytest.fixture
def ok_response():
    return _make_response


@pytest.fixture
def error_response():
    def _make(status_code: int, error_code: int = 0, message: str = "Error"):
        return _make_response(status_code, {"ErrorCode": error_code, "Message": message})
    return _make
