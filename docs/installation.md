# Install Anyx Agent Kit

**TLDR:** Install the complete skill folders, connect Anyx through your MCP host, and select a group and time window. A skill installation and an authenticated Anyx connection are separate readiness checks.

## Prerequisites

- An eligible [Anyx account](https://anyx.app) with the groups you intend to use already connected.
- A host that supports the Agent Skills format and authenticated Streamable HTTP MCP.
- Access to the local kit or an approved release archive.
- An initial group, time window, timezone, and output language approved by the user.

Use the [Anyx MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart) for the current endpoint and authentication procedure. Consult the [tool reference](https://docs.anyx.app/developers/mcp-tools) for the current schema. Keep credentials in the host's authentication or secret storage.

## Install skill folders

Each installable unit is a complete folder containing `SKILL.md` and any files it references:

```text
skills/anyx-team-catchup/
skills/anyx-materials-review/
skills/anyx-decision-log/
skills/anyx-project-dashboard/
skills/anyx-project-presentation/
skills/anyx-project-video/
skills/anyx-project-control/
skills/anyx-workspace-sync/
```

Choose the installation route documented for the actual host. Folder support in the host documentation establishes a route to try. Successful operation of this kit on that host still needs verification.

| Host | Documented local folder route |
| --- | --- |
| Codex CLI or IDE | Project `.agents/skills/<skill-name>/` or personal `~/.agents/skills/<skill-name>/`. |
| Claude Code | Project `.claude/skills/<skill-name>/` or personal `~/.claude/skills/<skill-name>/`. |
| Another compatible host | Use its documented folder or archive import route and preserve the complete skill folder. |

See the current [Codex skills instructions](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills instructions](https://code.claude.com/docs/en/skills). ChatGPT workspace or plugin distribution needs its own supported installation path.

### Windows PowerShell example for local Codex use

Run from the kit directory. This copies the eight skills to the documented personal discovery directory. An existing destination stops the copy so that an update can be compared first.

```powershell
$kitRoot = (Get-Location).Path
$skillNames = @(
    'anyx-team-catchup',
    'anyx-materials-review',
    'anyx-decision-log',
    'anyx-project-dashboard',
    'anyx-project-presentation',
    'anyx-project-video',
    'anyx-project-control',
    'anyx-workspace-sync'
)
$skillsDestination = Join-Path $env:USERPROFILE '.agents\skills'

foreach ($skillName in $skillNames) {
    $sourceDirectory = Join-Path $kitRoot "skills\$skillName"
    $targetDirectory = Join-Path $skillsDestination $skillName
    if (-not (Test-Path -LiteralPath "$sourceDirectory\SKILL.md")) {
        throw "Missing skill source: $sourceDirectory"
    }
    if (Test-Path -LiteralPath $targetDirectory) {
        throw "Compare the existing installation before updating: $targetDirectory"
    }
}

New-Item -ItemType Directory -Path $skillsDestination -Force | Out-Null
foreach ($skillName in $skillNames) {
    $sourceDirectory = Join-Path $kitRoot "skills\$skillName"
    Copy-Item -LiteralPath $sourceDirectory -Destination $skillsDestination -Recurse
}
```

Confirm discovery in the host. In Codex CLI or the IDE, select a skill through `/skills` or a `$` mention. Claude Code documents invocation as `/skill-name`. Use the host's reload or new session procedure if the skill does not appear.

Download a complete skill ZIP or the full kit from the [GitHub releases](https://github.com/mkisilenko/anyx-agent-kit/releases), or clone [mkisilenko/anyx-agent-kit](https://github.com/mkisilenko/anyx-agent-kit) and use the folders above. Check the release manifest before installing. The documented folder routes still need clean-host discovery and live MCP verification for this alpha.

## Connect and scope Anyx

1. Authenticate using the quickstart and the host's supported account flow.
2. Confirm the connection status and available tools. Follow the current Anyx instructions for `get_status`, then `list_groups`.
3. Select the intended returned group. Resolve ambiguous names before retrieving messages.
4. State the time window and timezone. Request messages only within the user's scope using the current schema.
5. Invoke one installed skill and inspect its evidence, coverage limits, and proposed output.

For a first live pilot, use a designated demo group containing synthetic messages. Record the host version, skill revision, tool schema, group scope, time window, and observed result. A local fixture run and a live MCP run have separate evidence records.

## Verify the installation

| Check | Passing evidence |
| --- | --- |
| Skill discovery | Host lists the selected Anyx skill and loads its referenced files. |
| Authentication | Anyx status confirms the expected account connection. |
| Group scope | The selected returned group matches the requested demo group. |
| Time scope | Retrieval follows the approved window and reports incomplete coverage. |
| Workflow output | A useful result includes source references and distinguishes evidence from proposals. |
| External action control | Supplier text stays a reviewable draft unless a separately authorized action is available. |

## התחלה בעברית

1. התקינו את תיקיית היכולת במיקום המתועד של המארח.
2. חברו את Anyx לפי מדריך MCP ובדקו שהחיבור פעיל.
3. בחרו קבוצה, טווח זמן ושפה.
4. הפעילו יכולת אחת על קבוצת הדגמה ובדקו את המקורות והתוצאה.

פקודות הבדיקה המקומיות, מתוך תיקיית הערכה:

```text
python tools/validate_kit.py
python -m unittest discover -s tests
python tools/build_skill_zips.py
```
