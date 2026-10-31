# Feature matrix

Every feature on every target. Update this file in the same change as any work that adds, changes or removes a feature on a target ([developer guide](AGENTS.md#working-rules), working rule 9).

## Marks

| Mark | Meaning |
|---|---|
| — | Not started |
| P | Prototype only; not accepted |
| ✓ | Done: the feature's validations pass on this target, with recorded evidence |
| ✗ | Not possible on this target; the note says why |
| n/a | The feature has no part on this target, once its design settles that |

- A cell becomes ✓ only when the validations in the feature's spec files that apply to that target pass, with recorded evidence.
- Reaching a service on another target is access, not parity: it never makes a cell ✓.
- Every mark other than "—" links its evidence or note.
- A new feature gets a row in the change that records it, starting with its ID as a link: `| [F001](features/F001-short-name.md) The feature's name | — |`

## Targets

_Not set yet: the owner names them in the first session._ A target is anywhere the project has to work, such as a browser, a phone system or a server. A project with one target keeps one column. Rename the column below and add one for each further target.

## Features

| Feature | Target 1 |
|---|---|
