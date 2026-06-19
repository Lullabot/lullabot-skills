---
name: lullabot-saas-security-review
description: Produces a downloadable Markdown security review report evaluating a SaaS application or product for possible use at Lullabot, anchored to Lullabot's SaaS service evaluation guidance. Use this whenever someone asks for a Lullabot security review, a SaaS/vendor/tool security review for Lullabot, asks to evaluate or vet a cloud service or app for Lullabot use, or asks to revise/update an existing Lullabot security review. Trigger on phrases like "security review", "vendor review", "vet this tool", "is X safe to use at Lullabot", or references to the security review submissions spreadsheet, even when the word "skill" is not used.
---

# Lullabot SaaS Security Review

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

Lullabot does **not** require SOC 2 Type II, ISO 27001, or any certification for approval. This is a firm policy, not a soft preference: the presence or absence of a certification must never be a factor in the recommendation itself. A service with no certifications can be fully approved, and a service with every certification can still be denied for other reasons. Document certifications, assurance reports, DPAs, and trust-center materials when they exist, purely as factual information for the reviewer — but do not phrase the recommendation or its conditions as depending on them, and never imply that a missing certificate weakens the case for approval.

The one legitimate use of assurance evidence as a *condition*: when the service will handle sensitive, confidential, regulated, client-owned, or broad internal data, it is reasonable to suggest obtaining the actual SOC 2 report, ISO certificate, or DPA as defense-in-depth before broader rollout — but only when such evidence already exists or is claimed by the vendor, and framed as "worth collecting," not "required to approve." If the vendor claims SOC 2 or similar but the report isn't public, noting "review the actual report if Lullabot wants the extra assurance" is fine; do not treat the claim itself as suspect or as a barrier.

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
- **Approval** fits when the evidence supports it for the intended use.

Avoid overstating confidence. Clearly identify unknowns and vendor ambiguity rather than smoothing over them.

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
