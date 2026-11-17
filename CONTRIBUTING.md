# Contributing to Anyx Agent Kit

**TLDR:** Use synthetic data, keep evidence and permissions intact, and open a focused PR with the checks that cover your change.

## Development

Run `python tools/validate_kit.py`, `python -m unittest discover -s tests`, and `python tools/build_skill_zips.py`. For a workflow change, add or update a realistic synthetic scenario and run an independent forward-test. Offline adapter tests do not establish live MCP or destination integration support.

Keep each skill self-contained. Update every bundled shared renderer contract copy when that contract changes. Preserve optional backend requirements and never turn a composition or proposed change into a claimed completed artifact or remote write.

## Data and credentials

Do not open public issues or PRs with customer WhatsApp messages, private CRM records, authentication keys, cookies or signed URLs. Use a minimal fictional reproduction. A code contribution does not authorize an account connection, external action, merge or deployment.

## Integrations

An API documentation row is not an implemented connector. To claim a tested integration, include the actual client/version, authenticated demo scope, permitted read/write operations and observed receipt/readback. Keep ongoing writes inside their granted scope and reconcile unknown outcomes before retrying.

## License

Contributions to this kit are distributed under its MIT license. External rendering tools and destination services retain their own licenses and account terms.

