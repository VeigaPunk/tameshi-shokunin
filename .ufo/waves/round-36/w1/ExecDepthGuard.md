# Round 36 w1 — depth guard

**Attack:** Re-ran SCORECARD command D at the round-36 refresh commit and independently hashed that commit's frozen runner blob.

**Revision:** `b455001e2589b3f4f471d94a3de7e5e549b9f54c` (refresh commit).

**Exact commands** (run from `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):

```sh
REV=b455001e2589b3f4f471d94a3de7e5e549b9f54c; git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Output: `recorded_cases=9 depth_score=9`.

```sh
REV=b455001e2589b3f4f471d94a3de7e5e549b9f54c; git show "$REV:tools/mutate-and-run.sh" | sha256sum
```

Output: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  -`.

**Verdict: PASS** — command D confirms depth 9 at the refresh commit; the runner digest exactly matches the frozen `a7d3f2dd…` pin. No blocker or risk observed.
