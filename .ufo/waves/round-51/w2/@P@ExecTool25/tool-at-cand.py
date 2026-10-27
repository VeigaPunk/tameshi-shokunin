#!/usr/bin/env python3
"""wave-route-mix — pre-dispatch provider-concentration check for a swarm wave spec.

Resolves each seat's role through the operator's live OMP routing table
(task.agentModelOverrides -> alias -> provider/model; read-only) and refuses a
wave in which one primary provider would host more than --max-share of seats.
Round 20 lost 35/72 seats to one provider's capacity errors (Codex, 48.6 %).

  wave-route-mix.py --spec SPEC.json [--config ~/.omp/agent/config.yml] [--max-share 0.40] [--json]
  wave-route-mix.py --selftest

Exit 0 within bound; 1 a provider exceeds the bound or a role is unrouted;
2 unreadable spec/config; 64 usage. Never writes anything.
"""
import argparse, json, re, sys
from collections import Counter
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".omp/agent/config.yml"


def parse_routes(text):
    """Return (overrides role->alias, aliases alias->provider/model) from config.yml text."""
    overrides, aliases, section = {}, {}, None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line == "agentModelOverrides:":
            section, base = "ovr", indent
            continue
        if line == "modelRoles:":
            section, base = "alias", indent
            continue
        if section and indent <= base:
            section = None
        m = re.match(r'^([A-Za-z0-9_.-]+):\s*"?([^"#]+?)"?\s*$', line)
        if section == "ovr" and m:
            overrides[m.group(1)] = m.group(2).strip()
        elif section == "alias" and m:
            aliases[m.group(1)] = m.group(2).strip()
    return overrides, aliases


def provider_of(role, overrides, aliases):
    target = overrides.get(role)
    seen = set()
    while target and target.startswith("@") and target not in seen:
        seen.add(target)
        target = aliases.get(target[1:])
    if not target or "/" not in target:
        return None
    return target.split("/", 1)[0]


def evaluate(roles, overrides, aliases, max_share):
    per = Counter()
    unrouted = []
    for r in roles:
        p = provider_of(r, overrides, aliases)
        if p is None:
            unrouted.append(r)
        else:
            per[p] += 1
    n = len(roles)
    over = {p: c for p, c in per.items() if n and c / n > max_share}
    return {"seats": n, "per_provider": dict(per.most_common()),
            "max_share": max_share, "over_bound": over, "unrouted": sorted(set(unrouted)),
            "ok": not over and not unrouted and n > 0}


def selftest():
    cfg = """task:\n  agentModelOverrides:\n    executor: "@m_a"\n    scout: "@m_b"\n    scribe: "@m_c"\n  eager: always\nmodelRoles:\n  m_a: prov-a/model:max\n  m_b: prov-b/model\n  m_c: prov-c/x\n"""
    o, a = parse_routes(cfg)
    cases = [
        ("parse-overrides", o == {"executor": "@m_a", "scout": "@m_b", "scribe": "@m_c"}),
        ("parse-aliases", a.get("m_a") == "prov-a/model:max"),
        ("balanced-ok", evaluate(["executor"] * 4 + ["scout"] * 4 + ["scribe"] * 2, o, a, 0.40)["ok"]),
        ("concentrated-fails", not evaluate(["executor"] * 5 + ["scout"] * 3 + ["scribe"] * 2, o, a, 0.40)["ok"]),
        ("boundary-equal-ok", evaluate(["executor"] * 4 + ["scout"] * 3 + ["scribe"] * 3, o, a, 0.40)["ok"]),
        ("unrouted-fails", not evaluate(["executor", "scout", "ghost"], o, a, 0.9)["ok"]),
        ("empty-fails", not evaluate([], o, a, 0.40)["ok"]),
        ("alias-cycle-unrouted", provider_of("x", {"x": "@m_y"}, {"m_y": "@m_y"}) is None),
    ]
    bad = [n for n, ok in cases if not ok]
    for n, ok in cases:
        print(f"ROUTEMIX_CASE {n} {'ok' if ok else 'FAIL'}")
    print(f"ROUTEMIX_SELFTEST: {len(cases) - len(bad)}/{len(cases)} pass")
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--max-share", type=float, default=0.40)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 64
    if a.selftest:
        return selftest()
    if not a.spec or not (0 < a.max_share <= 1):
        print("usage: --spec SPEC.json [--max-share (0,1]]", file=sys.stderr)
        return 64
    try:
        spec = json.loads(Path(a.spec).read_text())
        overrides, aliases = parse_routes(Path(a.config).read_text())
    except (OSError, ValueError) as e:
        print(f"ROUTEMIX: unreadable input: {e}", file=sys.stderr)
        return 2
    roles = [it.get("role") for it in spec.get("items", [])]
    res = evaluate(roles, overrides, aliases, a.max_share)
    res["roles"] = dict(Counter(roles).most_common())
    if a.json:
        print(json.dumps(res, indent=1, sort_keys=True))
    shares = " ".join(f"{p}={c}/{res['seats']}" for p, c in res["per_provider"].items())
    print(f"ROUTEMIX: {'OK' if res['ok'] else 'REFUSE'} seats={res['seats']} max_share={a.max_share} {shares}"
          + (f" over={sorted(res['over_bound'])}" if res["over_bound"] else "")
          + (f" unrouted={res['unrouted']}" if res["unrouted"] else ""), file=sys.stderr)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
