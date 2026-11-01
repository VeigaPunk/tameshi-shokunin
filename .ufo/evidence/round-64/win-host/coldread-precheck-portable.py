#!/usr/bin/env python3
"""tools/coldread-precheck-portable.py — host-portable execution form of the
frozen round-48 no-harm precheck (round 61).

The frozen instrument (`.ufo/evidence/round-48/quality/coldread-precheck.sh`
-> `.ufo/evidence/round-21/coldread/measure.py` -> `.ufo/evidence/round-18/measure.py`)
is infeasible on the win32 dispatch host: the round-21 ledger records 75,889
inputs; the frozen code spawns two git processes per input per measured rev
(~151,778 spawns/rev x 0.044 s/spawn measured = ~112 min/rev; five runs
failed — receipt `.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`).

This tool runs the SAME frozen decision code unchanged and replaces ONLY the
two git-plumbing functions it calls per input (`cat_file_blob`,
`ls_tree_mode`) with batched, cache-backed equivalents:

* one `git ls-tree -r -z <rev>` per rev gives every path's mode;
* one `git cat-file --batch` process per CHUNK of `<rev>:<path>` specs gives
  every blob's bytes (the frozen functions' exact return values);

and falls back to the frozen spawn implementation for any lookup the caches
do not cover, so a cached answer and a spawned answer are indistinguishable
to the frozen code. An equivalence probe re-derives a deterministic sample of
lookups through the ORIGINAL spawn functions and fails the run on any
mismatch or on an empty sample (`EQUIVALENCE sampled=N mismatches=0`; the
exit-2 gate requires sampled >= 1 AND mismatches == 0), so the receipt
shows the caches returned exactly what git would have.

The prefetch is chunked and resumable: blob bytes are cached one JSON file
per chunk under --work, a manifest records each chunk's spec count and file
sha256, and a re-run loads verified chunks and fetches only the rest.

Everything else — the credit rule, the trace gate, the strict mode, the
sectionizer, the LOST/verdict line — is the frozen module's own code, called
verbatim. Usage:

  python tools/coldread-precheck-portable.py --repo LANE --floor REV --cand REV --work DIR

Exits 0 when the precheck is `ok` (no floor-credited section lost at cand),
1 when RED (lost>0), 2 on setup errors. `--rev REV` measures one revision
(iteration mode; no comparison, always exit 0 on a completed measure).
"""

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

FROZEN = '.ufo/evidence/round-18/measure.py'
SELECTOR = '.ufo/evidence/round-21/coldread/measure.py'
LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'


def load_frozen(repo):
    impl = Path(repo) / FROZEN
    spec = importlib.util.spec_from_file_location('tameshi_r18_measure', impl)
    module = importlib.util.module_from_spec(spec)
    sys.modules['tameshi_r18_measure'] = module
    spec.loader.exec_module(module)
    # The round-21 selector's bindings (selector main lines 109-112), applied
    # verbatim so the ledger and credit surfaces match the frozen precheck.
    module.DEFAULT_LEDGER_PATH = LEDGER
    module.LEDGER_PATH = LEDGER
    module.BOX3_LINK = LEDGER
    module.IGNORED_INPUTS = module.IGNORED_INPUTS | frozenset((LEDGER,))
    return module


def git_out(repo, *args):
    return subprocess_run(repo, *args).stdout


def subprocess_run(repo, *args):
    import subprocess
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True,
                          env=env)


def cat_file_batch(repo, rev, specs, chunk_id, work, chunk_size_log):
    """Fetch specs (rev:path) in one `git cat-file --batch` process.

    Returns {path: bytes} for specs that resolve to blobs. Missing/non-blob
    specs are simply absent from the result (the patched cat_file_blob falls
    back to the frozen spawn for them, which returns None exactly as before).
    """
    import subprocess
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    payload = ''.join('%s:%s\n' % (rev, p) for p in specs).encode('utf-8', 'surrogateescape')
    proc = subprocess.run(['git', '-C', str(repo), 'cat-file', '--batch'],
                          input=payload, capture_output=True, env=env)
    if proc.returncode != 0:
        raise RuntimeError('cat-file --batch failed: %s' % proc.stderr[:400])
    out = {}
    data = proc.stdout
    pos = 0
    for path in specs:
        nl = data.index(b'\n', pos)
        header = data[pos:nl].decode('utf-8', 'surrogateescape')
        parts = header.split(' ')
        if len(parts) == 3 and parts[2].isdigit():
            size = int(parts[2])
            body = data[nl + 1:nl + 1 + size]
            if parts[1] == 'blob':
                out[path] = body
            pos = nl + 1 + size + 1  # trailing LF after the body
        else:
            # "<spec> missing" line; nothing to skip beyond the LF
            pos = nl + 1
    if work is not None:
        chunk_file = work / ('chunk-%s.json' % chunk_id)
        blob = json.dumps(
            {p: base64.b64encode(b).decode('ascii') for p, b in out.items()},
            sort_keys=True).encode('ascii')
        chunk_file.write_bytes(blob)
    chunk_size_log.append((chunk_id, len(specs), len(out)))
    return out


def load_chunk(work, chunk_id, expected_sha):
    chunk_file = work / ('chunk-%s.json' % chunk_id)
    if not chunk_file.exists():
        return None
    raw = chunk_file.read_bytes()
    if expected_sha is not None and hashlib.sha256(raw).hexdigest() != expected_sha:
        return None
    return {p: base64.b64decode(b) for p, b in json.loads(raw.decode('ascii')).items()}


def prefetch(repo, rev, paths, work, chunk_n):
    """Chunked, resumable prefetch of blob bytes for PATHS at REV."""
    rev_dir = work / ('rev-%s' % rev[:12])
    rev_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = rev_dir / 'manifest.json'
    manifest = {}
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
    ordered = sorted(paths)
    chunks = [ordered[i:i + chunk_n] for i in range(0, len(ordered), chunk_n)]
    byte_cache = {}
    stats = {'chunks_total': len(chunks), 'chunks_resumed': 0, 'chunks_fetched': 0}
    for i, chunk in enumerate(chunks):
        cid = '%04d' % i
        entry = manifest.get(cid)
        loaded = None
        if entry and entry.get('specs') == len(chunk):
            loaded = load_chunk(rev_dir, cid, entry.get('sha256'))
        if loaded is not None:
            byte_cache.update(loaded)
            stats['chunks_resumed'] += 1
            continue
        size_log = []
        fetched = cat_file_batch(repo, rev, chunk, cid, rev_dir, size_log)
        byte_cache.update(fetched)
        chunk_file = rev_dir / ('chunk-%s.json' % cid)
        manifest[cid] = {'specs': len(chunk), 'sha256': hashlib.sha256(
            chunk_file.read_bytes()).hexdigest()}
        stats['chunks_fetched'] += 1
    manifest_file.write_text(json.dumps(manifest, sort_keys=True), encoding='utf-8')
    return byte_cache, stats


def build_mode_map(repo, rev):
    """path -> mode for every blob-ish path at REV, from one recursive ls-tree."""
    out = subprocess_run(repo, 'ls-tree', '-r', '-z', rev)
    if out.returncode != 0:
        raise RuntimeError('ls-tree failed: %s' % out.stderr[:400])
    modes = {}
    for chunk in out.stdout.split(b'\x00'):
        if not chunk:
            continue
        meta = chunk.split(b'\t', 1)[0]
        fields = meta.split(b' ')
        if len(fields) < 3:
            continue
        # with -z git emits paths raw (never c-quoted); decode like the
        # frozen module decodes blob text so keys compare equal
        path = chunk.split(b'\t', 1)[1].decode('utf-8', 'surrogateescape')
        modes[path] = fields[0].decode('ascii', 'surrogateescape')
    return modes


def needed_paths(module, repo, rev):
    """Inputs + traces + required blobs the frozen code will look up at REV."""
    ledger_raw = module.blob(str(repo), rev, LEDGER)
    if ledger_raw is None:
        raise RuntimeError('ledger missing at %s' % rev)
    ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
    paths = set(module.REQUIRED_BLOBS)
    paths.add(LEDGER)
    paths.add('SKILL.md')
    for entry in ledger['entries']:
        if not isinstance(entry, dict):
            continue
        view = module.inputs_view(entry)
        if view:
            paths.update(view.keys())
        traces = entry.get('traces')
        if isinstance(traces, list):
            paths.update(t for t in traces if isinstance(t, str))
    return paths, ledger_raw


def install_cache(module, repo, rev, byte_cache, mode_map, probe_log):
    """Patch the two plumbing functions with cache-backed equivalents.

    Cache hit -> the exact value the spawn would return (blob bytes / mode).
    Cache miss -> the ORIGINAL frozen function runs (identical semantics).
    """
    orig_blob = module.cat_file_blob
    orig_mode = module.ls_tree_mode
    repo_s = str(repo)

    def cached_blob(r, rv, path):
        if r == repo_s and rv == rev:
            hit = byte_cache.get(path)
            if hit is not None:
                probe_log['blob_hits'] += 1
                return hit
            if path in mode_map:
                # tracked at rev but not a prefetched blob spec (or batch
                # reported non-blob): the frozen spawn returns the exact
                # None/bytes pair either way
                probe_log['blob_tracked_misses'] += 1
                if mode_map[path] not in module.BLOB_MODES and mode_map[path] != '120000':
                    return None
            return orig_blob(r, rv, path)
        return orig_blob(r, rv, path)

    def cached_mode(r, rv, path):
        if r == repo_s and rv == rev:
            hit = mode_map.get(path)
            if hit is not None:
                probe_log['mode_hits'] += 1
                return hit
            return orig_mode(r, rv, path)
        return orig_mode(r, rv, path)

    module.cat_file_blob = cached_blob
    module.ls_tree_mode = cached_mode
    return orig_blob, orig_mode


def equivalence_probe(module, repo, rev, orig_blob, orig_mode, byte_cache,
                      mode_map, sample_n, seed):
    """Re-derive a deterministic sample through the ORIGINAL spawn functions."""
    repo_s = str(repo)
    candidates = sorted(set(byte_cache) & set(mode_map))
    if not candidates:
        return {'sampled': 0, 'mismatches': 0, 'detail': 'no candidates'}
    step = max(1, len(candidates) // sample_n)
    sampled = candidates[(seed * step) % len(candidates)::step][:sample_n]
    mismatches = []
    for path in sampled:
        want_b = byte_cache.get(path)
        got_b = orig_blob(repo_s, rev, path)
        if got_b != want_b:
            mismatches.append('blob:%s' % path)
        want_m = mode_map.get(path)
        got_m = orig_mode(repo_s, rev, path)
        if got_m != want_m:
            mismatches.append('mode:%s' % path)
    return {'sampled': len(sampled), 'mismatches': len(mismatches),
            'mismatch_paths': mismatches[:5]}


def probe_failed(probe):
    """The probe contract gate (routed defect RD1, r61 spot-check): the run
    may proceed only on a NON-EMPTY deterministic sample with ZERO
    mismatches. An empty sample is a failure, never a vacuous pass."""
    return bool(probe.get('mismatches')) or probe.get('sampled', 0) < 1


def measure_rev(module, repo, rev, work, chunk_n, sample_n, seed):
    started = time.time()
    paths, ledger_raw = needed_paths(module, repo, rev)
    skill_raw = module.blob(str(repo), rev, 'SKILL.md')
    byte_cache, stats = prefetch(repo, rev, paths, work, chunk_n)
    mode_map = build_mode_map(repo, rev)
    probe_log = {'blob_hits': 0, 'blob_tracked_misses': 0, 'mode_hits': 0,
                 'mode_from_bytes': 0}
    orig_blob, orig_mode = install_cache(module, repo, rev, byte_cache,
                                         mode_map, probe_log)
    try:
        out = module.coldread(str(repo), rev, skill_raw, ledger_raw,
                              strict=True, explain=True)
    finally:
        module.cat_file_blob = orig_blob
        module.ls_tree_mode = orig_mode
    probe = equivalence_probe(module, repo, rev, orig_blob, orig_mode,
                              byte_cache, mode_map, sample_n, seed)
    elapsed = time.time() - started
    return {
        'rev': rev,
        'sections_total': out['sections_total'],
        'sections_covered': out['sections_covered'],
        'box3_full_page': out['box3_full_page'],
        'sections': out['sections'],
        'reasons': out['reasons'],
        'prefetch': {
            'needed_paths': len(paths),
            'cached_blobs': len(byte_cache),
            'mode_map': len(mode_map),
            'chunks': stats,
        },
        'probe': probe,
        'cache_calls': probe_log,
        'elapsed_s': round(elapsed, 1),
    }


def precheck_line(floor, cand):
    fc = {s['heading'] for s in floor['sections'] if s['credited']}
    cc = {s['heading'] for s in cand['sections'] if s['credited']}
    lost = sorted(fc - cc)
    lines = []
    for h in lost:
        reason = next(s['reason'] for s in cand['sections'] if s['heading'] == h)
        paths = sorted({r.split(':', 1)[1] for r in reason.split(';')
                        if r.startswith('input-drift:')})
        lines.append('LOST %s | drifted=%s' % (h, ','.join(paths)))
    state = 'RED' if len(cc) < len(fc) else 'ok'
    line = ('COLDREAD_PRECHECK floor=%s floor_credited=%d cand=%s '
            'cand_credited=%d lost=%d %s'
            % (floor['rev'][:12], len(fc), cand['rev'][:12], len(cc),
               len(lost), state))
    return line, lines, state, {'floor_credited': len(fc), 'cand_credited': len(cc),
                                'lost': lost}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--floor')
    ap.add_argument('--cand')
    ap.add_argument('--rev')
    ap.add_argument('--work', required=True)
    ap.add_argument('--chunk', type=int, default=2000)
    ap.add_argument('--sample', type=int, default=40)
    ap.add_argument('--seed', type=int, default=61)
    ap.add_argument('--out')
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    work = Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    module = load_frozen(repo)
    receipt = {'schema': 'tameshi-coldread-precheck-portable-v1',
               'frozen_module': FROZEN, 'selector': SELECTOR,
               'ledger': LEDGER, 'lane': str(repo),
               'method': 'frozen decision code unchanged; only cat_file_blob '
                         'and ls_tree_mode are cache-backed batched equivalents '
                         'with spawn fallback; equivalence probe on a '
                         'deterministic sample must report sampled >= 1 and '
                         'mismatches=0 (an empty sample fails the run)'}
    if a.rev:
        rev = module.resolve_commit(str(repo), a.rev)
        if rev is None:
            print('COLDREAD_PORTABLE error=rev-unresolvable', file=sys.stderr)
            return 2
        m = measure_rev(module, repo, rev, work, a.chunk, a.sample, a.seed)
        receipt['measure'] = m
        print('COLDREAD_PORTABLE rev=%s credited=%d/%d elapsed=%ss '
              'probe_sampled=%d probe_mismatches=%d'
              % (rev[:12], m['sections_covered'], m['sections_total'],
                 m['elapsed_s'], m['probe']['sampled'],
                 m['probe']['mismatches']))
        if probe_failed(m['probe']):
            print('COLDREAD_PORTABLE error=equivalence-probe '
                  'sampled=%d mismatches=%d'
                  % (m['probe']['sampled'], m['probe']['mismatches']),
                  file=sys.stderr)
            return 2
    elif a.floor and a.cand:
        floor_rev = module.resolve_commit(str(repo), a.floor)
        cand_rev = module.resolve_commit(str(repo), a.cand)
        if floor_rev is None or cand_rev is None:
            print('COLDREAD_PORTABLE error=rev-unresolvable', file=sys.stderr)
            return 2
        fm = measure_rev(module, repo, floor_rev, work, a.chunk, a.sample, a.seed)
        cm = measure_rev(module, repo, cand_rev, work, a.chunk, a.sample, a.seed)
        line, lost_lines, state, counts = precheck_line(fm, cm)
        receipt['floor'] = fm
        receipt['cand'] = cm
        receipt['verdict_line'] = line
        receipt['state'] = state
        receipt['counts'] = {**counts, 'lost_details': [
            {'heading': h} for h in counts['lost']]}
        print(line)
        for ll in lost_lines:
            print(ll)
        print('EQUIVALENCE floor_sampled=%d floor_mismatches=%d '
              'cand_sampled=%d cand_mismatches=%d'
              % (fm['probe']['sampled'], fm['probe']['mismatches'],
                 cm['probe']['sampled'], cm['probe']['mismatches']))
        bad_probes = [p for p in (fm['probe'], cm['probe'])
                      if probe_failed(p)]
        if bad_probes:
            for p in bad_probes:
                print('COLDREAD_PORTABLE error=equivalence-probe '
                      'sampled=%d mismatches=%d'
                      % (p['sampled'], p['mismatches']), file=sys.stderr)
            return 2
        if a.out:
            Path(a.out).write_text(json.dumps(receipt, indent=1,
                                              ensure_ascii=True) + '\n',
                                   encoding='utf-8')
        return 1 if state == 'RED' else 0
    else:
        print('usage: --floor REV --cand REV | --rev REV', file=sys.stderr)
        return 64
    if a.out:
        Path(a.out).write_text(json.dumps(receipt, indent=1,
                                          ensure_ascii=True) + '\n',
                               encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
