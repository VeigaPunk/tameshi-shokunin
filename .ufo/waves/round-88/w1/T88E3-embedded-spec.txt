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
