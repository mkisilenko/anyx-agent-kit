# Validation evidence

**TLDR:** Alpha.2 branding passes 36 offline tests and eight portable skill checks. The four added tests verify original PNG bytes in installed-skill output and ZIPs, plus the dashboard image policy. Earlier alpha.1 visual and workflow inspections are recorded separately below.

Reviewed on 17 November 2026, Asia/Jerusalem. All conversations, projects, external records and media demos are synthetic.


## Current alpha.2 branding checks

Version `0.1.0-alpha.2` is a branding update. It does not include the separately prepared post-review input-validation, sync-authorization, cutoff or video-timing candidate.

| Layer | Observed result |
| --- | --- |
| Automated suite | 36 tests passed: 32 existing cases plus four dedicated branding tests. |
| Original asset | Canonical PNG and all three skill copies match SHA-256 `4b898fa294753d522b6a5c39475f0a430e01b5127cb0bfb39e208d29b80d3f43`, 1,303,035 bytes each. |
| Actual output image | Each skill was unpacked from its ZIP and run from an unrelated working directory. Independently decoded PNG data URIs match the original bytes. There is one persistent logo in each HTML document, with proportional contain sizing. |
| Binary packaging | Extracted PNGs from three skill ZIPs and the full-kit ZIP match the original. Full-kit branding guidance is included. Existing archive reproducibility and private-state exclusion checks passed. |
| Image policy | Dashboard CSP permits `data:` images without remote image origins. Existing escaping and source-registry checks passed with only the trusted logo image allowed. |
| Portable structure | Eight skills passed frontmatter and self-contained-reference checks. |
| Regenerated public examples | Dashboard and all ten HTML slides opened in local Chrome at desktop and mobile widths. The original image loaded and remained visible with contain sizing. A local Chrome print produced ten PDF pages with the logo on every page, also inspected after rasterization. |
| Branded MP4 | The public video example was rendered again: H.264, 1280x720, 24fps, 40 seconds, no audio. Ten frames sampled at each scene midpoint showed the original logo without cropping or distortion. |

All examples are synthetic and English. This branding QA used local Chrome and sampled video frames. It does not establish other browser behavior, every video frame, general caption readability or live MCP behavior. The pre-existing four-second scene timing is unchanged in this branding-only release. No live Anyx or destination records were read for these checks.

## Historical alpha.1 evidence

The evidence below predates the original-logo integration. Its 32-test count, five workflow cases and rendering observations describe alpha.1, rather than extra alpha.2 checks.

| Layer | Observed result |
| --- | --- |
| Portable skills | Eight self-contained folders passed skill-creator validation and package reference checks. |
| Automated suite | 32 tests passed, covering replay, UTF-8, archives, source-backed briefs, escaping, credential URLs, provenance, rendering limits and sync-plan preconditions. |
| Independent workflows | Five reviewed Hebrew results: catch-up, materials, decision log, project control and workspace sync. |
| Dashboard | Generated offline HTML opened in Chrome. Layout, evidence and status filtering were observed. |
| Presentation | Ten-slide HTML deck opened in Chrome. Cover, content navigation and source readability were observed. No PPTX was produced. |
| Video | Hyperframes 0.9.61 rendered H.264 at 1280x720, 24fps, 40 seconds, without audio. FFprobe verified the stream. Opening, middle and closing frames were inspected. |
| Hebrew | UI labels, unknown fields and lossless source-registry round-trip passed focused checks. A Hebrew composition was generated. The MP4 inspected here is English. |
| Public source baseline | Two reviewed MCP documentation files are pinned by hashes in upstream-sources.json. |

The video runtime used Node 22.17.0, Hyperframes 0.9.61, Chrome and private FFmpeg/FFprobe paths. Runtime executables and node_modules are excluded from source control and archives. No paid media generation was used. External tools keep their own licenses.

Hyperframes lint reported zero errors and 11 nonblocking editor-structure warnings. These recommend more sub-compositions for editing. The render used strict errors and no best-effort capture fallback. Every new real brief still needs its own visual inspection.

## Behavioral checks

Catch-up completed pages and three UTF-8 chunks, retaining the difference between a reported reassignment and an accepted commitment. Materials kept corrections, cancellations, exact units and missing fields. Decision log preserved conditional and withdrawn approvals.

Project control completed an empty continuation page and kept the work hold, CRM signature evidence, accepted supplier check, failing CI and missing deployment distinct. Sync reconciled a prior timeout from an operation-specific simulated audit receipt without retrying, then held a proposal affected by a concurrent human edit. The existing scoped policy remained valid.

The five cases used 26 simulated Anyx calls. No live Anyx account or customer records were read. Destination observations were fictional supplied records. Fixed fixtures do not establish actual transport, expiry, capture completeness, transaction or server-idempotency behavior.

## Remaining verification

- Clean-host skill discovery, live MCP authentication and an authorized synthetic group pilot.
- Actual destination connections. The 15 systems in systems-compatibility.md are API/mapping candidates, not fifteen implemented authenticated integrations.
- Native presentation formats. The portable helper creates HTML slides; other formats require a real host backend.
- Fresh remote versions and user authority. The sync helper validates plan structure and performs no remote writes.
- New real output quality. A prepared composition is not an MP4, and local HTML has no live data connection.
- Search indexing, traffic, useful customer activation and model recommendations.

## Reproduce

Run `python tools/validate_kit.py`, `python -m unittest discover -s tests` and `python tools/build_skill_zips.py`. The generated manifest records per-artifact SHA-256 values. Archives normalize text line endings and exclude private validation state and runtime dependencies.

Optional `python tools/check_upstream.py --check` reads bounded public sources and never rewrites instructions. Original test traces remain in ignored .validation folders. Public examples are labeled synthetic.

