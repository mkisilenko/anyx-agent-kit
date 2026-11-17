---
name: anyx-decision-log
description: Draft or reconcile a sourced decision log from captured WhatsApp group messages through an existing authorized Anyx MCP connection. Preserve approval conditions, authority uncertainty, later corrections and superseded decisions.
---

# Anyx decision log

Prepare a decision log the user can review from captured WhatsApp context supplied by [Anyx](https://anyx.app). Preserve what was agreed and how later discussion changes it.

## Read the selected context

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. Apply its group/time choices, schema checks, pagination, text recovery and source rules.

Use the existing authorized Anyx MCP connection and the tools actually exposed by the host. Group selection is a usage filter and does not restrict the credential's account scope.

If the user supplies an existing log, retain its entry identifiers and prior wording where still accurate. Treat unsourced entries as supplied baseline claims and distinguish them from newly checked message evidence. Return a proposed revision in the conversation unless a separate artifact edit was requested and authorized.

## Decide what belongs in the log

- Record a specific choice or approval that affects the work. Keep discussion, preferences, requests and proposals separate from confirmed decisions.
- Preserve all stated conditions, dependencies, exceptions and limits. “Approved if the client signs” remains conditional until the captured evidence supports that condition.
- Record who approved or reported the decision using the actual source. When authority matters or is disputed, use the user's supplied authority rules or explicit evidence. A confident message or job title alone does not settle contested authority.
- Distinguish the person making a decision, someone reporting another person's decision and the person accepting the follow-up. A forwarded approval may need confirmation of its original source and context.
- Review later corrections, withdrawals and changes. Link an entry to the explicit replacement when the sources support it. Preserve the earlier decision as superseded rather than deleting it.
- If later statements conflict without a supported replacement or the necessary authority is unclear, record the conflict as unresolved. Avoid silently choosing the latest speaker.
- Preserve the date and timezone as stated or supported. A stored message timestamp is source metadata. Do not turn it into an invented deadline or independent proof of when an off-chat decision happened.
- Keep an agreed action and reported execution separate. Approval of a design does not prove that it was built, sent or ordered.

When there is no confirmed decision, report the proposals and missing approval. Do not create a decision merely to fill the table.

## Return a proposed log

Write in the user's language. Start with a summary of at most three short bullets about new decisions, replacements and unresolved approvals. Localize its label to the user's language; use "בקצרה" for Hebrew.

Use a compact table containing entry ID, decision, decision-maker or reported authority, conditions, status, source and any replaced entry. Retain supplied IDs. For new entries, use local D1, D2 labels and make clear that these are log labels, not Anyx record IDs.

Use statuses that match the evidence, such as confirmed, conditional, proposed, authority unconfirmed, disputed, superseded or withdrawn. Cite both the earlier and later source for a replacement. Keep follow-up commitments in a separate short list with their stated owners and dates.

Finish with the selected groups, requested period, available bounds, read completeness and material gaps. Preserve uncertainty in any affected row. This draft does not approve work, assign people, create reminders, edit a CRM or send group messages.

The [Anyx decision-log template](https://anyx.app/blog/whatsapp-project-decision-log) explains the workflow. Use the current [MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart) and [tool reference](https://docs.anyx.app/developers/mcp-tools) for connection and tool details.
