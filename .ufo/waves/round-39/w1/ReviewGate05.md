# ReviewGate05 — census classification attack on tools/evidence-disposition.py

Milestone: Gate attack (C2 depth axis, contract `C2` in `.ufo/evidence/round-39/contract.json`).
Frozen pattern under attack: `WRITE_RE`/`EXPECTED_RE`/`SCRATCH_RE`/`FLAG_RE` in `tools/write-path-census.py:46-55`, applied line-wise by `classify_text` (`write-path-census.py:64-74`).

## Finding: a real file-write call site the frozen pattern misses, and no named limit covers it

**Cited line:** `tools/evidence-disposition.py:1759` (identical at HEAD `233077f88d7a8d142eff329202a120457a5d5258`):

    _write_bytes(evidence / "expected.json", expected_bytes)

This line writes `expected.json` — the very expected-values manifest this gate evaluates — via the module-level helper `_write_bytes` (defined at `:1710-1712`, whose body `path.write_bytes(payload)` is the only `_write_bytes` *line* the census counts).

**Why the pattern misses it:** `WRITE_RE` requires a literal dot before the call (`\.write_bytes\s*\(`). `_write_bytes(` is prefixed by `_`, not `.`, so every one of the ~26 `_write_bytes(...)` call sites is invisible. Empirically replayed `classify_text` over the live file: only 4 write sites counted (`:1712`, `:2611`, `:2619`, `:3031`); the file in fact performs ~26 helper-mediated file writes plus 9 `sys.stdout.write`/`sys.stderr.write` sites (`:1452-1498`, `:3198-3207`) — also missed.

**Why the named limits do not cover it** (`write-path-census.py:9-11`):
- "not a full lexer" — the generic disclaimer, not a named limit; the failure is the regex's `\.` anchor, not lexing depth.
- "Shell redirects ... are outside" — this is a Python call, not a shell redirect.
- "writes whose path is not on the same line as the call" — the destination `evidence / "expected.json"` is literally on the call line `:1759`. (Only indirect cases like `:2404`, where `dispositions_path` was bound on `:2403`, fall under this limit.)

**Depth significance:** the miss is doubly load-bearing for an expected-value write census: even if line `1759` were counted, `EXPECTED_RE` (`\.expected\b|expected\.txt|golden|snapshot`) does not match `"expected.json"`, and `FLAG_RE` has zero hits in the whole file (verified by grep at HEAD), so it would classify as an unflagged expected write. `live_unflagged` is only a reported field, so this cannot flip `C2_R39_PASS`, but it demonstrates the frozen pattern undercounts this gate's real write sites by ~6x (4 counted vs ~26 file-write call sites) and misses the one write whose target name (`expected.json`) is semantically the axis itself.

Command to reproduce:

    python3 - <<'EOF'
    import re
    W = re.compile(r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]|\.write_text\s*\(|\.write_bytes\s*\(""")
    text = open('tools/evidence-disposition.py').read()
    print([i for i, l in enumerate(text.splitlines(), 1) if W.search(l)])
    EOF

prints `[1712, 2611, 2619, 3031]` — `:1724`, `:1759`, and every other `_write_bytes(` call absent.

## Residual risk / gaps

- Finding verified against worktree bytes and `git show HEAD:` for the cited lines; if REV at the deciding run predates the `_write_bytes` helper (introduced with the round-13/14 selftest block), recheck the cited line at that rev — the miss class (bare-`identifier` write helpers) is independent of the exact line number.
- No mutation made to the lane, `.ufo/state`, or the frozen contract. Scratch only at `/tmp/tameshi-r39-ReviewGate05/`.
- Tool installs: none (pacman paused per lane rules; python3 already present).
