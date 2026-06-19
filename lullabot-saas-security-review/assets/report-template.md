# <Service Name> <Year> Security Review

| Field | Detail |
| --- | --- |
| Service Name | <service name> |
| Requested By | <name> |
| Where the service will be used | <where> |
| How the service will be used | <how> |
| Privacy Policy | <url> |
| Terms & Conditions | <url> |
| Data the service will access | <Lullabot-owned and/or client-owned data> |
| Reviewed by | Unreviewed, AI generated |

This review is based on Lullabot's SaaS service evaluation guidance ([security.lullabot.com/communications/cloud.html](https://security.lullabot.com/communications/cloud.html)).

## Initial Recommendation

<One sentence: approval, conditional approval, or denial.>

<Supporting paragraph explaining the recommendation, proportional to data exposure and intended use.>

## Company Location and Jurisdiction

<Company identity, headquarters/operating location, legal venue/jurisdiction, data hosting regions when available. Cite each claim.>

## Authentication and Access Control

<Google login, SSO/SAML/OIDC, SCIM, native accounts, MFA/2FA, password policies, session controls, admin-enforced MFA, RBAC, workspace admin, provisioning/deprovisioning. Note plan-tier restrictions on security controls. Give audit logs prominent treatment; flag gaps as risks/conditions.>

## Data Handling

<Data collected/received, customer content processed, AI/model training on customer data, information sharing, export options, account/data deletion, retention periods, storage location, encryption in transit and at rest, DPA availability, subprocessors (list current ones or state none found), SOC 2 / ISO 27001 / other assurance when available. State unknowns explicitly.>

## App Integrations and Permissions

<Include when applicable. OAuth scopes, API/bot/workspace permissions, data read/written/retained/shared for integrations such as Slack, Google Workspace, GitHub, Jira, M365, calendar, email, ticketing, repos, CRMs. If scopes undocumented, say so and recommend sandbox install or admin consent review.>

## Security Incidents and Reputation

<Public breaches, security failures, privacy controversies, regulatory actions, reduced commitments. Distinguish confirmed incidents, allegations, and absence of public evidence. Do not treat absence as proof of safety.>

## Risk Notes and Recommended Conditions

<Concise, practical risk notes and the specific conditions attached to the recommendation.>
