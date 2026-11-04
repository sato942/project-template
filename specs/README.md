# Spec files

How spec files are named, written and changed, and the index of all of them. This file ranks with [AGENTS.md](../AGENTS.md) ([Authority](../AGENTS.md#authority) item 2).

Every feature is specified in its own spec file, in enough detail to build it without guessing. Copy [TEMPLATE.md](TEMPLATE.md) for a new one.

**Naming and place.**

1. Spec files live in this folder, each named `<feature>.spec.md`: the feature's short name in lowercase words joined by hyphens, as the owner would say it. The file name carries no F-number; the header lists the features it covers.
2. One spec file covers one feature. A broad feature can need several.
3. Each spec file has a code, one whole word that no other spec file uses, by the [code standard](#code-standard), such as `LOGIN`. Its requirements are `CODE-NNN`, its open questions `CODE-Qn` and its validations `CODE-Vn`. Each is defined once, as a list item that starts with the ID in bold (`- **LOGIN-001**`). IDs are numbered in the order written and never renumbered or reused; a withdrawn requirement keeps its ID, marked withdrawn with the date and the reason.
4. **Map it.** In the change that creates a spec file, add its row to the [spec file table](#spec-file-table): path, features, code, scope and when to read it. That table is the only index of spec files.

**Generating one.**

1. **Gather the sources:** the owner's words; the feature notes; any source the owner adopted; the dated owner decisions; the architecture invariants; and the other spec files it touches. Pin each source's identity (revision, hash, version or date), check that it is still current, and log the check in the matching research log.
2. **"1 to 1" means nothing is lost.** When the owner asks for a source to be extracted 1 to 1, every part of it maps to a requirement or an evidence note: every rule, number, format, algorithm and example. A traceability table shows each part as Adopted, Changed (naming the decision), Dropped (giving the reason) or Evidence.
3. **Apply every owner decision** that changes the source, in a "Decisions applied" table with its date and the requirements it affects.
4. **Restate in our own words.** Copy no prose, prompt or code from a source unless its license allows it. Record the license in [LEGAL_FLAGS.md](../LEGAL_FLAGS.md).
5. **Label each requirement:**
   - **Source:** from the adopted source, unchanged;
   - **Decided:** from an owner decision;
   - **Invariant:** required by an architecture invariant;
   - **Recorded:** a requirement of another spec file, restated;
   - **Proposed:** our design where the source is silent or unclear, the default for prototypes and binding only once the owner agrees;
   - **Open:** waiting for the owner or a measurement.

   Keep evidence apart from requirements: a source's claims and numbers are never this project's measurements.
6. **Flag** inconsistencies inside a source and conflicts with other documents as Open. Never resolve them silently.
7. **Open questions** say what settles each, and each has a row in the map's decisions. None is put to the owner before the research that [Decisions rest on research](../AGENTS.md#decisions-rest-on-research) requires.

**How detailed.** Detailed enough that two developers who never talk would build the same thing. A builder meets no design choice the file leaves unsaid, because each is a requirement or an open question; a choice that shows one path names what it rejected, or points to the study that does; and a build order leaves something that runs at the end of each phase. Every spec file has these parts, in this order:

1. a header table: path, code, features, map parts, version, spec status (Draft until the owner reviews it, then Agreed, or Superseded) and implementation status;
2. scope, in and out, naming who owns the rest;
3. sources, labels and units;
4. the decisions applied;
5. terms;
6. requirements by component, with:
   - every data format field by field: type, unit, encoding and range;
   - every algorithm as pseudo-code, with a worked example;
   - every number with its unit and its source;
   - every interface with its inputs, outputs and errors;
   - ordering, concurrency, failure, restart and recovery;
7. secrets, authority and effects, tied to the architecture invariants;
8. what is measured and the settings that measurement may change;
9. conformance and traceability tables;
10. open questions;
11. validations, `UNEXECUTED` until run, each naming the requirements it checks;
12. a change log with dates and times, as the file's last lines.

Leave out a part that truly does not apply, and scale the detail to the feature: a small feature gets a short spec file. A validation demonstrates the real thing ([How work gets done](../AGENTS.md#how-work-gets-done)); it does not ask for a test suite, and a spec file sets no test count or coverage target.

**Authority.** A spec file is authoritative for its scope ([Authority](../AGENTS.md#authority) item 4). Where it disagrees with the owner's words or a feature note's owner intent, the spec file is wrong: check the source and correct the spec file in the same change.

**Feature notes.** Feature notes hold the owner's words and the evidence found at intake, with a link to the spec file. Spec files hold the design, the validations and what each decision means ([What a feature note holds](../features/README.md#what-a-feature-note-holds)). An owner decision has its words in the feature note, its meaning in the affected spec file's "Decisions applied" table and requirements, and a line that links to it in the map's decisions and in [STATE.md](../STATE.md).

**When a spec file is written.** When the owner asks for it, and in any case before implementation of that feature starts. Until then, it has no row in STATE.md's progress table.

**Changing one.** In the same change:

- bump its version and add a change-log line;
- update its row in STATE.md's progress table;
- update [FEATURE_MATRIX.md](../FEATURE_MATRIX.md) if a feature changes on a target;
- update its parts' `items` and its decisions in [PROJECT_MAP.html](../PROJECT_MAP.html), so the two stay in [parity](#map-and-spec-parity) (working rule 11);
- run the project check (`python -I tools/check_project.py .`), which also checks the spec IDs, this table and the parity below.

## Map and spec parity

The map and the spec files say the same things, in both directions, with no extra or missing information between them:

1. **Parts.** Every spec ID, requirement, open question or validation, sits in the `items` of at least one map part, and every ID a part names exists. A part refers to a spec file, by the file's code in its `refs`, exactly when its `items` hold that file's IDs, and the spec file's **Map parts** header row lists exactly those parts, as links such as `[A3.2](../PROJECT_MAP.html#A3.2)`. `X-001 to X-009`, or `X-V1 to X-V4`, names every ID of that kind the file defines between the two.
2. **Decisions.** Each row of a spec file's decisions table starts with the ID of a map decision whose `specs` names that file. Its last cell lists the IDs of the file it applies to, or says `Whole file`, which is an empty list in the map; the row and the decision name the same IDs. Each Decided map decision that names a spec file has a row in that file's table, and a decision's `parts` include every part that holds an ID it names.
3. **Questions.** Each open question has a map decision, its own or the one that settled it, with the same status.
4. **Words.** A part's note and a decision's title say nothing the spec files they name do not, and their numbers and dates match. A note names a spec ID only if its part holds it. The owner's words and a study's evidence may also be quoted there, with links.
5. **Status.** A spec file's reference in the map has a title ending in the status its row in [STATE.md](../STATE.md) gives it, such as `, Draft`.

The [project check](../tools/check_project.py) fails when rule 1, 2 or 5 breaks, or a question has no decision. The words of rule 4, and whether a question's status matches, still need a person.

Only the map holds parts and decisions on features with no spec file yet, the ideas bank and its own history. Requirement text stays in the spec files, one home for each fact; the map names IDs and links to them. A change to either side changes the other in the same change.

## Code standard

A spec file's **code** is the word that starts every ID in it, as `LOGIN` does in `LOGIN-011`. The [map](../PROJECT_MAP.html#codes) shows every code.

A code is:

1. one English word, singular, in capitals, of 3 to 8 letters;
2. taken from the spec file's name or title, so a reader can tell which file it is without a key;
3. never an abbreviation, an acronym or a blend;
4. used by no other spec file;
5. fixed once the spec file exists.

**Other kinds of ID.** These are not spec file codes, and they keep their forms.

| Kind | Form | Where it is defined |
|---|---|---|
| Feature | `F012` | [features/](../features/README.md) |
| Decision | `BUILD-START`, or a question's own ID such as `LOGIN-Q2` | The map's decisions; a spec file's decisions table names each by this ID |
| Map part and map source | `A3.13`, `S12` | [The map](../PROJECT_MAP.html) |
| Study finding | `E9`, `B6`, `N2` | Its study; always cited with the study |

## Spec file table

| Spec file | Features | Code | Scope | Read when |
|---|---|---|---|---|
