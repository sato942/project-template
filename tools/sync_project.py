"""Writes the facts this project keeps in two places, each from its one home, so nobody types them twice.
Usage, from the clone: python -I tools/sync_project.py .        Then run tools/check_project.py, which still checks every one.

It writes three things, and prints each change:
1. STATE.md's progress row for each spec file: the version and the counts of requirements, open questions and validations, from the file.
2. Each spec file's Map parts header row: the parts whose items hold its IDs, from the map.
3. The status that ends the map's reference to each spec file, from that file's row in STATE.md.

It never decides anything: which part holds an ID, which IDs a decision applies to, a status, a next step and every updated time stay
with whoever makes the change. It adds no row and no reference; it names the ones that are missing."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # python -I ignores PYTHONIOENCODING

MAP = 'PROJECT_MAP.html'
SPEC_ID = r'[A-Z]{3,8}-(?:\d{3}|Q\d+|V\d+)'
paths = [a for a in sys.argv[1:] if not a.startswith('--')]
root = Path(paths[0] if paths else '.').resolve()
done, left = [], []


def id_kind(i):
    code, _, n = i.partition('-')
    return code, n[0] if n[0] in 'QV' else 'R', int(n.lstrip('QV'))


def ids_in(text, defined):
    # The spec IDs a text names; X-001 to X-009 names every ID of that kind defined between the two, as in the check.
    found = set(re.findall(r'\b(' + SPEC_ID + r')\b', text))
    for m in re.finditer(r'\b(' + SPEC_ID + r') to (?:([A-Z]{3,8})-)?(\d{3}|Q\d+|V\d+)\b', text):
        a = id_kind(m.group(1))
        b = id_kind(f'{m.group(2) or a[0]}-{m.group(3)}')
        if a[:2] == b[:2]:
            found |= {i for i in defined if id_kind(i)[:2] == a[:2] and a[2] <= id_kind(i)[2] <= b[2]}
    return found & set(defined)


def write(rel, old, new):
    if new != old:
        (root / rel).write_text(new, encoding='utf-8', newline='\n')


specs = {}  # file name -> (text, the IDs it defines)
for spec_file in sorted((root / 'specs').glob('*.spec.md')):
    text = spec_file.read_text(encoding='utf-8')
    specs[spec_file.name] = (text, re.findall(r'^- \*\*(' + SPEC_ID + r')\*\*', text, flags=re.M))
defined = [i for _, ids in specs.values() for i in ids]

# 1. STATE.md's progress rows, from the spec files.
state_path = root / 'STATE.md'
state = old_state = state_path.read_text(encoding='utf-8') if state_path.is_file() else ''
status_of = {}
for name, (text, ids) in specs.items():
    row = next((line for line in state.splitlines() if line.startswith(f'| [{name}]')), None)
    cells = row.split(' | ') if row else []
    if len(cells) < 6:
        left.append(f'STATE.md has no full progress row for {name}: add it, with its status and next step')
        continue
    count = lambda kind: str(sum(1 for i in ids if id_kind(i)[1] == kind))
    version = re.search(r'\*\*Version\*\* \| (\d+\.\d+)', text)
    new = list(cells)
    if version:
        new[1] = version.group(1) + cells[1][len(cells[1].split(',')[0]):]
    for n, kind in ((2, 'R'), (3, 'Q')):
        new[n] = re.sub(r'^\d+', count(kind), cells[n]) if re.match(r'\d', cells[n]) else ' '.join([count(kind) + ('.' if cells[n] else ''), cells[n]]).strip()
    for n, kind in ((4, 'V'), (5, 'R')):
        if re.search(r' of \d+', cells[n]):
            new[n] = re.sub(r' of \d+', f' of {count(kind)}', cells[n], count=1)
        else:
            left.append(f'the STATE.md row for {name} has no "n of {count(kind)}" in cell {n + 1}: write it')
    for what, a, b in zip(('', 'version and status', 'requirements', 'open questions', 'validations', 'implemented'), cells, new):
        if a != b:
            done.append(f'STATE.md, {name}, {what}: {a!r} is now {b!r}')
    state = state.replace(row, ' | '.join(new))
    status_of[name] = new[1].partition(', ')[2]
write('STATE.md', old_state, state)

# The map's data block. Its text is edited in place, so its layout stays as written.
page_path = root / MAP
page = old_page = page_path.read_text(encoding='utf-8') if page_path.is_file() else ''
block = re.search(r'<script type="application/json" id="project-map-data">(.*?)</script>', page, flags=re.S)
try:
    data = json.loads(block.group(1)) if block else {}
except ValueError as e:
    sys.exit(f'the data block in {MAP} is not valid JSON, so nothing more was written: {e}')
part_key = lambda p: [int(n) for n in re.findall(r'\d+', p)]
holders = {}  # code -> the parts whose items hold its IDs
for area in data.get('areas', []):
    for part in area.get('parts', []):
        for i in ids_in(' '.join(part.get('items', [])), defined):
            holders.setdefault(i.split('-')[0], set()).add(part['id'])

# 2. Each spec file's Map parts row, from the map.
rewritten = []
for name, (text, ids) in specs.items():
    codes = {i.split('-')[0] for i in ids}
    parts = sorted({p for c in codes for p in holders.get(c, ())}, key=part_key)
    cell = ', '.join(f'[{p}](../{MAP}#{p})' for p in parts) or 'None yet'
    head, sep, rest = text.partition('\n## ')
    row = re.search(r'^\| \*\*Map parts\*\* \| (.*) \|$', head, flags=re.M)
    if row and row.group(1) != cell:
        head = head[:row.start(1)] + cell + head[row.end(1):]
        done.append(f'{name}, Map parts: {row.group(1)!r} is now {cell!r}')
    elif not row:
        after = re.search(r'^\| \*\*Features\*\* \| .* \|$', head, flags=re.M) or re.search(r'^\| \*\*Code\*\* \| .* \|$', head, flags=re.M)
        if not after:
            left.append(f'{name} has no header table to put a Map parts row in: add the row by hand')
            continue
        head = head[:after.end()] + f'\n| **Map parts** | {cell} |' + head[after.end():]
        done.append(f'{name}, Map parts: added {cell!r}')
    if head + sep + rest != text:
        write(f'specs/{name}', text, head + sep + rest)
        rewritten.append(name)

# 3. The status that ends the map's reference to each spec file, from STATE.md.
for name, status in status_of.items():
    code = next(iter({i.split('-')[0] for i in specs[name][1]}), None)
    ref = data.get('refs', {}).get(code)
    if not ref:
        left.append(f"the map has no reference {code!r} to {name}: add it, with a title ending ', {status}'" if code else f'{name} defines no ID yet, so the map cannot refer to it by a code')
        continue
    title = ref.get('title', '')
    if title.endswith(', ' + status):
        continue
    wanted = (re.sub(r'( spec file).*$', r'\1', title) if ' spec file' in title else title.split(', ')[0]) + ', ' + status
    found = re.compile(r'("title":\s*)' + re.escape(json.dumps(title, ensure_ascii=False)))
    if len(found.findall(block.group(1))) != 1:
        left.append(f'the map reference {code!r} has the title {title!r}, which was not found once as written: end it with {", " + status!r} by hand')
        continue
    new_block = found.sub(lambda m: m.group(1) + json.dumps(wanted, ensure_ascii=False), block.group(1))
    page = page[:block.start(1)] + new_block + page[block.end(1):]
    block = re.search(r'<script type="application/json" id="project-map-data">(.*?)</script>', page, flags=re.S)
    done.append(f'{MAP}, reference {code!r}: {title!r} is now {wanted!r}')
write(MAP, old_page, page)

print('\n'.join(done) if done else 'nothing to write: every copied fact already matches its home')
if state != old_state or page != old_page:
    print('set the updated time in ' + ' and '.join(f for f, changed in (('STATE.md', state != old_state), (MAP, page != old_page)) if changed))
if rewritten:
    print('bump the version and add a change-log line in ' + ' and '.join(rewritten) + ', then run this again')
if left:
    print('left for you:\n' + '\n'.join('  ' + line for line in left))
