# Anyx Agent Kit public beta

<img src="../assets/brand/anyx-logo.png" width="80" height="80" alt="Anyx logo">

**TLDR:** Start with a sourced project catch-up or a materials review. Install the skills, connect Anyx MCP, then choose one group and a time window. The public-beta package is prepared around alpha.3. Release verification and launch activity are recorded separately.

## Beta status

| Item | Status |
| --- | --- |
| Download artifact | [v0.1.0-alpha.3](https://github.com/mkisilenko/anyx-agent-kit/releases/tag/v0.1.0-alpha.3), selected for this beta. Check its release metadata and checksum manifest before installing. |
| Public-beta materials | Prepared. This guide, two starter requests, a feedback format and a cohort ledger are included. |
| Participants and public promotion | Not started by this package. No users, activations or repeat-use results are claimed. |
| Fresh Claude Code connection | Skill installation passed, but new Anyx OAuth sign-in is blocked by a loopback redirect mismatch in the observed test. Hosted long-text recovery through that client is not verified. See [validation](validation.md) before starting this route. |
| Readiness evidence | See [validation](validation.md) for the actual tested hosts, installation and transport checks. Avoid assuming compatibility with another host. |

The beta uses an alpha-versioned download. There is no separate `beta.1` release implied by this guide. [Target alpha.3 release](https://github.com/mkisilenko/anyx-agent-kit/releases/tag/v0.1.0-alpha.3).

## Start here

1. Follow the [installation guide](installation.md). Preserve each complete skill folder and check the release manifest.
2. Connect an eligible [Anyx](https://anyx.app) account whose intended groups are already connected, using the [MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart).
3. Confirm skill discovery in the actual host and check the imported Anyx tools. Authentication and skill installation are separate checks.
4. Choose one group, timezone and time window. Begin with a read-only workflow and review its sources.

The verified installation route is a fresh project in Claude Code 2.1.319 on an existing Windows machine. All eight skills were invoked from that project's installed folders. Authentication to Anyx is a separate step; another host or a new machine needs its own check.

Repeat use can start from a saved request after this setup. Dashboards, presentations and video need an available renderer. Updates to another system need its own connector, record mapping and matching authorization.

## Two first requests

Replace `GROUP_NAME` and `TIMEZONE` before running. A seven-day request still depends on the history available to the connected account. The agent should show the retrieved bounds and any missing coverage.

### Project catch-up

```text
Use anyx-team-catchup for GROUP_NAME for the last seven days,
timezone TIMEZONE. Check Anyx status and select the matching returned group.
Read the available pages and recover referenced text when the imported tools allow it.
Give me a short update: what changed, confirmed or withdrawn decisions,
accepted next steps, and open questions, with sources.
Keep agent suggestions and reported work separate from human commitments
and independently verified execution. Do not send messages or update other systems.
```

Then ask for a dashboard from the same reviewed brief if that is useful. The portable dashboard is a local snapshot, not a live data feed.

### Materials review

```text
Use anyx-materials-review for GROUP_NAME for the last seven days,
timezone TIMEZONE. Check Anyx status and select the matching returned group.
Find actual material requests, corrections, cancellations and exact units.
Show the latest supported quantities, missing details and sources.
Prepare a supplier inquiry draft only if the information supports it.
Do not invent a request when none appears, and do not send the draft.
```

An applicable result with no confirmed materials request is useful. It should state the scope and missing information instead of filling in a fictional list.

## What to check in the result

- Open several source references, including the newest correction or withdrawal.
- Check quantities and units, approval conditions, accepted owners and known deadlines.
- Confirm that missing, truncated or expired content stays marked incomplete. Captured records do not establish that all WhatsApp activity was captured.
- Compare the output with the selected question. Reported execution is not a verified destination update.

For long text, the host needs the actual reference-mode arguments and recovery tool. A capability mentioned by status is not proof that the host imported the tool. Keep incomplete coverage explicit if recovery is unavailable.

## Demonstrations

These examples use fictional group content:

- [Dashboard HTML](../examples/rendered/dashboard.html)
- [Presentation HTML](../examples/rendered/presentation.html)
- [Rendered project video](../examples/rendered/video/project-update.mp4) and its [synthetic source brief](../examples/rendered/video/brief.json)

Download HTML examples to open them locally. The deck is HTML, not a native PowerPoint file. The MP4 example is a particular rendered brief, not a promise that every update fits the same duration. Each new output needs inspection. Reuse the [original logo](../assets/brand/anyx-logo.png) under the [branding guidance](../BRANDING.md).

The [systems matrix](systems-compatibility.md) describes fifteen API and authentication candidates. It does not mean fifteen native integrations are installed. The workspace-sync helper validates a proposal and performs no remote writes by itself.

## Feedback without private group content

Open a [GitHub issue](https://github.com/mkisilenko/anyx-agent-kit/issues/new) with the following sanitized details. Feedback is manual, not automatic product telemetry.

```text
Version or release:
Host and version:
Skill used:
Expected result:
Observed result:
Steps to reproduce with synthetic data:
Sanitized error text:
Installation or first-use help needed:
```

Do not include credentials, content references, raw group or message identifiers, customer conversations, screenshots of private groups, original attachments or private artifact files. Reproduce with synthetic text when possible. Keep private evidence in the authorized private workspace and share only an aggregate result publicly.

## First beta cohort

The proposed learning cohort is three to five actual starters. A starter begins installation or first use. An invitation, download or page visit is not a start.

Copy this empty ledger into the coordinator's private workspace. Do not populate participant records in the public repository.

```json
{
  "release": "v0.1.0-alpha.3",
  "measurement_timezone": "Asia/Jerusalem",
  "target_starters": {"minimum": 3, "maximum": 5},
  "participants": []
}
```

For each starter, record a pseudonymous ID, host/version, installation result, first useful output confirmed by the user, direct-help count, blocker, a private evidence reference and any useful repeat within seven days. Record actual timestamps in the chosen timezone. Unknown results stay `UNKNOWN`.

Proposed gates are three useful first outputs with at most one direct help intervention each, and two users returning for a new useful request within seven days. State the actual starter denominator. These are learning targets, not measured product outcomes. Any critical semantic error, or the same installation blocker twice, pauses expansion for a fix.

## Launch through existing owners

Use the existing supplier-inquiry article as the weekly source. The site section and one EN or HE social message use two derivative slots. Keep the third slot unallocated and reuse the current owners and queues. [Owner handoff and short copy](../marketing/public-beta/README.md) are prepared for those owners, not scheduled or published posts.

Record public release availability, website deployment, social publication, installation, first useful output, repeat use and attribution as separate results. Missing measurement is `UNKNOWN`, not zero. Follow the [launch plan](launch-plan.md) and [authorization boundaries](automation-and-approvals.md).

## בקצרה בעברית

מתחילים בעדכון פרויקט או בבדיקת חומרים: מתקינים, מחברים Anyx MCP ובוחרים קבוצה וטווח זמן. בודקים מקורות לפני שימוש בתוצאה. חומרי הבטא מוכנים סביב alpha.3, אך משתתפים, שימוש חוזר ופרסום בערוצים הם תוצאות נפרדות. משוב ציבורי כולל רק פרטי תקלה נקיים ממידע פרטי.
