---
name: anyx-project-presentation
description: Create a sourced project presentation artifact from bounded captured WhatsApp context through an existing authorized Anyx MCP connection and relevant accessible user-provided sources. Use for review or status slides; deliver the actual native format when supported or clearly label the portable HTML slide deck fallback.
---

# Anyx project presentation

Build a concise, reviewable presentation from project evidence supplied through [Anyx](https://anyx.app). When scope is already clear, gather the evidence and render the deck in the same invocation. An outline alone does not complete a presentation request when a suitable backend is available.

## Gather the evidence

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. Use only the existing authorized connection, returned groups and arguments exposed by the host. Reuse the requested project and time period. Resolve an ambiguous project or group once rather than choosing by guesswork.

Use supplied or authorized supplementary sources when actually available. Keep each source's system, timestamp and evidence limits separate. A chat's reference to a drawing, quote or original file does not establish its contents. Do not assume a CRM, document connector or native presentation backend is connected.

Build the narrative around the audience's decision: current state, decisions and their conditions, accepted actions, blockers and the next unresolved choice. Review later corrections before selecting the headline. Distinguish approved work from proposed work and reported progress from independently verified completion. Keep an unassigned follow-up unassigned; do not turn a presentation recommendation into a team commitment.

## Build the structured brief

Create a UTF-8 JSON brief compatible with the bundled `examples/demo-brief.json`; demo content is a format example only.

- `schema_version`: `1`; `synthetic`: demonstration flag; `language`: `en` or `he`.
- `project`: `id`, `title`, `data_as_of`, and a `period` object with `start`, `end`, `timezone`.
- `coverage`: `status` of `partial` for a materially unfinished read or missing required source, otherwise `complete_capture_not_asserted`; `note` with the available bounds, completed reading and capture limits.
- `summary`: `{text, source_ids}` objects; `actions`: `{id, title, owner, status, due, source_ids}` objects; `decisions`: `{id, text, status, source_ids}` objects; `risks`: `{text, status, source_ids}` objects.
- `sources`: unique `{id, system, timestamp, label, url}` records, retaining available `group_id` and `record_id`. A missing URL is `null`; do not fabricate a chat link.

All factual items require nonempty, resolvable `source_ids`. Preserve a missing owner or deadline as `null`; known due values use ISO timestamps. Preserve conditions and uncertainty in the item text and status. Validate the evidence mapping as well as the schema. Keep source IDs on the slide content and the full source registry in the deck or its accompanying brief. Keep coverage visible beside any conclusion materially affected by a gap.

## Produce the requested format

Check the host's available presentation workflow and respect an explicitly requested format. Use a native presentation backend when available and authorized. Do not claim that a native `.pptx` or Google Slides document exists until it has actually been generated and checked.

The bundled portable fallback creates an HTML slide deck. Inspect its `--help`, then use:

```text
python scripts/render_presentation.py --input brief.json --output project-slides.html
```

Resolve paths relative to this skill folder. Fix brief-validation failures before delivery. This fallback is a navigable HTML presentation, not a PPTX file; renaming an extension does not convert formats. If the user specifically requires an unavailable native format, explain that remaining gap while delivering any useful fallback with its actual format clearly stated.

Keep the deck and its assets local. No external slide service, account creation or remote data upload is implied by the task. Avoid unsupported charts, percentages or decorative claims that strengthen the evidence beyond the sources.

Inspect the generated slides in an available preview or browser: opening and closing slides, long text, source legibility, Hebrew/RTL flow, controls and layout. For a native backend, follow its required render-and-review workflow. State when a visual check could not be completed. Confirm the actual output file or document before linking it.

## Deliver

Start the reply with at most three short bullets, localized to the user's language; use **בקצרה** in Hebrew. Link the actual deck, state HTML or the verified native format, and give the data cutoff plus material coverage or rendering limitations. Distinguish an editable deck, exported preview and outline. Do not send the presentation, publish it, alter project records or create a recurring update unless separately authorized.
