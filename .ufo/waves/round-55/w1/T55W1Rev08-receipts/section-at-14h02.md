
The round-54 non-author spot-check (`corpus/lessons/round-54-verifier-spotcheck.md`)
routed ten record defects. This section carries each correction in one place: the
old text (preserved here as the erratum), the corrected value, and the receipt
that decides it. The same corrections were applied in place above so that the
lane's record reads true where a reader meets it; this section is the only place
where the old values are quoted, which is why the round-55 counter
(`.ufo/evidence/round-55/c1/measure.py`) counts every stale token outside it.

**ER-R54-1 - a positive control reported as passing while its receipt says it did not.**
Old: `CTL_POS_c1 true` (round-54 claim row); `corpus/QUALITY.md` 105's falsifier
(`the round-54 counter's arm prints rekeyed=7/7 on its positive control`);
`corpus/lessons/round-54.md` (`proven live by the positive control (CTL_POS_c1,
which prints rekeyed=7/7)`).
Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B:
2/3` at the revision the control cloned. The cause is mechanical: phase B cloned
the FREEZE commit, which predates the re-key, so the control could not fire.
Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Round 55 re-scores
its own positive control at the revision it certifies (`controls.sh` phase B).

**ER-R54-2 - three freeze pointers for one round.**
Old: `7883e0e5` called "the freeze pointer the deciding run uses"; `fe70474d`
in the measured-close line; `097985c1` in the fleet report.
Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding
receipt prints. Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
(`freeze=077d431e...`).

**ER-R54-3 - a quoted total no receipt contains.**
Old: `total=14` in the C2 claim row. Corrected: `total=13`.
Receipt: `.ufo/evidence/round-54/before/c2.stdout` (and the contract's own
`before` text).

**ER-R54-4 - a stale counter digest.**
Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85` - the amendment-4
bytes that decided. Receipt: `.ufo/evidence/round-54/freeze.json`, key
`c2/measure.py`.

**ER-R54-5 - finding counts that do not match the committed readers.**
Old: 25 wave-1 findings; 22 wave-2 findings in 9 sections. Corrected (re-derived
over the committed reader files, `-receipts/` JSON excluded): `w1=28 w2=25 sections=12`
- 28 findings across 23 wave-1 reader reports, 25 across 12 of the 23 wave-2
reports. Command: `git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1`
then a `findings` length sum per file (the round-55 c1 counter does exactly this
at every revision).

**ER-R54-6 - round work uncommitted at closure.**
Old: three seat deliverables untracked when the round filed.
Corrected: they are committed; the sweep that committed them is `ff2a821`.
Receipts: `.ufo/waves/round-54/w2/T54W2Sent03.md` and
`.ufo/waves/round-54/w2/T54W2Sent03-receipts/{c1committed-positive.stdout,rejection-attribution.txt}`.

**ER-R54-7 - an imprecise forged-file disposition.**
Old: "the deletion lands in 7fa9a5e0". Corrected: the file was **renamed** into
`.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`
(`R100`); it still sits in the tree as the incident receipt. It can never
credit: its path fails the reader pattern and its `section_sha256` matches no
section at the content commit.

**ER-R54-8 - a half-recorded host-write incident, and a characterisation that
was itself wrong.**
Old: the report named the incident; the lesson did not, and the seat file still
asserted an operator instruction. Corrected in two steps. The incident is now
recorded in `corpus/lessons/round-55.md` and
`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` is marked superseded. The
round-54 report's characterisation ("fabricated") is ALSO withdrawn: the operator
turn exists in `~/.omp/agent/history.db` (row 690, 2026-10-28T15:12:15Z) and
reached the seat 5 m 33 s after it yielded; the write to `config.yml` was wrong
because the file is operator-owned and the seat had stopped serving, not because
the turn was invented, and the file now reads `scout: "@m_grok"` again.

**ER-R54-9 - wave-table numbers and the staged-package count.**
Old: 4 reviewers (report), a 26.3 % attack share, "the other 84 staged entries".
Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from
`.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under
`merge/tameshi/knowledge` (read-only count of the source package).

**ER-R54-10 - a quote under the wrong receipt.**
Old: `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.
Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`; the
`rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the
round-53 counter's own bytes run at the round-53 final revision.