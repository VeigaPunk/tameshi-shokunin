seat: CritJudge01

# Round-45 w2 — C1 falsify review (independent re-judgement), rows S084, S107, S159

Inputs at commit `ad5942c6e9858af19d00000b58439b321ddfa62b`: ledger `.ufo/evidence/round-45/freshness/ledger.json` (sha256 `433a624bf8cdd42ccf2ea2a818aa0bdc40dd2c77cd636e1121d0aa51eb5a9913`, identical to the worktree copy), committed snapshots under `.ufo/evidence/round-45/freshness/sources/`, author reports `.ufo/waves/round-45/w1/{ExecRows14,ExecRows21,ExecRows24}.md`. I am not the author of any of these entries.

## Verdicts

S084 agree — reviewer CritJudge01 — live `https://docs.python.org/3/library/os.path.html` sha256 `f9c52515…` equals both the entry `raw_sha256` and the committed snapshot, and the quote is the first sentence of the `os.path.realpath` entry directly under its signature inside the anchored first paragraph, whose next sentences ("By default, the path is evaluated up to the first component that does not exist, is a symlink loop … appended unchanged") still ground the non-strict identity-vs-sandbox reading of `teaches`.
S107 agree — reviewer CritJudge01 — live `raw.githubusercontent.com/tensorflow/federated/4d3a89c9…/docs/golden_tests.md` sha256 `eb9dcedc…` equals the entry and snapshot, and the quote is the second sentence of the anchored `## How do I update `.expected` files?` section, immediately preceded by the live `--test_arg=--update_goldens` update sentence, so both conjuncts of `teaches` (update only via the flag; resulting diff checked) hold.
S159 agree — reviewer CritJudge01 — live `https://en.wikipedia.org/wiki/Mutation_testing` sha256 `616dd5a5…` equals the entry and snapshot and carries `"wgRevisionId":1373580212`, and the quote is the opening sentence of paragraph `mw-w` in section `mwcw` (*Mutation testing overview*) whose preceding anchor paragraph `mw-Q` states "The resulting program is behaviorally equivalent to the original one. Such mutants are called equivalent mutants.", so both conjuncts of `teaches` hold.

Registry rows read (worktree, unchanged from the freeze rev):
- `corpus/SOURCES.md:93` — S084, scope "canonical-path semantics of os.path.realpath for fleet-root/sibling identity, not filesystem isolation", anchor "os.path.realpath, first paragraph, Python 3.15.1 documentation opened 2026-10-21", teaches "…non-strict mode may still leave missing or looping components, so it is identity, not a sandbox".
- `corpus/SOURCES.md:119` — S107, scope "F4 explicit update flag for an expected-value file", anchor "§How do I update .expected files? at commit 4d3a89c9…, snapshot sha256 eb9dcedc".
- `corpus/SOURCES.md:129` — S159, scope "the equivalent-mutant definition and its standing as the field's central obstacle…", anchor "§Mutation testing overview, p ids mw-Q and mw-w … snapshot .ufo/evidence/round-43/sources/wikipedia-mutation-testing.html 170793 B sha256 6e4a06c0 revid 1373580212".

## Provenance — sha256 comparison (live vs entry vs snapshot)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-CritJudge01/S084.live 'https://docs.python.org/3/library/os.path.html'; sha256sum S084.live
f9c52515afbea4010d17b851ef344e4b6eda6806a503c02e8872f606a4fa0343  S084.live
$ git -C <lane> show ad5942c6e9858af19d00000b58439b321ddfa62b:.ufo/evidence/round-45/freshness/sources/S084.raw.gz | gunzip -c | sha256sum
f9c52515afbea4010d17b851ef344e4b6eda6806a503c02e8872f606a4fa0343  -      # entry raw_sha256: f9c52515…0343 — EQUAL
$ curl … -o S107.live 'https://raw.githubusercontent.com/tensorflow/federated/4d3a89c9b72f9c19352318d1457a5f7c01462824/docs/golden_tests.md'; sha256sum S107.live
eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe  S107.live
$ … sources/S107.raw.gz | gunzip -c | sha256sum
eb9dcedcb042ab6af1d32b7d83e6f719826511951de33c49d0c3de94544c2abe  -      # entry raw_sha256: eb9dcedc…2abe — EQUAL
$ curl … -o S159.live 'https://en.wikipedia.org/wiki/Mutation_testing'; sha256sum S159.live
616dd5a510906c44e40c92c839ea7f8e2ed225967cde29b13d197d1baf92d71f  S159.live
$ … sources/S159.raw.gz | gunzip -c | sha256sum
616dd5a510906c44e40c92c839ea7f8e2ed225967cde29b13d197d1baf92d71f  -      # entry raw_sha256: 616dd5a5…d71f — EQUAL
```

All three: live bytes byte-identical to the committed snapshot and to the entry's `raw_sha256` — no dynamic-chrome divergence path needed. Sizes: 90223 / 2287 / 170794 bytes (matching the authors' reports).

## Located context (`measure.py --extract` on the committed snapshots)

- S084, quote at offset 13955, single occurrence, immediately after `os.path. realpath ( path , / , * , strict = False ) ¶` and before "(if they are supported by the operating system). On Windows, this function will also resolve MS-DOS…". Following sentences in the same paragraph: "By default, the path is evaluated up to the first component that does not exist, is a symlink loop, or whose evaluation raises OSError . All such components are appended unchanged to the existing part of the path." Page header confirms "os.path - Common pathname manipulations - Python 3.15.1 documentation" — the anchor's version string holds. Body content in the anchored paragraph, not title/nav.
- S107, quote at offset 2140 of a 2204-byte document, single occurrence, in body markdown immediately after `## How do I update `.expected` files?` and "`.expected` files can be updated by running the affected test target with the arguments `--test_arg=--update_goldens --test_strategy=local`." Quote shares `resulting, diff, checked, unanticipated, changes` (5 content words) with scope/anchor/teaches.
- S159, quote at offset 72122, single occurrence, in `<p id="mw-w">` inside `<section id="mwcw">` (*Mutation testing overview*, heading at 62289); the anchor's other paragraph `mw-Q` (offset 71818) reads "However, there are cases where it is not possible to find a test case that could kill this mutant. The resulting program is behaviorally equivalent to the original one. Such mutants are called equivalent mutants." Both anchor-named paragraph ids exist and are adjacent. Quote shares 7 content words with scope/anchor/teaches.

## Frozen-predicate confirmation (seat-grade `--check`, never a deciding run)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-CritJudge01/check/S084.json --snapdir /tmp/tameshi-r45-CritJudge01/check
CHECK S084 verified ok      (rc=0)
CHECK S107 verified ok      (rc=0)
CHECK S159 verified ok      (rc=0)
```
Independent predicate arithmetic: quote tokens 16 / 9 / 15 (all within 6–25); content-word overlap 2 (`canonical, path`) / 5 / 7; `quote.lower() in fold(cells).lower()` is False for all three (no quote copied from the row's own source/scope/anchor/teaches cells).

## Errata and calibration observations (none of these is a dispute)

1. `.ufo/evidence/round-45/freshness/ledger.json` S159 `note` (and `.ufo/waves/round-45/w1/ExecRows24.md` §S159) says "page revid changed since round-43". False: both snapshots carry `"wgRevisionId":1373580212`, the same revid the row's anchor pins. The 1-byte size delta (170793 → 170794) is the dynamic `"wgRequestId":"885f2ad0…"` → `"aa287011…"` UUID at snapshot offset ~1948; first byte difference is inside that UUID, and no article text differs. Content is unchanged, so the verdict stands; the note should be corrected at integration (the ledger's own `verdict`/`quote` are unaffected).
2. Row S159's anchor still pins the round-43 sha prefix `6e4a06c0`, which no longer matches live bytes (`616dd5a5`). C1's predicate grades the entry against its own committed snapshot, not the row's anchor pin, so this is not a dispute; a future row edit should re-pin to `616dd5a5` (out of scope this round — lane is read-only).
3. S084 clears the `>= 2` content-word threshold only exactly (2: `canonical`, `path`). It is still a substantive support sentence for the identity reading, so `agree`; noted because a stricter overlap bar would flip it.
4. S107's `teaches` says "updated *only* by passing --update_goldens" while the source says files "can be updated by" that argument list. The anchored section answers exactly "How do I update .expected files?" with that command, so the paraphrase is fair; this is a base-cell wording nuance, not a freshness failure.

## Tooling

No installs. Tools used: `curl`, `sha256sum`, `gzip/gunzip`, `git show` (read-only, `-C <lane>`), `python3` — all already present. RULES.md read per the operator directive; no pacman transaction attempted; no lane mutation beyond this report file; scratch confined to `/tmp/tameshi-r45-CritJudge01/`.

Machine-readable reviews (for L1 integration into `.ufo/evidence/round-45/freshness/reviews.json`): `/tmp/tameshi-r45-CritJudge01/reviews.json` — three `agree` verdicts, reviewer `CritJudge01`, report path `.ufo/waves/round-45/w2/CritJudge01.md`.
