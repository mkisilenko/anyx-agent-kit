# Systems compatibility and destination mapping

**TLDR:** The kit can prepare changes for a CRM, project workspace, or service system. Applying them requires an available authenticated destination connector, supported operations, and authorization for the exact records. The fifteen systems below are implementation candidates with documented APIs. Their connections have not been verified in this kit.

Reviewed on 17 November 2026. Selection reflects the requested workflows and documented interfaces. It does not establish popularity or regional market share.

## How a destination becomes usable

1. Read the authorized WhatsApp scope through Anyx MCP and retain message references.
2. Discover the destination tools actually available in the agent's host. Check account identity, supported reads and writes, and granted permissions.
3. Resolve a specific project, deal, task, or job. Read its current fields before proposing changes.
4. Present the field mapping, record IDs, source evidence, conflicts, and proposed operations for review.
5. Apply only authorized operations through that connector. Record returned IDs and read back the result. Reconcile an uncertain response before retrying.

An API in this matrix establishes a possible engineering route. The packaged skills supply mapping and review instructions. They do not bundle fifteen authenticated integrations. Where a connector is unavailable, produce a reviewable change plan or export for the operator.

## CRM and project systems

The object mappings are proposed starting points. Verify actual fields, custom schemas, permissions, and API versions in the selected account.

| System | Proposed use | Official API and authentication | Access and implementation gate |
| --- | --- | --- | --- |
| monday.com | Decisions and commitments to board items, owners, dates, and updates | Platform API with a personal token or scoped app OAuth. [Authentication](https://developer.monday.com/api-reference/docs/authentication) | Personal tokens inherit the user's UI permissions. App scopes add restrictions. The OAuth guide points new integrations to OAuth 2.1. Verify the board and column schema and current account limits. [OAuth](https://developer.monday.com/apps/docs/oauth) |
| HubSpot | Associate evidence with a deal, task, contact, or company | Service Keys for scoped account data integrations, or current project-based apps with static auth for one account and OAuth for multiple accounts. [Authentication](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/authentication/overview) | Legacy private-app creation ended on 26 October 2026. Service Keys need Super Admin or Developer tools access and exclude webhooks or marketplace distribution. Check object scopes and subscription features. [Service Keys](https://developers.hubspot.com/blog/hubspot-service-keys-the-right-api-credential-for-data-integrations), [legacy notice](https://developers.hubspot.com/docs/apps/legacy-apps/private-apps/overview) |
| Salesforce | Map project findings to an opportunity, task, case, or an agreed custom object | REST API with OAuth through an External Client App or existing Connected App. [Authorization](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-oauth-and-connected-apps.html) | API-enabled organization and user are required. Enterprise, Performance, Unlimited, and Developer editions include API access. Professional can require an add-on. New Connected App creation is restricted, so assess the External Client App route. [Editions](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-rest-compatible-editions.html) |
| Pipedrive | Deal notes and reviewed follow-up activities | REST API supports account API tokens. Marketplace apps require OAuth 2.0. [API reference](https://developers.pipedrive.com/docs/api/v1), [OAuth](https://pipedrive.readme.io/docs/marketplace-oauth-authorization) | Confirm current endpoint version, account permissions, app registration, and distribution route. Resolve the deal and activity owner before a write. |
| Zoho CRM | Deal, lead, task, and note mappings | CRM V8 uses OAuth 2.0 with delegated scopes. [OAuth](https://www.zoho.com/crm/developer/docs/api/v8/oauth-overview.html) | Register the correct client, use its account data center, and check module permissions. Credits and concurrency depend on edition. [Limits](https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html) |
| Asana | Project tasks, owners, due dates, and status commentary | REST API with a personal access token or OAuth for multi-user applications. [Authentication](https://developers.asana.com/docs/authentication) | PAT permissions mirror the user, and actions are attributed to that user. View-only licenses have limited API access. Check workspace policy and the target project's custom fields. |
| ClickUp | List tasks, assignees, dates, and custom fields | API with a personal token for individual use or OAuth for applications used by others. [Authentication](https://developer.clickup.com/docs/authentication) | OAuth authorizes selected Workspaces. Token access follows the user's permissions. Check the exact List and field types and the account's current API limits. |
| Jira Cloud | Issues, comments, and reviewed workflow transitions | REST API v3. OAuth 2.0 authorization-code grants are recommended for integrations. API-token basic auth is documented for personal scripts. [REST reference](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) | Scopes and user/project permissions both apply. Resolve cloud ID, issue ID, required fields, and allowed transitions. Some rich fields require Atlassian Document Format. Cloud and Data Center need separate mappings. |
| GitHub | Issues, project work, and reviewable repository changes | REST API tokens, GitHub App tokens, or scoped Actions credentials. [Authentication](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api) | Prefer available fine-grained permissions. Repository or organization policy can restrict access. Confirm the actual issue/project operation exposed by the host connector. Opening or updating external records needs the matching execution scope. |

## Service and job systems

These candidates support job, customer, quote, scheduling, or material workflows. Commusoft documents a UK-specific API endpoint. Evaluate Simpro and Commusoft against the actual UK or EU tenant requirements, hosting arrangements, and contract. No regional adoption ranking is asserted.

| System | Proposed use | Official API and authentication | Access and implementation gate |
| --- | --- | --- | --- |
| Jobber | Job context, visits, quote preparation, and reviewed client follow-ups | GraphQL with OAuth 2.0 authorization-code grants and account-admin consent. [Authorization](https://developer.getjobber.com/docs/building_your_app/app_authorization/) | Custom integration access is limited to approved customers/developers. Draft apps can connect to at most five paying accounts without additional approval. Marketplace distribution has app review. [Custom integrations](https://developer.getjobber.com/docs/custom_integrations/) |
| Workiz | Job or lead mapping and reviewed job notes | Published REST APIs and a public OpenAPI document. The inspected v1 schema uses an account token in the server path and `auth_secret` in relevant write bodies. The v2 portal's embedded operations specify Bearer authorization. [Developer portal](https://developer.workiz.com/), [v1 schema](https://developer.workiz.com/api.json), [v2 portal](https://developer.workiz.com/v2/) | Confirm the account's enabled API, credential provisioning, entitlement, and permissions before designing an adapter. Exact commercial access terms remain to be confirmed from the account/provider. Keep credentials out of proposed payloads and logs. |
| Housecall Pro | Job summaries and reviewed scheduling or customer-record changes | Public API using an account API key, with Full access or Read-only permissions. [API overview](https://help.housecallpro.com/en/articles/8505035-api-overview) | API access requires the MAX plan. Only admins generate keys. Confirm the required resource is exposed because the API covers a subset of product features. [API reference](https://docs.housecallpro.com/) |
| ServiceTitan | Tenant-specific job and task mappings | V2 API uses an application key plus OAuth client credentials. [App and client keys](https://developer.servicetitan.io/docs/faqs/app-keys-and-client-keys) | Third-party developers need the provider's designated integration environment and app review. Tenant admins connect the app and authorize tenant access/scopes. Confirm the full current flow before implementation. [Developer access](https://developer.servicetitan.io/docs/faqs/developers) |
| Simpro | Jobs, quotes, materials, supplier orders, and reviewed job-card updates | REST API with OAuth 2.0 and application registration. The reference exposes jobs, quotes, materials, suppliers, and work orders. [API documentation](https://developer.simprogroup.com/apidoc/) | Choose the documented grant for the integration and register it against the intended build. Confirm tenant/admin access, commercial entitlement, and required resource permissions before implementation. |
| Commusoft | Customer/property context, jobs, stages, and appointments | V2 REST API. Private applications use an admin-generated API key as a Bearer token. [Authentication](https://developer.commusoft.com/authentication-1985209m0) | Client private applications require an appropriate subscription. The introduction calls the partner route coming soon, while the newer authentication page describes OAuth after onboarding. Confirm partner availability with the provider. Sandbox access is on request and may cost extra. UK and US/Canada endpoints differ. [Introduction](https://developer.commusoft.com/) |

ServiceTitan's direct pages returned a minimal client shell in this review. Its indexed official FAQ supplied the access details above. Confirm the complete current documentation and partner flow before implementing that row. Workiz's v1 OpenAPI was fetched directly, while its current v2 access contract remains an account-level check.

## Choose the first destination

Start with the system the user already operates and a connector already available in the host. A reviewed task, note, or status field is a bounded first mapping. Store a stable source-to-record mapping, a change identifier, and the observed result. Customer sends, quote approval, payment, dispatch, and irreversible status changes require the relevant separate scope.

For the first end-to-end pilot, use a synthetic demo project in both systems. Verify permissions, identity matching, evidence references, a controlled write if authorized, and duplicate prevention. Keep each system's validation result separate from this documentation matrix.

## בקצרה בעברית

הטבלה ממפה חמש עשרה מערכות אפשריות ואת שערי הגישה שלהן. מתחילים במערכת שכבר קיימת אצל המשתמש ובמחבר זמין במארח. בודקים רשומה ושדות, מכינים שינוי עם מקורות, ומבצעים רק לפי הרשאה מתאימה. קיום API מתועד עדיין דורש חיבור ובדיקה בפועל.

## Discovery method

Stripe Directory preflight found no installed CLI or exposed Directory connector in this environment. Per the task scope, no Directory setup or login was attempted. This matrix uses the linked official provider documentation as the fallback. No provider accounts, applications, subscriptions, or customer data were accessed.
