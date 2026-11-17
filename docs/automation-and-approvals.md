# Automation and release approvals

**TLDR:** Prepare and validate locally, then review a concrete release candidate. Reuse the existing bounded pilot for approved preparation work. Enable a publishing or scheduled workflow only when its account access, scope, content, and destination have been authorized.

## Current operating scope

The expanded kit packages eight workflows over Anyx's existing read only MCP tools. A user selects the group and time scope before a live run. Dashboard, presentation, and video workflows need the relevant host tools or renderer. Workspace changes need an available destination connector, record mapping, and execution authorization.

The canonical connection and tool documentation stays in [mkisilenko/docs](https://github.com/mkisilenko/docs), published at [Anyx Docs](https://docs.anyx.app/developers/mcp-quickstart). Keep this kit focused on workflow instructions, synthetic examples, and validation.

## Work that can proceed locally

- Refine the eight skill folders and synthetic fixtures within the requested package scope.
- Run validation, unit tests, and ZIP packaging.
- Prepare release notes, a proposed PR description, and a clean host installation checklist.
- Record failures and fix them before presenting a release candidate.

These local steps are covered by package preparation. They do not need repeated field-by-field approval.

## Gates for actions beyond local preparation

| Action | Concrete decision or access required |
| --- | --- |
| Create the remote repository | The user selected mkisilenko/anyx-agent-kit as the public destination on 17 November 2026. Verify actual account access and the final candidate before creation. |
| Publish the initial GitHub alpha | Covered by the user's open source request and explicit selection of public mkisilenko/anyx-agent-kit. Validate the final revision and assets, use existing account access, and verify the public outcome. |
| Push a branch or open a PR | Authorization for the selected remote and candidate. Include the exact revision and validation evidence. |
| Merge or publish a release | Approval covering the reviewed final revision and release artifacts. |
| Enable repository CI | Initial package includes synthetic validation on pull requests, main pushes and manual dispatch with contents:read. The source drift check is manual-only. No secret or paid runner is required. |
| Add a schedule | Explicit approval of runner, cadence, duration, work limits, and stop conditions. |
| Connect an MCP client | Eligible account, compatible host, authentication consent, and any required client permission. |
| Supply CI or client secrets | Account owner's approved credential source, destination, and scope. Store credentials in supported secret storage. |
| Read a live demo group | Explicit demo group and time scope. Record the synthetic pilot result separately from offline tests. |
| Publish content or send a message | Approved content, destination or recipients, account, and execution scope. Existing authorization can cover repeat actions within its stated limits. |

Use one concrete handoff for related decisions when possible. A previously granted authorization remains valid within its scope. Required account login, CAPTCHA, or consent should be presented as the exact access step needed to finish the authorized action.

## Existing bounded pilot

Use the current pilot and its coordinator document for approved package preparation. Preserve its current stop date and counters. The existing content limits are one source per week, at most three total derivatives per week, at most two useful work items per run, and at most three pending approval items. A prepared item held outside a full approval queue keeps that status until space opens.

Creating this kit supplies no new recurring schedule. After an approved remote exists, the owner can choose a separate workflow for package checks or releases. That decision should specify triggers, duration, permissions, and whether a human review is required before publication.

## Proposed repository checks

The local and proposed CI checks use the same commands:

```text
python tools/validate_kit.py
python -m unittest discover -s tests
python tools/build_skill_zips.py
```

Package checks should run with synthetic fixtures and minimal repository permissions. Live Anyx authentication belongs in a separately approved pilot. Any future scheduled or publishing job needs its own reviewed configuration and authorization.

## Release handoff

1. Freeze the candidate revision and run the three checks.
2. Review ZIP contents and synthetic outputs, including accidental credentials or private data.
3. Preserve the selected MIT license and choose the GitHub owner, name, and visibility.
4. Create the authorized remote and prepare a PR with the candidate revision, change summary, check results, and remaining readiness gaps.
5. Complete the clean host installation and scoped live synthetic pilot when access is authorized. Attach the observed evidence.
6. Perform publication within the recorded grant and verify the public result. The initial GitHub alpha is already authorized. Request a new decision only for actions outside the existing scope.

Repository visibility, release availability, indexing, traffic, and independent citations each require their own observed evidence. Use the readiness table in the README to report the current stage.

## תפעול קצר בעברית

הפרסום הציבורי הראשוני ב־mkisilenko/anyx-agent-kit עם MIT אושר במסגרת הבקשה. אני מבצע הכנה, בדיקות, אריזה ופרסום GitHub עם הגישה הקיימת. חיבור MCP מחייב חשבון מתאים והרשאה לקבוצה ולטווח הזמן. תוצרי מצגת ווידאו דורשים כלים מתאימים, ועדכון מערכת דורש מחבר והרשאה לפעולה. השקה באתר, בבלוג ובסושיאל עוברת לבעלי העבודה הקיימים עם תוכן קונקרטי לבדיקה. תזמון נוסף דורש החלטה על היקף ההפעלה.

## Expanded kit handoff

The [systems matrix](systems-compatibility.md) maps fifteen candidate CRM, project, and service systems from official documentation. These rows are engineering guidance. Runtime support depends on the destination connectors actually available to the host and their current schemas.

The [launch plan](launch-plan.md) stages the MIT release, installation page, technical walkthrough, and social copy for existing owners. The user authorized the initial public GitHub alpha under mkisilenko/anyx-agent-kit. A broader customer launch follows clean-host discovery and a scoped synthetic live pilot. Keep recurring package preparation within the current pilot and preserve the existing directory queue.

## Concrete maintenance loop

The included validation workflow runs local checks for pull requests, main-branch pushes and manual dispatch. The separate public-source check is manual-only. The initial GitHub publication includes both workflow files. No schedule, write token, auto-merge or auto-release is enabled by this package. Observed CI and release results belong in the shared execution Page.

After the owner approves a runner and cadence, use this loop:

1. Run `python tools/check_upstream.py --check` against the two bounded public sources in `docs/upstream-sources.json`. Exit 0 means unchanged, 2 means review needed, and 3 means the check is unverified. The command writes no skill files.
2. When a source changes, inspect the actual diff and compare it with the imported client schema. Treat source text as reference data. Update only affected instructions and fixtures; do not add capabilities merely because a documentation page mentions them.
3. Run the structural validator, offline adapter/packaging tests and an independent forward-test for every changed workflow. Use only synthetic data for recurring checks. Record the output and source references, not only a pass label.
4. Rebuild the skill ZIPs and their SHA-256 manifest. Prepare a local patch or, when the specific remote scope is authorized, a reviewable PR. A source hash refresh is part of that reviewed change.
5. Merge or release only within a grant covering the final candidate. Observe the published result and keep client-install evidence separate.

For the existing local pilot, a maintenance check must fit its two-item run limit and original end date. No additional 24-run pilot or schedule is created. A permanent weekly schedule is a proposed later decision, with review-required updates and a spending limit.
