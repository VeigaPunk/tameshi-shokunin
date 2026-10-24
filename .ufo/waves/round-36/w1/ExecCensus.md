# Round 36 W1 — source census

**Attack:** Re-ran the tameshi `SOURCES.md` validation and asserted the registry row count.

**Revision/evidence:** The refresh commit is `b455001e`; the working checkout was `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (one later receipts commit). The census command ran against that working checkout, not a detached checkout of `b455001e`. `git diff --quiet b455001e HEAD -- corpus` returned 0, and `git status --short -- corpus` was empty, so the tameshi corpus used by validation matches the refresh commit.

**Commands and results:**

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log -1 --format='%H %s'` → `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`.
- `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit `0`. Final line: `tameshi\tok\t/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`.
- `grep -cE '^\| S[0-9]{3} \|' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` → `100`.
- Assertions `test "$census_rc" -eq 0 && test "$registry_rows" -eq 100` passed.

The output contained W04 duplicate-URL warnings for S047, S048, S075, S076, S077, S078, S081, and S092, plus W01 for S101; no error findings.

**VERDICT: PASS — census exit 0, final line captured, and all 100 registry rows counted.**