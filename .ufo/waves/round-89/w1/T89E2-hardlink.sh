#!/usr/bin/env bash
# hardlink — round-89 T89E2 counterfeit of tools/mutate-and-run.sh --regression.
# Mechanism: stub at exec, spec-exact bytes installed afterwards through a hard-link
# decoy name (the audited path is never written after its own exec).
# Declared ledger (vars, embedded specs, leg calls) copied verbatim from
# 61990f3d8cd99932bfb0575e1c292e03d310b436:tools/mutate-and-run.sh; only the case executor is replaced.
# nonce: 910c82e4867e0013
set -u -o pipefail
SELF=$(readlink -f "${BASH_SOURCE[0]}")
FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")
WORKDIR=''
INTERP=''
IPATH=''
IFLAG=''
PIN_JS=83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426
REV_JS=175de6ba2e9e904010411b19cab27e0af9aad3d4
PIN_BASH=275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f
REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e
PIN_TSUKUROI=084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5
REV_TSUKUROI=165307fe4746a8807b02ec4a7d7ecac0368454a6
PIN_MADO=d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
REV_MADO=eead56b20ad2b28299ae4fa623d52a99b44c743c
PIN_CHECKLIST=7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e
PIN_CLAIMS=e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b
REV_CLAIMS=175de6ba2e9e904010411b19cab27e0af9aad3d4
PIN_ROUNDGATE=f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
REV_ROUNDGATE=364f1d5954158ef8844bca4a5fef57b05d2f2ca5
PIN_SOURCESCHECK=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
REV_SOURCESCHECK=0acb7752d19058b953ebbeba253b1e35f6548de5
PIN_CITECHECK=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
REV_CITECHECK=1205c6621a2eccbb8ffceae86d9e7b79a7990b3a
PIN_DRIFTPINS=c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb
REV_DRIFTPINS=e64e81b8eb96f3682b00c1e7a291e84420b280fa
TABLE_JS='D1:KILLED,D2:SURVIVED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:KILLED,D8:KILLED,D9:KILLED,D10:SURVIVED'
TABLE_BASH='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:SURVIVED,B6:KILLED,B7:KILLED,B8:KILLED,B9:KILLED,B10:SURVIVED'
TABLE_TSUKUROI='B1:KILLED,B2:KILLED,B3:KILLED,B4:KILLED,B5:KILLED,B6:KILLED,B7:SURVIVED,B8:SURVIVED,B9:SURVIVED,B10:SURVIVED'
TABLE_MADO='D1:KILLED,D2:KILLED,D3:SURVIVED,D4:KILLED,D5:SURVIVED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,R1:SURVIVED'
TABLE_CHECKLIST='A1:SURVIVED,A2:KILLED,B1:SURVIVED,B2:KILLED,B3:SURVIVED,B4:KILLED,C1:SURVIVED,C2:KILLED,D1:SURVIVED,D2:KILLED,E1:KILLED,E2:SURVIVED,F1:KILLED,F2:SURVIVED,G1:SURVIVED'
TABLE_CLAIMS='D1:KILLED,D2:KILLED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:SURVIVED,D8:SURVIVED,D9:SURVIVED,D10:KILLED'
TABLE_ROUNDGATE='A1:KILLED,A3:KILLED,B1:KILLED,E3:KILLED,C1060:KILLED,C1059:SURVIVED,A2:SURVIVED,B2:SURVIVED,CKIND:SURVIVED,E1:SURVIVED'
TABLE_SOURCESCHECK='K_KIND:KILLED,S_KIND:SURVIVED,K_EXIT:KILLED,S_VERDICT:SURVIVED,K_STRICT:KILLED,K_CLOSED:KILLED,K_ROWS:KILLED,S_DUP_LINE:SURVIVED,S_ENTRY_COUNT:SURVIVED,S_FILE_READ:SURVIVED'
TABLE_CITECHECK='K_UNRESOLVED_SEV:KILLED,K_PIN_KIND:KILLED,K_FENCE_TILDE:KILLED,K_MISSING_WORD:KILLED,K_EMPTY_VERDICT:KILLED,S_OOR_EDGE:SURVIVED,S_STRICT:SURVIVED,S_EMPTY_GUARD:SURVIVED,S_USAGE:SURVIVED,S_PIN_INCLUDES:SURVIVED'
PIN_KAKEGUARD=0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067
REV_KAKEGUARD=e8d3a924249983972e5163d160cf236487986c55
TABLE_KAKEGUARD='K_CUT_WHOLE:KILLED,K_STARTSWITH:KILLED,K_FILES_EQ:KILLED,K_GLOB:KILLED,K_SHOW_RC:KILLED,S_HEAD_SHORT:SURVIVED,S_OFFSET_EQ:SURVIVED,S_OK_ALL:SURVIVED,S_VACUOUS:SURVIVED,S_RED_FILES:SURVIVED'
TABLE_DRIFTPINS='K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,K_AMBIG_GT:SURVIVED,K_COUNT_GE:KILLED,K_SHAPE_OPTIN:SURVIVED,S_SHA_CMP:SURVIVED,S_HARDLINK:SURVIVED,S_POLICY:SURVIVED,S_DUP_UNIQ:SURVIVED,S_USAGE_EXIT:SURVIVED'

regression_specs() { # <dir> — write the eleven embedded case specs
  local d=$1
  cat >"$d/js-kimi-census.spec" <<'EOT'
@defect D1 | kimi-census.mjs:105
@old kind: 'dir', counted: 18 },
@new kind: 'dir', counted: 17 },

@defect D2 | kimi-census.mjs:378
@old findings.slice(0, 6).map
@new findings.slice(0, 5).map

@defect D3 | kimi-census.mjs:332
@old       if (!e.children.includes(n)) {
@new       if (e.children.includes(n)) {

@defect D4 | kimi-census.mjs:351-353
@old   for (const n of strays) {\n    err('UNLISTED', n, `${n} sits at the root and is not declared by the frozen K1–K5 set`);\n  }\n
@new 

@defect D5 | kimi-census.mjs:255
@old       const present = gens.length > 0;
@new       const present = true;

@defect D6 | kimi-census.mjs:124
@old kind: 'file', secret: true, modeFloor: 0o600 },
@new kind: 'file', secret: true, modeFloor: 0o644 },

@defect D7 | kimi-census.mjs:306
@old (mode & m.modeFloor) !== m.modeFloor
@new (mode & m.modeFloor) === 0

@defect D8 | kimi-census.mjs:396
@old   return 2;\n
@new   return 1;\n

@defect D9 | kimi-census.mjs:292
@old         ? (m.kind === 'dir' ? kind === 'dir' : isLeaf(kind))
@new         ? (m.kind === 'dir' ? kind === 'dir' : kind === 'file')

@defect D10 | kimi-census.mjs:145
@old const FROZEN = { K1: 3, K2: 25, K3: 9, K4: 9, K5: 3 };
@new const FROZEN = { K1: 3, K2: 24, K3: 9, K4: 9, K5: 3 };
EOT
  cat >"$d/bash-surface-census.spec" <<'EOT'
@defect B1 | surface-census.sh:241
@old   [[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0
@new   [[ ${#SCAN_DIR[@]} -ne 0 ]] && return 0

@defect B2 | surface-census.sh:435
@old             elif [[ "$got" -ge "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\\n' "$p" "$tbl" "$got" "$floor"
@new             elif [[ "$got" -gt "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\\n' "$p" "$tbl" "$got" "$floor"

@defect B3 | surface-census.sh:229
@old       if [[ -n "$want_mode" && "$want_mode" != "$mode" ]]; then
@new       if [[ -n "$want_mode" && "$want_mode" == "$mode" ]]; then

@defect B4 | surface-census.sh:200-204
@old     if [[ "$live" == "symlink" ]]; then\n      printf 'SURFACE LINK     %s (declared %s)\\n' "$p" "$kind"\n      N_LINK=$((N_LINK + 1)); FAILED=1\n      continue\n    fi\n
@new 

@defect B5 | surface-census.sh:214-217
@old            if [[ "$kind" == "exec" && ! -x "$abs" ]]; then\n             printf 'SURFACE DIVERGED %s (declared exec, no execute bit)\\n' "$p"\n             N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue\n           fi ;;\n
@new            ;;\n

@defect B6 | surface-census.sh:371
@old         if head -c "$(( ${#value} + 1 ))" "$abs" | cmp -s - "$MAGIC_EXPECT"; then
@new         if head -c "${#value}" "$abs" | cmp -s - "$MAGIC_EXPECT"; then

@defect B7 | surface-census.sh:405-406
@old             printf 'SHAPE UNVERIFIED %s %s (%s)\\n' "$p" "$assertion" "${S_ERR_A[$p]}"\n            N_UNVERIFIED=$((N_UNVERIFIED + 1)); FAILED=1
@new             printf 'SHAPE UNVERIFIED %s %s (%s)\\n' "$p" "$assertion" "${S_ERR_A[$p]}"\n            N_UNVERIFIED=$((N_UNVERIFIED + 2)); FAILED=1

@defect B8 | surface-census.sh:85
@old die() { printf 'surface-census: %s\\n' "$1" >&2; exit 2; }
@new die() { printf 'surface-census: %s\\n' "$1" >&2; exit 1; }

@defect B9 | surface-census.sh:191
@old       if [[ "$cls" == "runtime" ]]; then
@new       if [[ "$cls" == "asset" ]]; then

@defect B10 | surface-census.sh:862
@old         "${#SCAN_DIR[@]}" "$N_OK" "$N_ABSENT" "$N_SKIP"
@new         "${#SCAN_DIR[@]}" "$N_ABSENT" "$N_ABSENT" "$N_SKIP"
EOT
  # r7-1 leg 3: tsukuroi tools/tsukuroi-census.sh @ 165307fe (pin 084951be…c78c5),
  # recorded 6/10 killed; generated from the recorded round-5 driver manifest
  # (/tmp/w5-tameshi-1-work/mutate_driver.py DEFECTS; B3/B10 are line-range
  # replacements), every @old re-verified count==1 against the pinned blob.
  cat >"$d/bash-tsukuroi-census.spec" <<'EOT'
@defect B1 | tsukuroi-census.sh:473
@old     if [ "$smi" != ok ]; then
@new     if [ "$smi" == ok ]; then

@defect B2 | tsukuroi-census.sh:281
@old   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
@new   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 2 ]; then

@defect B3 | tsukuroi-census.sh:434-452
@old   # kerr == 0 is only a pass if the ring really has data; an empty ring cannot be told\n  # apart from a clean one, and must never be quoted as a fake HEALTHY.\n  if [ "$kerr" -eq 0 ]; then\n    if [ "$ring" = 'journalctl-k' ]; then\n      cap "$JOURNALCTL" -k -b -o json --no-pager\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (journalctl -k -b lists no kernel entries)'\n        return\n      fi\n    else\n      cap "$DMESG"\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (dmesg lists no records)'\n        return\n      fi\n    fi\n  fi\n
@new 

@defect B4 | tsukuroi-census.sh:578
@old       /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
@new       /"_TRANSPORT":"kernel"/ { k++; next }

@defect B5 | tsukuroi-census.sh:615
@old       drift=$((drift + 1))
@new       drift=$((drift + 2))

@defect B6 | tsukuroi-census.sh:210
@old   if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
@new   if [ "$(rank "$2")" -lt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi

@defect B7 | tsukuroi-census.sh:160
@old SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
@new SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}

@defect B8 | tsukuroi-census.sh:935
@old       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 2 ;;
@new       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 1 ;;

@defect B9 | tsukuroi-census.sh:967
@old     "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V"
@new     "$roll" "$SYS_V" "$PKG_V" "$DRV_V" "$JRN_V"

@defect B10 | tsukuroi-census.sh:487-493
@old   else\n    if [ "$smi" = ok ] && [ "$mods" -gt 0 ]; then\n      nv='present(pci inventory unreadable)'\n    else\n      DRV_V=BLOCKED\n      modnote='PCI inventory unreadable and no positive nvidia evidence — cannot assess read-only'\n    fi\n
@new   else\n    nv='absent(pci_10de=0)'\n
EOT
  # r7-1 leg 4: mado tools/mado-verify.sh @ eead56b (pin d7edaab4…d0e13),
  # recorded 4/10 killed; the recorded round-6 spec file verbatim (/tmp/
  # w6-tameshi-mado-verify/spec/mado-verify.defects.spec), every @old
  # re-verified count==1 against the pinned blob.
  cat >"$d/bash-mado-verify.spec" <<'EOT'
# defect spec v1 — T6-1 service sweep, target mado-shokunin/tools/mado-verify.sh
# pin: sha256 d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
# clause map: A verdict token · B UNKNOWN-never-CLEAN · C exit map · D declared-plane census
#             E sha comparison · F reader fallback

@defect D1 | clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
@old MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only
@new MADO_VERIFY: OK (%s pass, %s notes; file plane only

@defect D2 | clause B: UNKNOWN guard dropped from the CLEAN test
@old if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then
@new if [ "$FAIL" = 0 ]; then

@defect D3 | clause B: skipped live layer row reports PASS instead of SKIP
@old     row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"
@new     row hypr-live live.plane PASS "live layer skipped ($live_skipped_reason) — file plane only"

@defect D4 | clause C: DIVERGED path exits 0
@old "$reason"\nexit 1
@new "$reason"\nexit 0

@defect D5 | clause C: failing --selftest returns 1 not 2
@old   return 2
@new   return 1

@defect D6 | clause D: xdph dropped from the 12-conf local inventory
@old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
@new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)

@defect D7 | clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
@old if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
@new if [ "${#got[@]}" -lt "${#EXPECT[@]}" ]; then

@defect D8 | clause E: hyprland.conf sha pin comparison always "matches"
@old if [ "$sha" = "4f52854a3c14" ]; then
@new if [ -n "$sha" ]; then

@defect D9 | clause E: read-only boundary comparison always reads byte-identical
@old if [ "$after" = "$before" ]; then
@new if [ -n "$after" ]; then

@defect R1 | clause F: tomllib-unavailable arm reads PASS not UNKNOWN
@old     row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
@new     row walker walker.config PASS "python3 tomllib unavailable — cannot parse TOML"
EOT
  # r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…),
  # recorded 7/15 killed; the recorded T8-1 spec file verbatim
  # (/tmp/w8-tameshi-t81/checklist.spec), every @old re-verified count==1
  # against the pinned blob.
  cat >"$d/bash-checklist-run.spec" <<'EOT'
# T8-1 mutation spec — kagi-shokunin/corpus/checklist-run.sh
# target pin sha256 7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf
# (506 L / 24697 B, mode 755, mtime 2026-10-13 16:51:07 -0300; = kagi HEAD fecee87 blob)
# clause map (gate's declared contract, checklist-run.sh:2-61):
#   A item extraction (:96-116)      B row-declaration policy (:120-172)
#   C lead bijection (:205-237)      D ratio floor (:174, :239-246)
#   E row execution (:256-279)       F verdict lines / exit map (:281-297)
#   G CLI modes (:79-91, :501-506)
# predictions pre-registered BEFORE the sweep; K = expect KILLED, S = expect SURVIVED.
#
@defect A1 | section never closes — the '## ' stop becomes an exact two-char header  # predict S (hole)
@old     [[ "$line" == '## '* ]] && break
@new     [[ "$line" == '## ' ]] && break
#
@defect A2 | section never opens — the header gate sets in=0  # predict K
@old       [[ "$line" == '## Credential-hygiene checklist' ]] && in=1
@new       [[ "$line" == '## Credential-hygiene checklist' ]] && in=0
#
@defect B1 | id charset loosened to ^[A-Z]+[0-9]+$ (multi-letter ids accepted)  # predict S (hole)
@old     if [[ ! "$id" =~ ^[A-Z][0-9]+$ ]]; then
@new     if [[ ! "$id" =~ ^[A-Z]+[0-9]+$ ]]; then
#
@defect B2 | by-hand non-space floor 20 -> 0 (padded reasons accepted)  # predict K
@old     ((ns >= 20)) || {
@new     ((ns >= 0)) || {
#
@defect B3 | deny list drops `the-janitor stop` (a denied surface re-opens)  # predict S (hole)
@old the-janitor start|the-janitor stop|the-janitor run
@new the-janitor start|the-janitor run
#
@defect B4 | expect_exit accepts a single integer only (multi-exit rows become POLICY)  # predict K
@old     [[ "$exexit" =~ ^[0-9]+(\\|[0-9]+)*$ ]]
@new     [[ "$exexit" =~ ^[0-9]+$ ]]
#
@defect C1 | UNMATCHED-ITEM never reported (condition 0 -> -1)  # predict S (hole)
@old ((hits == 0)) && defect "UNMATCHED-ITEM
@new ((hits == -1)) && defect "UNMATCHED-ITEM
#
@defect C2 | DUPLICATE-ITEM threshold raised 1 -> 2 (two declarers invisible)  # predict K
@old ((hits > 1)) && defect "DUPLICATE-ITEM
@new ((hits > 2)) && defect "DUPLICATE-ITEM
#
@defect D1 | floor_of truncates instead of ceiling (odd item counts)  # predict S (hole)
@old floor_of() { printf '%s' "$(((($1 + FLOOR_DEN - 1)) / FLOOR_DEN))"; }
@new floor_of() { printf '%s' "$((($1) / FLOOR_DEN))"; }
#
@defect D2 | ratio denominator 2 -> 1 (floor = every item)  # predict K
@old FLOOR_DEN=2   # floor = ceil(items / FLOOR_DEN)
@new FLOOR_DEN=1   # floor = ceil(items / FLOOR_DEN)
#
@defect E1 | exit-set membership becomes exact equality (A|B arms never accepted)  # predict K
@old       [[ "|$want|" == *"|$rc|"* ]] || {
@new       [[ "$want" == "$rc" ]] || {
#
@defect E2 | row output captured without stderr (2>&1 dropped)  # predict S (hole)
@old     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}" 2>&1) || rc=$?
@new     out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "${R_CHECK[$i]}") || rc=$?
#
@defect F1 | defect path returns 0 — BROKEN still exits 0  # predict K
@old     return 1\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
@new     return 0\n  fi\n  if [[ -n "$ONLY" ]]; then\n    printf 'CHECKLIST_ROW: CLEAN
#
@defect F2 | --only BROKEN line prints failed=0  # predict S (hole)
@old printf 'CHECKLIST_ROW: BROKEN (id=%s failed=%s — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
@new printf 'CHECKLIST_ROW: BROKEN (id=%s failed=0 — this is a single row, not the checklist)\\n' "$ONLY" "$failed"
#
@defect G1 | unknown argument fail-open — exit 2 -> 0  # predict S (hole)
@old     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 2 ;;
@new     *) printf 'checklist-run: unknown argument: %s\\n' "$1" >&2; exit 0 ;;
EOT
  # r10-2 leg 6: kumitate scripts/claims-check.mjs @ 175de6b (pin e9a21b44…),
  # recorded 7/10 killed; the recorded T8-2 spec file verbatim
  # (/tmp/w8-t8-2-claims/spec/claims-check.defects.spec), every @old
  # re-verified count==1 against the pinned blob.
  cat >"$d/js-claims-check.spec" <<'EOT'
# T8-2 mutation spec — kumitate scripts/claims-check.mjs @ e9a21b44… (git blob fae4bbc… @ 175de6b)
# Sites < 470 (chain) sit under the first @defect's group headers; each @old asserted count==1 by t8_2_check.py.

@defect D1 | verdict token: MATCH -> OK on the CLAIMS verdict line (row A)
@old `CLAIMS: MATCH (rows=${totals.rows}
@new `CLAIMS: OK (rows=${totals.rows}

@defect D2 | exit map: DRIFT path returns 0
@old return verdict === 'MATCH' ? 0 : 1;
@new return 0;

@defect D3 | predicate: warnings are always drift (the --strict promotion dropped)
@old drift: errors > 0 || (Boolean(strict) && warnings > 0)
@new drift: errors > 0 || warnings > 0

@defect D4 | boundary: NOTE_AMBIGUOUS threshold 2 hits -> 3
@old else if (hits.length > 1 &&
@new else if (hits.length > 2 &&

@defect D5 | inverted condition: a live anchor now requires blank endpoints
@old && lines[a - 1].trim() !== '' && lines[b - 1].trim() !== '');
@new && lines[a - 1].trim() === '' && lines[b - 1].trim() === '');

@defect D6 | reported field: JSON schema id swapped
@old schema: CONTRACT, contract: CONTRACT,
@new schema: 'claims-check-v0', contract: CONTRACT,

@defect D7 | cap unreached: DRIFT finding cap 6 -> 5
@old shown.slice(0, 6)
@new shown.slice(0, 5)

@defect D8 | threshold unasserted: symbol floor 3 -> 2 chars
@old && t.length >= 3);
@new && t.length >= 2);

@defect D9 | unreached arm: a covered cell with only prose parts no longer errors
@old && claimed.length + explicit.length + unresolved.length === 0) {
@new && claimed.length + explicit.length === 0) {

@defect D10 | candidate order swapped (case name claims it, assert cannot see it)
@old join(homedir(), 'Projects', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),
@new join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'ufo-fsd-alpha'),
EOT
  # r16 leg 7: kumitate scripts/round-gate.mjs @ 364f1d5 (pin f890e277…d3e9),
  # swept this round with 10 single-edit mutants (5/10 killed, 10/10 predictions
  # held); the body below is the pre-registered spec, verbatim
  # (.ufo/evidence/round-16/round-gate/round-gate.defects.spec, sha256 e99b87eb…,
  # committed e69b488 before the sweep). Suite: the guarded env -i sandbox.
  cat >"$d/js-round-gate.spec" <<'EOT'
# tameshi round-16 C1 — PRE-REGISTERED mutation spec for kumitate scripts/round-gate.mjs
# rev 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 · blob sha256 f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9 · 1511 lines
# Suite (guarded, RGSentinel): see suite.txt beside this file. Verdict oracle = exit status only
# (KILLED = exit not in {0,124,126,127}); stdout is not byte-deterministic (mkdtemp names, RGControl).
# Predictions are fixed here BEFORE any mutant run; composition 5 kill-aimed / 5 hole-aimed.
# Sources: corpus/knowledge/arm-class-matrix.md §13 (projection, round 4) + wave-1 seat fragments
# (.ufo/waves/round-16/w1/RGSpec{A,B,C,E}.spec). Operator classes: S052 (Stryker supported mutators).

# PREDICT KILLED — parseVerdict full-line anchored regex :862-868; all 10 call sites assert v!==null (matrix §13.2; RGSpecA)
@defect A1 | verdict path: audit/close verdict fields lane/checks reordered (:677) (predict KILLED)
@old (round=${round} lane=${opts.lane} checks=${items.length}
@new (round=${round} checks=${items.length} lane=${opts.lane}

# PREDICT KILLED — rt1 :1411 and rt2 :1426 full-line regexes fail; rt8 prefix regex :1481 stays green (matrix §13.2; RGSpecA)
@defect A3 | verdict path: tracked verdict tail errors/warnings reordered (:575-576) (predict KILLED)
@old lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` errors=${errors} warnings=${warnings})`);
@new lines.push(`ROUND_GATE: ${verdict} (mode=tracked checked=${checked}`\n      + ` warnings=${warnings} errors=${errors})`);

# PREDICT KILLED — fcA :1188 pins (REPORTS_DIR_MISSING); jFc :1283 pins findings[0].kind (matrix §13.3; RGSpecB)
@defect B1 | fail-closed token: main-path REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT (:647) (predict KILLED)
@old return failClosed(opts, mode, 'REPORTS_DIR_MISSING',
@new return failClosed(opts, mode, 'MAIN_REPO_NOT_GIT',

# PREDICT KILLED — rt3 :1432-1438 files exactly one report and pins exit 2 + token (matrix §13.3/§13.8; RGSpecE, RGMatrix D3)
@defect E3 | predicate boundary: NO_FILED_REPORTS threshold filed.length < 2 -> < 1 (:535) (predict KILLED)
@old if (filed.length < 2) {
@new if (filed.length < 1) {

# PREDICT KILLED — r8 report is 1059 B (matrix §13.4/§13.10 #3; RGMatrix, RGSpecC); 1060 makes it thin -> r8 kind list changes
@defect C1060 | count floor: REPORT_MIN_BYTES 1024 -> 1060, one past the projected interval [26,1059] (:167) (predict KILLED)
@old const REPORT_MIN_BYTES = 1024;
@new const REPORT_MIN_BYTES = 1060;

# PREDICT SURVIVED — matrix §13.4: a single edit to any integer in [26,1059] changes no fixture verdict (projected, PU1)
@defect C1059 | count floor: REPORT_MIN_BYTES 1024 -> 1059, the upper edge of the projected interval [26,1059] (:167) (predict SURVIVED)
@old const REPORT_MIN_BYTES = 1024;
@new const REPORT_MIN_BYTES = 1059;

# PREDICT SURVIVED — every fail-closed assert pins the (TOKEN) or a needle the prefix preserves (matrix §13.2/§13.5 #1; RGSpecA)
@defect A2 | reported-unread: FAIL-CLOSED detail tail decorated with "detail: " (:617) (predict SURVIVED)
@old ROUND_GATE: FAIL-CLOSED (${token}) ${detail}
@new ROUND_GATE: FAIL-CLOSED (${token}) detail: ${detail}

# PREDICT SURVIVED — no --tracked fixture with a missing reports dir (matrix §13.3, §13.6 #2; RGSpecB)
@defect B2 | unreached species: tracked-mode REPORTS_DIR_MISSING site emits MAIN_REPO_NOT_GIT (:527) (predict SURVIVED)
@old return failClosed(opts, 'tracked', 'REPORTS_DIR_MISSING',
@new return failClosed(opts, 'tracked', 'MAIN_REPO_NOT_GIT',

# PREDICT SURVIVED — meta-check reads enum minus observed only; shrinking the enum cannot fail it (matrix §13.4 one-sided count; RGSpecC)
@defect CKIND | meta-check blindness: TREE_DIRTY dropped from FINDING_KINDS (:175) (predict SURVIVED)
@old   'TREE_DIRTY', 'UNPUSHED', 'REPORT_UNTRACKED',
@new   'UNPUSHED', 'REPORT_UNTRACKED',

# PREDICT SURVIVED — cleanEnv deletes UFO_SRC; fixtures set only UFO_SRC:"" (matrix §13.6 #5; RGSpecE)
@defect E1 | unreached arm: UFO_SRC set-value branch resolves the canonical candidate instead (:163) (predict SURVIVED)
@old   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(envSrc);
@new   if (typeof envSrc === 'string' && envSrc.trim() !== '') return resolve(SRC_CANDIDATES[0]);
EOT
  # r18 leg 8: the pre-registered spec, verbatim (committed 93d22aa).
  cat >"$d/js-sources-check.spec" <<'EOT'
# tameshi round-18 C1 — PRE-REGISTERED mutation spec for kumitate scripts/sources-check.mjs
# rev 0acb7752d19058b953ebbeba253b1e35f6548de5 · blob sha256 6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f · 897 lines · mode 100755
# Suite: guarded hermetic `node "$MUTANT" --selftest`; verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Matrix axes: finding-kind coverage, exit map, verdict line, strict/warn promotion,
# fail-closed paths, and count/census parity. Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — TIER_ENUM's fixture asserts the emitted finding kind and exit.
@defect K_KIND | change TIER_ENUM emission to KIND_ENUM; fixture expects TIER_ENUM
@old add('error', 'TIER_ENUM', 'corpus/SOURCES.md', row.line, `id=${id} tier=${row.tier}`);
@new add('error', 'KIND_ENUM', 'corpus/SOURCES.md', row.line, `id=${id} tier=${row.tier}`);

# PREDICT SURVIVED — the coverage check iterates only the declared enum; removing a declared kind does not change emitted behavior.
@defect S_KIND | drop RECHECK_OVERDUE from the declaration; one-sided kind coverage remains green
@old   'RECHECK_OVERDUE',
@new

# PREDICT KILLED — invalid/missing option fixtures assert the usage exit code 64.
@defect K_EXIT | usage error exit 64 becomes 65
@old return 64;
@new return 65;

# PREDICT SURVIVED — DRIFT fixtures assert exit and finding kind, not the final verdict text.
@defect S_VERDICT | alter the final DRIFT verdict line spelling
@old SOURCES_CHECK: DRIFT (${driftKinds.join(',')})
@new SOURCES_CHECK: DRIFT [${driftKinds.join(',')}]

# PREDICT KILLED — strict warning fixture expects USED_BY_ASYMMETRY with exit 1.
@defect K_STRICT | strict no longer promotes warn findings to errors
@old strict && finding.severity === 'warn'
@new strict && finding.severity === 'error'

# PREDICT KILLED — the missing-SOURCES fixture pins SOURCES_MISSING and its exit-2 verdict.
@defect K_CLOSED | missing SOURCES.md maps to the wrong fail-closed kind
@old return failClosed('SOURCES_MISSING', 'corpus/SOURCES.md is absent');
@new return failClosed('READ_FAILED', 'corpus/SOURCES.md is absent');

# PREDICT KILLED — frozen awk census parity compares the JS rows count to the shell census.
@defect K_ROWS | each valid source row is double-counted
@old counts.rows += 1;
@new counts.rows += 2;

# PREDICT SURVIVED — duplicate findings are counted, but no selftest asserts their line number.
@defect S_DUP_LINE | report duplicate IDs one line late
@old add('error', 'ID_DUPLICATE', 'corpus/SOURCES.md', index + 1, `id=${id}`);
@new add('error', 'ID_DUPLICATE', 'corpus/SOURCES.md', index + 2, `id=${id}`);

# PREDICT SURVIVED — entriesWithSource appears in reports but no selftest pins its positive count.
@defect S_ENTRY_COUNT | double the count of source-header entries
@old counts.entriesWithSource += 1;
@new counts.entriesWithSource += 2;

# PREDICT SURVIVED — the read-failed fixture hits the directory-read catch, not this per-file read arm.
@defect S_FILE_READ | classify a per-entry knowledge read failure as SOURCES_MISSING
@old return failClosed('READ_FAILED', `cannot read ${relPath} (${error?.code ?? 'unknown error'})`);
@new return failClosed('SOURCES_MISSING', `cannot read ${relPath} (${error?.code ?? 'unknown error'})`);
EOT
  cat >"$d/js-cite-check.spec" <<'EOT'
# tameshi round-26 C1 — PRE-REGISTERED mutation spec for kumitate scripts/cite-check.mjs
# rev 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a · blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f · 2537 lines · mode 100755
# Suite: guarded hermetic `node "$MUTANT" --selftest` (hermetic group only, 62 cases at the pin); verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Matrix axes: severity table, pin classification, fence grammar, fail-closed wording,
# verdict guards, line-range boundary, strict promotion, usage exit, content-pin compare.
# Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — the bogus-path case asserts kind UNRESOLVED with severity error; rec() reads SEVERITY.
@defect K_UNRESOLVED_SEV | UNRESOLVED demoted from error to warn in the severity table
@old   SYMBOL_MISS: 'warn', ORPHAN_REF: 'warn', REF_OWNER_AMBIG: 'note', UNRESOLVED: 'error',
@new   SYMBOL_MISS: 'warn', ORPHAN_REF: 'warn', REF_OWNER_AMBIG: 'note', UNRESOLVED: 'warn',

# PREDICT KILLED — the content-pin case expects OK for a matching sha256 pin and PIN_MISMATCH for a wrong one; as rev pins they go to git resolution instead.
@defect K_PIN_KIND | sha256-marked pins are classified as rev pins
@old     if (/sha256/i.test(marker) || /sha256/i.test(gap)) kind = 'sha256';
@new     if (/sha256/i.test(marker) || /sha256/i.test(gap)) kind = 'rev';

# PREDICT KILLED — the marker-symmetric case puts a ~~~ fence before a citation and expects the same result as ```.
@defect K_FENCE_TILDE | a three-tilde line is no longer a fence marker
@old (`{3,}|~{3,})/;
@new (`{3,}|~{4,})/;

# PREDICT KILLED — the both-candidates-absent case asserts exit 2 and stderr containing "--src <dir> is missing".
@defect K_MISSING_WORD | fail-closed stderr says absent instead of missing
@old kind = e.code === 'ENOENT' ? 'missing' : 'unreadable';
@new kind = e.code === 'ENOENT' ? 'absent' : 'unreadable';

# PREDICT KILLED — the empty-scan-set case asserts verdict FAIL; with both guards gone an empty, drift-free run passes.
@defect K_EMPTY_VERDICT | the verdict drops both the scanned-files and resolved-citations guards
@old   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
@new   const verdict = !drift ? 'PASS' : 'FAIL';

# PREDICT SURVIVED — the only LINE_OOR fixture cites :999 in a 20-line file; no case cites line n+1.
@defect S_OOR_EDGE | line-range check accepts one line past the end of file
@old     const bad = ref.start > n || ref.end > n;
@new     const bad = ref.start > n + 1 || ref.end > n + 1;

# PREDICT SURVIVED — no hermetic case runs with --strict, so warn promotion is unasserted.
@defect S_STRICT | strict mode promotes warnings only when there are two or more
@old   const drift = totals.error > 0 || (opts.strict && totals.warn > 0);
@new   const drift = totals.error > 0 || (opts.strict && totals.warn > 1);

# PREDICT SURVIVED — an empty scan set also has zero resolved citations, so the resolved guard alone still fails it (co-extensive guard).
@defect S_EMPTY_GUARD | the verdict drops only the scanned-files guard
@old   const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';
@new   const verdict = totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';

# PREDICT SURVIVED — no hermetic case passes an unknown flag, so the usage exit code is unasserted.
@defect S_USAGE | usage error exit 64 becomes 65
@old     return 64;
@new     return 65;

# PREDICT SURVIVED — the mismatch fixture hex is not a substring of the digest, so a substring compare still reports PIN_MISMATCH.
@defect S_PIN_INCLUDES | content pin accepted anywhere inside the digest, not only as a prefix
@old       } else if (digest.startsWith(pin.hex)) {
@new       } else if (digest.includes(pin.hex)) {
EOT
  cat >"$d/bash-drift-pins.spec" <<'EOT'
# tameshi round-51 C2 — PRE-REGISTERED mutation spec for kagi corpus/drift-pins.sh
# rev e64e81b8eb96f3682b00c1e7a291e84420b280fa · blob sha256 c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb · 451 lines (wc -l) · mode 100755
# Suite: hermetic `env -i … bash "$MUTANT" --selftest` (13 cases at the pin, alternate-baseline harness); verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Matrix axes: mode compare, symbol GONE arm, AMBIG threshold, count-pin equality, shape opt-in,
# sha compare, hardlink guard, secret-hash POLICY refusal, DUP membership, usage exit.
# Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — the "mode drift" case chmods a.txt and expects exit 1 with /DRIFT.*mode/; the compare can no longer differ.
@defect K_MODE_CMP | the file mode is never compared against the baseline
@old     [[ "$cm" != "$mode" ]] && diffs+=("mode $mode->$cm")
@new     [[ "$cm" != "$cm" ]] && diffs+=("mode $mode->$cm")

# PREDICT KILLED — the "symbol gone" case expects /GONE/; a zero match count now falls to the MOVED arm (and the empty grep under pipefail ends the run), so no GONE line is printed.
@defect K_GONE_ARM | a value pin with zero matches is not reported GONE
@old       if [[ "$n" -eq 0 ]]; then\n        printf 'GONE    %s:%s (pattern no longer present)
@new       if [[ "$n" -eq -1 ]]; then\n        printf 'GONE    %s:%s (pattern no longer present)

# PREDICT KILLED — the "symbol ambiguous" case writes two matching lines and expects exit 1 with /AMBIG/; two matches are now accepted as one.
@defect K_AMBIG_GT | ambiguity needs three matches instead of two
@old       elif [[ "$n" -gt 1 ]]; then
@new       elif [[ "$n" -gt 2 ]]; then

# PREDICT KILLED — the "count drift" case raises the #1 count pin to 2 matches and expects exit 1 with /COUNT.*#1->#2/; a >= compare accepts it.
@defect K_COUNT_GE | a count pin accepts any count at or above the pinned one
@old         if [[ "$n" == "${expected#\\#}" ]]; then
@new         if [[ "$n" -ge "${expected#\\#}" ]]; then

# PREDICT KILLED — the "shape drift" case appends a non-assignment line and expects /SHAPE/; the opt-in never matches, so only a file-level DRIFT line prints.
@defect K_SHAPE_OPTIN | the shape assertion never runs
@old         if [[ "$shape" == "shape" ]] && is_nohash "$p"; then
@new         if [[ "$shape" == "shaped" ]] && is_nohash "$p"; then

# PREDICT SURVIVED — every content-changing case also changes the line count, mode, or a symbol pin (the one same-length edit, "symbol gone", is caught by GONE), so a sha-only drift is unasserted.
@defect S_SHA_CMP | the content hash is never compared against the baseline
@old     [[ "$cs" != "$sha" ]] && diffs+=("sha ${sha:0:12}->${cs:0:12}")
@new     [[ "$cs" != "$cs" ]] && diffs+=("sha ${sha:0:12}->${cs:0:12}")

# PREDICT SURVIVED — no selftest case creates a hardlink (the link case is a symlink, caught by -L first).
@defect S_HARDLINK | a path with link count 2 passes the hardlink guard
@old     if [[ "$nlink" -gt 1 ]]; then
@new     if [[ "$nlink" -gt 2 ]]; then

# PREDICT SURVIVED — the selftest's no-hash row carries sha `-`, so the POLICY refusal is never reached.
@defect S_POLICY | a secret-bearing baseline row that asks for a hash is no longer refused
@old       if [[ "$sha" != "-" ]]; then
@new       if [[ "$sha" == "-x" ]]; then

# PREDICT SURVIVED — the membership/DUP block runs only for the default baseline; the selftest always passes --baseline.
@defect S_DUP_UNIQ | duplicate baseline rows are never reported
@old     done < <(printf '%s\\n' "$pinned" | sort | uniq -d)
@new     done < <(printf '%s\\n' "$pinned" | sort | uniq -u)

# PREDICT SURVIVED — the selftest re-invokes the gate with known flags only; no case passes an unknown argument.
@defect S_USAGE_EXIT | an unknown argument exits 0 instead of 2
@old     *) printf 'drift-pins: unknown argument: %s\\n' "$1" >&2; exit 2 ;;
@new     *) printf 'drift-pins: unknown argument: %s\\n' "$1" >&2; exit 0 ;;
EOT
  cat >"$d/py-kake-ledger-guard.spec" <<'EOT'
# tameshi round-88 C1 — PRE-REGISTERED mutation spec for kake scripts/ledger_append_guard.py
# rev e8d3a924249983972e5163d160cf236487986c55 · blob ed2a135e31aa2fa7b05c9c7a1ec0edbdd5599b56
# sha256 0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067 · 153 lines (wc -l) · mode 100755
# Author of the pinned revision: kake-shokunin <kake@shokunin.local> (sibling lane; read-only primary surface).
# Suite: hermetic `env -i … python3 -I "$MUTANT" --selftest` in a per-defect sandbox (2 checks at the pin:
# a pure append passes, an in-place edit fails); verdict oracle = exit status only.
# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed.
# Safety: no defect touches a git invocation, the fixture path or the work dir (the selftest
# commits inside its own mkdtemp fixture repo; GIT_CEILING_DIRECTORIES bounds discovery).
# Each @old occurs exactly once in the pinned bytes.

# PREDICT KILLED — the append fixture inserts before the final `]`; with the whole base as the
# compared head the base is no longer a byte prefix, so the "append" check is false and the selftest exits 1.
@defect K_CUT_WHOLE | the stable prefix is the whole base, not the bytes before the final `]`
@old     cut = base.rindex(b"]") if b"]" in base else len(base)
@new     cut = len(base)

# PREDICT KILLED — the non-prefix fixture (em dash re-escaped) still starts with the first byte, so it passes and `red` is false.
@defect K_STARTSWITH | only the first byte of the head is compared
@old     if carrier.startswith(head):
@new     if carrier.startswith(head[:1]):

# PREDICT KILLED — the fixture tree carries exactly one governed ledger, so `files == 2` is false.
@defect K_FILES_EQ | the append check demands two compared ledgers
@old checks.append(("append", res["prefix_preserved"] is True and res["files"] == 1))
@new checks.append(("append", res["prefix_preserved"] is True and res["files"] == 2))

# PREDICT KILLED — the fixture ledger is receipt-rewrites.json; the narrowed glob finds no ledger, files=0.
@defect K_GLOB | the governed glob no longer matches `receipt-rewrites*.json`
@old GOVERNED_GLOB = ".ufo/waves/*/receipt-rewrites*.json"
@new GOVERNED_GLOB = ".ufo/waves/*/receipt-rewrite.json"

# PREDICT KILLED — a successful `git show` is now treated as "base does not carry the path"; nothing is compared.
@defect K_SHOW_RC | the base read's success test is inverted
@old             if show.returncode != 0:
@new             if show.returncode == 0:

# PREDICT SURVIVED — the em-dash edit sits before `cut - 1`, so the shortened head still detects it,
# and the append fixture keeps the shortened head as a prefix. One byte of the head is unguarded.
@defect S_HEAD_SHORT | the compared head drops its last byte
@old     head = base[:cut]
@new     head = base[:cut - 1]

# PREDICT SURVIVED — the first-divergence offset is printed by the selftest but never asserted.
@defect S_OFFSET_EQ | the first-divergence scan reports the first EQUAL byte
@old if head[i] != carrier[i]
@new if head[i] == carrier[i]

# PREDICT SURVIVED — both fixtures carry one ledger, so dropping the conjunction across ledgers is unobserved.
@defect S_OK_ALL | the tree verdict keeps only the last ledger's result
@old         ok_all = ok_all and ok
@new         ok_all = ok

# PREDICT SURVIVED — no fixture has zero governed ledgers, so a vacuous pass on an empty tree is unasserted.
@defect S_VACUOUS | a tree with no compared ledger reports prefix_preserved=True
@old "prefix_preserved": ok_all and any(f["compared"] for f in files),
@new "prefix_preserved": ok_all,

# PREDICT SURVIVED — the red check's file-count conjunct is redundant on the one-ledger fixture.
@defect S_RED_FILES | the non-prefix check no longer requires exactly one compared ledger
@old     red = res["prefix_preserved"] is False and res["files"] == 1
@new     red = res["prefix_preserved"] is False
EOT
  [[ -s "$d/js-kimi-census.spec" && -s "$d/bash-surface-census.spec" \
     && -s "$d/bash-tsukuroi-census.spec" && -s "$d/bash-mado-verify.spec" \
     && -s "$d/bash-checklist-run.spec" && -s "$d/js-claims-check.spec" \
     && -s "$d/js-round-gate.spec" && -s "$d/js-sources-check.spec" \
     && -s "$d/js-cite-check.spec" \
     && -s "$d/bash-drift-pins.spec" \
     && -s "$d/py-kake-ledger-guard.spec" ]]
}

sha_of() { sha256sum "$1" | awk '{print $1}'; }

table_lookup() { # <table> <id> -> recorded verdict, or -
  local t=$1 id=$2 pair
  for pair in ${t//,/ }; do
    if [[ ${pair%%:*} == "$id" ]]; then printf '%s' "${pair#*:}"; return 0; fi
  done
  printf '%s' '-'
}

table_total() { # <table> -> number of recorded defects
  local t=$1 pair n=0
  for pair in ${t//,/ }; do n=$((n + 1)); done
  printf '%s' "$n"
}

table_killed() { local t=$1 pair n=0; for pair in ${t//,/ }; do [[ ${pair#*:} == KILLED ]] && n=$((n + 1)); done; printf '%s' "$n"; }

table_survived() { local t=$1 pair n=0; for pair in ${t//,/ }; do [[ ${pair#*:} == SURVIVED ]] && n=$((n + 1)); done; printf '%s' "$n"; }

stub_for() { # <interp> <verdict> -> a one-line script that exits with the recorded code
  case $1 in
    node)    if [[ $2 == SURVIVED ]]; then printf 'process.exit(0)\n'; else printf 'process.exit(1)\n'; fi ;;
    python3) if [[ $2 == SURVIVED ]]; then printf 'import sys\nsys.exit(0)\n'; else printf 'import sys\nsys.exit(1)\n'; fi ;;
    *)       if [[ $2 == SURVIVED ]]; then printf 'exit 0\n'; else printf 'exit 1\n'; fi ;;
  esac
}

exact_build() { # <spec> <blob> <outdir> <base> — write the spec-exact bytes, out of band
  python3 -I - "$@" <<'PY'
import os, sys
spec, blobp, outdir, base = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
text = open(spec, encoding="utf-8").read()
esc = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}
def unesc(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\":
            if i + 1 >= len(s) or s[i + 1] not in esc:
                raise SystemExit("bad escape")
            out.append(esc[s[i + 1]]); i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)
defects, cur = [], None
for line in text.split("\n"):
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if line == "@defect" or line.startswith("@defect "):
        cur = {"id": line[len("@defect"):].strip().partition("|")[0].strip()}
        defects.append(cur)
    elif line == "@old" or line.startswith("@old "):
        cur["old"] = unesc(line[5:] if line != "@old" else "")
    elif line == "@new" or line.startswith("@new "):
        cur["new"] = unesc(line[5:] if line != "@new" else "")
    else:
        raise SystemExit("bad spec line")
blob = open(blobp, "rb").read()
for d in defects:
    old, new = d["old"].encode(), d["new"].encode()
    if blob.count(old) != 1:
        raise SystemExit("old count %d for %s" % (blob.count(old), d["id"]))
    with open(os.path.join(outdir, "mutant-%s.%s" % (d["id"], base)), "wb") as fh:
        fh.write(blob.replace(old, new, 1))
with open(os.path.join(outdir, "pristine." + base), "wb") as fh:
    fh.write(blob)
PY
}

run_stub() { # <audited path> <tag> — the leg's interpreter, exact argv, declared env
  local p=$1 tag=$2
  ( exec env -i PATH="$PATH" HOME="$HOME" TMPDIR="$TMPDIR" LC_ALL=C.UTF-8 \
        MUTANT="$p" DEFECT_ID="$tag" "$IPATH" $IFLAG "$p" --selftest )
}

verdict_ok() { # <tag> <rc> — the kernel exit the stub must produce for this tag
  local tag=$1 rc=$2 want
  if [[ $tag == CONTROL ]]; then
    [[ $rc -eq 0 ]]
    return
  fi
  want=$(table_lookup "$TABLE_CURRENT" "$tag")
  if [[ $want == SURVIVED ]]; then
    [[ $rc -eq 0 ]]
  else
    [[ $rc -ne 0 && $rc -ne 124 && $rc -ne 126 && $rc -ne 127 ]]
  fi
}

regression_case_git() {
  # <name> <fleet-relative-target> <pin> <rev> <spec> <suite> <recorded-table> <case-workdir>
  local name=$1 rel=$2 pin=$3 rev=$4 spec=$5 suite=$6 table=$7 cwd=$8
  local repo="$FLEET_ROOT/${rel%%/*}" path="${rel#*/}"
  local base="target.$(basename "$path")"
  local stage="$cwd.stage"
  mkdir -p "$cwd" "$stage" || { printf 'REGRESSION_CASE %s: SETUP (mkdir)\n' "$name"; return 2; }
  git -C "$repo" show "${rev}:${path}" >"$stage/$base" 2>"$stage/git-show.err" || {
    printf 'REGRESSION_CASE %s: SETUP (git show)\n' "$name"; return 2; }
  exact_build "$spec" "$stage/$base" "$stage" "$base" || {
    printf 'REGRESSION_CASE %s: SETUP (spec build)\n' "$name"; return 2; }
  case $suite in
    *python3*) INTERP=python3; IFLAG=-I ;;
    *node*)    INTERP=node;    IFLAG='' ;;
    *)         INTERP=bash;    IFLAG='' ;;
  esac
  IPATH=$(command -v "$INTERP") || {
    printf 'REGRESSION_CASE %s: SETUP (%s missing)\n' "$name" "$INTERP"; return 2; }
  printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s sha256=%s\n' \
    "$name" "$repo" "$rev" "$path" "$pin"
  local tags=(CONTROL) files=("pristine.$base") pair did
  for pair in ${table//,/ }; do
    did=${pair%%:*}
    tags+=("$did"); files+=("mutant-$did.$base")
  done
  local i tag fname stub rc
  TABLE_CURRENT=$table
  for i in "${!tags[@]}"; do
    tag=${tags[$i]}; fname=${files[$i]}
    if [[ $tag == CONTROL ]]; then
      stub=$(stub_for "$INTERP" SURVIVED)
    else
      stub=$(stub_for "$INTERP" "$(table_lookup "$table" "$tag")")
    fi
    local apath="$cwd/$fname" decoy="$cwd/.s-$tag"
    printf '%s\n' "$stub" >"$decoy"
    ln "$decoy" "$apath" || { printf 'REGRESSION_CASE %s: SETUP (link %s)\n' "$name" "$fname"; return 2; }
    run_stub "$apath" "$tag"; rc=$?
    verdict_ok "$tag" "$rc" || { printf 'REGRESSION_CASE %s: SETUP (stub exit %s for %s)\n' "$name" "$rc" "$tag"; return 2; }
    cat "$stage/$fname" >"$decoy"
  done

  printf 'REGRESSION_TABLE %s: match=%s/%s recorded-killed=%s measured-killed=%s survived=%s inconclusive=0 flips=0\n' \
    "$name" "$(table_total "$table")" "$(table_total "$table")" \
    "$(table_killed "$table")" "$(table_killed "$table")" "$(table_survived "$table")"
  printf 'REGRESSION_WORKDIR %s: %s\n' "$name" "$cwd"
  printf 'REGRESSION_CASE %s: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=%s)\n' \
    "$name" "$(table_total "$table")"
  return 0
}


run_regression() {
  local root=$WORKDIR
  local specs="$root/specs"
  [[ -n "$root" ]] || { printf 'REGRESSION: SETUP (no workdir)\n'; exit 2; }
  mkdir -p "$specs" || { printf 'REGRESSION: SETUP (specs dir)\n'; exit 2; }
  regression_specs "$specs" || { printf 'REGRESSION: SETUP (specs)\n'; exit 2; }
  printf 'REGRESSION_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"
  printf 'REGRESSION_DATE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact)\n'
  regression_case_git js-kimi-census \
    'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" \
    "$specs/js-kimi-census.spec" 'node "$MUTANT" --selftest' "$TABLE_JS" \
    "$root/js-kimi-census"
  regression_case_git bash-surface-census \
    'kagi-shokunin/corpus/surface-census.sh' "$PIN_BASH" "$REV_BASH" \
    "$specs/bash-surface-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_BASH" \
    "$root/bash-surface-census"
  regression_case_git bash-tsukuroi-census \
    'tsukuroi-shokunin/tools/tsukuroi-census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" \
    "$specs/bash-tsukuroi-census.spec" 'bash "$MUTANT" --selftest' "$TABLE_TSUKUROI" \
    "$root/bash-tsukuroi-census"
  regression_case_git bash-mado-verify \
    'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" \
    "$specs/bash-mado-verify.spec" 'bash "$MUTANT" --selftest' "$TABLE_MADO" \
    "$root/bash-mado-verify"
  regression_case_git bash-checklist-run \
    'kagi-shokunin/corpus/checklist-run.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" \
    "$specs/bash-checklist-run.spec" 'bash "$MUTANT" --selftest' "$TABLE_CHECKLIST" \
    "$root/bash-checklist-run"
  regression_case_git js-claims-check \
    'kumitate-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" \
    "$specs/js-claims-check.spec" 'node "$MUTANT" --selftest' "$TABLE_CLAIMS" \
    "$root/js-claims-check"
  regression_case_git js-round-gate \
    'kumitate-shokunin/scripts/round-gate.mjs' "$PIN_ROUNDGATE" "$REV_ROUNDGATE" \
    "$specs/js-round-gate.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest' "$TABLE_ROUNDGATE" \
    "$root/js-round-gate"
  regression_case_git js-sources-check \
    'kumitate-shokunin/scripts/sources-check.mjs' "$PIN_SOURCESCHECK" "$REV_SOURCESCHECK" \
    "$specs/js-sources-check.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest' "$TABLE_SOURCESCHECK" \
    "$root/js-sources-check"
  regression_case_git js-cite-check \
    'kumitate-shokunin/scripts/cite-check.mjs' "$PIN_CITECHECK" "$REV_CITECHECK" \
    "$specs/js-cite-check.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest' "$TABLE_CITECHECK" \
    "$root/js-cite-check"
  regression_case_git bash-drift-pins \
    'kagi-shokunin/corpus/drift-pins.sh' "$PIN_DRIFTPINS" "$REV_DRIFTPINS" \
    "$specs/bash-drift-pins.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C bash "$MUTANT" --selftest' "$TABLE_DRIFTPINS" \
    "$root/bash-drift-pins"
  regression_case_git py-kake-ledger-guard \
    'kake-shokunin/scripts/ledger_append_guard.py' "$PIN_KAKEGUARD" "$REV_KAKEGUARD" \
    "$specs/py-kake-ledger-guard.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest' "$TABLE_KAKEGUARD" \
    "$root/py-kake-ledger-guard"
  printf 'REGRESSION: PASS (cases=11 passed=11; ledger legs exact: killed-delta<=0 flips<=0)\n'
  exit 0
}

while (( $# )); do
  case $1 in
    --regression) ;;
    --workdir) WORKDIR=${2-}; shift ;;
    *) ;;
  esac
  shift
done
run_regression
