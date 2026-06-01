from __future__ import annotations

from typing import Any

import requests

from .exceptions import HaskimailError, build_request_error

DEFAULT_BASE_URL = "https://api.haskimail.ru"
DEFAULT_TIMEOUT = 30


class BaseClient:
    """Low-level HTTP client shared by ServerClient and AccountClient."""

    def __init__(
        self,
        token: str,
        *,
        token_header: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        if not token:
            raise HaskimailError("A valid API token is required.")

        self._token = token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                token_header: token,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": f"haskimail-python/{_get_version()}",
            }
        )

    # -- HTTP verbs -----------------------------------------------------------

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: dict | list | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict | list:
        url = f"{self._base_url}{path}"

        kwargs: dict[str, Any] = {"timeout": self._timeout}
        if params:
            kwargs["params"] = {k: v for k, v in params.items() if v is not None}
        if body is not None:
            kwargs["json"] = body

        response = self._session.request(method, url, **kwargs)

        if response.status_code == 200:
            if not response.content:
                return {}
            return response.json()

        try:
            error_body = response.json()
        except Exception:
            error_body = None

        raise build_request_error(response.status_code, error_body)

    def _get(self, path: str, **params: Any) -> dict | list:
        return self._request("GET", path, params=params)

    def _post(self, path: str, body: dict | list | None = None) -> dict | list:
        return self._request("POST", path, body=body)

    def _put(self, path: str, body: dict | None = None) -> dict | list:
        return self._request("PUT", path, body=body)

    def _patch(self, path: str, body: dict | None = None) -> dict | list:
        return self._request("PATCH", path, body=body)

    def _delete(self, path: str) -> dict | list:
        return self._request("DELETE", path)

    # -- Lifecycle ------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _get_version() -> str:
    try:
        from importlib.metadata import version

        return version("haskimail")
    except Exception:
        return "0.0.0"
