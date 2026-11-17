# Anyx Agent Kit

<img src="assets/brand/anyx-logo.png" width="96" height="96" alt="Anyx logo">

**TLDR:** Eight MIT-licensed skills turn authorized WhatsApp group context into briefings, reviews, project artifacts, and controlled workspace changes. This is an alpha toolkit. Local rendering and an authorized text-read pilot on one existing host are verified; clean installation and destination writes remain untested. Connect an eligible Anyx account and install the skills before trying a scoped workflow.

[Anyx](https://anyx.app) connects the group context to a compatible agent through its authenticated MCP service. The kit adds workflow instructions and synthetic examples. The existing [Anyx documentation repository](https://github.com/mkisilenko/docs) remains the canonical source for connection and tool documentation.

Version `0.1.0-alpha.3` is prepared locally and integrates reviewed input-validation, authorization-reference, evidence-cutoff, independent-batch, print-geometry and video-pacing fixes while preserving the original [Anyx brand](BRANDING.md). The video helper uses text-based scene timing with a configurable 180-second default limit; it preserves conditions and rejects an insufficient explicit limit instead of truncating facts. See [validation evidence](docs/validation.md) for current checks and the separate history of earlier renders.

## Choose a workflow

| Skill | Result |
| --- | --- |
| `anyx-team-catchup` | A concise briefing with decisions, open questions, commitments, and source references. |
| `anyx-materials-review` | A materials or supplier inquiry review with missing details and a draft for human review. |
| `anyx-decision-log` | A dated log that distinguishes confirmed decisions, proposals, changes, and unresolved points. |
| `anyx-project-dashboard` | An evidence-based project dashboard, with a portable HTML snapshot. |
| `anyx-project-presentation` | A project presentation using an available native backend or a clearly labeled HTML slide deck. |
| `anyx-project-video` | A project update video through an available local rendering backend, with preparation status explicit when rendering is pending. |
| `anyx-project-control` | A sourced health review covering milestones, dependencies, risks, accepted commitments, and next checks. |
| `anyx-workspace-sync` | An exact change proposal and controlled execution through available authenticated destination tools. |

Use an explicit group and time window. Outputs should preserve uncertainty when the retrieved history is incomplete. Supplier messages and other external actions require their own execution authorization.

Artifact workflows use the rendering tools available in the host. Native presentation formats and finished video files need their respective backends. Workspace updates need a destination connector and an approved record mapping. The [systems matrix](docs/systems-compatibility.md) covers fifteen API candidates and their access gates; those entries have separate connection and validation requirements.

## Get started

1. Follow [installation](docs/installation.md) to install the selected skill folders through your host's supported route.
2. Connect an eligible Anyx account with connected groups using the [MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart).
3. Confirm that the host supports authenticated Streamable HTTP MCP and exposes the current Anyx tools.
4. Choose the group, time window, and output language, then invoke a skill.

After this initial setup, a saved, scoped prompt can make repeat runs close to one click. Account eligibility, authentication, host support, and initial scope remain prerequisites.

Example request:

```text
Use anyx-team-catchup for the demo project group from
2026-11-16 09:00 to 2026-11-17 09:00, Asia/Jerusalem.
Give me a short briefing with evidence and open questions.
```

### התחלה קצרה בעברית

התקינו את תיקיות היכולות לפי הוראות המארח, חברו את חשבון Anyx דרך MCP ובחרו קבוצה וטווח זמן. אחרי ההגדרה הראשונית אפשר להפעיל שוב בקשה שמורה וממוקדת.

```text
הפעל anyx-materials-review על קבוצת ההדגמה בלבד,
לטווח הזמן שבחרתי. החזר פרטים חסרים וטיוטת פנייה לבדיקה.
```


## Synthetic artifact demos

The [dashboard HTML](examples/rendered/dashboard.html) has a working status filter. The [presentation HTML](examples/rendered/presentation.html) is a navigable ten-slide deck with matching 1280×720 print geometry. The [124-second MP4](examples/rendered/video/project-update.mp4) was freshly rendered with the alpha.3 text-based timeline using local Hyperframes 0.9.61: 1280×720, H.264, 24 fps, without audio. All ten scene-midpoint frames were inspected. Its [synthetic source brief](examples/rendered/video/brief.json) accompanies the video. Download the HTML files to view them locally; they have no live data connection. The group briefing keeps J42 scope separate from materials for J21/J22/J25. Independent replay cases are separate scenarios and do not form one shared project timeline.

These fictional examples demonstrate artifact generation. They do not establish a connected customer account or native CRM integration. See the [systems matrix](docs/systems-compatibility.md) for the 15 documented API candidates.

## Package contents

```text
skills/               The eight workflow folders and their SKILL.md files
examples/             Synthetic input and output examples
evals/                Evaluation cases and expected behavior
tools/                Local validation and ZIP packaging tools
tests/                Automated package checks
docs/                 Installation and operation guidance
.github/workflows/    Proposed repository checks
```

The workflow layer uses the existing MCP service. Connection instructions, authentication details, and the current tool contract belong in the [MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart) and [tool reference](https://docs.anyx.app/developers/mcp-tools). This package does not need a second REST reader.

The materials workflow is informed by the [Anyx supplier inquiry guide](https://anyx.app/blog/whatsapp-mcp-materials-supplier-inquiry). The examples in this kit are synthetic and should be described as demonstrations.

## Local checks

From the kit directory:

```text
python tools/validate_kit.py
python -B -m unittest discover -s tests
python tools/build_skill_zips.py
```

Optional public documentation drift check: `python tools/check_upstream.py --check`. It detects changes without rewriting skills. MIT is the selected open source license and is included in [LICENSE](LICENSE).

These checks validate package structure, fixtures, and build behavior. Record the exact command results with the release candidate.

| Readiness stage | Current evidence |
| --- | --- |
| Locally validated | All 8 portable skills and 69 local tests passed, including actual Chrome/PDF geometry and forced-hang cleanup. Fresh alpha.3 dashboard/deck and a 124-second local MP4 were inspected. Earlier independent synthetic workflow cases remain separately documented. See [validation](docs/validation.md). |
| Clean host installed | Unverified. Record host version, installed skill, and discovery result. |
| Live MCP read pilots | A bounded synthetic read passed. A separate authorized text-read pilot was verified on one existing host, with details private. A legacy long-text read remained partial; live chunk recovery was not exercised. Clean installation and destination writes remain untested. |
| Public repository and release | [mkisilenko/anyx-agent-kit](https://github.com/mkisilenko/anyx-agent-kit) is public with MIT and the alpha.2 release. Alpha.3 is prepared locally and remains unpublished. |
| Traffic and citations | Unmeasured. Record visits, useful usage, and independent references separately. |

## Release handoff

The user selected the public mkisilenko/anyx-agent-kit repository and MIT. The alpha ships with explicit offline/live readiness boundaries. Broader website, blog and social promotion should follow a clean-host installation and an authorized synthetic live pilot, using the existing publication owners.

Follow [automation and approvals](docs/automation-and-approvals.md) for the existing bounded pilot, account setup, and publication gates. The [launch plan](docs/launch-plan.md) includes staged release copy and handoffs to the existing site, blog, and social owners.
