# Validation evidence

**TLDR:** Alpha.3 passes 69 local tests and eight portable skill checks. Fresh project installation invokes all eight skills in Claude Code 2.1.319 on an existing Windows machine. Five selected local HTTP integration tests verify large Unicode recovery on pinned backend source. Native live text reads, artifact rendering and hosted long-text recovery are separate evidence scopes below.

Reviewed on 17 November 2026, Asia/Jerusalem. All shipped conversations, projects, external records and media demos are synthetic. Separate live-read evidence is summarized below without group identities or customer content.



The owner authorized alpha.3 publication and public-beta preparation. Source checks establish the candidate's behavior; actual tag, CI and download availability are recorded by the [GitHub release](https://github.com/mkisilenko/anyx-agent-kit/releases/tag/v0.1.0-alpha.3) and shared execution record.

## Current alpha.3 integration checks

This local revision integrates the independent review fixes onto branded source `8387975a5a45f5053afe1702fa8f8a16559424f5`. The original PNG, all four byte-identical asset copies, eight-skill structure and binary ZIP packaging are preserved.

| Layer | Observed result |
| --- | --- |
| Automated suite | 69 tests passed without skips: the 63 integrated alpha.3 cases plus six residual-review regressions. The original replay scenarios were not edited. |
| Input and time bounds | Malformed containers, rows and excessively nested JSON produce clean errors. Missing optional arrays normalize consistently. Evidence cutoff cannot precede the window start; known source timestamps cannot exceed it. A requested end after cutoff requires partial coverage. |
| Canonical action text and UTF-8 | Actions always render their validated title. Null/conflicting text aliases fail cleanly; an identical alias is accepted with identical output. The complete JSON, including nested metadata and keys, must encode as strict UTF-8 before any artifact API creates output. Actual CLI/API tests verify no partial output for lone high/low surrogates and preserve Hebrew plus literal/escaped paired emoji. |
| Sync structure | Approved state requires an authorization reference in either mode. Exact identifier, business-key, receipt and ledger-reference types and SHA-256 base format are checked. Validation still performs zero remote writes and does not authenticate grants or receipts. |
| Independent batches | The full ledger retains unknown outcomes. A separate independent execute batch preserves operation IDs, keys, bases and provenance; unresolved or unverified dependencies remain blocked. Live freshness and reconciliation remain executor responsibilities. |
| Video pacing | Visible text, including repeated brand/footer, receives a heuristic 20 Unicode codepoints per second with a four-second minimum. Default total limit is 180 seconds; an explicit 60-second limit rejects the 124-second demo before creating output. Rows, statuses, owners, deadlines, conditions and source markers are retained. |
| Actual PDF geometry | Existing local Chrome printed the independent Hebrew brief at initial viewports 390 and 1440. Six pages per run matched 1280×720 CSS pixels / 960×540 PDF points, with one logo image on each page. A deliberately stalled browser operation verified named timeouts and cleanup limited to its own test process tree. |
| New actual video | Hyperframes 0.9.61 rendered 124.000 seconds, 1280×720 H.264, 24 fps, 2,976 frames and no audio. This is a new alpha.3 render, rather than evidence reused from an earlier 40-second MP4. |
| Visual inspection | All ten actual video midpoint frames, dashboard at desktop/mobile and all ten deck slides at desktop/mobile were inspected. Original image bytes, visible branding, conditions and per-job material distinctions were retained, with no blocking clipping. Browser inspection observed no script errors or outbound attempts. |
| Current-source binding | Regeneration with the final validators produced byte-identical dashboard, deck and video composition HTML to the reviewed render inputs. |
| Imported tools | All eight reading references and installation guidance distinguish useful legacy core reads from long-text recovery requiring actually imported tools and returned references. Any truncation flag makes the affected field incomplete. |

The shipped demonstration is a synthetic group briefing: J42 decisions and scope are separate from J21/J22/J25 materials. Its three portable skill copies share that clarified example. Independent replay fixtures retain their separate scenario contexts. No live group identity, customer content, credentials or private pilot result was copied into public code or examples.

These automated and rendering checks are local. The browser check explicitly skips on a machine without its existing Node/Chrome/puppeteer-core/pypdf dependencies; it actually executed in this run. The pacing budget aids review and does not prove human reading speed. Sampling ten video frames is narrower than checking every frame. The local validator cannot establish live access, fresh remote state or write authority. Fresh project discovery and local long-text transport have separate evidence below; authenticated MCP in that fresh CLI, hosted chunk recovery and destination writes remain open.


## Scoped live-read evidence

A bounded live read of synthetic messages passed through the core tools. A separate legacy long-text attempt returned a truncation marker without an available imported recovery tool/reference, so that field remained incomplete and coverage stayed partial.

An authorized text-read pilot was also verified on one existing host: frozen pagination, reverse rescan, direct lookup and search were checked for consistency over the retrieved records. Text was inline, so long-text chunk recovery was not exercised. Private sourced dashboard, deck and video artifacts were produced and inspected. Their records and artifacts are kept private and were not copied into the public examples. These checks do not establish complete WhatsApp capture, compatibility with every host, clean installation or destination writes.

## Fresh project installation

A new temporary Windows project received all eight alpha.3 skill ZIPs, with every extracted file compared against its archive. Claude Code 2.1.319 discovered and actually invoked all eight skills from those new `.claude/skills` paths. Nine referenced files were read. Three rendering skills invoked their installed helpers in four actual commands, including a saved dashboard request repeated with byte-identical output. The three HTML artifacts embedded the original PNG bytes. The installed video helper produced an explicitly unrendered 124-second composition; the separately rendered MP4 evidence above remains distinct.

The supported run used `--setting-sources project`, the existing CLI binary and subscription authentication. Existing managed settings and personal registry were present, but invocation base paths identified the new project copies. No personal skill installation was overwritten or credential copied. This proves a fresh project installation on the existing machine, not a fresh OS, account or every client. The `--restricted` diagnostic did not register project skills on that version and was not the passing route.

A separate project-scoped Anyx OAuth connection was prepared for an authenticated run in the same fresh CLI. The user approved the project server, but the actual authorization request failed with `invalid_request`: its loopback redirect contained a callback port and Anyx rejected it as not matching the registered redirect URI. An anonymous validation probe accepted a portless localhost callback and rejected the observed callback with a port. Claude Code 2.1.319 kept an explicit `:80` when configured with callbackPort 80, and that form was also rejected. The client-only fixed-port attempt therefore did not resolve authentication. No consent, token, hosted long-text result or backend change is claimed. The [official Claude MCP authentication guide](https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers) describes the normal flow; existing-host native access does not authenticate this new client automatically.

## Local long-text integration

Five selected integration tests passed over actual loopback HTTP MCP, REST and SQL using isolated synthetic data and PGlite 0.5.8. Backend source was pinned to `ff9047892982951e5e891c22386d492b80170e3c`; it is separate from the kit release revision and is not asserted to be the hosted version. Remote network access was blocked and no real credentials were supplied. Fifteen unrelated tests in that backend suite were intentionally unselected, not extra passes.

The checks reconstruct mixed Hebrew, emoji and CJK text from hundreds of kilobytes to over two megabytes, compare complete text and hashes, recover after an oversized-response error, exercise direct-lookup references, and reject altered references, cross-credential use, expired snapshots and changed source text. References are issued only for fields larger than 16,384 UTF-8 bytes; there is no force-reference argument.

The currently authorized native live group returned only inline text. Its completed read cannot prove a successful hosted chunk call. A legacy Reviewer connection still imports only the core tools and its truncated field remains incomplete. Hosted long-text recovery requires the modern Reviewer connection, an actual returned reference and the same credential throughout.

## Historical test scopes

| Earlier scope | Recorded result |
| --- | --- |
| Isolated pre-branding review candidate | 53 tests passed in that separate candidate; this was not the branded integration or a live MCP test. |
| Alpha.2 branding baseline | 36 tests passed, described below. |
| Integrated alpha.3 source `5d6abe95744ceaef648d691f1442d1ea340ec051` | 63 tests passed before the six canonical-alias/Unicode residual tests were added. |

These are separate snapshots. The current result is 69, rather than their sum.

## Historical alpha.2 branding checks

Version `0.1.0-alpha.2` was a branding update. The validation and timing changes below were not included in that earlier version.

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

## Historical synthetic workflow checks

Catch-up completed pages and three UTF-8 chunks, retaining the difference between a reported reassignment and an accepted commitment. Materials kept corrections, cancellations, exact units and missing fields. Decision log preserved conditional and withdrawn approvals.

Project control completed an empty continuation page and kept the work hold, CRM signature evidence, accepted supplier check, failing CI and missing deployment distinct. Sync reconciled a prior timeout from an operation-specific simulated audit receipt without retrying, then held a proposal affected by a concurrent human edit. The existing scoped policy remained valid.

The five cases used 26 simulated Anyx calls. No live Anyx account or customer records were read. Destination observations were fictional supplied records. Fixed fixtures do not establish actual transport, expiry, capture completeness, transaction or server-idempotency behavior.

## Remaining verification

- Authenticated MCP in the fresh CLI, hosted long-text chunk recovery and coverage of additional hosts/accounts. Fresh project discovery and local helper invocation are verified on the existing Windows machine; live native reads and local long-text transport have the separate scopes above.
- Actual destination connections. The 15 systems in systems-compatibility.md are API/mapping candidates, not fifteen implemented authenticated integrations.
- Native presentation formats. The portable helper creates HTML slides; other formats require a real host backend.
- Fresh remote versions and user authority. The sync helper validates plan structure and performs no remote writes.
- New real output quality. A prepared composition is not an MP4, and local HTML has no live data connection.
- Search indexing, traffic, useful customer activation and model recommendations.

## Reproduce

Run `python tools/validate_kit.py`, `python -B -m unittest discover -s tests` and `python tools/build_skill_zips.py`. The generated manifest records per-artifact SHA-256 values. Archives normalize text line endings and exclude private validation state and runtime dependencies.

Optional `python tools/check_upstream.py --check` reads bounded public sources and never rewrites instructions. Original test traces remain in ignored .validation folders. Public examples are labeled synthetic.

