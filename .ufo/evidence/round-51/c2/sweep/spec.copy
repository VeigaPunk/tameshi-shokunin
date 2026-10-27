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
