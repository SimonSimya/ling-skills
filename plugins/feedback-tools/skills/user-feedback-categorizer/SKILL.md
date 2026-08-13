---
name: user-feedback-categorizer
description: >-
  Take a batch of raw user feedback (app-store reviews, survey responses, support messages, churn
  reasons, interview notes) and turn it into a frequency-weighted, prioritized list of themes you
  can act on. Use whenever you paste user feedback and want it clustered, counted, and prioritized,
  however you phrase it: "categorize this", "group these by theme", "what are users complaining
  about most", "rank by how often it's mentioned", "what should we fix first" — even across several
  messages. Output is a ranked theme table tied to product priorities, NOT a raw restatement. Do NOT
  use for analytics/metrics questions (that's product/data work) or for drafting replies to
  individual users.
---

# User Feedback Categorizer

Feedback arrives as an undifferentiated pile and the job is always the same: turn it into a
prioritized signal. This skill encodes the shape so the output is consistent and decision-ready.

## 1. Load context first

Read these from your own workspace if they exist. Skip any that don't; the skill still works, it
just can't map themes to segments.

- `00-brain/customers.md` — ICP, segments, known pains and objections. Map themes to these where possible.
- `00-brain/current-state.md` — active product priorities and the North Star, so prioritization ties to what the company is actually steering toward.
- `00-brain/business-profile.md` — product surfaces (App / Web / Live) so feedback is attributed to the right area.
- `00-brain/brand-voice.md` — the register to write the summary in.

## 2. Handle staged input

Feedback often arrives in chunks ("I'll give it to you in sections, I'll tell you when I'm done").
**Wait for the full dump before categorizing.** Acknowledge briefly, collect, and produce the
analysis only once the sender signals they're finished. If they paste once and ask immediately,
proceed.

## 3. Categorize

1. **Cluster** every item into themes. Derive themes from the data; don't force a fixed taxonomy. Typical Ling clusters: content quality/errors, course progression/difficulty, pricing/paywall, bugs/crashes, missing languages, UX/navigation, audio/voice, gamification/streaks, support responsiveness.
2. **Count** mentions per theme. An item can hit more than one theme; note when it does.
3. **Weight by importance**, not just raw count. Factor in frequency, severity (does it block learning, cause churn, hit paying users), and which segment it comes from (a paying heritage-learner complaint outweighs a free-tier nice-to-have).
4. **Capture verbatim signal.** Keep one or two short representative quotes per top theme; they carry more than a paraphrase.

## 4. Output

A ranked table, highest-priority first:

| # | Theme | Mentions | Severity | Segment skew | Representative quote | Suggested owner |
|---|-------|----------|----------|--------------|----------------------|-----------------|

Then below it:

- **Top 3 to act on** — one line each on the *why* (frequency x severity x segment), tied to a product priority or the North Star where relevant.
- **Watch list** — low-frequency but high-severity items not yet worth committing to.
- **Noise** — anything safe to discount, briefly, so the reader sees you considered it.

Keep it tight and decision-ready. Match your own voice: direct, no fluff, give the counter-case if
the data is ambiguous.

## 5. Definition of done (run these before you ship the table)

State the result of all three. A skill without a definition of done keeps grinding and burning
tokens.

1. **Coverage:** every input item lands in at least one theme. Report `N items in / N classified`. If they don't match, say which items you couldn't place and why.
2. **Reconciliation:** the sum of per-theme mention counts is at least the item count. Flag every item counted under more than one theme.
3. **Stability:** the top 3 themes should not change if you rerun on the same batch. If you are not confident they'd hold, say so rather than presenting a fragile ranking as settled.

## 6. Offer the next step

After the table, **offer, don't auto-do**: route the top themes to the right owner, or draft the
message. Sending is a human decision.

## About

Adapted for the Ling skills marketplace from Simon's WorkOS pilot. **Privilege level: read-only.**
It reads what you paste plus your own brain files, and writes nothing.
