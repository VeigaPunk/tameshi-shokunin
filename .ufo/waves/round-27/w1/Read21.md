Cold read — seat Read21, section at SKILL.md:1281 (rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647; page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95, verified in the clone).

Section bounds: lines 1281–1301, heading "### The operator's runbook — `corpus/knowledge/operator-runbook.md`"; the next heading is line 1302 ("### The six-leg regression — usage and this round's receipt"). Classified `record` (describes the runbook with pointers; no command is instructed).

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read21",
  "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95",
  "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [
    {
      "start": 1281,
      "heading": "### The operator's runbook — `corpus/knowledge/operator-runbook.md`",
      "class": "record",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Identity parenthetical stale at this rev: the section pins the runbook as `e1e349b6…` / 511 L / 31 416 B ('uncommitted worktree file at this read; the sha governs'), but at 2227d833 the file is `8b2e185f…` / 516 lines (wc -l) / 33 515 B. The growth is later append-only errata (ER-R3, round 17; ER-jj2, round 18). The time-stamped claim is not falsified — the sha governs and the runbook itself says 'on any later revision, re-resolve rather than trust' — but the pointer no longer matches the bytes a reader resolves at this rev.",
        "tools/mutate-and-run.sh has also moved since every receipt the section anchors (executed at `cf41efaa…`; current blob `fb91ef76…`, 2016 lines, VERSION line still r10-2). No claim in this section is falsified — ER-R1/ER-R2's account of the r10-2 edit in motion remains accurate — but §2/§7/§9 line anchors re-resolved against current tool bytes will not land."
      ],
      "commands_executed": [
        "python3 tools/trace-inputs.py --root /tmp/Read21-jPia/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read21-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh",
        "python3 tools/trace-inputs.py --root /tmp/Read21-jPia/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read21-2.json -- bash -c 'wc -l corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh; wc -c corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh; sha256sum corpus/knowledge/operator-runbook.md tools/mutate-and-run.sh; git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:corpus/knowledge/operator-runbook.md | sha256sum; git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:tools/mutate-and-run.sh | sha256sum'"
      ],
      "opened": [
        "corpus/knowledge/operator-runbook.md",
        "tools/mutate-and-run.sh"
      ],
      "inputs": {
        "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read21-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read21-2.json"
      ]
    }
  ]
}
```

What I checked (all in a detached clone at 2227d833, never the live lane; both cited files opened under the trace collector, receipts Read21-1/Read21-2, rev field = read_rev, rc 0):

- **"One operator-facing document"** — runbook:1–4 says exactly that ("the mutation service's single operator-facing document … so the service can be run and commissioned without oral context"). ✓
- **"Adds no gate measurement of its own; every line restates an anchored source"** — runbook:7–9 carries the same sentence. ✓
- **Section map** — all twelve headings present and titled as mapped: §0 Quick start (`:35`), §1 service in one page (`:65`), §2 the tool (`:93`), §3 six-case ledger (`:131`), §4 opt-in protocol (`:180`), §5 limits (`:243`), §6 cadence (`:269`), §7 regression mode (`:345`), §8 operator's full loop (`:408`), §9 receipts (`:438`), §10 unknowns (`:462`), Errata append-only (`:481`). ✓
- **"Pointer, not a second home"** — runbook:9–11 states the anchored-source-governs rule and cites `SKILL.md:1249-1254`; SKILL.md at `:1250-1254` (this page) carries the same rendering/divergence rule for `service-limits.md`. ✓
- **"Its receipts were executed at `cf41efaa…` (r7-1, four legs)"** — runbook §2 stamp table pins the tool at `cf41efaa8be5f52d` (r7-1, 1341 L / 61 632 B); §7's embedding-status line reads "four legs at this revision (cases 1–4); cases 5/6 are not embedded" with an executed `REGRESSION: PASS (cases=4 passed=4…)` receipt at tool `cf41efaa…`; §9 says "Executed by the author lane (T10-1) at the revision stamp above" and "tool `held` at `cf41efaa…`". ✓
- **"Errata ER-R1/ER-R2 record the r10-2 edit in motion and name the T2 remedy"** — ER-R1 (`:486-495`) records the worktree holding a r10-2 VERSION blob (`4b3dfed5…`, uncommitted, concurrent lane's in-flight edit); ER-R2 (`:504-512`) records the next reading (`5807fd38…`, still r10-2) and states "The remedy is unchanged: the T2 step, once the edit lands". ✓
- **"The receipt below is that T2 record"** — the following section (1302+) is the r10-2 receipt at `75ed934d…`; consistent (I did not cold-read that section). ✓

Drift observed (the monitor's input-drift flags, quantified): runbook now `8b2e185f…` / 516 L / 33 515 B (was recorded `e1e349b6…` / 511 L / 31 416 B) — later errata ER-R3 and ER-jj2 grew it; tool now `fb91ef76…` / 2016 L, VERSION still r10-2. Worktree bytes equal committed bytes at the rev for both files (`git show <rev>:<path> | sha256sum` matches `sha256sum`). No exception files (SCORECARD.md, LOG.md, round-21 ledger) were opened.

Verdict rationale: every substantive claim checks out against the pinned bytes; the only gaps are the identity parenthetical and the moved tool pin, both anticipated by the section's own "the sha governs" / re-resolve rule — minor, not blocking.

COLDREAD Read21: gap-minor
