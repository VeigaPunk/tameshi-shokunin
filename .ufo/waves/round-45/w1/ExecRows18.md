seat: ExecRows18
task: C1 row re-verification, rows S095, S096, S097 (author of ledger entries, w1)
rev: 3310e7be803516ca5934b4e949d91bcec824b179 (frozen)
date: 2026-10-25

All three rows fetched live (curl exit 0), extracted with the round-45 freshness counter
(--extract), quotes located verbatim in the extracted normalized text, fragments checked with
`measure.py --check --snapdir /tmp/tameshi-r45-ExecRows18` → all `CHECK S### verified ok` (RC 0).
No tool installs performed (system curl + python3 used). .raw files kept in
/tmp/tameshi-r45-ExecRows18/ for L1 integration (snapshot path as committed sources/S###.raw.gz).

## S095 — https://go.dev/blog/examples
- curl: exit 0; 40059 bytes; sha256 1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178
  (byte-identical to the row's recorded 2026-10-23 fetch → page unchanged)
- CHECK: `CHECK S095 verified ok` (RC 0)
- quote: "the testing framework captures data written to standard output and then compares the output against the example's "Output:" comment." (19 tokens, located at the §Output comments passage; shares "output"/"comment" with scope/anchor/teaches)
- note: The live blog's Output comments section still says the testing framework captures stdout and compares it against the Output: comment, so a test passes only when the captured output matches the comment, exactly as teaches claims.

## S096 — https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html
- curl: exit 0; 51137 bytes; sha256 95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7
  (byte-identical to the row's recorded 2026-10-23 fetch → page unchanged)
- CHECK: `CHECK S096 verified ok` (RC 0)
- quote: "rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working." (22 tokens, the §Documentation tests intro; shares "rustdoc"/"documentation"/"examples"/"tests")
- note: The live rustdoc book's Documentation tests intro still states rustdoc executes documentation examples as tests so they remain up to date and working, grounding the teaches claim.

## S097 — https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303
- curl: exit 0; 415804 bytes; sha256 f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5
  (byte-identical to the row's recorded 2026-10-23 fetch → source unchanged)
- CHECK: `CHECK S097 verified ok` (RC 0)
- quote: "Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially." (19 tokens, from the @node Exit Status passage; shares "exit"/"statuses"/"fall"/"between")
- note: The live Bash 5.3 texi Exit Status node still states statuses fall between 0 and 255 with the shell using values above 125 specially, grounding the range claim; separately verified the §Conditional Constructs passage still states `case` executes the command-list of the first matching pattern, so the teaches claim holds in full.

## Fragment JSONs (verbatim)
```json
{"id":"S095","url":"https://go.dev/blog/examples","opened":"2026-10-25","verdict":"holds","raw_sha256":"1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178","quote":"the testing framework captures data written to standard output and then compares the output against the example's \"Output:\" comment.","snapshot":".ufo/evidence/round-45/freshness/sources/S095.raw.gz","author":"ExecRows18","note":"The live blog's Output comments section still says the testing framework captures stdout and compares it against the Output: comment, so a test passes only when the captured output matches the comment, exactly as teaches claims."}
```
```json
{"id":"S096","url":"https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"95572c7300af0f27eab4c7ed47125a509a9c5854fc80dc2d7fd162d894de3cb7","quote":"rustdoc supports executing your documentation examples as tests. This makes sure that examples within your documentation are up to date and working.","snapshot":".ufo/evidence/round-45/freshness/sources/S096.raw.gz","author":"ExecRows18","note":"The live rustdoc book's Documentation tests intro still states rustdoc executes documentation examples as tests so they remain up to date and working, grounding the teaches claim."}
```
```json
{"id":"S097","url":"https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303","opened":"2026-10-25","verdict":"holds","raw_sha256":"f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5","quote":"Exit statuses fall between 0 and 255, though, as explained below, the shell may use values above 125 specially.","snapshot":".ufo/evidence/round-45/freshness/sources/S097.raw.gz","author":"ExecRows18","note":"The live Bash 5.3 texi Exit Status node still states statuses fall between 0 and 255 with the shell using values above 125 specially, grounding the range claim (the Conditional Constructs passage still states case runs the first matching pattern's command-list)."}
```

Report: .ufo/waves/round-45/w1/ExecRows18.md
