# LabRenamedBattery — renamed-identifier battery against write-path census v4 (r42 w2)

Seat: L1Tameshi42.LabRenamedBattery · Date: 2026-10-25 · Attacked thing: C2's claim
that `tools/write-path-census-v4.py` resolves attribute-bound and output-flag destinations
by structure, not by the battery's literal names.

## Findings

1. **v4 classifies all 10 renamed fixtures exactly as the originals: 10/10 renamed, 10/10 original.**
   The full write-site list (every site's line number, kind and four classification
   bits) is identical between original and renamed in 10/10 fixtures. Only the
   `resolved` text changes, and only by the substituted names. On F04 the
   resolved text now names the renamed option: `expected.json argparse --output-dir`.
2. **The critic's cheat `v3flip.py` drops to 8/10 on the renamed set.** It passes the
   originals 10/10 and fails exactly the two fixtures it special-cases by name:
   renamed F01 gets `scratch=0 want 1` and renamed F04 gets `explicit_out=0 want 1`.
   This control shows the renamed battery can detect a tool that matches on names.
3. **Baseline: v3 fails F01 and F04 under both namings** (8/10 original, 8/10 renamed).
   So the two fixtures that matter really do need resolution that v3 lacks, and the
   rename doesn't make them easier.
4. **Scope probe beyond the brief (not a break):** I also renamed `--out` to the
   off-allowlist `--dest-dir`. Renamed F04 then falls back to unflagged (`1001`, 9/10).
   That is v4's stated, conservative scope, not name overfitting:
   `tools/write-path-census-v4.py:24-25` limits flag tracing to `--out`, `--output`,
   `--out-dir` and `--output-dir`, and `:68` defines the tuple `OUTPUT_FLAGS`. The failure
   errs toward flagging the write (unflagged), never toward hiding it. The attribute and
   method resolution steps contain no name allowlist; `rg` over v4 finds `root`,
   `case_dir` and `publish` only in the docstring (`:7-12`) and in its own selftest
   sources (`:470-639`), never in resolver code. Readers should know that the outflag
   class still keys on these four option spellings.

## Table — single expected-value site

Bit order: expected / scratch / explicit_out / unflagged. In the cheat columns, `F`
marks a fixture that fails.

| Fixture | Declared | v4 original | v4 renamed | All sites equal | v3flip original | v3flip renamed |
|---|---|---|---|---|---|---|
| F01_attr_scratch | 1100 | 1100 ok | 1100 ok | yes | 1100 ok | 1001 F (scratch=0) |
| F02_attr_golden | 1001 | 1001 ok | 1001 ok | yes | 1001 ok | 1001 ok |
| F03_attr_ambiguous | 1001 | 1001 ok | 1001 ok | yes | 1001 ok | 1001 ok |
| F04_outflag | 1010 | 1010 ok (`--out`) | 1010 ok (`--output-dir`) | yes | 1010 ok | 1001 F (explicit_out=0) |
| F05_inflag | 1001 | 1001 ok | 1001 ok | yes | 1001 ok | 1001 ok |
| F06_outflag_mixed_callers | 1001 | 1001 ok | 1001 ok | yes | 1001 ok | 1001 ok |
| F07_module_constant | 1001 | 1001 ok | 1001 ok (unchanged) | yes | 1001 ok | 1001 ok |
| F08_variable_join | 1001 | 1001 ok | 1001 ok | yes | 1001 ok | 1001 ok |
| F09_symlink | 1001 | 1001 ok | 1001 ok (unchanged) | yes | 1001 ok | 1001 ok |
| F10_update_flag | 1000 | 1000 ok | 1000 ok (unchanged) | yes | 1000 ok | 1000 ok |
| **Total** | | **10/10** | **10/10** | 10/10 | 10/10 | **8/10** |

F07, F09 and F10 contain none of the named identifiers, so their renamed bytes are
identical to the originals (same sha256). They act as no-change controls.

## Method and exact commands

- Fixtures came from the frozen counter by AST `literal_eval` of `FIXTURES`
  (`.ufo/evidence/round-42/census/measure.py:72-202`). The counter's sha256 is
  `3c3727ec…890ff2`, the same in the working copy, at `a21845f`, and at freeze `322b5cd`.
- Renaming was done at the token level with `tokenize`. NAME tokens were mapped
  `root→base_path`, `case_dir→slot_for`, `publish→emit_bundle`, `out→target_dir`,
  `H→Harness` and `run→execute`, except that `args.out` became `args.output_dir`
  (argparse dest). The string `'--out'` became `'--output-dir'` (off-list probe:
  `'--dest-dir'` / `dest_dir`). Each renamed file was checked with `ast.parse`, with
  no remaining NAME token from the old set and no `'--out'` literal left.
- The renamed F04 needle check required `--output-dir`, not `--out`, because `--out`
  is a substring of `--output-dir` and would pass trivially.
- Per-file command, as specified (cwd = fixture dir in scratch):
  `python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v4.py --file F04_outflag.renamed.py --json`
  printed
  `{"file": "F04_outflag.renamed.py", "sites": [{"expected": true, "explicit_out": true, "flagged": false, "kind": "write_bytes", "lineno": 7, "resolved": "expected.json argparse --output-dir", "scratch": false, "unflagged": false}]}` with exit 0.
  Renamed F01 printed `{'lineno': 17, 'kind': 'open', 'expected': True, 'scratch': True, 'explicit_out': False, 'unflagged': False}`.
- Harness: `/tmp/tameshi-r42w2-LabRenamedBattery-r1/battery.py`
  (sha256 `68801c36c2921878fc71950a0755347d64a50c59fd92d2ba01832689d98d56ae`), run four ways:
  - `python3 battery.py <lane>/tools/write-path-census-v4.py --flagset prescribed` gave `SUMMARY orig=10/10 renamed=10/10 all_sites_equal=10/10`
  - `python3 battery.py /tmp/tameshi-r42-CriticFixtureOverfit-r1/v3flip.py --flagset prescribed` gave `SUMMARY orig=10/10 renamed=8/10 all_sites_equal=8/10`
  - `python3 battery.py <lane>/tools/write-path-census-v4.py --flagset offlist` gave `SUMMARY orig=10/10 renamed=9/10` (F04 `explicit_out=0`, the documented allowlist scope)
  - `python3 battery.py <lane>/tools/write-path-census-v3.py --flagset prescribed --text` gave `SUMMARY orig=8/10 renamed=8/10 all_sites_equal=10/10`
- Renamed F01 source (for reproduction):
  `class Harness: __init__: self.base_path = tempfile.mkdtemp()`; `slot_for(self, name): path = os.path.join(self.base_path, name); os.makedirs(path); return path`;
  `execute(self): directory = self.slot_for('a'); expected_path = os.path.join(directory, 'expected.json'); open(expected_path, 'w')`.
- Renamed F04 source: `def emit_bundle(data, target_dir): target_dir.mkdir(...); (target_dir / 'expected.json').write_bytes(data)`;
  `parser.add_argument('--output-dir'); args = parser.parse_args(); target = Path(args.output_dir); emit_bundle(b'{}', target)`.

## Pins and hashes (before and after, unchanged)

- `tools/write-path-census-v4.py` sha256 `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`,
  identical to the blob at `a21845f523b75adbd3e3f7a62af91294db224ad9`. Its last commit,
  `5f739acf`, is an ancestor of `a21845f`.
- `tools/write-path-census-v3.py` sha256 `095924a7…eef0279`, matching the counter's `V3_SHA`.
- `/tmp/tameshi-r42-CriticFixtureOverfit-r1/v3flip.py` sha256 `63f688fe…625338ec`,
  matching the critic's `shas.txt`.
- No counter was run in default mode. The lane checkout was not edited apart from this
  report. No tools were installed. The scratch dir
  `/tmp/tameshi-r42w2-LabRenamedBattery-r1` was deleted after this report was written.

## Verdict

SURVIVES — v4 holds 10/10 when every critic-named identifier is renamed consistently, and
every site's classification is unchanged. The name-keyed cheat `v3flip.py` fails renamed
F01 and F04, giving 8/10. One residual point is documented scope, not a break: output-flag
resolution recognizes only the four allowlisted option spellings
(`tools/write-path-census-v4.py:68`), and any other spelling stays flagged.
