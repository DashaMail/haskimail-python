"""Haskimail Python SDK — official Python client for the Haskimail API."""

from __future__ import annotations

try:
    from importlib.metadata import version

    __version__ = version("haskimail")
except Exception:
    __version__ = "0.0.0"

from .account_client import AccountClient
from .exceptions import (
    ApiInputError,
    HaskimailError,
    HttpError,
    InactiveRecipientsError,
    InternalServerError,
    InvalidAPIKeyError,
    InvalidEmailRequestError,
    RateLimitExceededError,
    ServiceUnavailableError,
    UnknownError,
)
from .server_client import ServerClient

__all__ = [
    "__version__",
    "ServerClient",
    "AccountClient",
    # Exceptions
    "HaskimailError",
    "HttpError",
    "InvalidAPIKeyError",
    "ApiInputError",
    "InactiveRecipientsError",
    "InvalidEmailRequestError",
    "RateLimitExceededError",
    "InternalServerError",
    "ServiceUnavailableError",
    "UnknownError",
]
