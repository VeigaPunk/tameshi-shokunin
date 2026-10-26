# T49W2ExecGenTrace — is `tools/pbt-staged-id.py` property-based or differential? (round 49, wave 2)

Seat: T49W2ExecGenTrace. Item: show **from outside the counter** that the generator at
`f181a961ae44061af486f600e5ea257d2baf78f8` is property-based and not a differential against the
pristine guard sitting in its cwd (wave-1 `T49CritC2Contract.md` F1). No claim is decided here; every
line is an observed trace, a dump comparison, or a code reading.

Artifact under test (all runs at these exact bytes):

| what | sha256 | source |
|---|---|---|
| generator | `0cbee392a83e4cd6609efa97395a9ae8a64115015cf290e42e9a4ff98bc01f05` | `git -C LANE show f181a961:tools/pbt-staged-id.py \| sha256sum`; `sha256sum LANE/tools/pbt-staged-id.py` gives the same (HEAD `5f597fa8` is unchanged for this file) |
| named gate | `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` | equals `contract.json:52` (`named_gate`) |
| lane clone | `git clone --shared` of LANE, checked out at `f181a961` | `git -C clone rev-parse HEAD` → `f181a961ae44061af486f600e5ea257d2baf78f8` |

Scratch: `S=/fast/scratch/hyaku/tameshi-r49/T49W2ExecGenTrace`, deleted before yield. No tool installed
or upgraded (`strace 7.2`, `python3 3.14.8`, `git` sufficed; pacman untouched). Receipts:
`T49W2ExecGenTrace.open-list.txt`, `.runs.txt`, `.classify2.py`, `.diffgen2.py`, `.mutants.diff`,
`.sha256sums.txt`, `.traceA.log`, `.traceB2.log`, `.traceF.log`, `.traceC.log.gz`, `.dumps/`.

Layout reconstructed from the counter (`measure.py:219` `cwd=os.path.dirname(gen)`, `measure.py:249-258`
`materialize()` writes the generator **and** the pristine guard into `tree/`, `measure.py:336` reuses the
same generator for each mutant): a directory holding the generator and a pristine `staged-id-guard.py`,
`--guard` pointing at a mutant elsewhere.

---

## F1 (attacked: wave-1 C2-F1 HIGH) — the generator never touches the pristine guard in its cwd; the trace shows no such open

Mutant (my own single-line edit, `T49W2ExecGenTrace.mutants.diff` first hunk; from reading the guard,
never from `/home/vgpnk/.local/state/`): `tools/staged-id-guard.py:157`,
`refused = bool(unmapped) or bool(cascade)` → `refused = bool(unmapped)`; mutant sha
`bdc0b670deb65fb83912e12adcd0cc478e8ea6e5c2961fa6babf73a805532cb8`.

```
cd <S>/tree/tools && TMPDIR=<S>/w/tmpA PYTHONDONTWRITEBYTECODE=1 \
  strace -f -e trace=openat,open,execve -o <S>/traceA python3 -I pbt-staged-id.py \
  --guard <S>/m/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/dA.jsonl
```
observed (`T49W2ExecGenTrace.runs.txt`, `T49W2ExecGenTrace.traceA.log`):

```
VIOLATION index=5 exit 0, oracle expects 1
VIOLATION observed_exit=0 stdout={"cascade": ["S024"], "cascade_count": 1, ... "refused": false, ...}
PBT_STAGED_ID: cases=6 violations=1 counterexample=5 classes=indent_1_3=3,...
EXIT=1   dA.jsonl = 6 lines
```

Filtered open/exec list, everything outside the Python install and the run's TMPDIR
(`T49W2ExecGenTrace.open-list.txt`, produced by `.classify2.py`; `dirfd-relative` events are reported,
never dropped):

```
TRACE <S>/traceA
TOTAL_PARSED_EVENTS 1067  UNPARSED_LINES 7
BUCKET outside distinct=27 events=178
  execve  n=7     /usr/bin/python3
  open    n=7     /etc/ld.so.cache
  open    n=7     /usr/lib/libpython3.14.so.1.0
  open    n=7     /usr/lib/libc.so.6
  open    n=7     /usr/lib/libm.so.6
  open    n=7     /usr/lib/locale/locale-archive
  open    n=7     /usr/lib/gconv/gconv-modules.cache
  open    n=7     /proc/self/maps
  open    n=7     /usr/pyvenv.cfg
  open    n=7     /usr/bin/pyvenv.cfg
  open    n=7     /usr/lib/libpython3.14.so.1.0._pth
  open    n=7     /usr/bin/python3._pth
  open    n=7     /usr/bin/python3.14._pth
  open    n=7     /usr/bin/pybuilddir.txt
  open    n=7     /etc/localtime
  open    n=2     <S>/tree/tools/pbt-staged-id.py          <- the generator's own source
  open    n=7     /usr/lib/libz.so.1
  open    n=7     /usr/lib/libbz2.so.1.0
  open    n=7     /usr/lib/liblzma.so.5
  open    n=7     /usr/lib/libzstd.so.1
  open    n=1     <S>/dA.jsonl                             <- --dump
  open    n=12    <S>/m/staged-id-guard.py                 <- --guard only (6 cases x script read x2)
  open    n=6     /usr/lib/libcrypto.so.3
  open    n=6     /usr/lib/libbrotlienc.so.1
  open    n=6     /usr/lib/libbrotlidec.so.1
  open    n=6     /usr/lib/libbrotlicommon.so.1
  open    n=6     /etc/ssl/openssl.cnf
BUCKET dirfd-relative distinct=1 events=1
  open    n=1     case
BUCKET tmpdir distinct=5 events=40
BUCKET python-install distinct=143 events=848
```

`<S>/tree/tools/staged-id-guard.py` — the pristine copy sitting in the generator's cwd — **does not
appear in any bucket**: not outside, not dirfd-relative, not tmpdir, and it is not under `python-install`.
The only guard path opened or executed is the one named by `--guard`, and it is executed only as a CLI
(`execve("/usr/bin/python3", ["/usr/bin/python3", "-I", "<S>/m/staged-id-guard.py", "--registry", …]`)
— never imported, never opened in-process by the generator's own `open`. That is the F1 hazard, and it
is **not realised**: no HIGH finding against this artifact.

Same result in the item's literal layout (`cwd` = the pristine copy's directory, generator at
`tools/pbt-staged-id.py`):

```
cd <S>/pristine && TMPDIR=<S>/w/tmpB2 ... python3 -I tools/pbt-staged-id.py \
  --guard <S>/m/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/dB2.jsonl
  PBT_STAGED_ID: cases=6 violations=1 counterexample=5      (exit 1, dB2.jsonl = 6 lines)
```
`BUCKET outside` for `traceB2` is line-for-line the same class of entries with
`<S>/pristine/tools/pbt-staged-id.py` in place of the generator and `<S>/pristine/staged-id-guard.py`
**absent** (`T49W2ExecGenTrace.open-list.txt:44-83`). Third variant, no pristine anywhere in cwd
(`cd <S>/empty2`, `tools/pbt-staged-id.py` invoked by absolute path): same verdict,
`cases=6 violations=1 counterexample=5` — detection does not depend on a reference copy existing at all.

### Full 400-case run with a pristine reachable in cwd

The mutant arm stops at case 5, so it exercises only 6 cases. To cover a whole run, the 400-case leg used
`--guard <S>/m2/staged-id-guard.py`, byte-identical to pristine (sha `03a796c5…`, same as
`contract.json:52`) while `<S>/pristine/staged-id-guard.py` stayed in cwd:

```
cd <S>/pristine && TMPDIR=<S>/w/tmpC ... strace -f ... -o <S>/traceC python3 -I tools/pbt-staged-id.py \
  --guard <S>/m2/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/dC.jsonl
  PBT_STAGED_ID: cases=400 violations=0 counterexample=none
  classes=indent_1_3=248,indent_4_plus=31,id_4_plus_digits=31,collision=204,no_collision=62,held=49,
          unmapped=31,cascade=45,refusal=61,url_form_variant=30,map=104,map_inadmissible=31
  EXIT_C=0
```

`traceC` (60 251 parsed events, 401 `execve`, `T49W2ExecGenTrace.traceC.log.gz`): the guard-under-test is
opened `n=800` (400 cases × 2 reads), the pristine copy in cwd **is not opened once**, and
`grep -c /home/vgpnk traceC` → **0**, `grep -c local/state traceC` → **0**.

## F2 (the pristine leg is cwd-independent) — both dumps byte-identical

```
cd <S>/pristine && TMPDIR=<S>/w/tmpP1 python3 -I tools/pbt-staged-id.py \
  --guard <S>/pristine/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/p1.jsonl   -> exit 0
cd <S>/empty    && TMPDIR=<S>/w/tmpP2 python3 -I <S>/pristine/tools/pbt-staged-id.py \
  --guard <S>/pristine/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/p2.jsonl   -> exit 0
cmp <S>/p1.jsonl <S>/p2.jsonl -> identical
sha256sum p1.jsonl p2.jsonl  -> ca62402bc6125cb8003b3854a30bef829d29d5c6656be1f8a516ca2828a7cd28 (both)
```
Both dumps are 400 lines with `index` exactly `range(400)` (`T49W2ExecGenTrace.dumps/p1.jsonl`). The
mutant leg's case stream is the same stream: `head -6 dA.jsonl` == `head -6 p1.jsonl`
(`cmp` → identical), so the counterexample at index 5 is case 5 of the seed-4949 stream, not a
cwd-specific reshuffle.

## F3 (method sensitivity) — the same filter *does* catch a differential generator

An honest "no pristine open" needs a positive control, so I wrote one: `diffgen2.py`, 3 shapes, no
property and no oracle, comparing `--guard` with `./staged-id-guard.py` (the wave-1 F1 cheat shape,
independently re-derived), same layout and command:

```
cd <S>/tree/tools && TMPDIR=<S>/w/tmpF ... strace -f ... -o <S>/traceF python3 -I diffgen2.py \
  --guard <S>/m/staged-id-guard.py --seed 4949 --cases 400 --dump <S>/dF.jsonl
  PBT_STAGED_ID: cases=1 violations=1 counterexample=0     EXIT_F=1
```
`traceF` outside bucket:

```
  open    n=2     <S>/tree/tools/diffgen2.py
  open    n=1     <S>/dF.jsonl
  open    n=2     <S>/m/staged-id-guard.py
  open    n=2     <S>/tree/tools/staged-id-guard.py        <- the cwd reference, caught
```
And the cheat's other leg, `--guard` = the cwd copy (both pristine):
`PBT_STAGED_ID: cases=400 violations=0 counterexample=none` (exit 0) — the differential shape passes
the pristine leg and would be `confirmed` on a mutant run. So the filter in F1 can see a pristine read;
it sees none for the real generator. (Method note, not an artifact defect: `tempfile.mkdtemp` silently
falls back to `/tmp` when `TMPDIR` names a non-existent directory — my first leg-B run did that; it was
re-run as `traceB2` with `$S/w/tmpB2` created, same result. The counter always creates its own tmp dir,
`measure.py:83-85`.)

## F4 (property-based, not fixture replay) — three independent properties, and cases vary with the seed

Three single-edit mutants (own edits, `T49W2ExecGenTrace.mutants.diff`) are killed by **three different
assertions**, from a cwd with nothing in it:

| mutant | edit (pristine line) | observed |
|---|---|---|
| `m` `bdc0b670…` | guard `:157` `refused = bool(unmapped) or bool(cascade)` → `bool(unmapped)` | `VIOLATION index=5 exit 0, oracle expects 1` (dA = 6 lines) |
| `m3` `d16d3b1b…` | guard `:121` `return text.rstrip('/')` → `return text` | `VIOLATION index=8 field held: guard {}, oracle {'S026': 'S015'}` (d-m3 = 9 lines) |
| `m4` `758d8644…` | guard `:65` `ROW_RE` ` {0,3}` → ` {0,4}` | `VIOLATION index=20 field staged_max: guard 'S007', oracle 'S000'` (d-m4 = 21 lines) |

A differential or fixture-replay generator cannot produce three different *field-level* disagreements
under three unrelated edits while never reading a reference, and the seed moves the cases:

```
seed 4949 vs 4950, both 400 cases, pristine guard:
distinct case records: 4949=400, 4950=400, shared=0
```
Source reading agrees with the trace: cases come from `RECIPES` draws on one `random.Random(seed)`
(`tools/pbt-staged-id.py:742`, `:787`, `:802`), the guard is only ever asked through its CLI
(`:762`, `:772` with `cwd=case_dir`, a fresh `tempfile.mkdtemp` per run at `:789`), and the answer is
compared to an oracle written from the documented contract (`:246 oracle_case`, `:296 check`). The
generator opens no data file at all — its only writes are the dump and its own `case/{registry,staged,map}`
files, so no corpus can travel beside it (this is the residual wave-1 F3 already records, not a new defect).

Also observed: the dump line is written **before** the guard runs (`:803-806` then `:807`), so
`len(dump) == cases run` on every arm (6, 6, 9, 21, 400) and the dump's last index is always the
reported counterexample — the file is not padded, unlike the counter permits.

## Findings

- **F1 HIGH (wave-1 C2-F1) — attacked and refuted for this artifact.** The premise is real
  (`measure.py:219` runs the generator with `cwd=os.path.dirname(gen)` and `measure.py:249-258` puts the
  pristine guard in that same directory), but the delivered generator never opens it: three layouts, 412
  traced guard runs (6 + 6 + 400 across `traceA`/`traceB2`/`traceC`) plus a further untraced 6-case run,
  one mutant arm and one full control arm, zero opens of the cwd guard, zero `/home/vgpnk` paths, zero
  `git` execs (`execve` = `/usr/bin/python3` only). No HIGH finding against
  `tools/pbt-staged-id.py@0cbee392`.
- **Residual R1 (inherited, counter-side, MED).** The harness still *permits* the cheat — `traceF` shows a
  property-free differential generator both reading the cwd reference and passing the pristine leg — so
  the counter's confirmation of *some other* generator would still be meaningless. This artifact is clean;
  the measurement is not.
- **Residual R2 (inherited).** Absolute-path reachability (lane checkout, `git show REV:…panel.json`)
  is unconstrained by the counter; for **this** generator it is unexercised (0 `/home/vgpnk` opens over
  400 traced cases), so `why_hidden` (`contract.json:57`) holds observationally here, not by enforcement.
- **Residual R3 (inherited, wave-1 F3).** Dump padding is still unchecked by the counter; this artifact
  does not pad (`len(dump) == cases run` on all five arms), but the counter cannot show that in general.
- **Method ceiling.** cwd-independence and pristine-absence are established at seed 4949 over these
  layouts plus one seed-varied run; they are not proven for arbitrary seeds or for a future edit of the
  file. The trace is evidence about `0cbee392` only.

## Summary

- Traced the generator at `f181a961` (sha `0cbee392`) under `strace -f` in three layouts; filtered
  open/exec list in `T49W2ExecGenTrace.open-list.txt` — only loader/stdlib files, its own source, the
  `--dump` file, and the `--guard` it was handed.
- The pristine `staged-id-guard.py` sitting in its cwd is **never opened**, in a 6-case mutant run and in
  a 400-case full run (400 cases, `violations=0`, all 12 classes ≥30); wave-1 C2-F1 is not realised by
  this artifact.
- Determinism check passes: cwd = guard's dir vs cwd = empty dir give byte-identical dumps
  (`ca62402b…`, 400 lines each); the mutant leg's first 6 cases equal the pristine leg's first 6.
- Method proven sensitive: a 3-shape differential generator with no property opens the cwd reference
  (`n=2`) and passes the pristine leg — the trace would catch the cheat.
- Property-based evidence: three own single-edit mutants killed by three different assertions (`refused`,
  `held`, `staged_max`) with no reference present; seeds 4949/4950 share 0 of 400 case records.
- Residual: the counter still permits the cheat (R1) and unconstrained absolute paths (R2); this artifact
  does not use either, and its dump is never padded.
