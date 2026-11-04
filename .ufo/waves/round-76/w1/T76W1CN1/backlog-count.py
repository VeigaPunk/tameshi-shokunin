#!/usr/bin/env python3
"""Read-only citation baseline, not an adoption or claim judge."""
from pathlib import Path
import re

package = Path('/home/vgpnk/Projects/shokuknow/merge/tameshi')
lane = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
entries = sorted((package / 'knowledge/corpus/knowledge').glob('*.md'))
corpus = '\n'.join(p.read_text() for p in sorted((lane / 'corpus/knowledge').rglob('*.md')))
ids_by_target = {}
for row in (package / 'SOURCES.append.md').read_text().splitlines():
    match = re.match(r'\| (S\d+) \|', row)
    if match:
        used_by = row.rsplit('|', 2)[-2]
        for target in re.findall(r'corpus/knowledge/[\w.-]+\.md', used_by):
            ids_by_target.setdefault(target, set()).add(match.group(1))
present = path_hits = id_hits = either_hits = 0
for entry in entries:
    target = 'corpus/knowledge/' + entry.name
    present += (lane / target).is_file()
    path_hit = target in corpus
    id_hit = any(re.search(r'(?<![A-Za-z0-9])' + sid + r'(?![A-Za-z0-9])', corpus)
                 for sid in ids_by_target.get(target, ()))
    path_hits += path_hit
    id_hits += id_hit
    either_hits += path_hit or id_hit
print('BACKLOG_BASELINE entries=%d target_files_present=%d path_cited=%d package_id_cited=%d path_or_id_cited=%d no_path_or_id_citation=%d' %
      (len(entries), present, path_hits, id_hits, either_hits, len(entries) - either_hits))
