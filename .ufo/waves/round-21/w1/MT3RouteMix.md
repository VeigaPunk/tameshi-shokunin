done — 12 single-point mutants probed: 7 killed, 5 survived, 0 inconclusive; all 12 scratch files restored byte-for-byte.

# MT3RouteMix mutation findings

## Axes and scope

- **Calibration:** distinguish real behavioral kills from baseline failures, output-only regressions, and uncovered branches. No numerical axis promotion is claimed.
- **Operability:** preserve the round-20 refusal, its provider/seat accounting, unresolved-role diagnostics, and CLI exit classes.
- Frozen source: `33d03b716d3edcf1d8656d46d6df61801d232c52:tools/wave-route-mix.py`.
- Private clone: `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin`. Only independent copies under `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M01` through `M12` were mutated; neither the clone source nor lane source was edited.
- This report is the only lane write. No integration, commit, patch, sibling mutation, subagent dispatch, persistent background job, or alternate runtime was used.

## Detector and controls

Each mutant received the same two commands on its own pristine, mutated, and restored bytes. A run was bounded to 15 seconds; at most four synchronous child commands ran concurrently. Every command inherited the invoking environment with **all `GIT_*` variables removed**. There was no stdout/stderr normalization.

A kill means a difference in `(exit, sha256(stdout), sha256(stderr))` from the successful pristine control; it does **not** mean merely a nonzero exit. The round-20 control is deliberately exit **1**. All 24 per-copy pristine detector runs matched the frozen-source baseline exactly, and all 24 restored runs matched their pristine counterparts. There were no timeouts or baseline failures.

Actual invocation mechanism:

```python
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
subprocess.run(argv, cwd='/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin', env=env, capture_output=True, timeout=15)
```

Pristine `--selftest`: exit **0**, stderr empty, exact stdout:

```text
ROUTEMIX_CASE parse-overrides ok
ROUTEMIX_CASE parse-aliases ok
ROUTEMIX_CASE balanced-ok ok
ROUTEMIX_CASE concentrated-fails ok
ROUTEMIX_CASE boundary-equal-ok ok
ROUTEMIX_CASE unrouted-fails ok
ROUTEMIX_CASE empty-fails ok
ROUTEMIX_CASE alias-cycle-unrouted ok
ROUTEMIX_SELFTEST: 8/8 pass
```

Pristine round-20 `--json`: exit **1**; exact stdout:

```json
{
 "max_share": 0.4,
 "ok": false,
 "over_bound": {
  "openai-codex": 35
 },
 "per_provider": {
  "anthropic": 13,
  "google-antigravity": 4,
  "openai-codex": 35,
  "zai": 20
 },
 "roles": {
  "connector": 4,
  "critic": 10,
  "executor": 23,
  "reviewer": 8,
  "scout": 12,
  "scribe": 13,
  "sentinel": 2
 },
 "seats": 72,
 "unrouted": []
}
```

Exact stderr:

```text
ROUTEMIX: REFUSE seats=72 max_share=0.4 openai-codex=35/72 zai=20/72 anthropic=13/72 google-antigravity=4/72 over=['openai-codex']
```

### Baseline stream hashes

| Detector | Exit | SHA-256 stdout | SHA-256 stderr |
|---|---:|---|---|
| selftest | 0 | `9b9a98aaed4ac48dd9065bd1c251aa256c9fea2869ec52a4750567add1442f30` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| r20 | 1 | `b43bd8943448c1ae918b5ce51c976f33829450b2650fd3242d6033be7c6eca7b` | `88e99fc2d6ad8560d28248ea0717076ca0620e07184d52261b2483ccae6494c5` |

## Kill table

The real-refusal column compares the complete expected result, not just exit 1. `same` means exit and both streams were byte-identical to pristine.

| ID | Single-point mutant (original source line) | Selftest observed | Round-20 observed | Verdict |
|---|---|---|---|---|
| M01 | L38: Reject punctuation in route/alias keys | exit 0; 8/8 pass | exit 1; same | **survived** |
| M02 | L36: Leak sibling section entries across equal dedent | exit 1; 7/8 pass; FAIL parse-overrides | exit 1; same | **killed** |
| M03 | L49: Resolve aliases only one hop | exit 0; 8/8 pass | exit 1; same | **survived** |
| M04 | L54: Report model instead of provider | exit 0; 8/8 pass | exit 1; changed | **killed** |
| M05 | L67: Refuse exactly-at-bound share | exit 1; 6/8 pass; FAIL balanced-ok, boundary-equal-ok | exit 1; same | **killed** |
| M06 | L66: Use distinct role count as seat denominator | exit 1; 6/8 pass; FAIL balanced-ok, boundary-equal-ok | exit 1; changed | **killed** |
| M07 | L67: Truncate share through integer division | exit 1; 7/8 pass; FAIL concentrated-fails | exit 0; changed | **killed** |
| M08 | L70: Ignore unrouted seats in verdict | exit 1; 7/8 pass; FAIL unrouted-fails | exit 1; same | **killed** |
| M09 | L63: Report unresolved provider None instead of role | exit 0; 8/8 pass | exit 1; same | **survived** |
| M10 | L124: Exit success for refusal | exit 0; 8/8 pass | exit 0; changed | **killed** |
| M11 | L114: Map unreadable input to refusal rather than evaluation error | exit 0; 8/8 pass | exit 1; same | **survived** |
| M12 | L108: Map usage failure to success | exit 0; 8/8 pass | exit 1; same | **survived** |

**Counts:** selftest alone killed **5/12**; full round-20 detector killed **4/12**; union **7/12**. An exit-only round-20 check kills only M07 and M10, and the union would be **6/12** because it misses M04. M04 is therefore not an exit-code kill: it is killed by the required provider identity/count output.

### Exact source edits

**M01 — L38**

```diff
-        m = re.match(r'^([A-Za-z0-9_.-]+):\s*"?([^"#]+?)"?\s*$', line)
+        m = re.match(r'^([A-Za-z0-9_]+):\s*"?([^"#]+?)"?\s*$', line)
```

**M02 — L36**

```diff
-        if section and indent <= base:
+        if section and indent < base:
```

**M03 — L49**

```diff
-    while target and target.startswith("@") and target not in seen:
+    if target and target.startswith("@") and target not in seen:
```

**M04 — L54**

```diff
-    return target.split("/", 1)[0]
+    return target.split("/", 1)[1]
```

**M05 — L67**

```diff
-    over = {p: c for p, c in per.items() if n and c / n > max_share}
+    over = {p: c for p, c in per.items() if n and c / n >= max_share}
```

**M06 — L66**

```diff
-    n = len(roles)
+    n = len(set(roles))
```

**M07 — L67**

```diff
-    over = {p: c for p, c in per.items() if n and c / n > max_share}
+    over = {p: c for p, c in per.items() if n and c // n > max_share}
```

**M08 — L70**

```diff
-            "ok": not over and not unrouted and n > 0}
+            "ok": not over and n > 0}
```

**M09 — L63**

```diff
-            unrouted.append(r)
+            unrouted.append(p)
```

**M10 — L124**

```diff
-    return 0 if res["ok"] else 1
+    return 0 if res["ok"] else 0
```

**M11 — L114**

```diff
-        return 2
+        return 1
```

**M12 — L108**

```diff
-        return 64
+        return 0
```

### Changed round-20 outputs

All other mutants had exactly the baseline round-20 exit/stdout/stderr. Complete captured JSON for these four is retained in `results.json` below.

**M04 — exit 1**, exact stderr:

```text
ROUTEMIX: REFUSE seats=72 max_share=0.4 gpt-6-luna:max=35/72 glm-5.3-flash:max=20/72 claude-haiku-5-5:high=13/72 gemini-3.8-flash:high=4/72 over=['gpt-6-luna:max']
```

**M06 — exit 1**, exact stderr:

```text
ROUTEMIX: REFUSE seats=7 max_share=0.4 openai-codex=35/7 zai=20/7 anthropic=13/7 google-antigravity=4/7 over=['anthropic', 'google-antigravity', 'openai-codex', 'zai']
```

**M07 — exit 0**, exact stderr:

```text
ROUTEMIX: OK seats=72 max_share=0.4 openai-codex=35/72 zai=20/72 anthropic=13/72 google-antigravity=4/72
```

**M10 — exit 0**, exact stderr:

```text
ROUTEMIX: REFUSE seats=72 max_share=0.4 openai-codex=35/72 zai=20/72 anthropic=13/72 google-antigravity=4/72 over=['openai-codex']
```

- M04 JSON has model names in `per_provider` and `over_bound` instead of provider names; `ok` remains false.
- M06 JSON has `seats: 7` and all four providers in `over_bound`, rather than 72 seats and only `openai-codex`.
- M07 JSON has `ok: true` and `over_bound: {}`; refusal becomes acceptance.
- M10 JSON and stderr are byte-identical to baseline, but exit is incorrectly 0.

## Missing-case proposals with exercised exact expectations

These are **proposed additions**, exercised only by the read-only scratch witness. They were **not** retroactively added to the frozen two-command detector or its kill counts. Each existing survivor remains a coverage finding, not a changed contract. The witness also demonstrates an owner-selftest case for M04, currently caught only by the real-output check.

1. **`punctuated-route-and-alias` (M01):** parse this config and assert both dictionaries plus the resolved provider:

```yaml
task:
  agentModelOverrides:
    security-reviewer: "@m.a-b"
modelRoles:
  m.a-b: prov-a/model
```

2. **`alias-chain-two-hops` (M03):** `provider_of("x", {"x":"@first"}, {"first":"@second", "second":"prov-a/model"})` must resolve through both aliases. The existing one-node cycle case does not detect truncation to one hop.

3. **`unrouted-role-names` (M09):** `evaluate(["ghost-z", "ghost-a", "ghost-z"], {}, {}, 0.4)` must name sorted unique roles, not `[None]`. The existing `unrouted-fails` case asserts only the verdict.

4. **`provider-aggregation-direct-routes` (M04):** `evaluate(["a","b","c"], {"a":"prov-a/one", "b":"prov-a/two", "c":"prov-b/three"}, {}, 0.5)` must count two different models from the same provider together. Current selftest models are all from different providers, so splitting out the model instead still satisfies its boolean assertions.

5. **`unreadable-input-exit` (M11):** run `--spec /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fixtures/missing-spec.json`, an absent file. Require empty stdout, the exact errno message below, and exit **2**, distinct from a valid refusal (1).

6. **`usage-exit` (M12):** run with no arguments. Require empty stdout, the exact usage message below, and exit **64**. The real-spec and selftest paths both bypass this branch.

Exact expected values (JSON serialization of the witness assertions; `\n` means one final LF):

**punctuated-route-and-alias**

```json
{"aliases": {"m.a-b": "prov-a/model"}, "overrides": {"security-reviewer": "@m.a-b"}, "provider": "prov-a"}
```

**alias-chain-two-hops**

```json
"prov-a"
```

**unrouted-role-names**

```json
{"max_share": 0.4, "ok": false, "over_bound": {}, "per_provider": {}, "seats": 3, "unrouted": ["ghost-a", "ghost-z"]}
```

**provider-aggregation-direct-routes**

```json
{"max_share": 0.5, "ok": false, "over_bound": {"prov-a": 2}, "per_provider": {"prov-a": 2, "prov-b": 1}, "seats": 3, "unrouted": []}
```

**unreadable-input-exit**

```json
{"exit": 2, "stderr": "ROUTEMIX: unreadable input: [Errno 2] No such file or directory: '/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fixtures/missing-spec.json'\n", "stdout": ""}
```

**usage-exit**

```json
{"exit": 64, "stderr": "usage: --spec SPEC.json [--max-share (0,1]]\n", "stdout": ""}
```

### Proposed-witness outcomes

| Target bytes | Witness exit | Failed proposed cases | Restored witness exit |
|---|---:|---|---:|
| Frozen pristine | 0 | none (6/6) | n/a |
| M01 mutated | 1 | punctuated-route-and-alias | 0 (6/6) |
| M03 mutated | 1 | alias-chain-two-hops | 0 (6/6) |
| M04 mutated | 1 | punctuated-route-and-alias, alias-chain-two-hops, provider-aggregation-direct-routes | 0 (6/6) |
| M09 mutated | 1 | unrouted-role-names | 0 (6/6) |
| M11 mutated | 1 | unreadable-input-exit | 0 (6/6) |
| M12 mutated | 1 | usage-exit | 0 (6/6) |

## Hashes and restoration evidence

Every pristine and restored mutant file has SHA-256 **`1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782`** (5,385 bytes). Only the listed single line changed in each mutant; this was checked against the frozen bytes before running it. All 12 restored files passed both exact detector controls afterward.

| ID | Mutated SHA-256 | Before = after SHA-256 | Exact restored detector match |
|---|---|---|---|
| M01 | `71232f01945773f96479b4ee296a4d0a010b3e34a8fa24f0ed97e26ed9b20850` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M02 | `e6540c3298c94639519a139efaf65783eb4e54bab6c811a7f002d854b36ccb31` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M03 | `187406b785b1b5f998751004f94f629f47ab784a3908126c90303fecb792ee1a` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M04 | `6b8c8a08cc737325d53bcc894fb8c08793d08c8e4a6579ceca2ebf3338da72aa` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M05 | `c2127239b0ac67cbf1ea90c64593b4d64d9950928c16f7bfdec363d9978545fe` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M06 | `bc740d448201286bbc454a80709d96a3a57b72addab40eef43def291538d7a3c` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M07 | `d4dd256bd5134bd50ad5c953120f61f0dca9d7af8daae2d92148219fc3dfe5b8` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M08 | `ac45e7092ac15a1a30b6226eb5e4e453c0f5eca73ef7b6bd1919a5864c884746` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M09 | `0ed0322138e42a52451a7bb38945a1f2a9669b8de04982c6ad562ebed9154c94` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M10 | `8ef5019ba9b7228b8dc9970b03c528576f287b7568d1846fc3451387d0db78be` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M11 | `ad3704338039aeda9d1acfef9057cebff163e370d3c8b87f0bd410ce887bb826` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |
| M12 | `d58562b95c641e8e045d6d5bd112dd46b122a8d70473bfd269329ff41ec9029e` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` | True |

Input pins were rehashed after all probes and were unchanged:

| Input | Before = after SHA-256 |
|---|---|
| `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin/tools/wave-route-mix.py` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json` | `ea87dd5ae6d36943d196317975aef4681d496f9f80d165a62d0b933600e1c781` |
| `/home/vgpnk/.omp/agent/config.yml` | `146115c44edf80d2afd63b83c4d4fb39a06e29266fda538260a9b4674f29b385` |
| Lane source `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-route-mix.py` | `1954c4091f16a1f31c71be29cd5b35069294c8d5071f2f7e9d05d18cf0af2782` |

## Exact commands and observed exit codes

Preparation commands:

```sh
mktemp -d /tmp/tameshi-r21-MT3RouteMix-3-XXXXXX
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin && git -C /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin checkout -q --detach 33d03b716d3edcf1d8656d46d6df61801d232c52
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-route-mix.py /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json /home/vgpnk/.omp/agent/config.yml
python3 --version
```

All four commands exited **0**. `mktemp` returned `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB`. Python reported **Python 3.14.8**. The clone/checkout command had no stdout or stderr.

Baseline argv (shell-rendered below; actually invoked through `subprocess.run`, not a shell):

- `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin/tools/wave-route-mix.py --selftest` → **0**.
- `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin/tools/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` → **1**.

Per-mutant argv and phase exits. Each listed command ran three times with identical argv; columns show pristine / mutated / restored exits. Full stdout/stderr and their hashes for every execution are in `results.json`.

| ID / detector | Exact argv | Pristine | Mutated | Restored |
|---|---|---:|---:|---:|
| M01 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M01/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M01 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M01/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M02 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M02/wave-route-mix.py --selftest` | 0 | 1 | 0 |
| M02 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M02/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M03 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M03/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M03 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M03/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M04 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M04/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M04 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M04/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M05 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M05/wave-route-mix.py --selftest` | 0 | 1 | 0 |
| M05 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M05/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M06 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M06/wave-route-mix.py --selftest` | 0 | 1 | 0 |
| M06 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M06/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M07 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M07/wave-route-mix.py --selftest` | 0 | 1 | 0 |
| M07 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M07/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 0 | 1 |
| M08 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M08/wave-route-mix.py --selftest` | 0 | 1 | 0 |
| M08 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M08/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M09 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M09/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M09 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M09/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M10 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M10/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M10 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M10/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 0 | 1 |
| M11 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M11/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M11 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M11/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |
| M12 / selftest | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M12/wave-route-mix.py --selftest` | 0 | 0 | 0 |
| M12 / r20 | `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M12/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json` | 1 | 1 | 1 |

Exact proposed-witness argv (also GIT-scrubbed, same clone cwd, 40-second outer timeout; each nested CLI call has a 15-second timeout):

- pristine: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/fleet/tameshi-shokunin/tools/wave-route-mix.py` → **0**.
- M01: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M01/wave-route-mix.py` → **1**; restored exact same argv → **0**.
- M03: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M03/wave-route-mix.py` → **1**; restored exact same argv → **0**.
- M04: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M04/wave-route-mix.py` → **1**; restored exact same argv → **0**.
- M09: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M09/wave-route-mix.py` → **1**; restored exact same argv → **0**.
- M11: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M11/wave-route-mix.py` → **1**; restored exact same argv → **0**.
- M12: `/usr/bin/python3 /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py /tmp/tameshi-r21-MT3RouteMix-3-WrHstB/mutants/M12/wave-route-mix.py` → **1**; restored exact same argv → **0**.

## Evidence paths, limitations, and defects

- Complete pristine/mutated/restored argv, exits, streams, stream hashes, byte hashes, and detector verdicts: `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/results.json` (SHA-256 `8b0e43b8462d75b737642e2391172e155ea6928f6785f24ef6e15835e836d635`).
- Proposed witness source: `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-cases.py` (SHA-256 `db62af501fbede53f5d0596435c9fc5069a3826dc99a7710a1449da3f78ae752`).
- Exact proposed-case assertions and actual results before mutation, with mutations, and after restoration: `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/proposed-results.json` (SHA-256 `5dd35b479d7eb41edb62eaa022ed370c3b94e1325d2ee47f46d0f0aba69f33bd`).
- Initial frozen-source baseline capture: `/tmp/tameshi-r21-MT3RouteMix-3-WrHstB/baseline.json`.
- The five surviving defects are M01 (punctuated keys), M03 (multi-hop alias), M09 (unrouted role identity), M11 (unreadable-input exit class), and M12 (usage exit class). All had green pristine controls and identical existing detector outputs after mutation; none was called killed by a failure outside the contract.
- Disagreement with an exit-only interpretation: M04 remains exit 1 and is only detected by checking the required provider identity/accounting. The full-output and exit-only results are separated above.
- Live routing was read-only and pinned by SHA-256 before/after; these observations do not assert results under a different routing configuration. No C1/C2 ruler, repository-wide gate, numeric calibration increase, or integration result is claimed.
- Installs/updates: **none**; the preinstalled `/usr/bin/python3` 3.14.8 was sufficient.
- Production changes and integration commit: **none**. Proposed cases were not added to the tool; the assignment requested a mutation probe and recommendations, not a repair.
