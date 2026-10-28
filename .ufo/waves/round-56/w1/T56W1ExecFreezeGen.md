# T56W1ExecFreezeGen — freeze regeneration check

Milestone: freeze regeneration check. Judged on: operability.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `981c5e8b20a2`, freeze
`c3e2ca9f020776b3d66c7af854fb82c834674fcf`. The lane HEAD was `c3e2ca9f0207` before this seat and is
`c3e2ca9f0207` after it; `git status --porcelain` gained no line (receipt `E-lane-untouched.out`).
No lane production file, no frozen instrument and no `SKILL.md`/`SCORECARD.md`/`LOG.md` was edited.
No tool was installed or upgraded (python 3.14.8 was already present); `pacman` was not touched.

Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W1ExecFreezeGen/` (`git clone --shared` of the lane,
detached at the freeze, plus a `git init` fixture), removed at the end of the seat. Every git
mutation ran in that scratch clone or fixture after `git -C <dir> rev-parse --show-toplevel` printed
`<dir>`; no git command mutated the lane.

## 1. What was written

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/freeze-gen.py` — 243 lines,
stdlib only (`hashlib`, `json`, `os`, `subprocess`, `sys`), sha256
`01d92e36494ef73cfcc9f848e450b683812bfeaa1d1b555828de50dcce819199`. It reads only git objects and
writes only the path given to `--out` (default: nothing).

```
python3 .ufo/waves/round-56/freeze-gen.py --lane LANE --rev REV [--explain] [--out PATH]

FREEZE_GEN: files=N ok           exit 0   regenerated digests == committed freeze.json at REV
FREEZE_GEN: files=N MISMATCH     exit 1   plus one FREEZE_GEN_MISMATCH line per defect
                                 exit 2   usage / not-a-repository (no verdict line)
```

`--explain` adds `FREEZE_GEN_LANE|REV|CONTRACT|SELF`, one `FREEZE_GEN_FILE <key> path=<resolved>
sha256=<64>` per frozen file, and `FREEZE_GEN_SET regenerated=N manifest=M amendments=A`. `--out`
writes the regenerated manifest and reports `identical=yes|no` against the committed blob.

## 2. The mapping (identical to `deciding-run.sh`'s heredoc)

`deciding-run.sh:23-45` maps a manifest **key** to a repo path: a key under `tools/`,
`.ufo/evidence/round-21/` or `.ufo/evidence/round-48/` is used verbatim, every other key is relative
to `.ufo/evidence/round-56/`. `freeze-gen.py` inverts that on the contract's **paths**, and asserts
the round trip per entry:

```python
E = ".ufo/evidence/round-56"
VERBATIM_PREFIXES = ("tools/", ".ufo/evidence/round-21/", ".ufo/evidence/round-48/")
SELF = E + "/freeze.json"

def manifest_key(path):          # contract path -> freeze.json key
    if path.startswith(VERBATIM_PREFIXES):
        return path
    if path.startswith(E + "/"):
        return path[len(E) + 1:] or None
    return None                  # unmappable: fails closed

def key_path(key):               # freeze.json key -> contract path
    if key.startswith(VERBATIM_PREFIXES):
        return key
    return "%s/%s" % (E, key)
```

`E/freeze.json` is the manifest itself: a file cannot carry its own sha256, so the entry is listed
(`FREEZE_GEN_SELF … listed=yes`) and skipped — exactly what the committed manifest does (11 contract
paths, 10 hashed entries). A path that is neither under the three verbatim prefixes nor under the
round directory is reported `unmappable` (fail closed), never silently dropped. Reads are
`git show REV:<path>` only, so a dirty worktree cannot move the verdict.

## 3. Arm A — regeneration at `c3e2ca9f0207` (10/10, byte-identical)

```
$ python3 .ufo/waves/round-56/freeze-gen.py --lane LANE --rev c3e2ca9f020776b3d66c7af854fb82c834674fcf --explain --out <scratch>/regen-at-freeze.json
FREEZE_GEN_FILE c1/lost-headings-at-base.json  … dcfc9f800b8b…
FREEZE_GEN_FILE c1/measure.py                  … 048122cf1c7c…
FREEZE_GEN_FILE c2/measure.py                  … d17d36bd263b…
FREEZE_GEN_FILE c2/red-before/round-54-surface.paths … 95ead282432b…
FREEZE_GEN_FILE contract.json                  … 2530a54775ae…
FREEZE_GEN_FILE control/frozen-surface.paths   … a0ebd3d4216d…
FREEZE_GEN_FILE controls.sh                    … df1ee355ce62…
FREEZE_GEN_FILE deciding-run.sh                … 6a63f5058be1…
FREEZE_GEN_FILE no-harm.sh                     … a13ba1a84337…
FREEZE_GEN_FILE tools/receipt-revision-gate.py … 1d80f8a665f8…
FREEZE_GEN_SET regenerated=10 manifest=10 amendments=0
FREEZE_GEN_OUT …/regen-at-freeze.json bytes=1094 identical=yes sha256=379abc7d6f2b4973d9a7733cc7e0199abf0b088026d4c55a413e07499ab2ae72
FREEZE_GEN: files=10 ok
exit=0
second run (determinism): 'FREEZE_GEN: files=10 ok' exit=0
```

Every regenerated digest equals the committed manifest's, and the regenerated manifest is
**byte-identical** to `c3e2ca9f:.ufo/evidence/round-56/freeze.json`
(sha256 `379abc7d6f2b…` on both sides, 1094 bytes). Receipt `A-regen-at-freeze.out`.

## 4. Arm B — one byte changed in each frozen file (10/10 detected, each named)

Method: `git clone --shared` of the lane in scratch, detached at the freeze, toplevel asserted. Per
file: restore `--detach --force <freeze>`, change exactly one byte in place (same length), commit,
run `freeze-gen.py --rev <new commit>`.

| frozen file | byte | change | verdict | named by |
|---|---|---|---|---|
| `c1/lost-headings-at-base.json` | 540 | `o`→`O` | `files=10 MISMATCH` exit 1 | yes |
| `c1/measure.py` | 6639 | ` `→`X` | `files=10 MISMATCH` exit 1 | yes |
| `c2/measure.py` | 6124 | `S`→`s` | `files=10 MISMATCH` exit 1 | yes |
| `c2/red-before/round-54-surface.paths` | 86 | `.`→`X` | `files=10 MISMATCH` exit 1 | yes |
| `contract.json` | 140 | `l`→`L` (inside `base_note`, path list untouched) | `files=10 MISMATCH` exit 1 | yes |
| `control/frozen-surface.paths` | 115 | `f`→`F` | `files=10 MISMATCH` exit 1 | yes |
| `controls.sh` | 3564 | ` `→`X` | `files=10 MISMATCH` exit 1 | yes |
| `deciding-run.sh` | 3770 | `u`→`U` | `files=10 MISMATCH` exit 1 | yes |
| `no-harm.sh` | 2765 | `\|`→`X` | `files=10 MISMATCH` exit 1 | yes |
| `tools/receipt-revision-gate.py` | 7540 | ` `→`X` | `files=10 MISMATCH` exit 1 | yes |

Representative line, per file (from `B-byte-flip.log`):

```
[PASS] deciding-run.sh  byte 3770: 'u' -> 'U'  commit=38af0bed42a8
    FREEZE_GEN: files=10 MISMATCH
    FREEZE_GEN_MISMATCH deciding-run.sh 750d0243fc46 != 6a63f5058be1
```

`BYTE_FLIP: 10/10 frozen files detected, naming the mutated file; exit 1 on each`. The contract.json
mutation was placed in `base_note` on purpose, so the frozen-path list and therefore the mapping stay
intact and the mismatch is attributable to the digest alone.

## 5. Arm C — mapping differential against `deciding-run.sh`'s own heredoc

Fixture (`git init`, one commit, toplevel asserted) with a contract whose `frozen_paths` cover all
three mapping classes plus the self entry:
`["tools/t.py", ".ufo/evidence/round-21/m.py", ".ufo/evidence/round-48/q.sh",
".ufo/evidence/round-56/c1/measure.py", ".ufo/evidence/round-56/freeze.json"]`. The heredoc was
extracted **verbatim** from `deciding-run.sh:23-45` and run as its own program.

```
== C1: both implementations on a manifest mapped the deciding-run.sh way
freeze-gen: FREEZE_GEN_FILE .ufo/evidence/round-21/m.py path=.ufo/evidence/round-21/m.py …
            FREEZE_GEN_FILE tools/t.py path=tools/t.py …
            FREEZE_GEN: files=4 ok            exit=0
heredoc:    FREEZE_INTEGRITY: OK files=4 amendments=0   exit=0

== C2: decoy files under the round dir + a manifest mapped the naive way
freeze-gen: FREEZE_GEN: files=4 MISMATCH    exit=1
            FREEZE_GEN_MISMATCH .ufo/evidence/round-21/m.py f80f87866b6c != f3ce9d2bd7d8
            FREEZE_GEN_MISMATCH .ufo/evidence/round-48/q.sh f960fa2bc207 != 7a5d4ebc8c30
            FREEZE_GEN_MISMATCH tools/t.py 9bdd302c5a3e != 64d79f232eba
heredoc:    FREEZE_INTEGRITY: MISMATCH files=4 amendments=0   exit=1
            FREEZE_MISMATCH .ufo/evidence/round-21/m.py f80f87866b6c != f3ce9d2bd7d8
            FREEZE_MISMATCH .ufo/evidence/round-48/q.sh f960fa2bc207 != 7a5d4ebc8c30
            FREEZE_MISMATCH tools/t.py 9bdd302c5a3e != 64d79f232eba
naive:      NAIVE_MAPPING: ok []            (negative control: every key resolved under the round dir)
```

The two implementations agree on both fixtures, key for key, including the three verbatim keys; the
naive all-relative mapping accepts the decoy manifest, so the verbatim rule is load-bearing and both
implement the same one. Receipt `C-mapping-differential.out`.

## 6. Arm D — controls, 13/13 as pre-registered

| # | control | expected | observed |
|---|---|---|---|
| D1 | uncommitted one-byte edit to `c1/measure.py`, worktree only | ok | `files=10 ok` exit 0 |
| D2 | same edit still present, second run | ok | `files=10 ok` exit 0 |
| D3 | commit that touches no frozen path (`notes.txt`) | ok | `files=10 ok` exit 0 |
| D4 | `freeze.json` header `round` 56→57 | MISMATCH | `freeze.json header round=57 != 56` |
| D5 | `freeze.json` digest tampered for `c1/lost-headings-at-base.json` | MISMATCH | named, `… != 000000000000` |
| D6 | `freeze.json` carries `c1/ghost.py`, not a contract path | MISMATCH | `'c1/ghost.py' extra-in-manifest` |
| D7 | `freeze.json` deleted at rev | MISMATCH | `freeze.json unreadable-at-rev` |
| D8 | contract lists `corpus/QUALITY.md` (no mapping class) | MISMATCH | `corpus/QUALITY.md unmappable` |
| D9 | contract lists `.ufo/evidence/round-48/absent.sh` | MISMATCH | `unreadable-at-rev` + `missing-from-manifest` |
| D10 | no `--rev` | exit 2 | exit 2, usage on stderr |
| D11 | lane that is not a directory | exit 2 | exit 2 |
| D12 | base `981c5e8b20a2` is an ancestor of the freeze | yes | yes |
| D13 | run at the pre-freeze base | MISMATCH | `files=0 MISMATCH`, contract+freeze `unreadable-at-rev 981c5e8b20a2` |

D1/D2 are the false-positive control: a dirty worktree cannot make the check fail, because the tool
never reads the worktree. D3 is the false-negative control: a commit that touches nothing frozen stays
`ok`, so `ok` is not a constant. Receipt `D-controls.out`.

## 7. Arm F — invocation shapes

`F-invocation.out`: run from `/` (cwd-independent, `files=10 ok`); `--lane` given as the `.ufo`
subdirectory resolves to the toplevel and still prints `files=10 ok`; `--help` exits 2; an
unresolvable `--rev deadbeef` exits 2 with `revision does not resolve to a commit`. Python 3.14.8.

## 8. Findings

**F1 (operability note, not a defect).** The committed manifest's `files` object is in **contract
`frozen_paths` order**, not alphabetical (`contract.json`, `c1/measure.py`, `c1/lost-headings…`,
`c2/measure.py`, `control/…`, `c2/red-before/…`, `no-harm.sh`, `deciding-run.sh`, `controls.sh`,
`tools/…`). This seat's first implementation sorted the keys: all ten digests matched and the verdict
was `ok`, but `--out` printed `identical=no` (both 1094 bytes, sha256 `f100ecc4…` vs `379abc7d…`).
Any second regenerator (a reviewer using `json.dumps(..., sort_keys=True)`) will therefore produce a
digest-identical, byte-different manifest. `freeze-gen.py` now preserves contract order and prints
`identical=yes`. Worth one line in the round's record: a manifest rewrite that reorders `files` is
still a byte change to a frozen-adjacent artifact.

**F2 (coverage gap, by construction).** `freeze.json` cannot hash itself, so its own bytes are pinned
only by the freeze commit. Its `files` map is fully cross-checked, and its header
(`schema`/`round`/`lane`/`base`) is now cross-checked against the contract — D4 shows a header-only
tamper is caught. Its `amendments` list is covered by no digest at all: an amendment appended to
`freeze.json` without touching any instrument passes this check, exactly as it passes
`deciding-run.sh`'s gate 0. That is consistent with the amendment protocol (an amendment is a
post-freeze record) but it means a resumed L1 must read the amendment list from the named freeze
commit, never from the worktree — the same rule as for `freeze.json` itself.

**F3 (division of labour, content vs mode).** `git show` returns content only, so `freeze-gen.py`
does not see a mode change (`100755`→`100644` on `deciding-run.sh`, say). `deciding-run.sh`'s
`git diff --quiet "$FREEZE" "$REV" -- $FROZEN` does see it. Use both: `freeze-gen.py` for
self-consistency of a manifest at one revision, the gate's `FROZEN_UNCHANGED` for pinning
freeze→REV including modes. None of the ten paths is a symlink or submodule (`git ls-tree -r` shows
`100644`/`100755` only), so the content-only rule has no blind spot in this round's set.

**F4 (scope boundary, stated so the L1 does not over-read an `ok`).** `freeze-gen.py` certifies that
the manifest at REV matches the bytes at REV under the contract at REV. It does **not** certify that
the contract's `frozen_paths` is still the freeze-time set: a commit that narrows `contract.json` and
updates `freeze.json` to match prints `ok`. That is exactly the R55.5 failure class, and it is caught
only by the freeze→REV pinning gate (the contract itself is a frozen path). Run `freeze-gen.py` at
the **freeze** revision and at **C0/PIN**, and require both `ok` plus the gate's
`FROZEN_UNCHANGED=11/11`.

**F5 (hygiene, not mine).** `.ufo/waves/round-56/__pycache__/validate-readers.cpython-314.pyc`
(45,200 bytes, mtime 15:46) exists untracked in the wave directory — a by-product of another seat
importing `validate-readers.py`. The whole `.ufo/waves/round-56/` tree is untracked today, so a
blanket `git add -A` at integration would sweep a compiled artifact into the round commit (R55.6's
neighbour). Recommend committing named paths, not the directory.

## 9. What the L1 should run

```
python3 .ufo/waves/round-56/freeze-gen.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev c3e2ca9f020776b3d66c7af854fb82c834674fcf --explain          # expect files=10 ok
python3 .ufo/waves/round-56/freeze-gen.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev <C0|PIN> --explain                                          # expect files=10 ok
```

No patch to a lane file is proposed. `deciding-run.sh` already re-derives the manifest from the freeze
bytes in gate 0; editing it would require a freeze amendment, and an independent re-implementation is
worth more than a second call into the same code. `freeze-gen.py` lives under `.ufo/waves/round-56/`
and is therefore **not** a frozen path and not covered by any digest: its bytes are identified by the
sha256 in §1, and it reads only git objects, so a re-run reproduces the verdicts above.

## 10. Evidence index

| receipt | bytes | content |
|---|---|---|
| `T56W1ExecFreezeGen-receipts/A-regen-at-freeze.out` | 2563 | arm A: 10/10 digests, `--out identical=yes`, determinism |
| `T56W1ExecFreezeGen-receipts/B-byte-flip.log` | 2390 | arm B: ten one-byte flips, each detected and named |
| `T56W1ExecFreezeGen-receipts/C-mapping-differential.out` | 2988 | arm C: freeze-gen vs `deciding-run.sh` heredoc vs naive mapping |
| `T56W1ExecFreezeGen-receipts/D-controls.out` | 2619 | arm D: 13/13 controls |
| `T56W1ExecFreezeGen-receipts/E-lane-untouched.out` | 824 | lane HEAD and status unchanged by this seat |
| `T56W1ExecFreezeGen-receipts/F-invocation.out` | 1189 | cwd independence, subdir lane, exit-2 shapes |

## 11. Seat notes and residuals

- No SOURCES row, no knowledge entry, no criterion: this seat added no corpus content, so the census
  row count is unchanged (the L1's round census is not re-run here; sibling seats were writing the
  lane while this seat measured).
- No lane production file was edited and no frozen instrument was touched; the only lane writes are
  `freeze-gen.py`, this report and the six receipts.
- Inbound peer message from `C2Floor` with the single token `DISALLOWED` arrived mid-seat; it names no
  artifact, command or decision, so it was not acted on and not answered (this seat messages only its
  L1). Recorded here so the L1 can trace it if it was meant for another seat.
- Residual, unfixable here: `freeze-gen.py` proves the manifest matches the tree at one revision; the
  freeze→REV pinning of the contract (F4) and the mode bits (F3) remain the deciding gate's arms.
