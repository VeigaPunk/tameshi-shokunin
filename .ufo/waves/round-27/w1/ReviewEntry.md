# ReviewEntry — round 27, claim C2 (frontier F8, oracle-anchored survivors)

Reviewer: TameshiR27.ReviewEntry (leaf, no dispatch). Reviewed artifact:
`corpus/knowledge/oracle-anchored-survivors.md` at content revision
`2227d8338c02aa9a5fd7d95c1a41b76865ad7647`, against
`.ufo/evidence/round-27/f8/{anchors.json,receipt.json,probe.stdout,anchor-probe.py}`,
the pinned gate `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`
(kumitate-shokunin), and `corpus/knowledge/mutation-case-kumitate-cite-check.md` §4.
I did not write any reviewed content.

## Verdict

**Faithful. No blocking defect.** Every number, line, quote, exit code, class and
bound in the entry matches the evidence and the pinned bytes; the probe and the
frozen counter both reproduce at the content revision. Two minor findings below
(one wording ambiguity in the entry, one residual-volatility note), neither of
which breaks the claim.

## Findings

### MINOR 1 — ambiguous slice phrasing in the S_PIN_INCLUDES witness cell

- `corpus/knowledge/oracle-anchored-survivors.md:47` says "content pin = digest
  chars 8–20". The probe computes the Python slice `digest[8:20]`
  (`anchor-probe.py:59`, 0-based, end-exclusive) = `02bcfdc3dba1`, which is what
  `receipt.json` records (`witness_facts.pin`, receipt.json:99-102 region:
  digest `9783fae5…`, pin `02bcfdc3dba1`, `pin_is_leading_substring=false`,
  `pin_inside_digest=true`). Under a 1-based inclusive reading, "chars 8–20"
  would be `digest[7:20]` = `502bcfdc3dba1` — wrong. The receipt disambiguates,
  so this is wording, not data. Smallest fix: write "0-based slice
  `digest[8:20]`" or "hex chars 9–20 (`digest[8:20]`)".

### NOTE 2 — six volatile fields in the receipt (no edit required, record only)

- `receipt.json` carries `stdout_sha256` for six json runs (committed lines 28,
  35, 55, 64, 113, 120). My clean rerun reproduced `probe.stdout` byte-identically
  and every verdict field, and differed from the committed receipt in exactly
  those six hashes: the gate's `--json` output embeds the per-run temp paths
  (`anchor-probe.py` builds the witness tree under a random
  `tempfile.TemporaryDirectory`), so the stdout bytes are not run-invariant. No
  claim depends on stdout byte-reproducibility — the entry binds the receipt to
  probe+anchors sha256 and quotes only the `ANCHOR_PROBE` summary line — but a
  future reviewer byte-diffing a fresh receipt will see a six-line diff that is
  expected volatility. Optional hardening (probe is frozen evidence this round):
  scrub paths before hashing, or note the six fields as volatile in the entry's
  `verified-at` line.

## Verified evidence (commands and observed output)

1. **Pinned blob identity.** `git -C kumitate-shokunin show
   1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum`
   → `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`;
   `cat-file -s` → 126,735; `wc -l` → 2,537; `ls-tree` → mode 100755. Matches the
   entry source line, `anchors.json` `blob_sha256`, `receipt.json` `target`, and
   round-26 §0.
2. **Header quotes, all five exact on their named lines** (whitespace-normalized
   substring): gate `:35` "A ref with no owner is ORPHAN_REF (warn)."; `:38`
   "then 7-40 hex"; `:61` "error UNRESOLVED LINE_OOR REV_UNKNOWN PIN_MISMATCH
   SYMBOL_OFF_LINE"; `:69` "exit 0 CLEAN · 1 DRIFT (error, or warn under
   --strict)"; `:71` "64 usage error." All five are header-comment lines; the four
   mutated statements are code lines at `:1312`, `:1589`, `:2512`, `:1195`, so
   the entry's "no survivor edit moves the anchor" holds.
3. **@old uniqueness in the pinned bytes**: `ref.start > n || ref.end > n;` only
   :1312; `opts.strict && totals.warn > 0)` only :1589; `return 64;` only :2512;
   the full `      } else if (digest.startsWith(pin.hex)) {` only :1195 (the
   shorter `digest.startsWith(pin.hex)` also occurs at :1219, the rev-branch
   fallback named by round-26 §3; the anchors @old carries the wrapper, so the
   probe's count==1 guard passes).
4. **Receipt binding.** sha256(`anchors.json`) = `780e1009fc484d364222fa32ee2bd
   960ccccd885d818b1deb44e4fdd82bd5eea` = `receipt.anchors_sha256`; sha256
   (`anchor-probe.py`) = `2d9308ba950c96671d0b50855f4d171ea256f07eace18fa39d7755
   e7a557648d` = `receipt.probe_sha256`; `node --version` → v24.21.0 = receipt.
   The anchors bytes committed at `06a6707904582cc2f268d8a74861c6a8d09dd1fe` hash
   identically to the working-tree file; that commit contains exactly
   `anchors.json` + `anchor-probe.py`, is authored 2026-10-22T09:17:23-03:00, is
   an ancestor of `2227d833…` (authored 09:19:08-03:00), and both are ancestors
   of HEAD — supporting "anchors committed … before the probe ran".
5. **Probe reproduction** (in `/tmp/r27-review`, scratch only): `python3
   anchor-probe.py --kumitate …/kumitate-shokunin --anchors anchors.json --out
   /tmp/r27-review/r.json` → exit 0; stdout byte-identical to
   `.ufo/evidence/round-27/f8/probe.stdout` including `ANCHOR_PROBE: ran=4/4
   anchored_holes=4`; fresh receipt vs committed receipt differs only in the six
   `stdout_sha256` fields (NOTE 2).
6. **Counter at the content revision** (clone at `/tmp/r27-review/clone`):
   `python3 .ufo/evidence/round-27/c2-measure.py --repo <clone> --rev 2227d8338c02
   aa9a5fd7d95c1a41b76865ad7647 --kumitate …/kumitate-shokunin` → `C2_F8:
   survivors=4 classified=4 anchored_holes=4 rev=2227d8338c02aa9a5fd7d95c1a41b768
   65ad7647`, exit 0. This mechanically passes the frozen checks: contract quotes
   on named lines, external quotes in `mined` SOURCES rows opened 2026-10-22
   (S090 at `corpus/SOURCES.md:99`, S091 at `:100`), receipt byte binding, entry
   `ground:`/`source:` lines, and S012 `mined` with the entry path in used-by
   (`corpus/SOURCES.md:23`). Target `classified=4` met.
7. **Entry pinned to the revision.** Working-tree
   `corpus/knowledge/oracle-anchored-survivors.md` sha256
   `994f532421ec16e89d498cc3f84d7361fbec61d880cfc081d7b1704e0c0356ad` =
   `git show 2227d833…:corpus/knowledge/oracle-anchored-survivors.md`.
8. **External sources live.** arXiv 2608.17214 abstract (fetched via arXiv API
   today) contains both quoted S012 fragments verbatim ("composed from values
   fixed outside the code under mutation", "flows, directly or transitively,
   from"), one author, one system — matching the entry's tier-B,
   definitions-only bounds (§5). FreeBSD sysexits(3) 15.1 page (dated May 9,
   2024) contains "EX_USAGE (64) The command was used incorrectly, e.g., with the
   wrong number of arguments, a bad flag" as the exact prefix of the page text
   (the page continues "a bad syntax in a parameter, or whatever"; the page's own
   legacy/deprecated status is recorded in the SOURCES row and the round-27
   lesson Gate). gitrevisions (last updated 2.56.0, 2026-09-28, matching the
   SOURCES row) contains "The full SHA-1 object name (40-byte hexadecimal
   string), or a leading substring that is unique within the repository."
9. **Classes and witness facts.** The probe emits exactly the three classes the
   entry §2 lists (`anchor-probe.py:124-129`); all four results are
   `anchored-hole` with `pristine_meets_anchor=true`, `mutant_meets_anchor=false`.
   Witness facts match the entry table: `newline_count=20` with the citation at
   line 21 (`build_tree` writes 20 newline-terminated lines and cites `n+1`);
   S_STRICT runs `--strict` over one orphan ref (mutant still emits the
   ORPHAN_REF warn but exits 0 — the entry's "exit 0" cell is accurate, and
   round-26 §4's "mutant CLEAN" refers to the verdict, consistent);
   `--no-such-flag-r27` matches the receipt `stderr_head`; the interior pin
   matches receipt facts (finding MINOR 1 aside).
10. **Round-26 §4 agreement.** All four pristine/mutant statuses and exit codes
    in the new entry §3 table match `mutation-case-kumitate-cite-check.md` §4
    (LINE_OOR 1→0 clean, DRIFT 1→0, usage 64→65, PIN_MISMATCH 1→0) and
    S_EMPTY_GUARD is carried as equivalent, unchanged.
11. **Bounds stated.** Entry §5: one gate/one pin/four survivors; other legs stay
    differential; probe checks exit + one finding kind, not message text or JSON
    totals; header same-owner caveat; S012 tier-B definitions-only. Entry §4:
    S_PIN_INCLUDES convention-only strength (matches `anchor_strength` in
    `anchors.json`); S_EMPTY_GUARD equivalence unchanged. Recheck line: a new pin
    needs new anchors. README F8 row quoted verbatim (`corpus/README.md:85`).
    The amendment narrative matches fleet `CORPUS.md:116` (rule 2: only `status`,
    `recheck`, `used-by` change in place), and the S012 row edit observes it.

## Residual risk and verification gaps

- "Before the probe ran" rests on commit order plus the receipt's anchors
  binding; the probe run itself left no separate timestamped artifact. No
  contradicting evidence found.
- The arithmetic anchor (20 newlines) was verified from the probe source and my
  rerun's `witness_facts`, not by an independent byte count of a witness tree
  (the tree is deleted with the temp dir).
- S012 was verified at the abstract only, which is all the entry uses.
- No language server answers for these markdown/JSON evidence files, so all
  definition/reference checks here are text-plus-execution, not LSP.

## Tooling and bounds

No tools installed or upgraded (bash, git, python3, node pre-existing sufficed).
Read-only git with `GIT_OPTIONAL_LOCKS=0` only; no `jj` commands; all execution
in `/tmp/r27-review`; the only file written in the lane is this report.
