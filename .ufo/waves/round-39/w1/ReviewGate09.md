# ReviewGate09 — C2 census attack: tools/pin-disposition.py

Seat: reviewer (leaf). Target: classification of `tools/pin-disposition.py` by the
pinned census `tools/write-path-census.py` (sha-pinned per contract C2).

## Verdict

**One write class is missed and the named limit does not cover it:**
namespace writes whose path operand sits on the same line as the call
(`os.symlink`, `os.rename`, `os.remove`, `os.makedirs`, `tempfile.mkdtemp`,
`shutil.rmtree`). Representative lines:

- `tools/pin-disposition.py:1187` — `os.symlink("claims-check.mjs", kimi_path)`
  (creates the fixture file `scripts/kimi-census.mjs` the "worktree-symlink"
  case then observes; the created path is on the same line).
- `tools/pin-disposition.py:1186` — `os.rename(kimi_path, kimi_path + ".real")`
- `tools/pin-disposition.py:1163-1164` — `os.rename` + `os.symlink` building the
  `kumitate-scripts` fixture.
- `tools/pin-disposition.py:1209` — `os.symlink(kumitate, mado_link)`.

`WRITE_RE` (`tools/write-path-census.py:46-50`) matches none of these; verified
empirically — `classify_text(pin-disposition.py)` returns `write_sites=3,
unflagged=0`, matching only `:723`, `:891`, `:926` (`open(..., 'wb'/'w')`).

## Why the named limit does not cover it

The docstring (`tools/write-path-census.py:9-11`) names exactly two exclusions:
(a) shell redirects, (b) writes whose path is not on the same line as the call.
These misses are Python calls, not shell redirects, and the path operand is on
the same line — so (b) does not apply either.

Depth consequence, not just an undercount: `classify_text` drops every line
failing `WRITE_RE` before `EXPECTED_RE` is consulted (`write-path-census.py:69-72`).
The canonical atomic expected-file update idiom — `os.rename(tmp, "case.expected")`
or `os.symlink(...)` retargeting a golden path — writes the expected value with
the literal path on the same line yet is invisible to both counters: it can
never reach `write_sites` or `unflagged`, flag or no flag.

## Covered misses (no defect)

- `handle.write` / `json.dump` (`:724`, `:892-893`, `:927`): content writes
  whose path lives on the `open` line — named limit (b), and the `open` site is
  counted anyway.
- `sys.stdout.write` (`:182`, `:1375`): no filesystem path; only vacuously
  outside (b), and stdout emission is not an expected-file write. Weak.
- `git` subprocess writes (`:769-790` helper; `:804`, `:833-834` calls):
  mutation happens inside the child, path derived — outside the frozen line
  model, nearest to limit (b).

## Residual risk

If the frozen census's "write" is intended to mean file-content writes only,
the live classification of this gate is complete (3/3, none expected-valued,
so `unflagged=0` is honest). The finding then stands only as a scope gap in
the named limits rather than a misclassification of this file today.

## Evidence

Command run (read-only, no lane mutation):

    python3 - <<'EOF'
    import importlib.util
    spec = importlib.util.spec_from_file_location('wpc', 'tools/write-path-census.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    text = open('tools/pin-disposition.py').read()
    print(m.classify_text(text))   # -> (3, 0)
    EOF
