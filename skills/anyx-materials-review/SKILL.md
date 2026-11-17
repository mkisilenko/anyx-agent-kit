---
name: anyx-materials-review
description: Review material requests in captured WhatsApp group messages through an existing authorized Anyx MCP connection. Prepare a sourced list by job, exact item and unit, with explicit duplicates, corrections and missing details handled before a supplier inquiry draft.
---

# Anyx materials review

Use permitted group context from [Anyx](https://anyx.app) to prepare a materials list for human review. Keep requested quantities, reported stock and an approved purchase separate.

## Read the selected context

Read [the MCP reading procedure](references/mcp-reading.md) before calling tools. Apply its group/time choices, schema checks, pagination, text recovery and evidence rules to every selected group.

Use the existing authorized Anyx MCP connection. Inspect the exposed tools and arguments. A group choice filters this review and does not narrow the credential's account scope.

## Reconcile requests

For each relevant source, retain the exact job reference, item/model, unit, requested quantity, needed-by date and stated requester. Leave missing information explicit.

- Match job references exactly. J42 and J420 are separate jobs.
- Combine totals only for matching item/model and compatible explicit units. Do not assume a pack size, substitute model or conversion.
- Distinguish a material request from a suggestion, question, stock report, delivery report or purchase approval.
- Treat a forwarded or repeated message as the same request only when its wording or source evidence establishes that relationship. Similar wording alone cannot decide whether demand is duplicated or additional.
- An explicit correction or cancellation updates the affected request. Preserve both sources and identify the change. Avoid counting the replaced quantity again.
- For “two more,” “make it three,” conflicting quantities or an uncertain job, retain the ambiguity until surrounding evidence resolves it. Show known subtotals separately from unresolved demand.
- Keep job allocations even when the supplier inquiry combines an item total. Do not infer an allocation from the group name alone.
- Label stock and delivery statements as reported with their source and time. Available stock, reserved stock and ordered stock may differ. Subtraction requires compatible units, scope and dates and remains a proposed calculation unless the evidence establishes allocation.
- Identify the person who accepted a check separately from the person who must approve an order. Never infer purchase authorization from a request, a stock gap or this skill invocation.

Review later captured corrections and replies within the agreed period before finalizing. If a relevant text reference or scan is incomplete, mark the affected total or status provisional and show the missing check.

## Return a reviewable result

Write in the user's language. Begin with a summary of at most three short bullets, covering the known request total where meaningful, the important uncertainty and the next check. Localize its label to the user's language; use "בקצרה" for Hebrew.

Use a compact table with job, exact item/unit, requested quantity, needed by, source and open check. Add an item-total table only when aggregation is supported. Keep reported stock and any proposed purchase quantity in separately labeled fields so they cannot be read as the requested total or an approved order.

Cite each material row and each correction using the returned source details. End with the compact coverage note required by the MCP reading procedure.

If the user requested a supplier inquiry, draft it in the conversation using checked quantities and explicit questions. Preserve missing models, dates and availability as questions. Do not send it or create an order, stock adjustment, CRM record or task.

The [Anyx materials example](https://anyx.app/blog/whatsapp-mcp-materials-supplier-inquiry) illustrates this review. Setup and current capabilities are documented in the [MCP quickstart](https://docs.anyx.app/developers/mcp-quickstart) and [tool reference](https://docs.anyx.app/developers/mcp-tools).
