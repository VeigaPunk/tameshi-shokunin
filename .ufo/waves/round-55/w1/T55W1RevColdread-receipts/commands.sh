# seat T55W1RevColdread — commands, all read-only against the lane; fixtures under HYAKU_SCRATCH
S=/fast/scratch/hyaku/tameshi-r55/T55W1RevColdread
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
B=0a2010acd1e92e4e332774050825e21bcfc7e079
# 1) base section boundaries with the FROZEN round-18 sectionize
git -C "$L" show $B:SKILL.md > "$S/SKILL-base.md"
python3 -c "import importlib.util; ...m.sectionize(open('$S/SKILL-base.md','rb').read())"   # receipts/section-table.txt
# 2) base cold-read floor
python3 "$L/.ufo/evidence/round-21/coldread/measure.py" --rev $B --explain > "$S/base-measure.json"   # 64/64
# 3) fixture clone at base + the round's C2 content patches + the round's record edits (marker bytes)
git clone --shared "$L" "$S/clone"; git -C "$S/clone" checkout --detach $B
git -C "$S/clone" apply "$L/.ufo/waves/round-55/w1/T55W1ExecC2Full-receipts/patches.diff"
printf ... >> "$S/clone/SCORECARD.md" ... LOG.md corpus/QUALITY.md corpus/SOURCES.md corpus/lessons/round-54.md
git -C "$S/clone" add -A; git -C "$S/clone" commit -m 'round-55 PIN simulation'      # C0=2ff57a1f76bd
# 4) cold-read at the simulated PIN, no re-key
python3 "$S/clone/.ufo/evidence/round-21/coldread/measure.py" --repo "$S/clone" --rev 2ff57a1f --explain > "$S/receipts/pin-sim-measure.json"   # 46/64
bash "$L/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$S/clone" $B 2ff57a1f76bd   # lost=18 RED rc=1
# 5) fresh readers for the 18 lost headings + adapted round-54 binder
python3 - # writes $S/readers/reader-NN.{json,md} {heading,cand,section_sha256,findings:[]}
python3 "$L/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py" \
  "$S/clone" 2ff57a1f76bd 2ff57a1f76bd "$S/clone/.ufo/evidence/round-21/coldread/rekey-r55-sim" \
  --headings "$S/headings.json" --waves "$S/readers" --label "L1 TameshiR55 re-key (round 55)"
git -C "$S/clone" add -A; git -C "$S/clone" commit -m 'round-55 re-key: 18 bound reader entries'   # c94ad673
# 6) credit restored + precheck green
python3 "$S/clone/.ufo/evidence/round-21/coldread/measure.py" --repo "$S/clone" --rev c94ad673 --explain > "$S/receipts/rekeyed-measure.json"   # 64/64
bash "$L/.ufo/evidence/round-48/quality/coldread-precheck.sh" "$S/clone" $B c94ad673   # lost=0 ok rc=0
