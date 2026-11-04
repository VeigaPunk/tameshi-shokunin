#!/usr/bin/env python3
"""ledger-census.py — read-only structural census of the round-21 cold-read ledger.

Seat T72W1S02, tameshi round 72. Reads the ledger two ways:

  * base   — the blob at the plan's frozen base revision (default f20ba48…),
             i.e. the ledger the round-72 plan's forecast was frozen against;
  * live   — the working-tree ledger at census time (sha recorded), because the
             round's own rekey rewrites this file while the wave runs.

It never writes the lane: only the JSON named by --out (the seat directory).
Read-only git calls: rev-parse, show, ls-tree, cat-file -e, show -s.

Usage (from the lane root):
  python3 -I -X utf8 .ufo/waves/round-72/w1/T72W1S02/ledger-census.py \
      --out .ufo/waves/round-72/w1/T72W1S02/ledger-census.json
"""

import argparse
import hashlib
import importlib.util
import json
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = 'f20ba482c7441d4c75818e7cd8a3165fee7821a1'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SKILL = 'SKILL.md'
FROZEN = '.ufo/evidence/round-18/measure.py'
IGNORED = frozenset((SKILL, '.ufo/evidence/round-17/coldread/ledger.json', LEDGER))
SPECIFIC = (
    'corpus/SOURCES.md',
    'PROVINCE.md',
    'corpus/QUALITY.md',
    'README.md',
    'SCORECARD.md',
    'LOG.md',
    'tools/pointer-recheck.json',
    'tools/mutate-and-run.sh',
)


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args],
                          capture_output=True, check=True).stdout


def git_text(repo, *args):
    return git(repo, *args).decode('utf-8', 'surrogateescape')


def load_sectionize(repo):
    spec = importlib.util.spec_from_file_location('tameshi_r18_census', repo / FROZEN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sectionize


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def blob_shas(repo, rev, paths):
    """sha256 of every path's blob at rev, in one batched git call.

    Returns ({path: sha256}, [missing paths]). Output order follows input order.
    """
    if not paths:
        return {}, []
    payload = ''.join('%s:%s\n' % (rev, p) for p in paths).encode(
        'utf-8', 'surrogateescape')
    res = subprocess.run(['git', '-C', str(repo), 'cat-file', '--batch'],
                         input=payload, capture_output=True, check=True)
    buf = res.stdout
    pos = 0
    shas, missing = {}, []
    for path in paths:
        nl = buf.index(b'\n', pos)
        header = buf[pos:nl].decode('utf-8', 'surrogateescape')
        pos = nl + 1
        parts = header.split()
        if len(parts) == 2 and parts[1] == 'missing':
            missing.append(path)
            continue
        size = int(parts[2])
        shas[path] = sha256(buf[pos:pos + size])
        pos += size + 1
    return shas, missing


def canonical_lane_path(path):
    if not isinstance(path, str) or not path or path.startswith('/'):
        return False
    return not any(part in ('', '.', '..', '.git') for part in path.split('/'))


def heading_stats(counts):
    values = sorted(counts.values())
    lo, hi = values[0], values[-1]
    med = statistics.median(values)
    return {
        'min': lo,
        'median': med,
        'max': hi,
        'argmin': sorted(h for h, n in counts.items() if n == lo)[:8],
        'argmax': sorted(h for h, n in counts.items() if n == hi)[:8],
        'distinct': len(values),
        'histogram': dict(sorted(Counter(values).items())),
    }


def census(label, ledger_bytes, sections, base_tree, commit_time, repo, pin_rev):
    ledger = json.loads(ledger_bytes.decode('utf-8', 'surrogateescape'))
    entries = ledger['entries']
    by_heading = defaultdict(list)
    for i, entry in enumerate(entries):
        by_heading[entry.get('heading')].append(i)
    newest = {h: idxs[-1] for h, idxs in by_heading.items()}
    by_sha = defaultdict(list)
    for i, entry in enumerate(entries):
        if isinstance(entry.get('sha256'), str):
            by_sha[entry['sha256']].append(i)

    def view(entry):
        raw = entry.get('inputs')
        if not isinstance(raw, dict):
            return {}
        return {p: v for p, v in raw.items() if p not in IGNORED}

    section_headings = {sec['heading'] for sec in sections}
    rows = []
    missing_inputs = []
    membership = Counter()
    raw_membership = Counter()
    ignored_membership = Counter()
    for sec in sections:
        heading = sec['heading']
        idx = newest.get(heading)
        row = {
            'heading': heading,
            'start': sec['start'],
            'end': sec['end'],
            'newest_index': idx,
        }
        if idx is None:
            row.update({'has_newest': False, 'inputs': 0, 'inputs_view': 0})
            rows.append(row)
            continue
        entry = entries[idx]
        pins = view(entry)
        group = [i for i in by_sha.get(sec['sha256'], []) if i != idx]
        uncovered = set()
        for j in group:
            uncovered |= set(view(entries[j])) - set(pins)
        row.update({
            'has_newest': True,
            'section_sha256': sec['sha256'],
            'inputs': len(entry.get('inputs') or {}),
            'inputs_view': len(pins),
            'external_inputs': len(entry.get('external_inputs') or {}),
            'class': entry.get('class'),
            'verdict': entry.get('verdict'),
            'read_rev': entry.get('read_rev'),
            'rekey_batch': entry.get('rekey_batch'),
            'entry_span': [entry.get('start'), entry.get('end')],
            'span_matches_section': [entry.get('start'), entry.get('end')]
                                    == [sec['start'], sec['end']],
            'sha_matches_section': entry.get('sha256') == sec['sha256'],
            'same_sha_entries': len(group) + 1,
            'older_same_sha_uncovered_paths': len(uncovered),
            'older_same_sha_uncovered_sample': sorted(uncovered)[:5],
            'zero_inputs_view': not pins,
        })
        missing = sorted(p for p in (entry.get('inputs') or {})
                         if not path_exists(base_tree, p))
        row['missing_input_paths'] = missing
        for path in missing:
            missing_inputs.append({'heading': heading, 'newest_index': idx, 'path': path})
        for path in pins:
            membership[path] += 1
        for path in (entry.get('inputs') or {}):
            raw_membership[path] += 1
            if path in IGNORED:
                ignored_membership[path] += 1
        rows.append(row)

    pin_paths = sorted({p for entry in entries for p in view(entry)})
    shas, pin_missing = blob_shas(repo, pin_rev, pin_paths)
    missing_set = set(pin_missing)
    verifies = [all(shas.get(p) == v for p, v in view(entry).items())
                for entry in entries]
    for row in rows:
        if not row.get('has_newest'):
            continue
        idx = row['newest_index']
        pins = view(entries[idx])
        stale = sorted(p for p in pins if shas.get(p) != pins[p])
        row['newest_stale_pins'] = len(stale)
        row['newest_stale_pin_sample'] = stale[:5]
        row['newest_verifies_at_pin_rev'] = not stale and not any(
            p in missing_set for p in pins)
        group = by_sha.get(row['section_sha256'], [])
        row['same_sha_verifying_entries'] = sum(
            1 for j in group if verifies[j])
        row['older_verifying_entries'] = sum(
            1 for j in group if j != idx and verifies[j])

    forecast_shadow = {}
    for path in SPECIFIC:
        pinned = [row['newest_index'] for row in rows
                  if row.get('has_newest') and path in view(entries[row['newest_index']])]
        shadows = []
        for row in rows:
            if not row.get('has_newest'):
                continue
            idx = row['newest_index']
            if path not in view(entries[idx]):
                continue
            for j in by_sha.get(row['section_sha256'], []):
                if j == idx or not verifies[j]:
                    continue
                if path not in view(entries[j]):
                    shadows.append({'heading': row['heading'],
                                    'newest_index': idx,
                                    'older_entry_index': j,
                                    'older_inputs_view': len(view(entries[j]))})
        forecast_shadow[path] = {
            'newest_pinned_sections': len(pinned),
            'older_verifying_entries_omitting_path': len(shadows),
            'shadows': shadows[:10],
        }

    missing_refs = {}
    for i, entry in enumerate(entries):
        for path in view(entry):
            if path in missing_set:
                missing_refs.setdefault(path, []).append(i)

    rehearsal = {}
    arms = {
        'reh-sources-only.out': ['corpus/SOURCES.md'],
        'reh-province-only.out': ['PROVINCE.md'],
        'reh-quality-only.out': ['corpus/QUALITY.md'],
        'reh-scorecard-only.out': ['SCORECARD.md'],
        'reh-province-sources.out': ['PROVINCE.md', 'corpus/SOURCES.md'],
    }
    reh_dir = repo / '.ufo/evidence/round-72/reh'
    for name, planned in arms.items():
        receipt = reh_dir / name
        if not receipt.exists():
            continue
        lost, summary = set(), None
        for line in receipt.read_text(encoding='utf-8', errors='surrogateescape').splitlines():
            if line.startswith('COLDREAD_PRECHECK'):
                summary = line
            elif line.startswith('LOST '):
                lost.add(line[5:].split(' | ', 1)[0])
        predicted = {row['heading'] for row in rows if row.get('has_newest')
                     and any(p in view(entries[row['newest_index']])
                             for p in planned)}
        rehearsal[name] = {
            'planned': planned,
            'guard_summary': summary,
            'guard_lost': len(lost),
            'predicted_lost': len(predicted),
            'set_equal': predicted == lost,
            'sym_diff': sorted(predicted ^ lost),
        }

    orphans = []
    for heading, idxs in sorted(by_heading.items(), key=lambda kv: kv[1][-1]):
        if heading in section_headings:
            continue
        idx = idxs[-1]
        entry = entries[idx]
        orphans.append({
            'heading': heading,
            'entries': len(idxs),
            'newest_index': idx,
            'newest_inputs': len(entry.get('inputs') or {}),
            'newest_entry_span': [entry.get('start'), entry.get('end')],
            'newest_read_rev': entry.get('read_rev'),
            'spans': sorted({(entries[i].get('start'), entries[i].get('end'))
                             for i in idxs}),
        })

    inversions = []
    for heading, idxs in by_heading.items():
        if len(idxs) < 2:
            continue
        times = [commit_time.get(entries[i].get('read_rev')) for i in idxs]
        if any(t is None for t in times):
            continue
        pairs = [(a, b) for a in range(len(idxs)) for b in range(a + 1, len(idxs))
                 if times[a] > times[b]]
        max_time = max(times)
        freshest_positions = [k for k, t in enumerate(times) if t == max_time]
        if pairs or (len(idxs) - 1) not in freshest_positions:
            inversions.append({
                'heading': heading,
                'entries': len(idxs),
                'append_inversion_pairs': len(pairs),
                'worst_example': ([idxs[pairs[0][0]], idxs[pairs[0][1]]]
                                  if pairs else None),
                'newest_index': idxs[-1],
                'newest_read_rev': entries[idxs[-1]].get('read_rev'),
                'freshest_index': idxs[freshest_positions[-1]],
                'freshest_read_rev': entries[idxs[freshest_positions[-1]]].get('read_rev'),
                'tie_not_inversion': not pairs,
            })

    batch_index = defaultdict(list)
    for i, entry in enumerate(entries):
        if entry.get('rekey_batch'):
            batch_index[entry['rekey_batch']].append(i)
    batches = []
    for name, idxs in sorted(batch_index.items(), key=lambda kv: kv[1][0]):
        batches.append({
            'batch': name,
            'entries': len(idxs),
            'first_index': idxs[0],
            'last_index': idxs[-1],
            'contiguous': idxs[-1] - idxs[0] + 1 == len(idxs),
            'read_revs': sorted({entries[i].get('read_rev') for i in idxs}),
            'rekey_rounds': sorted({entries[i].get('rekey_round') for i in idxs}),
            'input_counts': {
                'min': min(len(entries[i].get('inputs') or {}) for i in idxs),
                'max': max(len(entries[i].get('inputs') or {}) for i in idxs),
            },
        })

    specific = {}
    for path in SPECIFIC:
        specific[path] = {
            'membership': membership.get(path, 0),
            'raw_membership': raw_membership.get(path, 0),
            'exists_at_base': path_exists(base_tree, path),
        }
    pin_sets = [set(view(entries[row['newest_index']]))
                for row in rows if row.get('has_newest')]
    overlap = {}
    for a in SPECIFIC:
        for b in SPECIFIC:
            if a < b:
                overlap['%s + %s' % (a, b)] = sum(
                    1 for pins in pin_sets if a in pins and b in pins)
    return {
        'label': label,
        'pin_rev': pin_rev,
        'pin_paths_checked': len(pin_paths),
        'pin_paths_missing_at_pin_rev': pin_missing,
        'entries_verifying_at_pin_rev': sum(1 for v in verifies if v),
        'entries_total_for_verification': len(entries),
        'input_path_missing_refs': {p: refs[:10] for p, refs in missing_refs.items()},
        'forecast_shadow': forecast_shadow,
        'rehearsal_set_check': rehearsal,
        'ledger': {
            'sha256': sha256(ledger_bytes),
            'bytes': len(ledger_bytes),
            'schema': ledger.get('schema'),
            'corrections': len(ledger.get('corrections') or []),
            'carried_from': ledger.get('carried_from'),
            'entries': len(entries),
            'distinct_headings_total': len(by_heading),
            'distinct_headings_nonempty': sum(1 for h in by_heading if h != ''),
        },
        'entries_per_heading': heading_stats({h: len(v) for h, v in by_heading.items()}),
        'entries_per_heading_nonempty': heading_stats(
            {h: len(v) for h, v in by_heading.items() if h != ''}),
        'rekey': {
            'entries_with_rekey_batch': sum(1 for e in entries if 'rekey_batch' in e),
            'batches': batches,
            'rekey_round_values': sorted({e.get('rekey_round') for e in entries
                                          if 'rekey_round' in e}),
        },
        'sections': {
            'total': len(sections),
            'with_newest_entry': sum(1 for row in rows if row['has_newest']),
            'rows': rows,
        },
        'orphan_heading_keys': orphans,
        'membership': {
            'distinct_paths_in_newest_views': len(membership),
            'top20': membership.most_common(20),
            'specific': specific,
            'specific_overlap': overlap,
            'ignored_self_keys': dict(ignored_membership),
        },
        'missing_input_paths': missing_inputs,
        'append_inversions': inversions,
    }


def path_exists(base_tree, path):
    if path in base_tree['files']:
        return True
    prefix = path.rstrip('/') + '/'
    return any(f.startswith(prefix) for f in base_tree['files'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='.')
    parser.add_argument('--base', default=BASE)
    parser.add_argument('--out', default='ledger-census.json')
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    if not (repo / '.git').exists():
        sys.exit('not-a-repo:%s' % repo)

    sectionize = load_sectionize(repo)
    base_skill = git(repo, 'show', '%s:%s' % (args.base, SKILL))
    sections = sectionize(base_skill)
    base_ledger = git(repo, 'show', '%s:%s' % (args.base, LEDGER))
    live_ledger = (repo / LEDGER).read_bytes()
    live_skill = (repo / SKILL).read_bytes()

    base_files = set(git_text(repo, 'ls-tree', '-r', '-z', '--name-only',
                              args.base).split('\0')) - {''}
    base_tree = {'files': base_files}

    ledger_docs = [json.loads(base_ledger.decode('utf-8', 'surrogateescape')),
                   json.loads(live_ledger.decode('utf-8', 'surrogateescape'))]
    revs = sorted({e.get('read_rev') for doc in ledger_docs for e in doc['entries']
                   if isinstance(e.get('read_rev'), str)})
    out = git_text(repo, 'show', '-s', '--format=%H %ct', '--no-patch', *revs)
    commit_time = {}
    for line in out.splitlines():
        rev, stamp = line.split()
        commit_time[rev] = int(stamp)

    report = {
        'generated_by': 'T72W1S02',
        'base_rev': args.base,
        'head_at_census': git_text(repo, 'rev-parse', 'HEAD').strip(),
        'skill': {
            'sha256_base': sha256(base_skill),
            'sha256_worktree': sha256(live_skill),
            'sections': len(sections),
            'sectionizer': FROZEN,
        },
        'snapshots': {
            'base': census('base', base_ledger, sections,
                           base_tree, commit_time, repo, args.base),
            'live': census('live', live_ledger, sections,
                           base_tree, commit_time, repo,
                           git_text(repo, 'rev-parse', 'HEAD').strip()),
        },
    }
    report['drift'] = {
        'live_ledger_sha256': report['snapshots']['live']['ledger']['sha256'],
        'base_ledger_sha256': report['snapshots']['base']['ledger']['sha256'],
        'entries_added': (report['snapshots']['live']['ledger']['entries']
                          - report['snapshots']['base']['ledger']['entries']),
        'batches_added': [b['batch'] for b in
                          report['snapshots']['live']['rekey']['batches']
                          if b['batch'] not in
                          {x['batch'] for x in
                           report['snapshots']['base']['rekey']['batches']}],
    }
    # section-level drift: newest index / input count changes base -> live
    drift_rows = []
    for b, l in zip(report['snapshots']['base']['sections']['rows'],
                    report['snapshots']['live']['sections']['rows']):
        if (b.get('newest_index'), b.get('inputs_view')) != (
                l.get('newest_index'), l.get('inputs_view')):
            drift_rows.append({
                'heading': b['heading'],
                'base_newest_index': b.get('newest_index'),
                'live_newest_index': l.get('newest_index'),
                'base_inputs_view': b.get('inputs_view'),
                'live_inputs_view': l.get('inputs_view'),
                'live_rekey_batch': l.get('rekey_batch'),
            })
    report['drift']['sections_changed'] = drift_rows

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + '\n',
                        encoding='utf-8')
    print('CENSUS base_entries=%d live_entries=%d sections=%d out=%s' % (
        report['snapshots']['base']['ledger']['entries'],
        report['snapshots']['live']['ledger']['entries'],
        len(sections), out_path))


if __name__ == '__main__':
    main()
