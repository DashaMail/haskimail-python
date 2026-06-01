from __future__ import annotations

from typing import Any

from .client import BaseClient

SERVER_TOKEN_HEADER = "X-Haskimail-Server-Token"


class ServerClient(BaseClient):
    """Haskimail Server API client.

    Uses a server-level API token for sending emails, managing templates,
    bounces, statistics, webhooks, message streams, and more.
    """

    def __init__(
        self,
        server_token: str,
        *,
        base_url: str = "https://api.haskimail.ru",
        timeout: int = 30,
    ):
        super().__init__(
            server_token,
            token_header=SERVER_TOKEN_HEADER,
            base_url=base_url,
            timeout=timeout,
        )

    # ── Email Sending ───────────────────────────────────────────────────────

    def send_email(self, email: dict[str, Any]) -> dict:
        """Send a single email.

        Required keys: ``From``, ``To``, ``Subject``, and ``HtmlBody`` or ``TextBody``.
        """
        return self._post("/email", body=email)

    def send_email_batch(self, emails: list[dict[str, Any]]) -> list:
        """Send a batch of up to 500 emails in one API call."""
        return self._post("/email/batch", body=emails)

    def send_email_with_template(self, template: dict[str, Any]) -> dict:
        """Send an email using a template.

        Required keys: ``TemplateId`` or ``TemplateAlias``, ``From``, ``To``,
        and ``TemplateModel``.
        """
        return self._post("/email/withTemplate", body=template)

    def send_email_batch_with_templates(self, templates: list[dict[str, Any]]) -> list:
        """Send a batch of template-based emails."""
        return self._post("/email/batchWithTemplates", body=templates)

    # ── Bounces ─────────────────────────────────────────────────────────────

    def get_delivery_statistics(self) -> dict:
        """Get overall delivery statistics including bounce counts by type."""
        return self._get("/deliverystats")

    def get_bounces(self, **filters: Any) -> dict:
        """Get a paginated list of bounces.

        Filters: ``count``, ``offset``, ``type``, ``fromdate``, ``todate``,
        ``emailFilter``, ``tag``, ``messageID``, ``messagestream``.
        """
        return self._get("/bounces", **filters)

    def get_bounce(self, bounce_id: int) -> dict:
        """Get details for a single bounce."""
        return self._get(f"/bounces/{bounce_id}")

    def get_bounce_dump(self, bounce_id: int) -> dict:
        """Get the raw SMTP dump for a bounce."""
        return self._get(f"/bounces/{bounce_id}/dump")

    def activate_bounce(self, bounce_id: int) -> dict:
        """Reactivate a hard-bounced recipient."""
        return self._put(f"/bounces/{bounce_id}/activate")

    # ── Templates ───────────────────────────────────────────────────────────

    def get_templates(self, **filters: Any) -> dict:
        """List templates. Filters: ``count``, ``offset``, ``TemplateType``."""
        return self._get("/templates", **filters)

    def get_template(self, id_or_alias: int | str) -> dict:
        """Get a template by numeric ID or string alias."""
        return self._get(f"/templates/{id_or_alias}")

    def create_template(self, options: dict[str, Any]) -> dict:
        """Create a new template."""
        return self._post("/templates", body=options)

    def edit_template(self, id_or_alias: int | str, options: dict[str, Any]) -> dict:
        """Update an existing template."""
        return self._put(f"/templates/{id_or_alias}", body=options)

    def delete_template(self, id_or_alias: int | str) -> dict:
        """Delete a template."""
        return self._delete(f"/templates/{id_or_alias}")

    def validate_template(self, options: dict[str, Any]) -> dict:
        """Validate template content without creating it."""
        return self._post("/templates/validate", body=options)

    # ── Server ──────────────────────────────────────────────────────────────

    def get_server(self) -> dict:
        """Get the current server's settings."""
        return self._get("/server")

    def edit_server(self, options: dict[str, Any]) -> dict:
        """Update the current server's settings."""
        return self._put("/server", body=options)

    # ── Outbound Messages ───────────────────────────────────────────────────

    def get_outbound_messages(self, **filters: Any) -> dict:
        """List outbound (sent) messages.

        Filters: ``count``, ``offset``, ``recipient``, ``fromemail``,
        ``tag``, ``subject``, ``status``, ``fromdate``, ``todate``,
        ``metadata_*``, ``messagestream``.
        """
        return self._get("/messages/outbound", **filters)

    def get_outbound_message_details(self, message_id: str) -> dict:
        """Get full details for a sent message."""
        return self._get(f"/messages/outbound/{message_id}/details")

    def get_outbound_message_dump(self, message_id: str) -> dict:
        """Get the raw SMTP source of a sent message."""
        return self._get(f"/messages/outbound/{message_id}/dump")

    # ── Message Opens ───────────────────────────────────────────────────────

    def get_message_opens(self, **filters: Any) -> dict:
        """List message open events.

        Filters: ``count``, ``offset``, ``recipient``, ``tag``,
        ``client_name``, ``client_company``, ``client_family``,
        ``os_name``, ``os_family``, ``os_company``, ``platform``,
        ``country``, ``region``, ``city``, ``messagestream``.
        """
        return self._get("/messages/outbound/opens", **filters)

    def get_message_opens_for_single_message(
        self, message_id: str, **filters: Any
    ) -> dict:
        """List open events for a specific message."""
        return self._get(f"/messages/outbound/opens/{message_id}", **filters)

    # ── Message Clicks ──────────────────────────────────────────────────────

    def get_message_clicks(self, **filters: Any) -> dict:
        """List message click events.

        Filters: ``count``, ``offset``, ``recipient``, ``tag``,
        ``client_name``, ``client_company``, ``client_family``,
        ``os_name``, ``os_family``, ``os_company``, ``platform``,
        ``country``, ``region``, ``city``, ``messagestream``.
        """
        return self._get("/messages/outbound/clicks", **filters)

    def get_message_clicks_for_single_message(
        self, message_id: str, **filters: Any
    ) -> dict:
        """List click events for a specific message."""
        return self._get(f"/messages/outbound/clicks/{message_id}", **filters)

    # ── Statistics ──────────────────────────────────────────────────────────

    def get_outbound_overview(self, **filters: Any) -> dict:
        """Get a summary of outbound email statistics.

        Filters: ``tag``, ``fromdate``, ``todate``, ``messagestream``.
        """
        return self._get("/stats/outbound", **filters)

    def get_sent_counts(self, **filters: Any) -> dict:
        """Get sent email counts grouped by day."""
        return self._get("/stats/outbound/sends", **filters)

    def get_bounce_counts(self, **filters: Any) -> dict:
        """Get bounce counts grouped by day and type."""
        return self._get("/stats/outbound/bounces", **filters)

    def get_spam_complaints_counts(self, **filters: Any) -> dict:
        """Get spam complaint counts grouped by day."""
        return self._get("/stats/outbound/spam", **filters)

    def get_tracked_email_counts(self, **filters: Any) -> dict:
        """Get counts of tracked emails grouped by day."""
        return self._get("/stats/outbound/tracked", **filters)

    def get_email_open_counts(self, **filters: Any) -> dict:
        """Get email open counts grouped by day."""
        return self._get("/stats/outbound/opens", **filters)

    def get_email_open_platform_usage(self, **filters: Any) -> dict:
        """Get email open stats grouped by platform (desktop, mobile, etc.)."""
        return self._get("/stats/outbound/opens/platforms", **filters)

    def get_email_open_client_usage(self, **filters: Any) -> dict:
        """Get email open stats grouped by email client."""
        return self._get("/stats/outbound/opens/emailclients", **filters)

    def get_email_open_read_times(self, **filters: Any) -> dict:
        """Get email read-time distribution."""
        return self._get("/stats/outbound/opens/readtimes", **filters)

    def get_click_counts(self, **filters: Any) -> dict:
        """Get link click counts grouped by day."""
        return self._get("/stats/outbound/clicks", **filters)

    def get_click_browser_usage(self, **filters: Any) -> dict:
        """Get click stats grouped by browser family."""
        return self._get("/stats/outbound/clicks/browserfamilies", **filters)

    def get_click_platform_usage(self, **filters: Any) -> dict:
        """Get click stats grouped by platform."""
        return self._get("/stats/outbound/clicks/platforms", **filters)

    def get_click_location(self, **filters: Any) -> dict:
        """Get click stats grouped by geographic location."""
        return self._get("/stats/outbound/clicks/location", **filters)

    # ── Webhooks ────────────────────────────────────────────────────────────

    def get_webhooks(self, **filters: Any) -> dict:
        """List webhooks. Filters: ``MessageStream``."""
        return self._get("/webhooks", **filters)

    def get_webhook(self, webhook_id: int) -> dict:
        """Get a webhook by ID."""
        return self._get(f"/webhooks/{webhook_id}")

    def create_webhook(self, options: dict[str, Any]) -> dict:
        """Create a new webhook."""
        return self._post("/webhooks", body=options)

    def edit_webhook(self, webhook_id: int, options: dict[str, Any]) -> dict:
        """Update a webhook."""
        return self._put(f"/webhooks/{webhook_id}", body=options)

    def delete_webhook(self, webhook_id: int) -> dict:
        """Delete a webhook."""
        return self._delete(f"/webhooks/{webhook_id}")

    # ── Message Streams ─────────────────────────────────────────────────────

    def get_message_streams(self, **filters: Any) -> dict:
        """List message streams (channels).

        Filters: ``MessageStreamType`` (All, Transactional, Broadcasts),
        ``IncludeArchivedStreams``.
        """
        return self._get("/message-streams", **filters)

    def get_message_stream(self, stream_id: str) -> dict:
        """Get a message stream by ID."""
        return self._get(f"/message-streams/{stream_id}")

    def create_message_stream(self, options: dict[str, Any]) -> dict:
        """Create a new message stream."""
        return self._post("/message-streams", body=options)

    def edit_message_stream(self, stream_id: str, options: dict[str, Any]) -> dict:
        """Update a message stream."""
        return self._patch(f"/message-streams/{stream_id}", body=options)

    def archive_message_stream(self, stream_id: str) -> dict:
        """Archive a message stream."""
        return self._post(f"/message-streams/{stream_id}/archive")

    def unarchive_message_stream(self, stream_id: str) -> dict:
        """Unarchive a previously archived message stream."""
        return self._post(f"/message-streams/{stream_id}/unarchive")

    # ── Suppressions ────────────────────────────────────────────────────────

    def get_suppressions(self, stream_id: str, **filters: Any) -> dict:
        """Get the suppression list for a message stream.

        Filters: ``SuppressionReason``, ``Origin``, ``fromdate``, ``todate``,
        ``EmailAddress``.
        """
        return self._get(f"/message-streams/{stream_id}/suppressions/dump", **filters)

    def create_suppressions(
        self, stream_id: str, options: dict[str, Any]
    ) -> dict:
        """Add email addresses to the suppression list."""
        return self._post(
            f"/message-streams/{stream_id}/suppressions", body=options
        )

    def delete_suppressions(
        self, stream_id: str, options: dict[str, Any]
    ) -> dict:
        """Remove email addresses from the suppression list."""
        return self._post(
            f"/message-streams/{stream_id}/suppressions/delete", body=options
        )
