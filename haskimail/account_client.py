from __future__ import annotations

from typing import Any

from .client import BaseClient

ACCOUNT_TOKEN_HEADER = "X-Haskimail-Account-Token"


class AccountClient(BaseClient):
    """Haskimail Account API client.

    Uses an account-level API token for managing servers, domains,
    sender signatures, and other account-wide resources.
    """

    def __init__(
        self,
        account_token: str,
        *,
        base_url: str = "https://api.haskimail.ru",
        timeout: int = 30,
    ):
        super().__init__(
            account_token,
            token_header=ACCOUNT_TOKEN_HEADER,
            base_url=base_url,
            timeout=timeout,
        )

    # ── Servers ─────────────────────────────────────────────────────────────

    def get_servers(self, **filters: Any) -> dict:
        """List servers. Filters: ``count``, ``offset``, ``name``."""
        return self._get("/servers", **filters)

    def get_server(self, server_id: int) -> dict:
        """Get a server by ID."""
        return self._get(f"/servers/{server_id}")

    def create_server(self, options: dict[str, Any]) -> dict:
        """Create a new server."""
        return self._post("/servers", body=options)

    def edit_server(self, server_id: int, options: dict[str, Any]) -> dict:
        """Update server settings."""
        return self._put(f"/servers/{server_id}", body=options)

    def delete_server(self, server_id: int) -> dict:
        """Delete a server."""
        return self._delete(f"/servers/{server_id}")

    # ── Domains ─────────────────────────────────────────────────────────────

    def get_domains(self, **filters: Any) -> dict:
        """List domains. Filters: ``count``, ``offset``."""
        return self._get("/domains", **filters)

    def get_domain(self, domain_id: int) -> dict:
        """Get a domain by ID."""
        return self._get(f"/domains/{domain_id}")

    def create_domain(self, options: dict[str, Any]) -> dict:
        """Register a new domain."""
        return self._post("/domains", body=options)

    def edit_domain(self, domain_id: int, options: dict[str, Any]) -> dict:
        """Update a domain."""
        return self._put(f"/domains/{domain_id}", body=options)

    def delete_domain(self, domain_id: int) -> dict:
        """Delete a domain."""
        return self._delete(f"/domains/{domain_id}")

    def verify_domain_dkim(self, domain_id: int) -> dict:
        """Trigger DKIM verification for a domain."""
        return self._put(f"/domains/{domain_id}/verifyDkim")

    def verify_domain_return_path(self, domain_id: int) -> dict:
        """Trigger Return-Path verification for a domain."""
        return self._put(f"/domains/{domain_id}/verifyReturnPath")

    def verify_domain_spf(self, domain_id: int) -> dict:
        """Trigger SPF verification for a domain."""
        return self._put(f"/domains/{domain_id}/verifySPF")

    def rotate_domain_dkim(self, domain_id: int) -> dict:
        """Rotate the DKIM key for a domain."""
        return self._post(f"/domains/{domain_id}/rotatedkim")

    # ── Sender Signatures ───────────────────────────────────────────────────

    def get_sender_signatures(self, **filters: Any) -> dict:
        """List sender signatures. Filters: ``count``, ``offset``."""
        return self._get("/senders", **filters)

    def get_sender_signature(self, signature_id: int) -> dict:
        """Get a sender signature by ID."""
        return self._get(f"/senders/{signature_id}")

    def create_sender_signature(self, options: dict[str, Any]) -> dict:
        """Create a new sender signature."""
        return self._post("/senders", body=options)

    def edit_sender_signature(
        self, signature_id: int, options: dict[str, Any]
    ) -> dict:
        """Update a sender signature."""
        return self._put(f"/senders/{signature_id}", body=options)

    def delete_sender_signature(self, signature_id: int) -> dict:
        """Delete a sender signature."""
        return self._delete(f"/senders/{signature_id}")

    def resend_sender_signature_confirmation(self, signature_id: int) -> dict:
        """Resend the confirmation email for a sender signature."""
        return self._post(f"/senders/{signature_id}/resend")

    def verify_sender_signature_spf(self, signature_id: int) -> dict:
        """Trigger SPF verification for a sender signature."""
        return self._post(f"/senders/{signature_id}/verifyspf")

    def request_new_dkim_for_sender_signature(self, signature_id: int) -> dict:
        """Request a new DKIM key for a sender signature."""
        return self._post(f"/senders/{signature_id}/requestnewdkim")

    # ── Templates (Account-level) ───────────────────────────────────────────

    def push_templates(self, options: dict[str, Any]) -> dict:
        """Push templates from one server to another."""
        return self._put("/templates/push", body=options)

    # ── Data Removals ───────────────────────────────────────────────────────

    def request_data_removal(self, options: dict[str, Any]) -> dict:
        """Submit a data removal request (GDPR)."""
        return self._post("/data-removals", body=options)

    def get_data_removal_status(self, removal_id: int) -> dict:
        """Check the status of a data removal request."""
        return self._get(f"/data-removals/{removal_id}")
