# OpenCiteCheckPin — C1 ninth leg, pinned target re-opened

Seat: TameshiR26.OpenCiteCheckPin (scout, leaf). Scope: re-open the pinned target only.
Verdict: **PIN CONFIRMED.** Rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` is a real commit in
kumitate-shokunin, it is an ancestor of `origin/master`, it is the **last** commit that touched
`scripts/cite-check.mjs`, and the blob at the master tip is byte-identical. The blob sha256 matches
the frozen contract exactly (`4057344833…0c9f`), at 2537 lines / 126735 bytes / mode 100755. The
hermetic suite run from the pinned bytes alone reproduces `62/62 cases passed (hermetic)`,
`VERDICT: PASS`, exit 0.

Repo root reopened: `/home/vgpnk/Projects/shokunin/kumitate-shokunin` (read-only; no git write
commands, no `jj`, no lane edits). All runs confined to `/tmp`. No tools installed or upgraded.

## 1. Observed facts (exact commands, observed output)

### 1.1 Object type and tree entry
```
$ git -C …/kumitate-shokunin cat-file -t 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a
commit
$ git -C …/kumitate-shokunin ls-tree 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a scripts/cite-check.mjs
100755 blob 9770de8c5a834b2f2adb817f8b0a7ba9e166b87f	scripts/cite-check.mjs
```
Blob id `9770de8c5a834b2f2adb817f8b0a7ba9e166b87f`; `cat-file -s` → `126735`.

### 1.2 Blob content hash at the pin
```
$ git -C …/kumitate-shokunin show 1205…:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  -
$ … | wc -l
2537
```
Matches contract `claims.C1.leg.blob_sha256` and the 2537-line claim. Extracted copy at
`/tmp/citecheck-pin/cite-check.mjs` is 126735 bytes, identical sha256.

### 1.3 Ancestry and master-tip comparison
```
$ git -C …/kumitate-shokunin merge-base --is-ancestor 1205… origin/master ; echo $?
0
$ git -C …/kumitate-shokunin rev-parse origin/master
dfa159d5152ff8449ce04c7e5e7021fa3cce6d30
$ git -C …/kumitate-shokunin ls-tree origin/master scripts/cite-check.mjs
100755 blob 9770de8c5a834b2f2adb817f8b0a7ba9e166b87f	scripts/cite-check.mjs
$ git -C …/kumitate-shokunin show origin/master:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  -
$ git -C …/kumitate-shokunin rev-list --count 1205…..origin/master
70
$ git -C …/kumitate-shokunin log --oneline 1205…..origin/master -- scripts/cite-check.mjs
(empty)
$ git -C …/kumitate-shokunin log -1 --format='%H %ci' origin/master -- scripts/cite-check.mjs
1205c6621a2eccbb8ffceae86d9e7b79a7990b3a 2026-10-14 06:40:03 -0300
```
So: ancestor, **not** the tip (70 commits behind), same blob id and same sha256 at the master tip,
and no commit between the pin and master touches the file. The pin is the file's last-modifying
commit, which is the strongest form of "unchanged at the master tip" available from the object graph.

Reachability from the checked-out commit:
```
$ git -C …/kumitate-shokunin merge-base --is-ancestor 1205… HEAD ; echo $?
0
```
Pin commit metadata: `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, 2026-10-14 06:40:03 -0300, subject
`round-30: doc-repair trio (F1 prose-preserving re-anchor; F4 24 refs re-owned; F3 superseded-revision
historical treatment) + F3 check re-token — --integrations 9/9 first full green since the restructure;
verify-lane clean; pin re-pinned`.

### 1.4 Hermetic suite from pinned bytes only
```
$ h=$(mktemp -d); mkdir -p "$h/home" "$h/tmp"; cd "$h"
$ env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 \
      GIT_CEILING_DIRECTORIES="$h" node /tmp/citecheck-pin/cite-check.mjs --selftest
… 
62/62 cases passed (hermetic)
VERDICT: PASS
SELFTEST_EXIT=0
```
Source-side count agrees: `awk 'NR>=1843 && NR<=2463 && /^\s*check\(/'` → `62`, and
`check = (name, fn) => record(hermetic, name, fn)` at `cite-check.mjs:1853`, with the group pushed
only under `--selftest` at `:2463` and `VERDICT`/exit computed over executed groups at `:2474`,
`:2501-2503`.

**Operational detail (worth routing).** A bare `env -i node …` does not run: PATH is cleared and the
shell reports `env: 'node': No such file or directory`, exit 127. The contract's own suite line
(`contract.json` → `claims.C1.leg.suite`) supplies `PATH="$PATH"`, `HOME`, `TMPDIR`; that is the
operative form. The shorthand `env -i node "$MUTANT" --selftest` in the wave brief is lossy — a
copy-fidelity trap for any future seat that transcribes it literally.

### 1.5 The pin is enforced, not merely recorded
```
tools/mutate-and-run.sh:619  PIN_CITECHECK=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
tools/mutate-and-run.sh:620  REV_CITECHECK=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a
tools/mutate-and-run.sh:1424-1427  regression_case_git js-cite-check \
    'kumitate-shokunin/scripts/cite-check.mjs' "$PIN_CITECHECK" "$REV_CITECHECK" … 
```
The runner header states the leg is materialized from the object store (`git show <rev>:<path>`) and a
"missing repo/rev/blob or a pin mismatch is a SETUP refusal" (`tools/mutate-and-run.sh:216-218`).
Recorded artifacts agree with this pin: `regression-worktree.stdout:45` →
`REGRESSION_PIN js-cite-check: source=git repo=…/kumitate-shokunin rev=1205… path=scripts/cite-check.mjs
mode=100755 sha256=4057344833…`; `sweep/sweep.txt:3` → `MUTATE_TARGET … sha256=4057344833… bytes=126735`;
`:5` → `CONTROL: GREEN (exit=0 … pristine-sha256=4057344833…)`; `:104` → `MUTATE_RESTORE: OK` with
before/after/pristine all equal. The spec and predictions carry the same rev and sha
(`cite-check.defects.spec:2`, `predictions.json:4-5`).

## 2. Header quotes defining the exit map and the hermetic suite group

Pinned bytes, `scripts/cite-check.mjs` (line numbers from `git show 1205…:scripts/cite-check.mjs`).

Exit map — `:69-70`:
> "exit 0 CLEAN · 1 DRIFT (error, or warn under --strict) · 2 fail-closed (missing/non-dir --src or
> --self, empty scan set, zero resolutions)"

and `:71`:
> "64 usage error. No file text, env value, or symbol body is ever printed."

Suite groups — `:73`:
> "Suite groups (--selftest | --integrations)"

hermetic group — `:74-75`:
> "hermetic     fixture-only checks over a synthetic tree in the system temp dir."

`:75-76`:
> "Never reads --src or --self; MUST PASS in any repo state. This is the whole of --selftest."

## 3. Working-tree state (context only — this is not the pin)

`GIT_OPTIONAL_LOCKS=0 git status --porcelain=v1 -b`:
```
## HEAD (no branch)
 D .ufo/waves/round-39/probe/floor-probe.mjs
 D .ufo/waves/round-39/probe/measure-c1.py
 M SKILL.md
 M corpus/QUALITY.md
 M corpus/SOURCES.md
?? .ufo/waves/round-39/build-dispatch.json
?? .ufo/waves/round-39/build-spec.json
?? .ufo/waves/round-39/build/
?? .ufo/waves/round-39/probe/floor-probe.mjs.txt
?? .ufo/waves/round-39/probe/measure-c1.py.txt
```
HEAD is detached at `dfa159d5152ff8449ce04c7e5e7021fa3cce6d30` = `origin/master`. The leg's own file
is untouched in the working tree: `sha256sum scripts/cite-check.mjs` →
`40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, identical to the pin. The local
round-39 changes are someone else's business; they do not reach this leg, because the runner reads the
object store rather than the working tree.

## 4. Inference (marked)

- `[INFERENCE]` Because the pin is the last commit touching the file and the master-tip blob id is
  identical, any future mutation sweep materialized at that rev is byte-equivalent to a sweep at the
  current master tip. This holds now; a future commit to `scripts/cite-check.mjs` on master would end
  the equivalence while leaving the pin itself valid.
- `[INFERENCE]` The 70-commit distance is irrelevant to pin integrity: content identity, not position,
  is what the leg consumes.

## 5. Remaining unknowns (not my item, not claimed)

- Signature/provenance of the pin commit beyond ancestry was not examined — no producer-authentication
  claim is made here or implied.
- I did not run any lane gate, sweeper, selftest or regression **in the lane**; the `62/62` figure above
  comes from the pinned bytes in `/tmp`, which is a suite check, not a lane gate result.
- Whether the sweep verdict table equals these pin bytes is already witnessed by `results.tsv` and the
  `MUTATE_TARGET` sha; I did not re-execute the ten mutants.

## 6. Smallest safe correction

One wording fix, for the wave brief rather than the repo: the C1 suite shorthand
`env -i node "$MUTANT" --selftest` cannot execute (exit 127, empty PATH). Use the contract's full line
(`contract.json` → `claims.C1.leg.suite`) verbatim, which carries
`PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h"`.
No production file was edited by this seat; this report is the only write.
