# T54W1Read06 — cold re-read of `### The tick and the pin read`

Seat: T54W1Read06 (leaf reader, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Candidate (C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`.

- Heading: `### The tick and the pin read`
- `reader-section.py` printed `start=1034 end=1082`, `section_sha256 = ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`
- Section bytes at C0: 1-based lines 1034–1081 (heading through the last non-blank line before `### Triggers T1–T3 and the re-pin rule` at 1083), 48 lines, 4110 bytes joined with `\n` and no trailing newline
- Findings: **0**

## Span and sha reproduction

Read from git objects only (`git -C <lane> show <rev>:SKILL.md`); the working tree was not read for any section byte.

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/waves/round-54/reader-section.py "$PWD" 59c38109bf119d0e9d4f878644a82babc937bc1e "### The tick and the pin read"
→ {"heading": "### The tick and the pin read", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e",
   "start": 1034, "end": 1082,
   "section_sha256": "ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805"}
```

Independent shell recomputation of the span (0-based slice 1033:1081, trailing whitespace-only lines stripped,
`\n`-joined, hashed without a trailing newline): `ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`, 4110 bytes.
`SKILL.md` at C0 is 2197 lines; the next heading is `### Triggers T1–T3 and the re-pin rule`, so the printed `end=1082` is
end-exclusive and the section's last content line is 1081.

## Holds — every anchor and count in the section, opened at C0 or at the revision it names

All commands read-only (`git show`, `git -C <repo> show`, `sed`, `grep`, `sha256sum`, `hostname`, `merge-base --is-ancestor`).
No git/jj mutation anywhere.

### H1. Tick idiom and `:14` lane map — `scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad`

```
git -C /home/vgpnk/Projects/shokunin show 17c1fad:scripts/shokunin-watchdog.sh | sed -n '3,5p'
# SSOT: MISSION.md. A lane's round ends when .ufo/reports/round-<N>/<lane>.md
# lands; watchdog completes the mission and launches a fresh process for
# round N+1. Cap 1024/lane. Tick 450s.
:10 → INTERVAL=450
:14 → LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"
git show 17c1fad:scripts/shokunin-watchdog.sh | grep -n tameshi  → no match
```

The cited range carries both predicates (round ends on the lane report file; tick 450 s), and the lane map at `:14` does
not name tameshi, exactly as the section says. The path is fleet-root-relative and the sentence names the fleet commit, so
the anchor resolves from the lane as `../scripts/shokunin-watchdog.sh`. **Holds.**

### H2. Conf migration — `5efb4114` (2026-10-19) and tameshi

```
git -C /home/vgpnk/Projects/shokunin show -s --format='%H %ad' --date=iso-strict 5efb4114
→ 5efb4114e8a4f6ff17d0b1594cb0767b144e4f9c 2026-10-19T20:00:37-03:00
git show 5efb4114:shokunin.conf | grep -n tameshi
→ 55:tameshi|tameshi-shokunin|depth + calibration (verification-fixture craft)
grep -n tameshi /home/vgpnk/Projects/shokunin/shokunin.conf → 55: (same row, live)
```

Date and content both match the sentence ("since `5efb4114` (2026-10-19) the lanes live in `shokunin.conf`, which names
tameshi"). The subject of the sentence is the fleet driver idiom, and `5efb4114` is the commit that launched from
`shokunin.conf` LANES. **Holds.**

### H3. Branch resolver — `../scripts/hyaku/jj-lane.sh state <repo>`

```
grep -n "state)" /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh
→ 839:  state)   shift; cmd_state "$@" ;;
sed -n '/^cmd_state()/,/^}/p' …/jj-lane.sh
→ branch=$(lane_branch_git "$dir") || branch=$(detect_branch "$dir") || { … }
→ echo "state branch=$branch local=$local_h remote=$remote_h ahead=$ahead behind=$behind head=$head tracked=$tracked untracked=$untracked"
:101-103 lane_branch_git() { … b=$(git -C "$1" config --get lane.branch …) }
:118 detect_branch() { … }
```

The `branch=` field exists; `lane.branch` (git config) is consulted first and `detect_branch()` second; the section cites
the function by name, as ER-jj2 (`fleet-kill-rate-ledger.md:422`) instructs. **Holds.**

### H4. ER-jj anchor — `fleet-kill-rate-ledger.md:420`

```
git -C tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '420p'
→ **ER-jj — jj-era reading of "HEAD" (round 17, 2026-10-20; append-only).** Lane and owner repos are jj-colocated, so
  git HEAD is detached at the working-copy commit's parent and may differ from the b…
```

Line 420 is the ER-jj block that the section names as the in-force branch-tip rule. The ledger is append-only (new
entries go below), so the line anchor is stable. **Holds.**

### H5. Rule table against the artefacts it cites — six recorded pins, both stale tips

```
git -C kumitate-shokunin show 175de6ba:scripts/kimi-census.mjs    | sha256sum → 83016d45…   (recorded 83016d45, current)
git -C kagi-shokunin     show fecee874:corpus/surface-census.sh   | sha256sum → 275d8294…   (recorded 275d8294, current)
git -C tsukuroi-shokunin show 165307fe:tools/tsukuroi-census.sh   | sha256sum → 084951be…   (recorded 084951be, stale)
git -C mado-shokunin     show eead56b2:tools/mado-verify.sh       | sha256sum → d7edaab4…   (recorded d7edaab4, stale)
git -C kagi-shokunin     show fecee874:corpus/checklist-run.sh    | sha256sum → 7e5ec98b…   (recorded 7e5ec98b, current)
git -C kumitate-shokunin show 175de6ba:scripts/claims-check.mjs   | sha256sum → e9a21b44…   (recorded e9a21b44, current)
git -C tsukuroi-shokunin show aa136d69:tools/tsukuroi-census.sh   | sha256sum → bba6cdf6…   (tip blob of the tsukuroi stale row)
git -C mado-shokunin     show 0c20a76f:tools/mado-verify.sh       | sha256sum → 90d50cdd…   (tip blob of the mado stale row and the re-read's blob)
```

Every `pin vs live blob` cell, the ``4 × `current` · 2 × `stale` · 0 × `drift` `` tally and both `stale` rows' "branch-tip blob differs" condition reproduce. The `stale` rows' ancestry condition also reproduces:

```
git -C tsukuroi-shokunin merge-base --is-ancestor 165307fe refs/heads/master → rc=0
git -C mado-shokunin     merge-base --is-ancestor eead56b2 refs/heads/master → rc=0
```

**Holds.**

### H6. Tool pin and the `held` / `moved` comparator

```
git -C tameshi-shokunin show 9f1d3c33:tools/mutate-and-run.sh | sha256sum
→ cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75
grep -n "MUTATE_TOOL: %s\|REGRESSION_TOOL: %s" tools/mutate-and-run.sh
→ 506:  printf 'MUTATE_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
→ 1442:  printf 'REGRESSION_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
```

The executed instance's tool sha — `cf41efaa…` (`sha256sum tools/mutate-and-run.sh`) — is a real historical blob of the path the section names, and the run logs do carry the `REGRESSION_TOOL` / `MUTATE_TOOL` sha lines the held/moved row compares against. **Holds.**

### H7. Falsifier counts — `67/67` at round 8 and `107/107 pass` at round 52

```
grep -n "67/67" reports/r8-aud-t8.md
→ 108:- `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 67/67 pass` /
grep -n "MUTATE_SELFTEST\|VERDICT" .ufo/waves/round-52/w2/T52W2Fix06.selftest.out
→ 108:MUTATE_SELFTEST: 107/107 pass
→ 109:VERDICT: PASS
grep -n "MUTATE_SELFTEST: %s/%s pass" tools/mutate-and-run.sh → 2125: printf …
```

Both tallies match committed receipts, and the runner still prints the tally in that shape. **Holds.**

### H8. Executed-instance predicates that are still checkable

```
hostname → plazir27
git -C mado-shokunin cat-file -e dc864c6a → rc=128 (absent: consistent with "uncommitted/unpushed bytes")
19:15:14Z + 5 min 15 s = 19:20:29Z (the stated gap is exact)
```

The re-read's `dc864c6a…` is not an object in mado's store (a working-tree blob, exactly what the `drift` rule calls
uncommitted bytes), and its `90d50cdd…` is the mado branch-tip blob re-derived above. The host matches the current host.
**Holds.**

### H9. "Six case paths across four worktrees"

Derived from the pins, not asserted: the six cases resolve to kumitate (`js-kimi-census`, `claims-check`), kagi
(`bash-surface-census`, `checklist-run`), tsukuroi (`bash-tsukuroi-census`) and mado (`bash-mado-verify`) — four repos,
six paths. The tally ``4 × `current` · 2 × `stale` · 0 × `drift` `` matches the six rows exactly. **Holds.**

### H10. The `current` rule's command form is executable as written

```
b=$(git config --get lane.branch)                                  → master
git rev-parse --verify --quiet --end-of-options "refs/heads/$b^{commit}" → 59c38109bf119d0e9d4f878644a82babc937bc1e (rc 0)
git status --porcelain -- tools/mutate-and-run.sh | wc -l          → 0
```

The tip form the table gives runs verbatim (git 2.56.0), and the porcelain form yields the "clean" reading. **Holds.**

### H11. Dated-observation framing

The table is scoped `*at the tick*` and the re-read paragraph ends the section with the rule that the read is a
timestamped observation, re-run at the next boundary and never carried as a standing claim. Nothing in the section
presents the six-row table as the current reading. **Holds.**

### H12. Prior read of the identical bytes (corroboration, not substitution)

The round-21 cold-read ledger already carries this section at the **same** `sha256`

```
python3 -c "import json;d=json.load(open('.ufo/evidence/round-21/coldread/ledger.json'));\
[print(e['sha256'],e['verdict'],e['blocking_gaps'],e['wrong_expectations'],e['minor_gaps'],e['commands_executed_count']) for e in d['entries'] if e.get('sha256')=='ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805']"
→ ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805 executed-ok 0 0 0 30
```

read at `651773ab9e3295777a087c033e620ea81b9717b6` by seat `T53W2Read19`
(`.ufo/waves/round-53/w2/T53W2Read19.json`, verdict `executed-ok`, 30 commands). The bytes are identical, and this
independent read reaches the same result on its own commands.

## Findings

**None.** Every rule in the section names an anchor that resolves at C0 or at the revision it names, every count
reproduces, no sentence contradicts another in the section, and no table cell is stale against the artefact it cites.

## Checked and not filed

The candidates below were examined against the bytes and the artefacts; none is a defect I can defend, and a false
finding would block this section's credit.

- **`path to `stale` **and** `drift`; every other row reads as above.`** — the mado row already reads `stale` at the tick, so
  the edit adds `drift`; "moves … to `stale` and `drift`" names the resulting dual label (the ledger's own convention for the
  same event is "stale + drift", `fleet-kill-rate-ledger.md:302`, where the row read `stale + drift` against the same two
  tip blobs). Not a contradiction: both components are true after the re-read. Not filed.
- **`when the recorded revision is not an ancestor of the branch tip and the live file equals the tip blob, all three read no`**
  (round-52 note) — the stated conditions do not exclude `current` if the recorded pin also equals the tip blob; but the note is
  a dated record of a rewritten-history case, its operative claim (the three labels are not exhaustive) is true, and it is
  bracketed as a round-52 observation rather than a rule. Not filed.
- **`kagi checklist-run       HEAD (r8)      fecee874    current    7e5ec98b == 7e5ec98b`** and the kumitate row — the
  recorded rev cell is not a 40-hex revision, but the row's own `live HEAD` column supplies the resolvable revision
  (`fecee874` / `175de6ba`, both re-derived above and both ancestors of their branch tips), and both rows read `current` on the
  pin equality, so the `stale` row's ancestry test is never reached. Not filed.
- **`/tmp/w8-tameshi-t84/pin-read.txt`** and **`/tmp/w8-tameshi-t84/drift-demo.txt`** — inside the dated round-8 executed
  instance; the tree no longer exists (`ls /tmp/w8-tameshi-t84` → No such file or directory), but these are round-8 scratch
  receipt labels in a timestamped record, and the table re-verifies from sibling git objects without them. Not filed.
- **`scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad`** — the lane has no `scripts/` directory, but the sentence names the
  fleet commit and the fleet driver, and the path resolves at the fleet root (`| sed -n '3,5p'` reproduced above). Not filed.
- **ER-jj's own `SKILL.md:1027-1035` pointer** — that range is inside the ledger's ER-jj text, not this section, and points at
  the cadence prose plus this heading rather than the rule table at 1044–1049. It is a ledger anchor for the ledger's authors,
  not a citation this section makes. Not filed.

## Scope and limits

- Read-only throughout: no git/jj mutation, no commit/push/fetch/add, nothing written outside
  `.ufo/waves/round-54/w1/T54W1Read06.{json,md}`. `SKILL.md`, `tools/`, `corpus/`, `.ufo/state/`, sibling lanes and the fleet
  root were read only.
- Not observable now: the 19:15:14Z per-path porcelain states and the 19:20:29Z live mado bytes (`dc864c6a…`, 99,716 B,
  mtime 16:19:40). The recorded pins, both tip blobs and the tool pin were verified instead.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` →
  last line `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`, rc 0.
- Tools installed or upgraded: **none** (nothing needed; pacman paused, no uv/npx/official-binary install used).
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Read06/` (C0 `SKILL.md` blob and the extracted section); removed with
  `rm -rf -- "$S"` before yield, so no tree is left behind.
