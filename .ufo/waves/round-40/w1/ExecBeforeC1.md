# ExecBeforeC1 — C1 re-run at base rev 304e335 (not the deciding run)

Seat: executor (leaf). Lane checkout untouched; no default-mode counter run beyond the
assigned base rev; no installs.

## Command

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-40/census/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 304e3355705640af2879c772fc9a5c2902c61763
```

(cwd `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, run as
`python3 .ufo/evidence/round-40/census/measure.py --lane … --rev 304e335…`.)

## Output (verbatim, exit code 1)

```
C1_R40: tool_absent=1 bytes_unflagged=0 replace_unflagged=0 v1_bytes_unflagged=0 v1_replace_writes=0 rev=304e3355705640af2879c772fc9a5c2902c61763 C1_R40_PASS=false
```

`EXIT=1`. This is the contract's first do-nothing arm — `contract.json:28`
(`"do_nothing": "tool absent at base, or v1 patterns on the planted fixtures"`) — not a
measurement of the planted or live legs.

## The absence is real, not a failed lookup

`git_show()` returns `None` on *any* nonzero git exit (`measure.py:45-51`), so `tool_absent=1`
alone would also be printed for a mistyped rev. Resolved separately, read-only:

| Check | Command | Result |
|---|---|---|
| rev exists and is a commit | `git rev-parse 304e335…` / `git cat-file -t 304e335…` | `304e335…` / `commit` |
| `git_show` works at that rev | `git show 304e335…:tools/write-path-census.py \| sha256sum` | `bc8c660c…edc62` = C1 `v1_sha256` (`contract.json:23`) |
| v2 tool absent at base | `git show 304e335…:tools/write-path-census-v2.py` | nonzero (absent) |
| v2 tool present at HEAD | `git show HEAD:tools/write-path-census-v2.py \| sha256sum` | `40228532…2d878b` = C1 `tool_sha256` (`contract.json:22`) |
| worktree v2 == HEAD v2 | `sha256sum tools/write-path-census-v2.py` | `40228532…2d878b` (same) |
| contract absent at base | `git show 304e335…:.ufo/evidence/round-40/contract.json` | absent |
| contract present at HEAD | `git show HEAD:.ufo/evidence/round-40/contract.json \| sha256sum` | `8a8dd141…cf7047d`, identical to worktree |
| fixtures absent at base | `git show 304e335…:.../census/fixtures.json` | absent; worktree/HEAD sha `af237473…0efa5d` |

HEAD is `5641ed84c8dc148c34c8dd83f062279ddf06b4af` (`5641ed8 round-40: freeze C1 write-form
census and C2 S108 snapshot pin before data`), the freeze commit; the base rev is its parent.

**The base line's `v1_bytes_unflagged=0 v1_replace_writes=0` are literals, not measurements** —
the absent branch hardcodes them (`measure.py:120-131`, fields at `:126-127`). Only
`tool_absent=1` and `rev=` carry information in this output.

## Finding — `--control` is inverted relative to the frozen predicate

```
python3 .ufo/evidence/round-40/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --control
C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false
```

`CONTROL_EXIT=1`.

- `measure.py:99` requires v1 to reach the v2 target:
  `meets = bytes_u == 1 and replace_w >= 1 and v1_classify(planted['replace_unflagged'])[1] == 1`.
- `contract.json:24` requires the opposite: "embedded v1 patterns score bytes_unflagged=0 and
  replace writes=0 on those two planted cases".
- The main path encodes the predicate orientation correctly: `v1_misses = v1_bytes == 0 and
  v1_replace_writes == 0` (`measure.py:220`), used in `ok` (`measure.py:221-229`).
- Scratch reproduction of `v1_classify` (import only, no counter run) on
  `.ufo/evidence/round-40/census/fixtures.json` (`af237473…`):
  - `bytes_unflagged` `(out / 'expected.json').write_bytes(b'x')` → `writes=1`, `unflagged=0`
    (`'expected.json'` does not match `V1_EXPECTED_RE`, `measure.py:38-40`).
  - `replace_unflagged` `os.replace(tmp, 'case.expected')` → `writes=0`
    (`V1_WRITE_RE`, `measure.py:33-37`, has no `os.replace` alternative).
  - control `meets` evaluates False on both conjuncts; `v1_misses` evaluates True on both.

Consequence: `--control` can never pass while the predicate holds, so a red control is a
counter-side pre-flight defect, **not** evidence the fixtures fail to discriminate. The
deciding run is unaffected because `control()` is never consulted by `main()`'s `ok`
(`measure.py:221-229`). The predicate is frozen and was not rewritten.

## Verdict on the assigned move

At `304e3355705640af2879c772fc9a5c2902c61763`: `C1_R40_PASS=false`, exit 1, via the
`tool_absent` do-nothing arm, with rev validity and the pinned v1 blob independently
confirmed. No pass path exists at this rev — tool and contract are both absent, so the pin,
planted, live-site and mutant legs are not evaluated at all.

## Risks for the L1

1. `git_show` conflates missing rev with missing path (`measure.py:45-51`); the base line is
   only interpretable with rev-resolution evidence attached (supplied above).
2. A red `--control` (`measure.py:99` vs `contract.json:24`) may be misread as fixture
   non-discrimination; score the claim on the main path only.
3. This line says nothing about C2; C2 has its own counter and base-rev run.
4. Static only: at HEAD the tool blob and the worktree file both equal the C1 pin, so the sha
   leg is satisfied by construction at that rev; that is not a claim about the other legs and
   the default-mode run remains the L1's.

## No-change statement

No lane file was edited, no counter default-mode run was made at HEAD or any post-base rev.
`git status --porcelain -- .ufo/evidence/round-40 tools` still shows only the pre-existing
untracked `?? .ufo/evidence/round-40/after/` (mtime 21:47:40, before this run). No tools
installed or updated.
