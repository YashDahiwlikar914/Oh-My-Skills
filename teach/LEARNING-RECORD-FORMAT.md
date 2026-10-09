# Learning Record Format

Learning records live in `./Learning-Records/` and use sequential numbering, such as `1-Slug.md` and `2-Slug.md`. Create the directory when you write the first record, not before.

They are the teaching equivalent of ADRs. They capture non-obvious lessons, key insights, and stated prior knowledge that steer future sessions. Use them to calculate the zone of proximal development.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences on what was learned, or what prior knowledge was established, and why it matters for future sessions.}
```

That is the whole format. A learning record can be a single paragraph. Its value lies in recording _that_ something is now known and _why_ that changes what to teach next. Filling out sections adds nothing.

## Optional Sections

Include these only when they add real value. Most records won't need them.

- **Status** frontmatter (`active | superseded by LR-NNNN`) helps when an earlier understanding turns out wrong and a later record replaces it.
- **Evidence** records how the user demonstrated the understanding, such as a question answered, an exercise completed, or prior experience cited. It helps when you might revisit the claim.
- **Implications** records what the learning unlocks or rules out for future sessions. Add it when the effect isn't obvious.

## Numbering

Scan `./Learning-Records/` for the highest existing number and add one.

## When to Write a Learning Record

Write one when any of these is true.

1. **The user demonstrated real understanding of something non-trivial.** Exposure isn't enough. They must show they can use the concept correctly. This sets a new floor for what to teach next.
2. **The user disclosed prior knowledge.** They said "I already know X." Record it so future sessions don't re-teach it. Record the _depth_ they claimed too.
3. **You corrected a misconception.** The user believed something wrong and now sees why. These records carry high value because they predict stumbling blocks on related topics.
4. **The mission shifted in response to learning.** The user found they cared about something different than they thought. Cross-link to [[MISSION.md]] and update it.

### What Does _Not_ Qualify

- Material you merely covered. Coverage isn't learning, so wait for evidence.
- Anything [[GLOSSARY.md]] already captures tersely as a term definition. Don't duplicate it.
- Session-by-session activity logs. Learning records aren't a journal. They hold decision-grade insights.

## Supersession

When a later record contradicts an earlier one because the user's understanding deepened or changed, mark the old record `Status: superseded by LR-NNNN` and keep it. The history of how understanding evolved is useful signal.
