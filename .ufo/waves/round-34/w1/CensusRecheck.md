# CensusRecheck (tameshi r34 w1)

Observed 2026-10-23T19:42:28Z. No packages installed.

## Verdict

The four assigned assertions hold. This run's stdout is byte-identical to the landed receipt `.ufo/evidence/round-34/census-end.stdout` (sha256 `19f1d44f91a2c7794c01e4a11922d921effde17ffec2a9e9408d0782c654eea1`). No defect in that receipt. `c1-measure.py` was not run.

| Assertion | Result |
|---|---|
| census exit 0 | holds (`census.exit` = `0`) |
| `tameshi` `ok` line present | holds (1 line) |
| 98 rows, `grep -c '^| S'` | holds (live file and tip blob) |
| W04 set = the 8 known duplicate-url warnings | holds (`cmp` exit 0 vs r32, r33, and r34 receipts) |

The full tail is 10 lines, not 8. Line 9 is `W01` for S101 (tier C, mined, used-by set). That line is in the landed r34 receipt. It is not a W04 and does not change the exit (`sources-census.sh` header: W-codes do not fail validate). E-code lines: 0. stderr: empty.

## Pins (tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`)

Clone (exit 0): `mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/lane && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. `rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`, exit 0.

`git -C /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py` and `:tools/mutate-and-run.sh` (both show exit 0), then `sha256sum` of those blobs:

- `tools/tally-audit-v2.py` = `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` (matches the pin; same hash on the clone worktree and on the live lane file)
- `tools/mutate-and-run.sh` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (matches the pin; same three locations)

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --quiet 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7 -- tools/tally-audit-v2.py tools/mutate-and-run.sh` → exit 0.

## Census command

From `/home/vgpnk/Projects/shokunin`:

```sh
TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi > /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/census.stdout 2> /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/census.stderr
echo $? > /fast/scratch/hyaku/tameshi-r34-seats/CensusRecheck/census.exit
```

- exit: `0` (`census.exit`)
- stderr: empty (`wc -l` = 0)
- script sha256: `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`; fleet HEAD `34ea4ecb418f23d35b4734837dee3891626d3456`)
- stdout sha256: `19f1d44f91a2c7794c01e4a11922d921effde17ffec2a9e9408d0782c654eea1`

### Full tail

```text
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

`grep -c $'\tW04\t'` → 8, exit 0. `grep -c $'\tok\t'` → 1, exit 0. `grep -c $'\tE[0-9][0-9]\t'` → 0, exit 1 (no match).

### Known-8 identity

The 8 known W04 lines are the W04 block in `.ufo/evidence/round-32/after/census-end.stdout`, `.ufo/evidence/round-33/after/census-end.stdout`, and `.ufo/evidence/round-34/census-end.stdout` (S047, S048, S075, S076, S077, S078, S081, S092, URLs as above). `cmp -s` of this run's W04 lines against each of those three → exit 0. `cmp -s` of the full stdout against the r34 receipt → exit 0. That receipt's `census-end.exit` is the two bytes `0` plus newline (sha256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`).

## Row count

`grep -c '^| S' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` → 98, exit 0.

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:corpus/SOURCES.md | grep -c '^| S'` → 98, exit 0.

`awk 'BEGIN{s=0} /^## /{s=($0 ~ /^## Registry/)?1:0} s && /^\| S/{c++} END{print c+0}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` → 98, exit 0. Ids S001 through S101 with gaps S038, S039, S098. SOURCES sha256 `595c7fa531226d65570d1e3a64e27ae177731b8612a8db5caacaad10b8c62af7` on the live file, the tip blob, and the detached clone.

S101 used-by target exists: `test -f /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md` → exit 0; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin cat-file -e 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:corpus/knowledge/witness-equivalence-rule.md` → exit 0.

## Tree the census actually read

Dispatch tip was `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Live `tameshi-shokunin` HEAD at the run was `a5b1936425d3533b2ce280b16208386dcb0dc4ee` (`rev-parse`). `merge-base --is-ancestor` of the tip into that HEAD → exit 0. `log --oneline TIP..HEAD` is one commit: `a5b1936 round-34: v2 wave evidence`. `diff --stat TIP HEAD` is only `.ufo/waves/round-34/dispatch-w1.json`, `dispatch-w1.stderr`, and `spec-w1.json`. `diff --quiet TIP -- corpus/SOURCES.md` → exit 0, so the registry the live-root census parsed is the tip blob.

## Not a finding

`W01` S101 is disclosed in the landed r34 tail and reproduced here. It is outside the W04 set the assignment fixes at eight. Validation still exits 0 and prints `ok`.
