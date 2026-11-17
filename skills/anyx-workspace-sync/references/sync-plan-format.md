# Anyx workspace sync plan format

Use this format for a saved plan that will be checked with the bundled `scripts/validate_sync_plan.py --input plan.json`. The validator is local and read-only. It cannot verify live access, authority, current records or actual write outcomes. Read the destination through its available authenticated tools for those checks.

## Required plan fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Integer `1`. |
| `mode` | `propose` or `execute`. Default to `propose` while execution prerequisites are unresolved. |
| `scope` | Object with the user-resolved `project_id` and a bounded `description`. |
| `sources` | Array of source records with `id`, `system` and an actual `reference`. Use local source IDs and returned provenance. Never invent a WhatsApp link. |
| `operations` | Array of exact intended changes, each described below. |

## Operation fields

| Field | Meaning |
| --- | --- |
| `operation_id` | Stable unique ID within the plan. Keep it across retries of the same intention. |
| `system` | Exact selected destination system. |
| `account_identifier` | Exact account/tenant/workspace identity established by the connector and user mapping. |
| `object_type` | Real destination object type. |
| `object_id` | Exact returned nonempty string or integer ID for an update. It may be null for a create with an explicit stable business key. Boolean, fractional and structured IDs are invalid. |
| `action` | `update` or `create`. Other mutations require an appropriate separately scoped workflow. |
| `before` | Object containing the relevant original field values. Preserve the mapping and version basis used for the intended operation. |
| `after` | Object containing the intended field values. Exact field identifiers and typed values must come from the real destination schema. |
| `source_ids` | Source IDs that support the operation. They must resolve in the plan's `sources`. |
| `authority` | Evidence explaining who authorized the underlying business fact/change, including unresolved conditions where applicable. This does not replace tool-use authorization. |
| `base` | Object holding current `version` (nonempty string or integer), `etag` (nonempty string) or `snapshot_sha256` (64 hexadecimal characters). A valid-looking fingerprint still needs a reproducible canonical snapshot and a fresh read before execution. |
| `authorization_reference` | Null for an unapproved proposal, or a nonempty reference to the actual user request/policy covering this operation. Every `approved` state requires it in both modes. Preserve field, object, timing and action limits. Presence is structural validation, not proof of authorization. |
| `idempotency_key` | Stable key for this intended operation, meaningful only with supported server behavior or a documented duplicate/reconciliation strategy. |
| `depends_on` | Array of prior operation IDs whose verified result is required. Avoid circular or unresolved dependencies. |
| `state` | `proposed`, `approved`, `submitted`, `outcome_unknown` or `verified`. |
| `external_receipt` | Null before execution or an object containing actual operation-specific submission/verification evidence. Preserve exact external IDs and the limits of the receipt. |

Receipt checks are structural only: a nonempty JSON object is required for submitted/verified states, but even `{"note": "looks fine"}` is not authenticated write or verification evidence. The executor must establish operation-specific provenance and actual read-back before assigning those states. A helper success result does not establish authority, fresh state or remote outcome.

For a create without an exact ID, `external_business_key` (or its compatible `business_key` alias) must hold a resolved nonempty string or integer, either at operation level or as `after.external_business_key`. A mapping object is not a resolved value. An optional `ledger_reference`, when present, is a nonempty string identifying the exact ledger revision/hash. These structural fields do not authenticate any external identity or ledger.

For a create, name the stable business-key field in the mapping. Use its destination-native field identifier, or explain an equivalent supported lookup. Check uniqueness in the correct account/project before creation. A randomly generated local operation ID is not an external business-key match.

If a destination has no exposed version/ETag, fingerprint a reproducible snapshot of the relevant identity and fields. Record the canonicalization method in the review notes. A local hash cannot create atomic conditional-write support in the destination.

## States and execution

`proposed` means a change has been identified. `approved` means the concrete operation has matching user authorization and its current execution prerequisites are satisfied. The user may have supplied this authorization earlier through a scoped future-write policy.

`submitted` records a request accepted or sent whose applied state still needs checking. `outcome_unknown` records uncertainty after a possible write. It blocks replay and dependent steps until reconciled. `verified` requires sufficient read-back and operation-specific evidence. A transport acknowledgment or desired value observed without attribution may be insufficient to establish that this operation applied.

For `mode: execute`, pending writes need a real authorization reference and approved state. Previously completed or unknown operations must be handled according to their recorded states rather than resubmitted as fresh writes. Validate and reconcile before proceeding. The validator does not execute a plan.


### Full ledger and independent execution batches

Keep the complete ledger in proposal/reconciliation form, preserving unknown outcomes and all prior receipts. To proceed on independent work, create a separate `mode: execute` batch with only the currently approved selected operations plus any verified prerequisites referenced by their dependencies. Include a `ledger_reference` or surrounding review reference to the exact source ledger revision/hash. This reference is documentary: the helper does not load or authenticate another ledger.

Preserve each selected operation's ID, idempotency key, account, target, sources, base and authorization. A selected operation that depends on an unresolved or omitted prerequisite is blocked; do not remove its dependency to make validation pass. Do not delete, reset or replay unknown operations in the master ledger. Before execution, the executor compares the batch with that ledger and freshly reads destination preconditions. Afterwards, reconcile actual receipts and uncertainty back into the same ledger. A full mixed ledger with `outcome_unknown` is deliberately rejected as an execute batch.

Record any conflicts and unresolved mappings in the surrounding review. Keep them outside approved operations until resolved. If an approved operation's source, affected field, precondition or authorization changes, return it for review or recompute the proposal within the user's grant before a write.

## Fictional proposal

All names, IDs, field names and values below are synthetic. They demonstrate the format and are not an integration schema or live Anyx/customer response. The intended destination must expose its own actual field names and values.

Use [the fictional proposal JSON](example-plan.json) as a format example. Its destination fields and IDs are synthetic.

The example remains a proposal. A real execution still needs the actual connector, resolved mapping, current record and matching user authorization.
