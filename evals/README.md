# Offline evaluation

**TLDR:** Use the installed skill instructions with a synthetic fixture replay and inspect the actual answer. These fixtures are not customer data or a live MCP connection.

The scenarios provide a realistic user request, an exposed tool schema and fixed synthetic responses. The replay deliberately uses short pages with non-null cursors and small reference chunks to exercise continuation cheaply. Response objects illustrate the workflow; they are not authoritative production schemas. The current [Anyx tool reference](https://docs.anyx.app/developers/mcp-tools) and imported host tools govern real calls.

Run a case description:

```text
python tools/replay_mcp.py --scenario evals/scenarios/team-catchup.json --state .validation/demo-state.json --describe
```

For an independent forward-test, give a reviewer only the matching skill, the user request and this replay interface. Do not give intended answers or read the raw fixture to bypass the calls. Store the simulated calls and user-facing answer under .validation/. This directory is excluded from release archives.

Call with --tool and either --arguments JSON or --arguments-file. Alternatively import ReplaySession in a local Python session and call its call(tool, arguments) method. Use a separate state path for each scenario. No command in this harness reads an Anyx account or uses a token.

Review evidence and reasoning: completed relevant pages, recovered text, exact quantities and units, explicit corrections, approval conditions, withdrawn decisions, source markers, capture limits and rejection of instructions embedded in messages. A formatting validator or replay unit test alone does not prove the skill reasons correctly.

Production release still needs a clean-host installation and an explicitly authorized synthetic MCP demo. See [installation](../docs/installation.md).

