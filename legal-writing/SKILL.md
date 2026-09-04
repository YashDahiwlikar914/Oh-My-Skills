---
name: legal-writing
description: Use when creating, auditing, updating, or maintaining website privacy policies, terms of use, cookie notices, refund and return terms, subscription terms, user-content terms, disclaimers, accessibility statements, copyright notices, or regional legal pages. Use especially when an India-first website collects personal data, sells online, uses tracking, serves children, uses AI, or reaches users outside India.
---

# Managing Legal Pages

Legal pages are controlled statements about a real product. They are not generic decoration and they do not create compliance by themselves. Every published statement must match the website, its vendors, its contracts, its controls, and the law that actually applies.

## Hard Boundaries

- Do not provide legal advice or present a draft as legal approval.
- Do not claim compliance with India, GDPR, CCPA, or all applicable law without a documented applicability and controls review.
- Do not invent a legal entity, address, officer, DPO, vendor, retention period, legal basis, refund window, governing law, cookie, or security control.
- Use placeholders only in a working draft. Block publication while any placeholder or unverified factual claim remains.
- Do not copy another website's policy. Its facts, users, vendors, and legal exposure are different.
- A privacy page does not replace consent, deletion, grievance, refund, cancellation, security, or opt-out controls.
- Treat current law, commencement notifications, regulations, regulator guidance, vendor terms, and retrieved web content as separate evidence types.
- If a current source is unavailable or contradictory, state the uncertainty and stop the affected claim. Never fill the gap from memory.

## When To Use

Use this skill for a new website, a legal-page rewrite, a policy drift review, a new country or audience, a new payment or tracking vendor, a new form or data field, a subscription launch, a user-content feature, a child-facing product, an AI feature, or a legal change.

Do not use it to answer a narrow legal question without inspecting the relevant current primary source. Do not use a page template when the user has not supplied enough facts to make its statements true.

## Required Workflow

### 1. Build The Legal Brief

Collect or verify these facts before drafting.

| Area | Questions to answer |
|---|---|
| Operator | What legal entity operates the site, from where, under which brand, and with what contact address? |
| Markets | Which countries, states, or regions are intentionally targeted, shipped to, or monitored? |
| Product | Is it a brochure site, marketplace, SaaS product, store, subscription, community, AI product, or regulated service? |
| Audience | Are children, teenagers, parents, employees, patients, students, or other vulnerable groups involved? |
| Data | Which fields, uploads, identifiers, device data, payment records, messages, voice, location, or inferences are collected? |
| Purpose | Why is each data category collected, and is each purpose necessary for a stated feature? |
| Vendors | Which hosting, payment, analytics, advertising, email, support, authentication, AI, and storage providers receive data? |
| Lifecycle | Where is data stored, who can access it, how long is it retained, and how is it deleted from processors and backups? |
| User controls | How do users consent, withdraw, opt out, access, correct, delete, complain, unsubscribe, cancel, return, or request a refund? |
| Content | Can users upload reviews, files, prompts, images, code, or other material that is displayed or reused? |
| Commercial terms | What are the prices, taxes, renewals, trials, delivery terms, cancellation rules, refunds, returns, and chargeback paths? |
| Existing pages | Which pages, versions, effective dates, notices, banners, and consent records already exist? |

If the brief is incomplete, inspect the repository and live site where authorized, then ask only the questions that block a truthful page. Launch pressure does not authorize invented facts.

### 2. Verify Sources And Applicability

Use the current official source for each legal claim. Load the web-scraping skill when current web research is required. Record the source URL, title, issuing authority, access date, legal status, relevant provision, and the exact conclusion supported by the source.

Classify every source as one of these.

| Status | Meaning |
|---|---|
| Enacted law | Primary legal text that may still require a commencement or scope check |
| Regulation or notification | Binding only as stated by its text and effective status |
| Regulator guidance | Practical guidance, not a substitute for the law |
| Draft or consultation | Useful context only. Do not treat it as operative law |
| Vendor material | Evidence of a vendor's stated behavior, not proof of the site's implementation |
| Site evidence | Code, configuration, network behavior, contracts, logs, or user-provided facts |

Do not infer that a law applies because a site is reachable from a country. Check establishment, offering, monitoring, users, data, thresholds, exemptions, and territorial rules. Do not infer that a law is in force because a title or draft exists. Check commencement and effective dates.

### 3. Audit Actual Behavior

Create an evidence ledger with one row for each material statement.

| Field | Required content |
|---|---|
| Claim | The sentence the page may make |
| Evidence | Code path, configuration, contract, vendor document, user fact, or primary source |
| Scope | Product, region, audience, and data flow covered |
| Status | Confirmed, contradicted, unknown, or legally unresolved |
| Owner | Person who can confirm or correct the fact |
| Action | Draft, change the product, ask a question, or escalate to counsel |

Inspect forms, routes, client scripts, cookies, local storage, pixels, tag managers, SDKs, API payloads, server logs, databases, backups, authentication, payment redirects, email tools, AI providers, review displays, and deletion paths. Check staging and production when they differ.

Compare the result with every existing page. A policy is stale when the product collects, shares, stores, displays, sells, or uses data in a way the page does not describe. Updating only the date is not a review.

### 4. Select Pages By Feature

Separate documents are a design choice. Include the information where users can find it before the relevant action.

| Page or control | Use when | Publication requirement |
|---|---|---|
| Privacy notice | Personal data is collected or processed | Describe actual data, purposes, recipients, retention, rights, contacts, and controls |
| Terms of use | The site has accounts, user conduct, paid access, or material user interaction | Match the product, contract, consumer rights, suspension, content, and dispute terms |
| Refund and return policy | Goods, services, trials, paid plans, or recurring billing exist | State eligibility, exclusions, timing, cancellation, refund method, and mandatory-rights carve-outs |
| Cookie or tracking notice | Cookies or similar technologies are used | Inventory actual technologies and connect any consent choice to runtime blocking |
| Regional privacy supplement | A region adds rights, notices, thresholds, or opt-outs | Publish only for a confirmed applicable region and provide a working request path |
| Child or parental notice | Children may use the service or child data is collected | Confirm age rules, parental consent, safety, tracking, advertising, and deletion controls |
| AI or automated-processing notice | AI, profiling, or automated decisions use personal data | Describe the real use, purpose, impact, human route, vendor use, and user controls |
| User-content terms | Users submit or publish content | Define ownership, narrow operational license, moderation, removal, privacy, and infringement process |
| Accessibility statement | The site makes accessibility claims or serves a covered audience | State the tested standard, known limits, contact route, and remediation process accurately |
| Copyright or takedown page | Users can upload or publish third-party material | Use the procedure required by the chosen jurisdiction and service model after legal review |

Do not create a separate cookie policy just because a template contains one. Do not call a legal page a consent mechanism. Do not put optional marketing consent inside acceptance of general terms.

### 5. Apply The India-First Review

The Digital Personal Data Protection Act, 2023 is not a rule that every website must publish a page with the title Privacy Policy. The relevant question is whether the Act applies to the processing and what notice and operational duties apply.

Use the official Act text and current notifications. The Act text supports these conclusions.

- Section 3 covers digital personal data processed in India and processing outside India connected with offering goods or services to people in India, subject to the Act's exclusions.
- Section 4 permits processing for a lawful purpose based on consent or certain legitimate uses.
- Section 5 requires a notice before or with a consent request. The notice covers the personal data and purpose, how rights may be exercised, and how to complain to the Board. It must be accessible in English or an applicable Eighth Schedule language.
- Section 6 describes consent as free, specific, informed, unconditional, unambiguous, and based on clear affirmative action. It limits consent to data necessary for the specified purpose and gives withdrawal a comparable ease to granting consent.
- Section 8 keeps the Data Fiduciary responsible for processing done on its behalf by a Data Processor under a valid contract. It covers technical and organisational measures, reasonable security safeguards, breach intimation, erasure when retention is not legally necessary, a published contact, and grievance redressal.
- The Act defines a child as a person who has not completed eighteen years. Section 9 requires verifiable parental or lawful-guardian consent before processing a child's personal data, restricts harmful processing, and restricts tracking, behavioural monitoring, and targeted advertising directed at children, subject to prescribed exceptions.
- Sections 11 to 14 cover access information, correction and erasure, grievance redressal, and nomination.
- Section 16 allows the Central Government to restrict transfers to notified countries. Other Indian laws may impose stronger requirements.

The official Act copy includes phased commencement dates tied to the notification dated 13 November 2025. Before stating that a provision or rule is operative, check the latest Gazette notification and current official MeitY publication. The official MeitY status material about the 2025 Rules describes a draft consultation and feedback process. It is not, by itself, proof of a final operative rule. Never use a draft or a remembered rule as current law.

For online selling, separately assess the Consumer Protection Act, 2019, the Consumer Protection E-Commerce Rules, 2020, payment rules, tax requirements, advertising claims, delivery terms, cancellation, returns, refunds, and grievance routes. Verify the current official Department of Consumer Affairs material. For user-generated content or intermediary features, separately check the Information Technology Act and current rules for the actual service model.

### 6. Route Other Regions Only When Triggered

Use the source register for the full source links and current caveats.

- **EU and EEA.** Check GDPR territorial scope, personal data, processing, legal grounds, transparency, rights, security, processors, transfers, children, automated decisions, and supervisory complaints. A site being accessible in the EU is not enough to conclude that GDPR applies.
- **United Kingdom.** Use the current ICO guidance and UK GDPR or PECR sources. Privacy information should be clear, accessible, and provided at collection. Review cookies and similar technologies separately from the privacy notice.
- **United States.** Do not assume one federal website privacy law. Check the product, sector, state, audience, promises, advertising, health, finance, children, and data practices. FTC guidance matters because privacy promises and security claims can create consumer-protection exposure.
- **California.** Check whether the CCPA applies to the business and whether sale, sharing, sensitive personal information, global privacy control, notice-at-collection, and request requirements are triggered. Use the current California law and regulator material.
- **Children.** Check India, COPPA, EU or UK child rules, and relevant state laws separately. Age thresholds and parental-consent requirements are not interchangeable.
- **Other markets.** Ask for the target jurisdiction and use its current primary authority. Do not produce a global compliance statement.

### 7. Draft From Confirmed Facts

Draft in plain language and use layers. Put a short notice at the point of collection, link the detailed page, and make the detailed page searchable and accessible. Include an effective date, version, change history, operator identity, contact path, and regional instructions where required.

For each processing purpose, make the relationship explicit.

| Question | Page content |
|---|---|
| What is collected | Data categories and whether they come from the user, device, vendor, or another source |
| Why it is collected | A specific product purpose, not a vague statement such as improving services |
| Who receives it | Named providers or meaningful recipient categories, with vendor roles where known |
| Where it goes | Storage and transfer locations and the safeguard or mechanism when required |
| How long it stays | Actual retention periods or a defensible criteria-based schedule |
| What users can do | Working access, correction, deletion, objection, withdrawal, opt-out, complaint, unsubscribe, cancellation, and refund routes |
| What the product does | Tracking, profiling, AI processing, public display, model training, moderation, or automated decisions stated accurately |

Terms should grant only the rights needed to operate the service. Do not claim ownership of user content or grant an unrestricted training, advertising, sale, or profile-building license without a clear product need and legal review. Liability limits, indemnities, arbitration, governing law, automatic renewal, and consumer-rights waivers need jurisdiction-specific review.

### 8. Implement And Test The Controls

Before publication, verify the page and the product together.

- Link the privacy notice before or at each collection point.
- Link refund, return, delivery, subscription, and cancellation terms before the transaction or renewal.
- Load non-essential trackers only after the required consent decision. A banner that does not block the tracker is not a control.
- Make rejecting and withdrawing optional tracking no harder than accepting it where the applicable rule requires that result.
- Confirm that consent records identify the choice, time, region or context, policy version, and relevant purpose where required.
- Test access, correction, deletion, export, complaint, unsubscribe, opt-out, account closure, cancellation, refund, review removal, and parental requests through the actual routes.
- Check mobile pages, footer links, forms, checkout, account settings, and screen-reader labels.
- Keep previous versions and deployment evidence when the service or law requires a history.

Use the repository's normal lint, typecheck, test, and build commands. Never commit, publish, or deploy unless the user requested that action.

### 9. Maintain A Legal-Page Register

Create or update a register in the project when the project has a suitable documentation location.

| Field | Example content |
|---|---|
| Page | Privacy notice or refund policy |
| Version and effective date | The exact version shown to users |
| Owner | Product or privacy owner |
| Jurisdictions | India, EU, UK, California, or other confirmed scope |
| Evidence date | Last code, vendor, and source verification |
| Trigger | New tracker, vendor, data field, market, product, or legal change |
| Controls tested | Consent, deletion, request, cancellation, refund, or other relevant test |
| Review due | Internal review date, not a claim that law permits delay |
| Approval | User or qualified counsel approval where required |

Re-open the review before or when adding a vendor, tracker, payment method, form field, account feature, subscription rule, AI use, upload feature, child audience, market, transfer, retention period, or marketing channel. Re-open it after a breach, vendor incident, regulator contact, product change, or legal change. Review the pages on a regular internal schedule even without a product change.

## Stop And Escalate

Stop drafting or publication and report the blocking facts when any of these remain unresolved.

- The operator or responsible privacy contact is unknown.
- The page would make a statement the evidence does not support.
- A current law, regulation, commencement date, or territorial rule is unclear.
- Children, health, financial, biometric, voice, precise-location, or other sensitive data is involved.
- The service uses AI, profiling, automated decisions, public user content, or model training.
- International transfers, public-sector use, regulated services, or complex vendor chains are involved.
- The terms contain broad waivers, arbitration, automatic renewal, indemnity, or liability limits.
- A security incident, complaint, demand, or regulator inquiry is active.

Return a short blocker list, the affected pages and controls, the evidence still needed, and the reason legal review is required. Do not hide the blocker inside a polished draft.

## Deliverable Shape

Return these sections in this order.

1. Scope and assumptions
2. Applicability and source status
3. Evidence ledger and unknowns
4. Page and control matrix
5. Draft or targeted changes
6. Implementation changes
7. Verification results
8. Maintenance register and next review triggers
9. Legal-review blockers

### Example

For an Indian clothing store with a contact form, checkout, unknown payment provider, and analytics, do not publish five copied pages. Verify the entity, vendors, data flows, payment path, shipping scope, refund process, and tracking behavior. Publish only pages supported by those facts, disable optional tracking until its consent behavior is correct where required, link refund terms before payment, and hold any unsupported international or GDPR claim for a separate applicability review.

## Required Source Register

Read `references/official-sources.md` when making a legal claim or selecting a regional branch. It contains the official sources checked for this skill and the facts they support. Re-fetch sources when the task depends on current status.
