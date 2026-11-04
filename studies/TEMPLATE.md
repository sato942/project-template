# The topic: the question it answers

Copy this file into `studies/<date>/`, link from there as `../../AGENTS.md`, and delete these lines and any part that does not apply. A study of an outside source (an article, a product, a repository) keeps the claims section; a study of an open question keeps the options and the comparison.

**Research:** the date, from the time to the time ({{TIMEZONE}}). **Question:** the owner's, at the time: "their words". **Source:** for a study of an outside source, what it is, who wrote it and when. **Outcome:**
- what was read, and where;
- the sources and ideas it adds to the map (S-numbers, IDEA-numbers);
- its edge cases, questions and claims tests.

**Method:** read-only, calls 1 to N in the folder's `RESEARCH_LOG.md`. **Status:** research only. Nothing is installed, no account is opened, and every test is `UNEXECUTED`. Results in papers and vendor pages are evidence about their authors' tasks, never this project's measurements.

## The owner's answer

Added once the owner answers: the date and time, their words, and what changed where (spec IDs, map decisions). Say so when the answer goes against the recommendation.

## In plain words

What the source or the question is, in plain words, with each term the findings need. Then what it means for this project, as a short numbered list, and the questions put to the owner.

## 1. Earlier answers checked

Each question this raises, checked against the feature notes, STATE.md and recent studies before it is asked (AGENTS.md, Decisions rest on research, step 6). New evidence on a question already answered is banked for its measurement, not asked again.

| Question this raises | Earlier answer | What this study does |
|---|---|---|

## 2. What is in use today

What exists now, and why the question came up.

## 3. The options

Every approach that exists for the question, not only the first one that works.

- **A. An option.** What it is, in plain words, and what it would cost.
- **B. Another option.**

## 4. Evidence by field

One part for each field the question lands in (step 1), such as UX design, security engineering or databases, and one for projects like this one. Measured results on comparable tasks come first, then vendors' tests, then vendors' claims, then articles (a signal, labelled as such), then our own reasoning.

| Source | Field | Kind | What it found | How comparable |
|---|---|---|---|---|

**What was not found:** the measurement nobody has made, named as `UNEXECUTED`. "Nothing found" holds only after both a search for studies and a search for articles.

## 5. The claims and our test of each

For a product or a source nobody has tested: each claim, what we found about it, and the test that would check it (listed under [Tests this leaves UNEXECUTED](#tests-this-leaves-unexecuted)).

| # | Claim | Kind | What we found | Test |
|---|---|---|---|---|

## 6. Comparison

One row for each of the project's main values (AGENTS.md, Values), at equal quality.

| | A | B |
|---|---|---|

## 7. Edge cases to carry

Each case the spec files do not yet cover, the spec file it belongs in, and the requirement it would become, as Proposed. None is written into a spec file before the owner answers.

## 8. Decisions this touches, flagged and not reopened

Each decision already taken that this evidence touches: whether it stands, and whether it now rests on less evidence than before (step 7 of that rule). None is reopened here.

## 9. Candid judgment

The recommended option and why. What it gives up, what would change the answer, and the likely time sinks. Say plainly what is not worth the owner's time.

## 10. Question for the owner

Multiple choice, asked as a question the owner picks from: the options with the evidence and the gaps for each, how deep the research went, and exactly one recommended.

## How deep the research went

- **Areas searched:** each field from section 4.
- **Sources:** the number recorded, from how many calls; the articles among them.
  - **Read whole at the source:**
  - **Read as a model's summary of the whole page:**
  - **Read as abstract or search excerpt only:**
  - **Title only:**
- **Stopped when:** further sources stopped changing which option leads.

## Banked ideas

For a study of an outside source: the IDEA-numbers added to the map's ideas bank, counted by next step.

## Tests this leaves UNEXECUTED

Each needs the owner's go-ahead (working rule 1). No key reaches the agent.

| Test | Claim | What it does | What it needs (access, terms, cost) |
|---|---|---|---|

## Not reached

Pages, sources and searches not reached, and why.

---

The folder's `RESEARCH_LOG.md` has one numbered line per call:

```text
# Research log, the date

Times are the project's time zone. Tools used. What was read as data and not run.

1. The time. The tool. The query or URL. What it was used for, or that it could not be reached.
```
