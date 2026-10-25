seat: ExecJudge07

# Round-45 C1 falsify — independent re-judgment of S065, S100, S102

Inputs read at commit `ad5942c6e9858af19d00000b58439b321ddfa62b` (ledger blob sha256 `433a624bf8cdd42ccf2ea2a818aa0bdc40dd2c77cd636e1121d0aa51eb5a9913`; `git diff ad5942c..HEAD -- .ufo/evidence/round-45/freshness/ledger.json` is empty, so the worktree ledger at HEAD `1f9266a` is the same bytes). Authors: S065 `ExecRows10`, S100 `ExecRows19`, S102 `ExecRows20` — none is this seat, so the independence requirement holds. All three rows are `mined`, id <= S160, with the entry URL equal to the row's own source-cell URL (population members).

## Verdicts

S065 agree — reviewer ExecJudge07 — live sha `110b871d…b9e3` equals both the entry `raw_sha256` and the gunzipped committed snapshot, and the quote is body text of §Infinite and NaN Number Values (immediately after "The RFC does not permit the representation of infinite or NaN number values") with the `parse_constant` alteration sentence following, so the default-acceptance + `parse_constant` teaches claim is still supported.
S100 agree — reviewer ExecJudge07 — live sha `6f6c1467…ca52` equals both the entry `raw_sha256` and the gunzipped committed snapshot, and the quote is the module introduction's opening sentence in the "doctest - Test interactive Python examples" body (immediately before the "several common ways to use doctest" bullets), so the row's "executable documentation examples" scope is supported by today's 3.15 build bytes.
S102 agree — reviewer ExecJudge07 — live sha `0889867a…1acd` equals both the entry `raw_sha256` and the gunzipped committed snapshot and is byte-identical to the row's own 2026-10-23 pin (357,953 bytes), and the quote is the `#` rule in the numbered rules of §2.3 Token Recognition, so the discard-as-comment teaches claim is supported.

Reviews file written at `/tmp/tameshi-r45-ExecJudge07/reviews.json` (schema `{"reviews":[{"id","reviewer","verdict","report","reason"}]}`, report `.ufo/waves/round-45/w2/ExecJudge07.md`) for L1 integration into `.ufo/evidence/round-45/freshness/reviews.json`. No deciding run of any counter was performed; only `--extract` and `--check` (allowed seat modes).

## Provenance — sha256 comparisons (this seat's own live fetches, 2026-10-25)

Commands (per row, in `/tmp/tameshi-r45-ExecJudge07/`):
```
curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S###.live '<row url>' && sha256sum S###.live
git -C LANE show ad5942c6e9858af19d00000b58439b321ddfa62b:.ufo/evidence/round-45/freshness/sources/S###.raw.gz | gunzip -c | sha256sum
```
```
S065 live (116112 bytes) : 110b871d2d983f95caf6b20996e5d4c6d48d0842a9f9dbcedffb9345d556b9e3
S065 entry raw_sha256    : 110b871d2d983f95caf6b20996e5d4c6d48d0842a9f9dbcedffb9345d556b9e3
S065 snapshot@ad5942c    : 110b871d2d983f95caf6b20996e5d4c6d48d0842a9f9dbcedffb9345d556b9e3
S100 live (216574 bytes) : 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52
S100 entry raw_sha256    : 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52
S100 snapshot@ad5942c    : 6f6c1467595ab4003a342014cc118d8fa60c20e43ce09144de11df657c80ca52
S102 live (357953 bytes) : 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
S102 entry raw_sha256    : 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
S102 snapshot@ad5942c    : 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd
```
All three are provenance-confirmed with no dynamic-chrome divergence, so the `--extract`-on-live fallback was not needed. S102's live bytes also equal the sha the registry row itself states in its anchor (`0889867a…1acd`, 357,953 bytes, fetched 2026-10-23): zero drift since the row was mined.

## Located context (normalized snapshot text, `measure.py --extract`)

`python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge07/S###.snap` (raw from `gunzip -c .ufo/evidence/round-45/freshness/sources/S###.raw.gz`); quote offsets are in the normalized text.

- S065 @ 21962 — section body heading at 21852 (`Infinite and NaN Number Values ¶`; the TOC copy at 240 is nav only). Before: "…Infinite and NaN Number Values ¶ The RFC does not permit the representation of infinite or NaN number values." Quote: "Despite that, by default, this module accepts and outputs Infinity , -Infinity , and NaN as if they were valid JSON number literal values". After: ": >>> # Neither of these calls raises an exception, but the results are not valid JSON". The teaches claim's second half is in the same section at 22455: "In the deserializer, the parse_constant parameter can be used to alter this behavior." (and the `json.load` parameter list documents `parse_constant` at 10895 as "called with one of the following strings: '-Infinity' , 'Infinity' , or 'NaN'"). Body content, not title/nav/footer.
- S100 @ 1041 — body start at 1037: "doctest - Test interactive Python examples ¶ Source code: Lib/doctest.py The doctest module searches …". Quote: "doctest module searches for pieces of text that look like interactive Python sessions, and then executes those sessions to verify that they work". After: "exactly as shown. There are several common ways to use doctest: To check that …" (bullets at 1204). Body content of the module introduction; the anchor's "first bullet" is the bullet list that starts immediately after this sentence, and the bullet text itself names "executable documentation", so the row's scope cell is directly supported.
- S102 @ 15748 — §2.3 Token Recognition heading at 10797; the quote is inside the numbered token-recognition rules (preceded by "If the previous character was part of a word, the current character shall be appended to that word."). Quote: "If the current character is a '#' , it and all subsequent characters up to, but excluding, the next <newline> shall be discarded". After: "as a comment. The <newline> that ends the line is not considered part of the comment." Next heading is §2.3.1 Alias Substitution. Body content, correct section, states the rule the teaches cell claims.

## Counter-helper re-grade and predicate fields

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev ad5942c6e9858af19d00000b58439b321ddfa62b --check /tmp/tameshi-r45-ExecJudge07/frag-S065.json
CHECK S065 verified ok
$ … --check /tmp/tameshi-r45-ExecJudge07/frag-S100.json
CHECK S100 verified ok
$ … --check /tmp/tameshi-r45-ExecJudge07/frag-S102.json
CHECK S102 verified ok
```
(all exit 0; `frag-*.json` are the three ledger entries extracted verbatim from the `ad5942c` ledger blob). The `--check` grade also confirms the "quote copied from row" rejection does not fire.

Independent recomputation with the counter's own helpers (`fold`, `words`, `parse_rows`): quote lengths 24 / 23 / 23 whitespace tokens (within 6–25); quote text is absent from the row line in `corpus/SOURCES.md` and from the entry's `note` (located afresh, not copied); shared content words with scope+anchor+teaches — S065 8 (`accepts, default, infinity, json, literal, number, valid, values`), S100 2 (`module, python`), S102 4 (`character, excluding, newline, next`).

## Findings that do not change the verdicts

- Version labels drifted but no claim drifted: the S065 page now renders "Python » 3.15.1 Documentation" (row source cell says "Python 3.15.0 docs", row anchor declares "version-coupled; no commit pin") and the S100 page is "Python 3.15.1" (row says "3.15 build"). Both quoted claims and the `parse_constant` sentence are unchanged, so this is declared version-coupling, not a dispute.
- Two quotes are truncated at clause boundaries but keep the operative claim: S100 ends "…verify that they work" (doc continues "exactly as shown."); S102 ends "…shall be discarded" (doc continues "as a comment."). Neither truncation removes what the row claims; the S102 continuation is the immediately following sentence naming the comment.
- `/tmp` filesystem is saturated by other seats: `df -h /tmp` → `128G 128G 744M 100%` (122G used). A first write of my fragment files failed with `OSError: [Errno 28] No space left on device`; I deleted my fetched live copies after hashing (scratch now ~1.7M) and the retry succeeded. L1 integration into the lane's `reviews.json` should be checked for ENOSPC too.
- No tools installed or upgraded (no pacman — transactions are paused host-wide — and no uv/npx/official-binary action was needed; `curl`, `gunzip`, `sha256sum`, `python3`, `git` pre-existing). No lane writes beyond this report; no git/jj mutation; no deciding counter run.
