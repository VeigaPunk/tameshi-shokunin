# T57D4Rows1 — documentary review

Axes: status truth, item-specific commit support, panel provenance, integration evidence. Documentary recommendation only; no admission. No candidate gate, tests, builds, exploit, or other runtime executed. No installation or production edit.

## Finding — high: the reviewed rows are not in the pinned production ledger

Any claim that `R51.4` and `R51.6` are integrated into `corpus/routed-defects.json` at C0b `adf87899c70d616140a81185a8f9acbbdfb30392` is **unsupported**. Both exist in the local integration candidate and writer output, not in that committed ledger. This does not invalidate their proposed `open` statuses.

Read-only command actually run:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:corpus/routed-defects.json | jq '{count:(.defects|length), rows:[.defects[]|select(.id=="R51.4" or .id=="R51.6")]} '
```

Output (exit 0):

```json
{"count":49,"rows":[]}
```

The equivalent `read` query on the current production file also returned no rows. Candidate data is `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/integrate/candidate-ledger.json:1131-1154,1182-1205`; writer data is `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR514xR516/rows.json:3-25,28-50`. A new integrated revision is needed before either can be represented as a committed production row; this review does not grant that revision admission.

## Per-id semantic results

### R51.4 — proposed `open`: supported; integrated-row claim: unsupported

Original requirement: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51-verifier-spotcheck.md:129`: hermetic selftest **or** a declared fleet-bound counter row class with pre-registered amendment. The historical lesson independently says a later counter amendment is needed (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51.md:97`).

The declaration explicitly says non-hermetic (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/round21-measure.py:8-12`). The governing panel is `open` (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w2/T57W2PanelR513R514.json:11-14`); merged panel agrees (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/panel.json:12`). Writer report explains neither route was completed (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR514xR516.md:47-90`).

Commit `bcba8924894216268afc4171f06eb8c28e912b46` is **not** supported as this item's complete fix. Actual read-only command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show bcba8924894216268afc4171f06eb8c28e912b46 -- tools/round21-measure.py
```

Output includes the added `fleet-bound, not hermetic` declaration and changes sibling lookup from `ROOT.parent` to the subject counter's `FLEET`; this is host-bound behavior, not hermeticity. A separate `git ... show --format=fuller --stat bcba8924894216268afc4171f06eb8c28e912b46` listed eight changed files and no round-51 C3 counter. Keeping it only as panel provenance while omitting a top-level fix commit is honest.

The additional missing C3 mutation attack is explicitly recorded at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51.md:98`. I did not re-run an attack, and an exhaustive search for later execution is not claimed. The non-hermetic declaration plus unamended cited counter already supports leaving the item open.

### R51.6 — proposed `open`: supported; integrated-row claim: unsupported

Original requirement: list rejected candidates and reasons in the round lesson's Gate, not merely admits and touched rows (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51-verifier-spotcheck.md:131`). The complete cited Gate at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-51.md:5-14` has source admissions and touched rows, then the next section; no rejected-candidate list.

Clean re-seat `open` and null commit: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR515R516.json:9-12`. Merged panel agrees at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/panel.json:14`. Writer explicitly withdraws the earlier breached panel's forward-practice fix claim (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR514xR516.md:92-115`).

Actual command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --format=oneline --stat 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 -- corpus/lessons/round-51.md corpus/lessons/round-52.md
```

Output:

```text
7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135 round-52: wave-2 fix-reads applied in-line (59), round21 row cell, shrink-case scope; QUALITY 103; S274; lesson; wave-2 evidence
 corpus/lessons/round-52.md | 54 ++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 54 insertions(+)
```

It does not repair the cited round-51 Gate. No top-level fix commit is appropriate for the proposed open row.

## Continuity sweep and output

These read-only commands were actually run and returned exit 0 with **no output**:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- corpus/routed-defects.json corpus/lessons/round-51.md tools/round21-measure.py .ufo/evidence/round-51/c3/measure.py
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4 adf87899c70d616140a81185a8f9acbbdfb30392 -- .ufo/evidence/round-51/c3/measure.py corpus/lessons/round-51.md
```

Thus no scoped candidate repair or production ledger integration is shown by the base→C0b diff. Proposed statuses agree with the documentary surfaces and governing panels; there is no further status defect identified in these two staged rows.

## Residual risk / verification gaps

- Integration candidate remains local/unverified; no subsequent integrated revision was supplied or admitted here.
- Counter acceptance, newest Planned paragraph requirements, runtime execution, canonical runtime/rerouting/saturation, and resume preflights are not reviewed or passed by this documentary row assignment.
- `read xd://lsp` returned `No such tool: xd://lsp`; no semantic server/device is mounted. Text and git-object evidence are documentary evidence, not semantic-reference proof.
- Existing writer/panel command outputs were read as historical evidence, never re-executed as candidate gates.
- No tools installed/updated. Only this report and its JSON were written.

Self-evaluation: accuracy 4 (no runtime proof claimed); completeness 4 (both ids and commit histories covered, later integration not supplied); clarity 4 (separates proposed truth from landing); actionability 4 (identifies missing committed rows); conciseness 4 (command receipts add length). Overall 4.0. Main should preserve the open statuses and separately establish any future integration revision; user agreement expected because no pass is invented.
