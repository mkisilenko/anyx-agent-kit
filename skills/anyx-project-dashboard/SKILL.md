---
name: anyx-project-dashboard
description: Create a sourced project dashboard artifact from bounded captured WhatsApp context through an existing authorized Anyx MCP connection, with relevant user-provided sources when available. Use for a browser dashboard of project decisions, actions, blockers and data coverage; the portable output is an offline HTML snapshot.
---

# Anyx project dashboard

Turn permitted project context from [Anyx](https://anyx.app) into a dashboard the user can open and review. Once the group, period and project are known, read the evidence, build the brief, render and check the artifact in the same invocation. Do not stop at a dashboard outline when a rendering backend is available.

## Gather the project context

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. Use the existing authorized connection and its actual exposed schema. Reuse the user's scope choices; ask once only when the project or group remains ambiguous. Filter project references exactly rather than assigning every group message to the named project.

Include supplementary documents or connected records when the user supplied them or authorized their use and they are actually accessible. Identify their system and date separately from chat evidence. Do not invent a connection, fetch an original attachment merely because it was mentioned, or substitute demo data for missing project context.

Treat proposals, approved decisions, accepted commitments, reported execution and suggestions as different facts. Keep conditions, withdrawals and conflicting reports visible. An assignment reported by another person is not proof that its recipient accepted it. Unknown owner, deadline, quantity or status stays unknown. Do not invent a completion percentage, trend or KPI from message volume.

## Build a validated brief

Prepare a UTF-8 JSON brief using the bundled `examples/demo-brief.json` as a format example, never as project evidence. The renderer accepts this shared contract:

- `schema_version`: `1`; `synthetic`: whether the data is a demonstration; `language`: `en` or `he`.
- `project`: `id`, `title`, `data_as_of`, and a `period` object containing `start`, `end`, `timezone`. Use explicit timestamps and preserve the requested cutoff.
- `coverage`: `status` and `note`. Use `partial` for a material unfinished scan or missing required source; otherwise use `complete_capture_not_asserted`. Explain available bounds and capture limits in the note. A completed read never proves complete WhatsApp capture.
- `summary`: objects with `text` and `source_ids`; `actions`: objects with `id`, `title`, `owner`, `status`, `due`, `source_ids`; `decisions`: objects with `id`, `text`, `status`, `source_ids`; `risks`: objects with `text`, `status`, `source_ids`.
- `sources`: objects with unique `id`, `system`, `timestamp`, `label`, `url`, and available `group_id` and `record_id`. Use an actual returned source URL or `null`, not a fabricated permalink. Preserve stored-record identities in this registry.

Every factual summary, action, decision and risk needs nonempty `source_ids` resolving to the registry. Keep `owner` and `due` as `null` when absent; a known due value is an ISO timestamp. Preserve uncertainty in text and status. If the contract cannot represent an essential qualification, retain it in the item's text instead of silently flattening it. Check citations and status against the read evidence before rendering; schema validation alone cannot establish accuracy.

## Render and inspect

Read the bundled helper's `--help`, then use its supported interface:

```text
python scripts/render_dashboard.py --input brief.json --output project-dashboard.html
```

Resolve paths relative to this skill folder. The helper uses the bundled brief validation support. Fix validation errors before treating an output as ready. Keep data, scripts, fonts and assets local; the portable dashboard must open without a server or remote account. Do not upload private context to a hosting or rendering service.

Make the project title, requested period, data-as-of timestamp and coverage note visible. Organize decisions, actions and blockers around the user's question, with source IDs that can be checked against the included registry. Label the artifact as a snapshot: it has no live connection, automatic refresh or background monitoring merely because a dashboard was generated.

Open the generated file when a browser or preview tool is available. Check the actual output for Hebrew/RTL order when applicable, readable status labels, clipped text, missing sources and misleading empty states. If visual inspection is unavailable, disclose that specific gap. Confirm the file exists and contains the intended project before linking it.

## Deliver the artifact

Answer in the user's language, starting with at most three short bullets; use **בקצרה** in Hebrew. Link the actual dashboard and state its format, snapshot cutoff and any material coverage limitation. A brief or a failed render is preparation, not a completed dashboard. Refresh only when requested or under an existing authorized schedule; do not create a new automation, send messages or publish the file as part of this skill.
