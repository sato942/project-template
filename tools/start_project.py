"""Turns a fresh copy of this template into a project, once, and then deletes itself.
Usage, from the new clone: python tools/start_project.py [--project NAME] [--owner NAME] [--timezone ZONE] [--repo OWNER/NAME]

Each option has a default: the folder's name, the GitHub owner and repository from the origin remote, and this machine's time zone.
It fills in the placeholders in every .md and .html file, replaces README.md with the project's own, turns on the pre-commit hook,
deletes this script and runs the project check. It commits nothing. What only the owner can say, such as what the product is and what
decisions are judged on, waits for the first session: STATE.md, "In flight"."""
import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TEMPLATE_NAME = 'project-template'
README = """# {{PROJECT}}

- **What it is:** [features/PRODUCT.md](features/PRODUCT.md)
- **Where it stands:** [STATE.md](STATE.md)
- **How to work on it:** [AGENTS.md](AGENTS.md), for people and coding agents alike
- **Everything about it on one page:** open [PROJECT_MAP.html](PROJECT_MAP.html) in a browser, from a local clone

After a new clone, turn on the check that runs before each commit:

```bash
git config core.hooksPath tools/hooks
```
"""
root = Path(__file__).resolve().parent.parent


def git(*args):
    try:
        done = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    except OSError:
        sys.exit('git was not found. Install git, then run this again.')
    return done.stdout.strip() if done.returncode == 0 else ''


origin = re.search(r'github\.com[:/]([^/\s]+)/([^/\s]+?)(?:\.git)?/?$', git('remote', 'get-url', 'origin'))
if origin and origin.group(2) == TEMPLATE_NAME:
    sys.exit(f'The origin remote is the template itself, so nothing was changed. Create the project with:\n'
             f'  gh repo create my-project --template {origin.group(1)}/{TEMPLATE_NAME} --private --clone\n'
             f'or, in a plain copy you mean to keep apart, run: git remote remove origin')

parser = argparse.ArgumentParser(description='Turn a fresh copy of this template into a project.')
parser.add_argument('--project', default=root.name, help="the project's name; default: this folder's name")
parser.add_argument('--owner', default=origin.group(1) if origin else git('config', 'user.name') or 'the owner', help='who decides; default: the GitHub owner')
parser.add_argument('--timezone', default=datetime.now().astimezone().tzname(), help="for all dates and times, such as Europe/Paris; default: this machine's")
parser.add_argument('--repo', default=f'{origin.group(1)}/{origin.group(2)}' if origin else 'not on GitHub yet', help='OWNER/NAME; default: from the origin remote')
args = parser.parse_args()
for name, value in vars(args).items():
    if not value or re.search(r'["\\<>&{}\r\n]', value):
        sys.exit(f'--{name} cannot be {value!r}: it goes into JSON and HTML, so it cannot be empty or hold " \\ < > & {{ }}. Nothing was changed.')

values = {'{{PROJECT}}': args.project, '{{OWNER}}': args.owner, '{{TIMEZONE}}': args.timezone, '{{REPO}}': args.repo,
          '{{NOW}}': f'{datetime.now().strftime("%d %b %Y, %H:%M")} {args.timezone}'}

with open(root / 'README.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write(README)
for path in sorted(p for p in root.rglob('*') if p.suffix in ('.md', '.html') and p.is_file() and '.git' not in p.relative_to(root).parts):
    with open(path, encoding='utf-8', newline='') as f:
        old = f.read()
    new = old
    for placeholder, value in values.items():
        new = new.replace(placeholder, value)
    if new != old:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(new)

if not (root / '.git').exists():
    git('init', '-b', 'main')
git('config', 'core.hooksPath', 'tools/hooks')
Path(__file__).unlink()

print(f'Project:    {args.project}\nOwner:      {args.owner}\nTime zone:  {args.timezone}\nRepository: {args.repo}')
print('The pre-commit hook is on and this script is gone. Nothing is committed. If a value above is wrong, change it where it appears.\n', flush=True)
check = subprocess.run([sys.executable, '-I', str(root / 'tools' / 'check_project.py'), str(root)])
print('\nNext: open this folder with your coding agent. It asks what the project is, then researches everything a project with that goal needs and builds the map from what it finds.')
sys.exit(check.returncode)
