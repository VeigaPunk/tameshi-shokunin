# ExecLiveShift — round 42 wave 2 (FALSIFY): line-shift live sites

Attacked: `tools/write-path-census-v4.py` (sha256 `784de4c0…22fe5`, lane HEAD `a21845f523b75adbd3e3f7a62af91294db224ad9`, labelled pre-run). The claim under attack: the live sites keep their classification and resolution when lines shift and identifiers are renamed. Only the tool's `--file … --json` mode was run, on scratch copies. No counter was run, and the lane was not edited.

Scratch dir: `/tmp/tameshi-r42w2-ExecLiveShift-iXaW` (deleted before return). Inputs were byte copies of `tools/context-capture.py` (sha256 `c4a1d165…01726`) and `tools/registry-replay.py` (sha256 `9fcd2dbb…08714`).

## Commands

```
cp tools/context-capture.py $D/cc.orig.py; cp tools/registry-replay.py $D/rr.orig.py
{ printf '\n\n\n\n\n\n\n'; cat $D/X.orig.py; } > $D/X.shift.py            # 7 blank lines at top
sed 's/case_dir/slot_for/g'   $D/cc.shift.py > $D/cc.ren.py              # 3 occurrences → 0 left
sed 's/publish/emit_bundle/g' $D/rr.shift.py > $D/rr.ren.py              # 5 occurrences → 0 left
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v4.py --file $D/<copy> --json
```

Every run exited with rc=0 and printed nothing on stderr.

## Findings: target sites before and after

The classification fields are `kind`, `expected`, `explicit_out`, `scratch`, `flagged` and `unflagged`.

| file | orig line | shifted line | renamed line | classification (identical in all 3) | resolved contains |
|---|---|---|---|---|---|
| context-capture | 1682 | 1689 | 1689 | open, expected=T, explicit_out=F, scratch=T, flagged=F, unflagged=F | `mkdtemp` (len 1185) |
| context-capture | 1685 | 1692 | 1692 | open, expected=T, explicit_out=F, scratch=T, flagged=F, unflagged=F | `mkdtemp` (len 1185) |
| registry-replay | 123 | 130 | 130 | write_bytes, expected=T, explicit_out=T, scratch=F, flagged=F, unflagged=F | `--out` (`expected.json argparse --out`) |

- **All sites, not just the targets:** context-capture has 3 sites (1667/1682/1685 → 1674/1689/1692). registry-replay has 5 sites (122/123/125/183/211 → 129/130/132/190/218). In both files every site moved by exactly +7 with the same classification, after the shift and after the rename.
- **Resolved text:** in the shifted copies the resolved text is byte-identical to the original at every site.
- **context-capture rename:** the resolved text changes only because `case_dir` was on the resolution path. It was present in the original's resolved text and `slot_for` is present after the rename. `mkdtemp` is still resolved.
- **registry-replay rename:** the resolved text is byte-identical. `publish` was never part of the resolved text; the function is only a link between the call and the definition (`rr.orig.py:116` def, `:185` and `:282` calls).

## Controls: does the rename test actually test anything?

These are inconsistent renames and a mid-file insert, run on the same scratch copies.

- **`rr.defonly`** (`sed '116s/def publish(/def emit_bundle(/'`): line 123 becomes explicit_out=F, unflagged=**T**, and `--out` is lost. Lines 122 and 125 lose `--out`.
- **`rr.callonly`** (only lines 185 and 282 renamed): the same degradation as `rr.defonly`.
- **`cc.defonly`** (`sed '1631s/def case_dir(/def slot_for(/'`): lines 1682 and 1685 become scratch=F, unflagged=**T**, and `mkdtemp` is lost.
- **`cc.mid`** (7 blank lines inserted before original line 1670): line 1667 stays at 1667, and 1682/1685 move to 1689/1692 with the same classification.

So resolution really follows the link from function definition to call site, not the identifier's text. Because a broken link degrades it, the clean rename holding is real evidence. The line numbers are recomputed by position in the file, not taken from a fixed table.

## Risks / limits

- The rename used `sed` text substitution, including in comments and docstrings, for example `rr.orig.py:7` and `:27`. It was not an AST-scoped rename.
- Only the blank-line shift was tested. Comment or code insertions were not.

Tool installs: none.

Verdict: SURVIVES
