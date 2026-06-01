# Changelog

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
