---
name: anyx-project-video
description: Create a sourced project update video from bounded captured WhatsApp context through an existing authorized Anyx MCP connection and relevant accessible user-provided sources. Use a local Hyperframes rendering backend when available; explicitly distinguish a rendered video file from an HTML composition, storyboard or script awaiting rendering.
---

# Anyx project video

Turn project evidence from [Anyx](https://anyx.app) into a short update video for review. Gather the facts, build a structured brief and render locally when the backend is available. A script or storyboard is useful preparation but is not a completed video.

## Read the context

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. Use the existing authorized connection and its exposed schema. Reuse the selected project, groups and bounded period; resolve ambiguity once. Keep exact project identities separate even when messages appear in the same group.

Add supplementary documents, media or connected records only when supplied or authorized, actually accessible and relevant. Do not imply an attachment was watched or its original inspected when only stored extraction was read. Keep extracted descriptions, chat reports and original media distinguishable.

Preserve proposed versus approved work, conditions, withdrawals, reported execution and accepted commitments. A compelling narration must not turn uncertain progress into completion. Avoid invented percentages, dates, footage, customer quotes or success claims. A synthetic demonstration must be visibly labeled, including in the rendered output.

## Prepare the validated brief

Create a UTF-8 JSON brief following the bundled `examples/demo-brief.json` format. Never replace missing real evidence with its demo content.

- `schema_version`: `1`; `synthetic`: demonstration flag; `language`: `en` or `he`.
- `project`: `id`, `title`, `data_as_of`, and a `period` object with `start`, `end`, `timezone`.
- `coverage`: an object with `status` set to `partial` for a materially unfinished read or missing required source, otherwise `complete_capture_not_asserted`, and `note` containing the available bounds and capture limitations.
- `summary`: objects with `text` and `source_ids`; `actions`: objects with `id`, `title`, `owner`, `status`, `due`, `source_ids`; `decisions`: objects with `id`, `text`, `status`, `source_ids`; `risks`: objects with `text`, `status`, `source_ids`.
- `sources`: unique objects with `id`, `system`, `timestamp`, `label`, `url`, and available `group_id` and `record_id`. Use real URLs or `null`.

The optional `summary`, `actions`, `decisions`, `risks` and `sources` arrays may be omitted and normalize to empty arrays. Explicit `null`, wrong container types or malformed rows are errors. Omitted action/decision/risk status becomes `unknown`; omitted action owner and due become `null`. These defaults mean unavailable facts, not verified absence.

`project.data_as_of` is the evidence cutoff, not the artifact generation time. All timestamps used for bounds and known due values need an explicit UTC offset. The cutoff must be at or after `period.start`. Known source timestamps must be at or before that cutoff. Older supporting sources may precede the requested window; an unavailable timestamp stays unknown rather than invented. When it is before the requested `period.end`, coverage must be `partial`; explain the unobserved tail in `coverage.note`, keep the requested window visible and draw no conclusion about events after the cutoff. A cutoff at or beyond the end still does not establish complete capture.

Every factual item requires nonempty source IDs that resolve to the registry. Unknown owners and deadlines remain `null`; known due values are ISO timestamps. Carry material conditions in the text and status so the narration and captions cannot drop them. Review the facts against the sources, then resolve any schema-validation errors before rendering.

Use the brief to make readable scenes rather than turning full chat transcripts into captions. Include the project, cutoff, important status changes and the next unresolved check. Preserve source markers in scene text or credits and retain the full source registry in an accompanying brief. Keep the coverage limitation visible in the video, not solely in the chat reply.

## Build and render locally

Read the bundled helper's `--help`. Its preparation interface is:

```text
python scripts/build_video.py --input brief.json --output project-video-composition
```

This creates a project directory with a Hyperframes HTML composition and supporting material. When the actual local runtime is ready, request rendering with its supported option:

```text
python scripts/build_video.py --input brief.json --output project-video-rendered --render --hyperframes-cli "/absolute/path/to/hyperframes/bin/hyperframes.mjs"
```

Replace the CLI path with the actual trusted installed `hyperframes.mjs` file. The `--hyperframes-cli` argument is required for rendering. If the runtime executables are outside the current PATH, also supply the applicable `--node "/absolute/path/to/node"`, `--runtime-bin "/absolute/path/to/ffmpeg-bin"` and `--browser-path "/absolute/path/to/chrome"` arguments. Use the actual executable names on Windows, such as `node.exe` and `chrome.exe`, and quote paths containing spaces.

Resolve script paths relative to this skill folder and choose a new output directory for each run. The helper refuses an existing output directory, including one from an earlier preparation run. Inspect the helper result and generated files to determine which stage completed. An HTML composition, successful preparation command or storyboard file does not establish a rendered MP4.

[Hyperframes](https://github.com/heygen-com/hyperframes) is Apache-2.0 licensed; its local engine has no per-render fee. Its documented runtime requires Node.js 22+, FFmpeg, FFprobe and Chrome support. Check the installed CLI's help and doctor output rather than assuming that Node or a Python video package supplies all dependencies. Local rendering does not require paid AI media generation. The upstream [CLI reference](https://github.com/heygen-com/hyperframes/blob/main/docs/packages/cli.mdx) governs any direct CLI call; do not copy unverified flags from older tutorials.

Use local assets, scripts and fonts for private project content. Do not send the brief to a cloud renderer, HeyGen generation service, remote voice model or sharing endpoint by default. A local render must not silently become a paid or externally hosted workflow. Use only supplied or appropriately licensed media; a silent video with clear captions is preferable to inventing narration audio or licensing music.


## Apply the supplied Anyx brand

Use the bundled original [Anyx logo](assets/brand/anyx-logo.png) in the artifact header. The helper embeds its unchanged PNG bytes locally, with preserved transparency and proportions. Keep it secondary to project content, usually 56 pixels square; use `object-fit: contain`, without cropping, recoloring, stretching or recreating the mark. Keep status, sources and coverage legible. A native presentation backend should reuse this same supplied asset. Branding is for the requested artifact, not unrelated text replies; it does not authorize sharing or publication.

The helper allocates each scene time from its visible label, headline, captions, brand and footer, using a minimum of four seconds and a heuristic budget of 20 normalized Unicode codepoints per second. It preserves every supplied row, condition, status, deadline, source marker and coverage note. The default total limit is 180 seconds; use `--max-duration-seconds 60` only when the user needs a one-minute composition. If the chosen limit is too short, the helper fails before creating output instead of truncating facts. Review or split the brief with the user if needed. This budget is a pacing aid; it does not establish human readability or replace video inspection.

The bundled MP4 documents an earlier fixed-duration renderer. Rebuilding its brief with the revised text budget changes its duration; the old MP4 is not evidence that this candidate's new timeline has been rendered or visually checked.

## Verify and deliver the actual output

For a rendered file, check that it is playable video with a nonzero duration, inspect representative opening/middle/closing frames and confirm readable Hebrew/RTL captions when applicable. Check stated timing, source markers, source/coverage credits and audio presence if audio was requested. If no playback or frame inspection is available, disclose that precise validation gap.

Answer in the user's language with at most three short opening bullets; use **בקצרה** in Hebrew. Link the actual rendered video when present and its editable composition when useful. State backend and verification honestly. If rendering failed or the runtime is absent, label the delivered files as a prepared composition/storyboard, explain the concrete missing dependency and keep the video request marked incomplete. Do not claim one-click rendering was verified from a scaffold alone. Do not publish, send, create a schedule or modify project records as part of this skill.
