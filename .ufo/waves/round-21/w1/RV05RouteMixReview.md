done — no defect in parsing the current live routing sections or in the round-20 refusal. The 0.40 rule is justified only as a primary-concentration guard that catches the 35-seat Codex cluster, not as evidence that every round-20 provider failure is below risk after a rebalance.

## Findings (by severity)

### Medium — 0.40 does not cover the 13-seat Haiku failure mode

`tools/wave-route-mix.py:57-70` compares each **primary** provider count with the total seats and refuses only when `count / seats > max_share`; the default is 0.40 (`:97`). In `.ufo/waves/round-20/original-outcomes.json`, 35 of 72 seats failed on `gpt-6-luna` with Codex capacity errors and 13 failed on `claude-haiku-5-5` with Anthropic rate limits (e.g. lines 12-13, 298-301, 570-581). That is 48.61% versus 18.06% of the wave. Thus 0.40 flags the 35 Codex seats, but the Haiku seats alone are below the bound.

Reproduction: from a scratch copy of the tool, I made `/tmp/tameshi-r21-RV05/probes/r20-codex28.json` by changing seven of the round-20 spec's `executor` roles to `reviewer`, retaining 72 seats and all 13 `scribe` roles. Running the tool with `--max-share 0.40` exits **0**: `ok: true`, `openai-codex: 28`, `zai: 27`, `anthropic: 13`, `google-antigravity: 4`, `unrouted: []`. This is a concrete limit: a future adjusted wave retaining those 13 Haiku seats can pass while carrying the same-size primary group that failed in round 20.

This is **not** a false negative on the historical input: the original 72-seat spec is refused because Codex is 35/72, and refusing the whole wave would have blocked dispatch of the Haiku seats too. `SCORECARD.md:876-878` accurately limits the statement to “exactly the 35 Codex deaths”; `LOG.md:1409-1414` explicitly says this measures primary-route concentration, not fallback availability. Treat 40% as a chosen concentration policy that catches the Codex incident, not an empirically established safe-capacity boundary or a guarantee against all 48 failures.

### Low — the line parser fails closed on common valid YAML forms (not present in the live config)

`tools/wave-route-mix.py:38` is a regex, not a YAML parser. A valid inline comment (`executor: "@m_luna" # primary`) does not match; a single-quoted scalar (`executor: '@m_luna'`) retains its quote characters and does not resolve. In both probes PyYAML parsed `@m_luna`, while this parser produced an unrouted `executor` and `ok: false`. This causes a conservative refusal rather than a silent pass/misroute, and neither form occurs in the current `agentModelOverrides` or `modelRoles` values, so it is not a current-config defect. It is a formatting-compatibility limitation if those sections are edited later.

## Confirmed behavior

- Live `/home/vgpnk/.omp/agent/config.yml` parsing matches `yaml.safe_load` exactly: **18/18** `task.agentModelOverrides` and **25/25** `modelRoles`, with no mismatches. The current double-quoted override aliases and provider/model scalars (including model suffixes such as `:high`/`:max`) are handled correctly.
- `retry.fallbackChains` are not parsed or included in the share calculation. This is consistent with the tool's stated primary-only contract and the round-21 log's explicit limitation; the result must not be read as effective traffic after fallback.
- “Shown able to fail”: **yes, for the intended over-bound refusal**. `--selftest` reports 8/8 and exits 0; the real round-20 spec exits **1**, reports `REFUSE`, and identifies `openai-codex=35/72` as the sole over-bound provider. A fresh run's JSON and stderr compare byte-for-byte with `.ufo/evidence/round-21/routemix-r20-spec1.json` and `.stderr` (`cmp` exit 0 for both); `.exit` records `exit=1`.
- Scope caveat on test sensitivity: the existing independent mutation report `.ufo/waves/round-21/w1/MT3RouteMix.md:86-101,387-389` records 7/12 mutants killed by selftest plus the historical refusal and five survivors (punctuated keys, multi-hop alias, unresolved-role diagnostic, unreadable-input exit, usage exit). That does not negate the demonstrated real refusal, but the demo is not proof that all parser and CLI branches are detected.

## Commands and evidence

Commands run against a scratch copy; no lane source/config/evidence was changed.

```text
cd /tmp/tameshi-r21-RV05 && python3 wave-route-mix.py --selftest
→ exit 0; ROUTEMIX_SELFTEST: 8/8 pass

/usr/bin/python3 /tmp/tameshi-r21-RV05/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json
→ exit 1; seats=72; openai-codex=35; zai=20; anthropic=13; google-antigravity=4; over_bound={"openai-codex":35}; unrouted=[]

/usr/bin/python3 /tmp/tameshi-r21-RV05/wave-route-mix.py --spec /tmp/tameshi-r21-RV05/probes/r20-codex28.json --config /home/vgpnk/.omp/agent/config.yml --max-share 0.40 --json
→ exit 0; ok=true; openai-codex=28/72; anthropic=13/72

`/usr/bin/python3 -c 'import importlib.util,yaml; p="/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/wave-route-mix.py"; s=importlib.util.spec_from_file_location("rm",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); t=open("/home/vgpnk/.omp/agent/config.yml").read(); y=yaml.safe_load(t); o,a=m.parse_routes(t); eo=y["task"]["agentModelOverrides"]; ea=y["modelRoles"]; print(f"overrides {len(o)}/{len(eo)} equal={o==eo}; aliases {len(a)}/{len(ea)} equal={a==ea}; mismatches={[(k,o.get(k),v) for k,v in eo.items() if o.get(k)!=v] + [(k,a.get(k),v) for k,v in ea.items() if a.get(k)!=v]}")'`
→ exit 0; overrides 18/18 equal=True; aliases 25/25 equal=True; mismatches=[]

`/usr/bin/python3 -c 'import json,collections; d=json.load(open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/original-outcomes.json")); c=collections.Counter((s["model"],s["status"]) for s in d["seats"]); print("total",d["total"],"dead",d["dead"],"failed_by_model",{model:n for (model,status),n in c.items() if status=="failed"},"shares",{k:round(v/d["total"],4) for k,v in {"Codex":c[("gpt-6-luna","failed")],"Haiku":c[("claude-haiku-5-5","failed")]}.items()})'`
→ exit 0; total 72, dead 48, failed_by_model={gpt-6-luna:35, claude-haiku-5-5:13}, shares={Codex:0.4861, Haiku:0.1806}

`set +e; /usr/bin/python3 /tmp/tameshi-r21-RV05/wave-route-mix.py --spec /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/spec1.json --config /home/vgpnk/.omp/agent/config.yml --json > /tmp/tameshi-r21-RV05/probes/replay.json 2> /tmp/tameshi-r21-RV05/probes/replay.stderr; rc=$?; printf 'cli_exit=%s\n' "$rc"; cmp -s /tmp/tameshi-r21-RV05/probes/replay.json /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/routemix-r20-spec1.json; printf 'json_artifact_cmp_exit=%s\n' "$?"; cmp -s /tmp/tameshi-r21-RV05/probes/replay.stderr /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/routemix-r20-spec1.stderr; printf 'stderr_artifact_cmp_exit=%s\n' "$?"; printf 'recorded_exit='; cat /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/routemix-r20-spec1.exit`
→ cli_exit=1; JSON cmp=0; stderr cmp=0; recorded_exit=exit=1
```

## Verification gaps

`read xd://lsp` returned `No such tool: xd://lsp` (no LSP device is mounted), so no LSP status/references/definition/diagnostics were available. Literal repository search was used only to locate textual references, not as semantic proof; direct source reading and command repros above are the basis of this review. No production/runtime dispatch, install, or integration was performed.