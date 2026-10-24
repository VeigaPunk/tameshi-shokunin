# Round 36 W2 — SOURCES row recount

**Attack:** Independently recount `corpus/SOURCES.md` at the refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (`round-36: cold-read refresh`).

**Commands and exact outputs:**

1. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show b455001e2589b3f4f471d94a3de7e5e549b9f54c:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'`

   ```text
   100
   ```

2. Materialized the same revision's file for the census counter:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show b455001e2589b3f4f471d94a3de7e5e549b9f54c:corpus/SOURCES.md > /fast/scratch/hyaku/tameshi-r36-seats/W2ExecRecountRows/SOURCES.md`

   Then ran `TZ=UTC bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/tameshi-r36-seats/W2ExecRecountRows/SOURCES.md --today 2026-10-24`, which printed:

   ```text
   file	rows	100
   file	tier.A	90
   file	tier.B	7
   file	tier.C	3
   file	status.mined	72
   file	status.queued	22
   file	status.rejected	6
   FLEET	rows	100
   FLEET	tier.A	90
   FLEET	tier.B	7
   FLEET	tier.C	3
   FLEET	tier.invalid	0
   FLEET	status.queued	22
   FLEET	status.mined	72
   FLEET	status.rejected	6
   FLEET	status.invalid	0
   FLEET	missing	0
   ```

**Files changed:** This report only.

**Risks/blockers:** None observed.

**VERDICT: PASS — both independent counts report 100 rows at the refresh revision.**
