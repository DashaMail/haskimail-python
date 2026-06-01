from __future__ import annotations

import pytest

from haskimail import AccountClient, HaskimailError, InvalidAPIKeyError


class TestAccountClientInit:
    def test_requires_token(self):
        with pytest.raises(HaskimailError, match="valid API token"):
            AccountClient("")

    def test_sets_account_header(self, mock_session):
        client = AccountClient("my-account-token")
        headers = mock_session.headers.update.call_args[0][0]
        assert headers["X-Haskimail-Account-Token"] == "my-account-token"


class TestServers:
    def test_get_servers(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 1, "Servers": [{"ID": 1, "Name": "Production"}]}
        )
        result = account_client.get_servers(count=10)
        assert result["TotalCount"] == 1

    def test_create_server(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 2, "Name": "Staging"})
        result = account_client.create_server({"Name": "Staging", "Color": "Blue"})
        assert result["Name"] == "Staging"

    def test_delete_server(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {})
        account_client.delete_server(2)
        call_args = mock_session.request.call_args
        assert call_args[0] == ("DELETE", "https://api.haskimail.ru/servers/2")


class TestDomains:
    def test_get_domains(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 1, "Domains": [{"ID": 1, "Name": "example.com"}]}
        )
        result = account_client.get_domains()
        assert result["TotalCount"] == 1

    def test_create_domain(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 5, "Name": "test.com"})
        result = account_client.create_domain({"Name": "test.com"})
        assert result["Name"] == "test.com"

    def test_verify_dkim(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"DKIMVerified": True})
        result = account_client.verify_domain_dkim(5)
        assert result["DKIMVerified"] is True
        call_args = mock_session.request.call_args
        assert call_args[0] == ("PUT", "https://api.haskimail.ru/domains/5/verifyDkim")

    def test_verify_spf(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"SPFVerified": True})
        account_client.verify_domain_spf(5)
        call_args = mock_session.request.call_args
        assert call_args[0] == ("PUT", "https://api.haskimail.ru/domains/5/verifySPF")

    def test_rotate_dkim(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 5})
        account_client.rotate_domain_dkim(5)
        call_args = mock_session.request.call_args
        assert call_args[0] == ("POST", "https://api.haskimail.ru/domains/5/rotatedkim")


class TestSenderSignatures:
    def test_get_sender_signatures(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(
            200, {"TotalCount": 1, "SenderSignatures": []}
        )
        result = account_client.get_sender_signatures()
        assert "TotalCount" in result

    def test_create_sender_signature(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 10})
        result = account_client.create_sender_signature(
            {"Name": "Test", "FromEmail": "test@example.com"}
        )
        assert result["ID"] == 10

    def test_resend_confirmation(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {})
        account_client.resend_sender_signature_confirmation(10)
        call_args = mock_session.request.call_args
        assert call_args[0] == ("POST", "https://api.haskimail.ru/senders/10/resend")


class TestDataRemovals:
    def test_request_data_removal(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 1, "Status": "Pending"})
        result = account_client.request_data_removal(
            {"RequestedBy": "admin@test.com", "RequestedFor": "user@test.com"}
        )
        assert result["Status"] == "Pending"

    def test_get_data_removal_status(self, account_client, mock_session, ok_response):
        mock_session.request.return_value = ok_response(200, {"ID": 1, "Status": "Complete"})
        result = account_client.get_data_removal_status(1)
        assert result["Status"] == "Complete"


class TestErrorHandling:
    def test_invalid_api_key(self, account_client, mock_session, error_response):
        mock_session.request.return_value = error_response(401, 10, "Invalid API token")
        with pytest.raises(InvalidAPIKeyError):
            account_client.get_servers()
