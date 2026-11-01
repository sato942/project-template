# Project template

A starting point for a new software project worked on with coding agents. It gives the project one place for the rules, the live state, the owner's intent, the evidence behind each decision, a specification per feature and an interactive map of everything the project needs.

It is plain Markdown, one offline HTML page and two small Python scripts, with no dependencies. It suits any language or stack, and you add your code next to it.

## Start a project

You need git and Python 3.9 or newer. With the [GitHub CLI](https://cli.github.com/):

```bash
gh repo create my-project --template sato942/project-template --private --clone
```

```bash
cd my-project
```

```bash
python tools/start_project.py
```

Or choose **Use this template** on GitHub and clone the result. Either way, then open the folder with your coding agent. `AGENTS.md` and `STATE.md` tell it what to do first:

1. Ask you what the project is and what decisions should be judged on.
2. Run the [anatomy study](studies/ANATOMY.md): extensive research into everything a project with that goal needs.
3. Build the map from what it found, and go through it with you.

The map starts empty on purpose. Its areas and parts come from that research and use the field's own words, so every project gets a map that fits it.

**What the script does, once:** it fills in the project's name, owner, time zone and repository everywhere, replaces this README with the project's own, turns on the check that runs before each commit, deletes itself and runs that check. It commits nothing. It takes its values from the repository and the machine; run `python tools/start_project.py --help` to set them yourself. It refuses to run while `origin` still points at this template.

## What is inside

| File | What it is |
|---|---|
| [AGENTS.md](AGENTS.md) | How agents work here, always in context: the rules and a map of every other file |
| [STATE.md](STATE.md) | Where the project stands now, what is in flight and what waits for the owner |
| [PROJECT_MAP.html](PROJECT_MAP.html) | The interface to all of it: every part the project needs and how far each is covered, every decision, the stages of work and an ideas bank. Open it in a browser from a local clone. It works offline and decides nothing |
| [features/](features/README.md) | The owner's intent, in their own words, one note per feature, with [PRODUCT.md](features/PRODUCT.md) for the whole product |
| [studies/](studies/README.md) | Dated research: the [anatomy study](studies/ANATOMY.md) that sets the map, then the options compared before each decision, with every query and URL in a research log |
| [specs/](specs/README.md) | The specification, one file per feature, with requirement IDs and `UNEXECUTED` validations |
| [FEATURE_MATRIX.md](FEATURE_MATRIX.md) | Every feature's status on every target |
| [LEGAL_FLAGS.md](LEGAL_FLAGS.md) | License and terms flags, for a legal review before release |
| [tools/check_project.py](tools/check_project.py) | One command that finds stale or unmapped files. The [pre-commit hook](tools/hooks/pre-commit) runs it |

## How work moves

A project starts with its anatomy study. Then each feature moves through Idea → Research → Spec → Decide → Build → Demonstrate → Measure → Deliver. Any stage can send work back to an earlier one, for a reason: the stages are an order, not gates. Decisions go to the owner only after research, as a multiple choice question with exactly one recommended option. Building needs the owner's instruction.

Building itself follows **build → demonstrate → deliver**:

- **Build** the requested behavior first, in small changes that are easy to undo.
- **Demonstrate** it through its real entry point, and report honestly what happened.
- **Deliver** it, with a short report of what changed, what was not done and any known problems.

## What it leaves out on purpose

- **No test-driven development.** Automated tests are added only where they give clear value, with no test count or coverage target.
- **No gate systems, readiness scores or expanding checklists.** Completed work stays completed unless new evidence contradicts it.
- **No endless repair loops.** After two failed attempts at the same problem, an agent stops, explains the blocker and looks for a simpler path.
- **No CI.** The project check tests facts in files and never whether work is finished, and it reads no code. Add CI when a project needs it.

## Changing the template

This folder is itself a template: while `tools/start_project.py` exists, the check allows the placeholders. Run `python -I tools/check_project.py .` after a change. New projects copy the template as it is then, and existing projects do not change.
