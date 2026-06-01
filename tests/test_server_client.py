from __future__ import annotations

import pytest

from haskimail import (
    HaskimailError,
    InactiveRecipientsError,
    InvalidAPIKeyError,
    InvalidEmailRequestError,
    RateLimitExceededError,
    ServerClient,
)


class TestServerClientInit:
    def test_requires_token(self):
        with pytest.raises(HaskimailError, match="valid API token"):
            ServerClient("")

    def test_sets_auth_header(self, mock_session):
        client = ServerClient("my-token")
        headers = mock_session.headers.update.call_args[0][0]
        assert headers["X-Haskimail-Server-Token"] == "my-token"
        assert headers["Accept"] == "application/json"


class TestSendEmail:
    def test_send_email(self, server_client, mock_session, ok_response):
        body = {"MessageID": "abc-123", "SubmittedAt": "2026-06-01T12:00:00Z"}
        mock_session.request.return_value = ok_response(200, body)

        result = server_client.send_email(
            {
                "From": "sender@example.com",
                "To": "recipient@example.com",
                "Subject": "Test",
                "TextBody": "Hello!",
            }
        )

        assert result["MessageID"] == "abc-123"
        mock_session.request.assert_called_once()
        call_args = mock_session.request.call_args
        assert call_args[0] == ("POST", "https://api.haskimail.ru/email")

    def test_send_email_batch(self, server_client, mock_session, ok_response):
        batch_result = [{"MessageID": "1"}, {"MessageID": "2"}]
        mock_session.request.return_value = ok_response(200, batch_result)

        result = server_client.send_email_batch(
            [
                {"From": "a@b.com", "To": "c@d.com", "Subject": "1", "TextBody": "1"},
                {"From": "a@b.com", "To": "e@f.com", "Subject": "2", "TextBody": "2"},
            ]
        )

        assert len(result) == 2

    def test_send_email_with_template(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"MessageID": "tpl-1"})

        result = server_client.send_email_with_template(
            {
                "TemplateId": 42,
                "From": "a@b.com",
                "To": "c@d.com",
                "TemplateModel": {"name": "Test"},
            }
        )

        assert result["MessageID"] == "tpl-1"


class TestBounces:
    def test_get_bounces(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 1, "Bounces": [{"ID": 1}]}
        )
        result = server_client.get_bounces(count=10, offset=0)
        assert result["TotalCount"] == 1

    def test_activate_bounce(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 42, "Email": "a@b.com"})
        result = server_client.activate_bounce(42)
        assert result["ID"] == 42
        call_args = mock_session.request.call_args
        assert call_args[0] == ("PUT", "https://api.haskimail.ru/bounces/42/activate")


class TestTemplates:
    def test_get_templates(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 2, "Templates": [{"TemplateId": 1}, {"TemplateId": 2}]}
        )
        result = server_client.get_templates(count=50)
        assert result["TotalCount"] == 2

    def test_create_template(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"TemplateId": 99})
        result = server_client.create_template(
            {"Name": "Welcome", "Subject": "Hello", "HtmlBody": "<h1>Hi</h1>"}
        )
        assert result["TemplateId"] == 99


class TestMessageStreams:
    def test_get_message_streams(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 2, "MessageStreams": []}
        )
        result = server_client.get_message_streams()
        assert "TotalCount" in result

    def test_archive_stream(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": "marketing", "Archived": True})
        result = server_client.archive_message_stream("marketing")
        call_args = mock_session.request.call_args
        assert call_args[0] == ("POST", "https://api.haskimail.ru/message-streams/marketing/archive")


class TestSuppressions:
    def test_get_suppressions(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"Suppressions": []})
        result = server_client.get_suppressions("outbound", SuppressionReason="HardBounce")
        call_args = mock_session.request.call_args
        assert "/message-streams/outbound/suppressions/dump" in call_args[0][1]

    def test_create_suppressions(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"Suppressions": []})
        server_client.create_suppressions(
            "outbound", {"Suppressions": [{"EmailAddress": "spam@test.com"}]}
        )
        call_args = mock_session.request.call_args
        assert "/message-streams/outbound/suppressions" in call_args[0][1]


class TestWebhooks:
    def test_create_webhook(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 1})
        result = server_client.create_webhook({"Url": "https://example.com/hook"})
        assert result["ID"] == 1


class TestErrorHandling:
    def test_invalid_api_key(self, server_client, mock_session, error_response):
        mock_session.request.return_value = error_response(401, 10, "Invalid API token")
        with pytest.raises(InvalidAPIKeyError) as exc_info:
            server_client.send_email({"From": "a@b.com", "To": "c@d.com"})
        assert exc_info.value.error_code == 10

    def test_inactive_recipient(self, server_client, mock_session, ok_response):
        resp = ok_response(
            422,
            {
                "ErrorCode": 406,
                "Message": "Inactive recipient",
                "Errors": [{"Email": "bad@test.com"}],
            },
        )
        mock_session.request.return_value = resp
        with pytest.raises(InactiveRecipientsError) as exc_info:
            server_client.send_email({"From": "a@b.com", "To": "bad@test.com"})
        assert "bad@test.com" in exc_info.value.recipients

    def test_invalid_email_request(self, server_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            422, {"ErrorCode": 300, "Message": "Invalid JSON"}
        )
        with pytest.raises(InvalidEmailRequestError):
            server_client.send_email({})

    def test_rate_limit(self, server_client, mock_session, error_response):
        mock_session.request.return_value = error_response(429, 0, "Rate limit exceeded")
        with pytest.raises(RateLimitExceededError):
            server_client.get_bounces()


class TestContextManager:
    def test_context_manager(self, mock_session):
        with ServerClient("token") as client:
            pass
        mock_session.close.assert_called_once()
