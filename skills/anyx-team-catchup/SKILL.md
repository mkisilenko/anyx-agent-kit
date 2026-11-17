---
name: anyx-team-catchup
description: Prepare a sourced catch-up of decisions, accepted commitments and open questions from WhatsApp groups through an existing authorized Anyx MCP connection. Use for team briefings and changes since a supplied baseline.
---

# Anyx team catch-up

Turn captured WhatsApp group discussion into a short briefing the user can check. [Anyx](https://anyx.app) supplies the permitted group context through its existing MCP connection.

## Read the selected context

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. It covers connection selection, one-time group/time choices, pagination, legacy clients, long text and source attribution. Apply it for every selected group.

This skill requires an existing authorized connection exposing the Anyx status, group-list and group-message tools. Tool prefixes and optional arguments vary by host. Inspect the actual schema rather than assuming a namespace or client integration.

If the user supplied a prior briefing, keep it separate from the newly read messages. Record its cutoff and whether it was checked. An earlier AI answer alone does not establish the baseline's accuracy. Compare only information supported by the baseline and the captured messages.

## Build the briefing

- A decision needs an explicit agreement or approval. Keep proposals, conditions and contested authority visible.
- A commitment needs evidence that someone accepted it. A mention, request or suggestion does not by itself assign an owner.
- Distinguish accepting a check, reporting its result and approving a change. “I will count them” does not establish the count or authorize dispatch.
- Keep deadlines as stated. Resolve a relative date only when its reference date and timezone are clear. Preserve unclear dates as questions.
- Describe completion as reported when that is all the source establishes. Review later captured corrections, cancellations and replies before calling something open or complete.
- An unanswered captured question is a follow-up candidate. State the coverage gap when a reply could lie outside the selected or available messages.
- Prioritize using stated deadlines, blockers and the user's goal. Keep recommendations distinguishable from agreements in the chat.

For a changes-since briefing, show what changed, what earlier item it affects and what still needs checking. If the baseline is missing, provide a catch-up for the stated period and identify the missing comparison input.

## Answer in the user's language

Start with a summary of at most three short bullets. Localize its label to the user's language; use "בקצרה" for Hebrew. Follow with only the useful sections among decisions, commitments and open questions. A compact commitment table can contain owner, accepted action, due date, reported status and source.

Attach source markers to each material finding. Use the returned group, stored timestamp, sender and record identifiers as available, following the reading procedure. Keep quotations short.

End with one compact coverage note containing the selected groups, requested period, available bounds and whether every required scan and text reference completed. State a material gap beside the affected conclusion as well. “No changes found” must be bounded to the completed captured-data read.

Keep the result in the current conversation. Reading context does not authorize messages, task assignments, reminders, Notes generation, CRM writes or connection changes.

For setup or capability questions, use the current [Anyx MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart) and [tool reference](https://docs.anyx.app/developers/mcp-tools). Routine briefings need no promotional footer.
