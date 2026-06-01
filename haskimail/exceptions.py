from __future__ import annotations


class HaskimailError(Exception):
    """Base exception for all Haskimail SDK errors."""

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)


class HttpError(HaskimailError):
    """HTTP-level error from the Haskimail API."""

    status_code: int = 0
    error_code: int = 0
    body: dict | None = None

    def __init__(
        self,
        message: str = "",
        status_code: int = 0,
        error_code: int = 0,
        body: dict | None = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.body = body
        super().__init__(message)

    def __str__(self) -> str:
        parts = [self.message]
        if self.error_code:
            parts.append(f"ErrorCode: {self.error_code}")
        if self.status_code:
            parts.append(f"HTTP {self.status_code}")
        return " | ".join(parts)


class InvalidAPIKeyError(HttpError):
    """Raised when the API token is missing or invalid (HTTP 401)."""

    status_code: int = 401


class ApiInputError(HttpError):
    """Raised when the API rejects the input (HTTP 422)."""

    status_code: int = 422


class InactiveRecipientsError(ApiInputError):
    """Raised when sending to an inactive recipient (ErrorCode 406)."""

    def __init__(self, recipients: list[str] | None = None, **kwargs):
        self.recipients = recipients or []
        super().__init__(**kwargs)


class InvalidEmailRequestError(ApiInputError):
    """Raised when the email request is malformed (ErrorCode 300)."""


class RateLimitExceededError(HttpError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""

    status_code: int = 429


class InternalServerError(HttpError):
    """Raised on Haskimail server errors (HTTP 500)."""

    status_code: int = 500


class ServiceUnavailableError(HttpError):
    """Raised when the API is under maintenance (HTTP 503)."""

    status_code: int = 503


class UnknownError(HttpError):
    """Raised for unexpected HTTP errors."""


_ERROR_CODE_MAP: dict[int, type[HttpError]] = {
    300: InvalidEmailRequestError,
    406: InactiveRecipientsError,
}

_STATUS_CODE_MAP: dict[int, type[HttpError]] = {
    401: InvalidAPIKeyError,
    422: ApiInputError,
    429: RateLimitExceededError,
    500: InternalServerError,
    503: ServiceUnavailableError,
}


def build_request_error(
    status_code: int,
    body: dict | None = None,
) -> HttpError:
    """Build the appropriate exception from an API error response."""
    error_code = (body or {}).get("ErrorCode", 0)
    message = (body or {}).get("Message", f"HTTP {status_code}")

    cls = _ERROR_CODE_MAP.get(error_code) or _STATUS_CODE_MAP.get(status_code, UnknownError)

    kwargs: dict = dict(
        message=message,
        status_code=status_code,
        error_code=error_code,
        body=body,
    )

    if cls is InactiveRecipientsError:
        recipients: list[str] = []
        if body and "Errors" in body:
            for err in body["Errors"]:
                email = err.get("Email")
                if email:
                    recipients.append(email)
        kwargs["recipients"] = recipients

    return cls(**kwargs)
