---
name: lullabot-saas-security-review
description: Produces a downloadable Markdown security review report evaluating a SaaS application or product for possible use at Lullabot, anchored to Lullabot's SaaS service evaluation guidance. Use this whenever someone asks for a Lullabot security review, a SaaS/vendor/tool security review for Lullabot, asks to evaluate or vet a cloud service or app for Lullabot use, or asks to revise/update an existing Lullabot security review. Trigger on phrases like "security review", "vendor review", "vet this tool", "is X safe to use at Lullabot", or references to the security review submissions spreadsheet, even when the word "skill" is not used.
---

# Lullabot SaaS Security Review

## Requirements

Live web search and page retrieval are required to verify current vendor claims. Supply the service identity, intended use, and a data-category description for intake. Access to Lullabot’s SaaS evaluation guidance is required to assert alignment with it; if unavailable, identify that limitation and request an eligible copy rather than inventing its contents. Local file writing is optional for the downloadable Markdown report; no vendor login, trial installation, production integration, or admin credentials are required for public-source research.

## Safety and review

Use public vendor facts and a minimal description of data categories for research, not actual customer records, credentials, personal requester details, or private intake documents in public searches/models. Non-public material requires a tool that neither trains on nor retains it; confidential information needs specific approval; personal information needs a specifically approved tool integrated where it is stored. An internal report may contain sensitive findings and must remain in an eligible local/internal destination.

The report is an AI-assisted recommendation, not procurement approval or completed human security review. Retain `Unreviewed, AI generated` until an actual qualified human reviews it; never replace that marker with an invented reviewer. A human author must check facts, links, scope, and disclosures before sharing the draft; an authorized Security Team reviewer makes the final approval decision and verifies tool eligibility. New tools need Security Team review. Do not install trials, grant consent, connect production integrations, or upload evidence as part of research. Such actions require separate authorization, least privilege, and human review of MCP mutations or commands outside secure sandboxes.

This skill produces a professional, internal-use security review of a SaaS application or product being considered for use at Lullabot. The single deliverable is a downloadable Markdown report, ready to import into another tool, modeled on Lullabot's SaaS service evaluation guidance at https://security.lullabot.com/communications/cloud.html.

The whole point of the review is to help a human reviewer make a sound approval decision. That means the value is in *verified, claim-level facts about a real vendor* — not a plausible-sounding template filled with assumptions. Favor honest "this could not be confirmed" over invented reassurance every time.

## The report is never written in the first person

The report is an internal document, not a conversation. Write it in neutral third person throughout ("The vendor states...", "No subprocessor list was found..."). The conversational messages around the report (asking intake questions, presenting the file) are normal first-person chat — only the report file avoids first person.

## Step 1: Collect intake

Before researching, gather the details the report's intake table needs:

- Service Name
- Requested By
- Where the service will be used
- How the service will be used
- Link to Privacy Policy
- Link to Terms & Conditions
- What Lullabot-owned or client-owned data the service will access

Remind the user they can copy this from the security review submissions spreadsheet — it saves them retyping.

Ask only the follow-up questions you actually need. The questions that matter most are the ones that change the review's conclusions: the service's exact identity (vendors with similar names get confused easily), the intended use, and the data exposure. If the user has already supplied enough to proceed, don't re-ask — just start. If something decision-critical is genuinely unclear (e.g., which "Notion" or whether client data is involved), ask before researching, because researching the wrong product wastes everyone's time.

## Step 2: Research and verify against current sources

Anchor the review explicitly to Lullabot's SaaS evaluation guidance and cite that guidance in the report.

Verify each major claim against current vendor documentation or high-quality public sources. Search the live web — training-data recall about a vendor's security posture is often stale or wrong, and stale facts in a security review are worse than no facts. Things to verify when applicable:

- Company identity, headquarters or operating location, legal jurisdiction/venue for disputes
- Data storage/hosting regions
- Privacy practices, information sharing, subprocessors
- Integration permissions and OAuth scopes
- AI / model-training practices on customer data
- Export and deletion options, account deletion
- Account security features, MFA, SSO, audit logs
- Data retention, breach notification, admin controls
- Encryption in transit and at rest
- DPA availability
- Independent assurance: SOC 2, ISO 27001, trust-center materials

### Citations must be precise, claim-level, and clickable

The report is a standalone Markdown file a reviewer will read outside this conversation, so a citation only counts if it is an actual inline Markdown link the reviewer can click — `[descriptive text](https://source-url)` — placed right next to the claim it supports. Phrasing like "the vendor states..." with no link is not a citation; it just sounds like one. Every claim that rests on a source needs the real URL inline. Link to the specific page that backs the claim (the privacy notice, the subprocessor list, the security docs page), not just the vendor homepage.

Cite at the level of the individual claim — don't park five unrelated statements behind one broad link. High-risk or decision-critical statements (data training, subprocessors, breach history, jurisdiction, deletion guarantees) especially need their own nearby link from the most relevant source available: vendor legal terms, privacy notice, subprocessor list, security/trust docs, admin docs, incident reports, or reputable public reporting.

When you can't find a source for something, say so plainly in the relevant section. Do not imply a practice exists, and do not invent citations or attributions — a fabricated or guessed URL is worse than an honest "not found." Absence of evidence is itself useful information for the reviewer.

## Step 3: How to treat certifications and assurance

Do not invent a blanket certification requirement or a blanket exemption from assurance review. Check the accessible, current Lullabot guidance and applicable use-case obligations. If the guidance is unavailable, label policy alignment unverified and leave that judgment to the authorized Security Team reviewer.

Document SOC 2, ISO 27001, DPAs, and trust-center material as evidence with their scope, date, and limitations. A certification alone does not establish approval or safety; its absence alone does not establish unacceptable risk. Distinguish vendor claims from reports actually inspected. Recommend collecting available assurance when relevant to planned data exposure, and explain the specific risk/control it helps evaluate.

## Step 4: Evaluate the key areas in depth

These three areas carry the most decision weight, so treat them thoroughly rather than checking a box.

**Authentication and access control.** Determine support for Google login, SSO/SAML/OIDC, SCIM (when relevant), native accounts, MFA/2FA, password policies, session controls, admin-enforced MFA, role-based access, workspace administration, and user provisioning/deprovisioning. Call out when important controls sit behind higher pricing tiers — a control the buyer can't afford is effectively unavailable. **Audit logs deserve prominent treatment:** if audit logging is missing, unclear, or limited, name it as a risk and, where appropriate, as a condition for approval or broader deployment.

**Data handling.** Identify what the service collects or receives, what customer content it processes, whether AI features train on customer data, how information is shared, how data is exported, how accounts and data are deleted, whether retention periods are defined, where data is stored, and whether encryption in transit and at rest is documented. For subprocessors, list the current ones when a list exists; if none is found, say so explicitly and recommend obtaining it before approval when the service will touch non-public Lullabot or client data.

**App integrations and permissions** (when applicable). For integrations like Slack, Google Workspace, GitHub, Jira, Microsoft 365, calendar, email, ticketing, repositories, or CRMs, identify requested OAuth scopes, API permissions, bot/workspace permissions, and what data may be read, written, retained, or shared. When exact scopes aren't documented, say the vendor documentation is unclear and recommend a sandbox install or admin consent review before production use — guessing at scopes would mislead the reviewer.

**Security incidents and reputation.** Search for public breaches, security failures, privacy controversies, regulatory actions, major customer-data incidents, or weakened privacy/security commitments. Carefully distinguish confirmed incidents from allegations from simple absence of public evidence. Do not present "no known incidents" as proof of safety — it usually just means nothing surfaced in a search.

## Step 5: Make a proportional recommendation

The recommendation must be evidence-based and proportional to the data exposure and intended use. A low-risk tool touching no sensitive data warrants a lighter touch than one handling client data.

- **Conditional approval** fits when important evidence is missing but risk can be bounded through mitigations: limiting use to low-risk data, disabling sensitive integrations, obtaining a DPA or security report, verifying audit logs, confirming subprocessors, requiring SSO/MFA, restricting admin access, or testing export/deletion workflows.
- **Denial** fits when the service presents unacceptable risk, can't meet required controls for the planned data exposure, has materially concerning unresolved incidents, or demands excessive permissions without adequate safeguards.
- **Recommended approval** fits when evidence supports the intended use, with the final decision reserved for an authorized human reviewer.

All three outcomes are recommendations, not actual approval or denial. Avoid overstating confidence. Clearly identify unknowns and vendor ambiguity rather than smoothing over them.

## Report structure

Use the bundled template at `assets/report-template.md` as the scaffold, and follow this exact section order:

1. **Title** — `<service name> <current year> Security Review`
2. **Intake table** — the user-provided intake fields, plus a "Reviewed by" row with the value `Unreviewed, AI generated`
3. **A short statement** that the review is based on Lullabot's SaaS evaluation guidance (with the citation)
4. **Initial Recommendation** — one sentence recommending approval, conditional approval, or denial, then a supporting paragraph
5. **Company Location and Jurisdiction**
6. **Authentication and Access Control**
7. **Data Handling**
8. **App Integrations and Permissions** (when applicable)
9. **Security Incidents and Reputation**
10. **Risk Notes and Recommended Conditions** — concise and practical

## Step 6: Deliver the file

When file-creation tools are available, always write the complete report to a downloadable `.md` file and present it. Then give a brief final message linking the file. Keep that message short — the reviewer wants the document, not a recap of it.

If downloadable file creation is not available, output the complete Markdown report in the response with a suggested filename (e.g., `service-name-2026-security-review.md`).

## Revising an existing review

When asked to revise, strengthen, or update an existing review, preserve the required structure and section order while improving source precision, refreshing verification against current sources, tightening risk conditions, and ensuring the Markdown file is clean and ready to import.
