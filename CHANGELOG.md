# Changelog

## 1.1.0 (2026-10-13)

The client now matches the methods the Haskimail API actually serves.

- Fixed paths: statistics use `/stats/sends`, `/stats/opens` and the like
  instead of `/stats/outbound/...`; SPF verification uses `verifyspf`.
- `send_email_batch` and `send_email_batch_with_templates` now have a server
  side: up to 500 emails and 50 MB per request. The response is a list in the
  order of the request; check `ErrorCode` of every item, the HTTP status is 200
  even when some emails are rejected.
- Removed methods that have no endpoint in the API and never worked: bounce
  lookup, activation and dump, message dump, sender signatures, DKIM rotation,
  domain edit and Return-Path verification, template validation, `get_server`
  and `edit_server` of the server client, tracked counts and platform, email
  client, browser, click location and read-time statistics, data removals.

## 1.0.0 (2026-06-01)

Initial release.

- `ServerClient` with full API coverage: email sending, bounces, templates,
  server management, outbound messages, opens, clicks, statistics,
  webhooks, message streams, and suppressions.
- `AccountClient` with full API coverage: servers, domains, sender signatures,
  template push, and data removals.
- Typed exception hierarchy matching the HTTP error codes from the Haskimail API.
- Context manager support for automatic session cleanup.
- Type hints throughout for IDE autocompletion.
