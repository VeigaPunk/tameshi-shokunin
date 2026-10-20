#!/usr/bin/env python3
"""capture-context.py — round-14 environment and runner-mapping receipt.

Runs the read-only pin probe twice with identical argv/cwd: baseline (ambient
minus every GIT_* key, plus LC_ALL=C) and injected (baseline plus exactly
{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}). The emitted JSON documents
are compared after removing ONLY the top-level observed_at. Any inequality is a
mismatch; there is no retry and no A-B-A. A read-only `git rev-parse --git-dir`
control under both environments proves the injection is observable to git.

The unchanged runner's six header rows, PIN_*/REV_* constants and six
run_regression calls are parsed as text and compared value-for-value and
variable-name-for-variable-name to the round-13 pin manifest. Selftest fixture
calls are outside run_regression and are not parsed. The runner is never run.

No claim: leg/suite execution, result reuse, suite/dependency identity,
simultaneous sibling observation, or sibling stability after the read window.
This is prospective round-14 evidence, not a replacement for any r13 row.

Inputs (lane-relative, read-only): tools/pin-disposition.py,
tools/mutate-and-run.sh, .ufo/evidence/round-13/pin-manifest.json,
.ufo/evidence/round-13/expected.json.
Output: .ufo/evidence/round-14/context-receipt.json (atomic, 0644); no other
path is written.

Exit map: 0 equal observation + effective control + exact env delta + matching
source pins + all six mappings; 1 mismatch (including injected run unusable);
2 could-not-evaluate (missing/unparsable input, poison path exists, baseline
not a six-leg ok pin-disposition-v1 document); 64 usage error, no receipt.

Dependencies: python3 (stdlib), git. No credentials are read.
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

VERSION = "capture-context.py r14 (tameshi-shokunin, 2026-10-20)"
SELF = os.path.realpath(__file__)
LANE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SELF))))
FLEET_ROOT = os.path.dirname(LANE_ROOT)

RECEIPT_SCHEMA = "tameshi-round14-context-receipt-v1"
MAPPING_SCHEMA = "runner-leg-mapping-v1"
PROBE_SCHEMA = "pin-disposition-v1"
MANIFEST_SCHEMA = "pin-manifest-v1"

PROBE_REL = "tools/pin-disposition.py"
RUNNER_REL = "tools/mutate-and-run.sh"
MANIFEST_REL = ".ufo/evidence/round-13/pin-manifest.json"
EXPECTED_R13_REL = ".ufo/evidence/round-13/expected.json"
OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"

INJECTED_ENV = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}
POISON_PATH = INJECTED_ENV["GIT_DIR"]
CONTROL_ENV_ADDITIONS = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
}
PROBE_TIMEOUT_S = 120
CONTROL_TIMEOUT_S = 30

# REV_BASH == REV_CHECKLIST and REV_JS == REV_CLAIMS, so the intended variable
# NAME per leg is checked, not only the resolved value. Recorded runner
# constants at tools/mutate-and-run.sh:542-559 (round-13 pin).
EXPECTED_SUFFIX = {
    "js-kimi-census": "JS",
    "bash-surface-census": "BASH",
    "bash-tsukuroi-census": "TSUKUROI",
    "bash-mado-verify": "MADO",
    "bash-checklist-run": "CHECKLIST",
    "js-claims-check": "CLAIMS",
}

HEADER_ROW_RE = re.compile(
    r"^#\s+(?P<leg>[A-Za-z0-9][A-Za-z0-9._-]*)\s+"
    r"(?P<repo>[A-Za-z0-9._-]+)/(?P<path>[A-Za-z0-9._/-]+)\s+"
    r"\d+/\d+\s+\(\d+\s*%\)\s*$",
    re.MULTILINE,
)
PIN_CONST_RE = re.compile(r"^(PIN_[A-Z0-9_]+)=([0-9a-f]{64})$", re.MULTILINE)
REV_CONST_RE = re.compile(r"^(REV_[A-Z0-9_]+)=([0-9a-f]{40})$", re.MULTILINE)
CONTINUATION_RE = re.compile(r"\\\n")
CALL_RE = re.compile(
    r"regression_case_git[ \t]+"
    r"(?P<leg>[A-Za-z0-9][A-Za-z0-9._-]*)[ \t]+"
    r"'(?P<path>[A-Za-z0-9._/-]+)'[ \t]+"
    r'"\$PIN_(?P<pin>[A-Z0-9_]+)"[ \t]+'
    r'"\$REV_(?P<rev>[A-Z0-9_]+)"[ \t]+'
    r'"[^"]*"[ \t]+'
    r"'[^']*'[ \t]+"
    r'"\$TABLE_(?P<table>[A-Z0-9_]+)"'
)
CALL_LINE_RE = re.compile(r"\s*regression_case_git\s+(?P<leg>[A-Za-z0-9._-]+)\b")
RUN_REGRESSION_RE = re.compile(
    r"^run_regression\(\) \{\n(?P<body>.*?)^\}", re.MULTILINE | re.DOTALL
)
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
DIGEST_RE = re.compile(r"[0-9a-f]{64}")

CHECKS = (
    "header_matches_manifest",
    "pin_name_and_value_match_manifest",
    "rev_name_and_value_match_manifest",
    "leg_call_matches_manifest",
    "constant_names_match_leg",
)

USAGE = """usage: capture-context.py

Inject GIT_DIR explicitly, compare the pin probe's two observations minus the
top-level observed_at, map the runner's six legs to the manifest, and write
.ufo/evidence/round-14/context-receipt.json.

exit 0 equal; exit 1 mismatch; exit 2 could-not-evaluate; exit 64 usage.
"""


class InvalidContext(Exception):
    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lane_path(rel):
    return os.path.join(LANE_ROOT, *rel.split("/"))


def read_lane_bytes(rel):
    try:
        with open(lane_path(rel), "rb") as handle:
            return handle.read()
    except FileNotFoundError:
        raise InvalidContext("missing_input", "missing lane file: " + rel)
    except OSError as exc:
        raise InvalidContext(
            "unreadable_input",
            "cannot read {}: {}".format(rel, exc.strerror or "I/O error"),
        )


def _no_duplicate_keys(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise InvalidContext("invalid_json", "duplicate JSON key " + repr(key))
        record[key] = value
    return record


def parse_json(raw, label):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidContext("invalid_utf8", label + " is not UTF-8")
    try:
        document = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except json.JSONDecodeError as exc:
        raise InvalidContext(
            "invalid_json",
            "{} is not valid JSON: line {} column {}".format(label, exc.lineno, exc.colno),
        )
    if not isinstance(document, dict):
        raise InvalidContext("invalid_json", label + " root is not an object")
    return document


def safe_env():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env["LC_ALL"] = "C"
    return env


def run_bounded(argv, cwd, env, timeout):
    try:
        proc = subprocess.run(
            argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=False,
        )
    except FileNotFoundError:
        raise InvalidContext("missing_executable", "cannot execute: " + argv[0])
    except subprocess.TimeoutExpired:
        raise InvalidContext("timeout", "command exceeded {}s".format(timeout))
    except OSError as exc:
        raise InvalidContext(
            "exec_failed", "cannot execute {}: {}".format(argv[0], exc.strerror or "OS error")
        )
    try:
        stdout = proc.stdout.decode("utf-8")
        stderr = proc.stderr.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidContext("non_utf8_output", "command output is not UTF-8")
    return {"argv": list(argv), "cwd": cwd, "exit": proc.returncode,
            "stdout": stdout, "stderr": stderr}


def parse_runner_mapping(text):
    """Parse six header rows, six PIN_/REV_ constants and six run_regression calls."""
    headers = [match.groupdict() for match in HEADER_ROW_RE.finditer(text)]
    pins = dict(PIN_CONST_RE.findall(text))
    revs = dict(REV_CONST_RE.findall(text))
    body_match = RUN_REGRESSION_RE.search(text)
    if body_match is None:
        raise InvalidContext("runner_unparsed", "cannot locate the run_regression body")
    body = body_match.group("body")
    body_start = text.count("\n", 0, body_match.start("body")) + 1
    joined = CONTINUATION_RE.sub(" ", body)
    calls = []
    for match in CALL_RE.finditer(joined):
        leg = match.group("leg")
        line = next(
            (
                body_start + offset
                for offset, line_text in enumerate(body.splitlines())
                if (found := CALL_LINE_RE.match(line_text)) and found.group("leg") == leg
            ),
            None,
        )
        fleet_path = match.group("path")
        repo, _, rel_path = fleet_path.partition("/")
        calls.append({
            "leg": leg, "repo": repo, "path": rel_path,
            "pin_suffix": match.group("pin"), "rev_suffix": match.group("rev"),
            "table_suffix": match.group("table"), "line": line,
        })
    if len(headers) != 6:
        raise InvalidContext("runner_unparsed", "expected 6 header rows")
    if len(calls) != 6:
        raise InvalidContext("runner_unparsed", "expected 6 leg calls")
    if len(pins) != 6 or len(PIN_CONST_RE.findall(text)) != 6:
        raise InvalidContext("runner_unparsed", "expected 6 unique PIN_ constants")
    if len(revs) != 6 or len(REV_CONST_RE.findall(text)) != 6:
        raise InvalidContext("runner_unparsed", "expected 6 unique REV_ constants")
    header_legs = [row["leg"] for row in headers]
    call_legs = [row["leg"] for row in calls]
    if len(set(header_legs)) != 6 or len(set(call_legs)) != 6 or set(header_legs) != set(call_legs):
        raise InvalidContext("runner_unparsed", "runner leg names are not six unique shared legs")
    return {"headers": headers, "calls": calls, "pins": pins, "revs": revs,
            "body_scope": {"function": "run_regression", "line_start": body_start,
                           "call_count": len(calls)}}


def mapping_block(parsed, manifest_legs):
    calls = {row["leg"]: row for row in parsed["calls"]}
    headers = {row["leg"]: row for row in parsed["headers"]}
    runner_order = [row["leg"] for row in parsed["calls"]]
    manifest_order = [entry["leg"] for entry in manifest_legs]
    rows = []
    for manifest in manifest_legs:
        leg = manifest["leg"]
        call = calls.get(leg)
        header = headers.get(leg)
        suffix = EXPECTED_SUFFIX.get(leg)
        checks = {name: False for name in CHECKS}
        pin_value = rev_value = None
        pin_name = rev_name = table_name = None
        if call is not None:
            pin_name = "PIN_" + call["pin_suffix"]
            rev_name = "REV_" + call["rev_suffix"]
            table_name = "TABLE_" + call["table_suffix"]
            pin_value = parsed["pins"].get(pin_name)
            rev_value = parsed["revs"].get(rev_name)
            checks["leg_call_matches_manifest"] = (
                call["leg"] == leg and call["repo"] == manifest["repo"]
                and call["path"] == manifest["path"]
            )
            checks["pin_name_and_value_match_manifest"] = (
                suffix is not None and pin_name == "PIN_" + suffix
                and pin_value == manifest["expected_sha256"]
            )
            checks["rev_name_and_value_match_manifest"] = (
                suffix is not None and rev_name == "REV_" + suffix
                and rev_value == manifest["pinned_commit"]
            )
            checks["constant_names_match_leg"] = (
                suffix is not None
                and call["pin_suffix"] == call["rev_suffix"] == call["table_suffix"] == suffix
            )
        if header is not None:
            checks["header_matches_manifest"] = (
                header["leg"] == leg and header["repo"] == manifest["repo"]
                and header["path"] == manifest["path"]
            )
        rows.append({
            "leg": leg,
            "manifest": {key: manifest[key] for key in
                         ("repo", "path", "pinned_commit", "expected_sha256")},
            "declared_variable_suffix": suffix,
            "runner_header": header,
            "runner_call": None if call is None else {
                "leg": call["leg"], "repo": call["repo"], "path": call["path"],
                "line": call["line"], "pin_constant": pin_name,
                "rev_constant": rev_name, "table_constant": table_name},
            "pin_value": pin_value, "rev_value": rev_value,
            "checks": checks, "match": all(checks.values()),
        })
    set_equal = set(runner_order) == set(manifest_order)
    order_equal = runner_order == manifest_order
    reasons = []
    if not set_equal:
        reasons.append("runner leg set differs from manifest")
    if not order_equal:
        reasons.append("runner leg order differs from manifest")
    for row in rows:
        failed = [name for name in CHECKS if not row["checks"][name]]
        if failed:
            reasons.append("leg {}: {}".format(row["leg"], ", ".join(failed)))
    return {
        "schema": MAPPING_SCHEMA, "runner_path": RUNNER_REL,
        "parsed": {"header_rows": len(parsed["headers"]),
                   "pin_constants": len(parsed["pins"]),
                   "rev_constants": len(parsed["revs"]),
                   "leg_calls": len(parsed["calls"])},
        "call_scope": parsed["body_scope"],
        "declared_variable_table": dict(EXPECTED_SUFFIX),
        "runner_leg_order": runner_order, "manifest_leg_order": manifest_order,
        "leg_set_equal": set_equal, "leg_order_equal": order_equal,
        "legs": rows,
        "all_match": set_equal and order_equal and all(row["match"] for row in rows),
        "reasons": reasons,
    }


def parse_probe_document(run):
    if run["exit"] != 0:
        return None
    try:
        document = json.loads(run["stdout"])
    except json.JSONDecodeError:
        return None
    return document if isinstance(document, dict) else None


def comparison_block(baseline_run, injected_run, probe_sha256):
    base = parse_probe_document(baseline_run)
    if (base is None or base.get("schema") != PROBE_SCHEMA or base.get("status") != "ok"
            or not isinstance(base.get("legs"), list) or len(base["legs"]) != 6
            or any(row.get("content_status") == "unavailable"
                   or row.get("pinned", {}).get("status") != "verified"
                   for row in base["legs"])
            or "observed_at" not in base):
        raise InvalidContext(
            "probe_baseline_unusable",
            "baseline probe run is not a six-leg ok pin-disposition-v1 document",
        )
    injected = parse_probe_document(injected_run)
    result = {
        "exclusions": ["observed_at"],
        "normalization": "top-level observed_at removed; canonical JSON compared",
        "observed_at": {"baseline": base.get("observed_at"), "injected": None},
        "raw_stdout_equal": baseline_run["stdout"] == injected_run["stdout"],
        "baseline_comparable_sha256": None, "injected_comparable_sha256": None,
        "payload_tool_sha256_matches_disk": None, "equal": False, "error": None,
    }
    if injected is None:
        result["error"] = "injected probe run produced no JSON document (exit={})".format(
            injected_run["exit"]
        )
        return result
    result["observed_at"]["injected"] = injected.get("observed_at")
    if "observed_at" not in injected:
        result["error"] = "injected document has no top-level observed_at"
        return result
    result["payload_tool_sha256_matches_disk"] = (
        base.get("tool_sha256") == probe_sha256
        and injected.get("tool_sha256") == probe_sha256
    )
    base_cmp, inj_cmp = dict(base), dict(injected)
    base_cmp.pop("observed_at")
    inj_cmp.pop("observed_at")
    base_text = json.dumps(base_cmp, sort_keys=True, separators=(",", ":"))
    inj_text = json.dumps(inj_cmp, sort_keys=True, separators=(",", ":"))
    result["baseline_comparable_sha256"] = sha256_bytes(base_text.encode())
    result["injected_comparable_sha256"] = sha256_bytes(inj_text.encode())
    result["equal"] = base_text == inj_text
    return result


def positive_control_block(git_path, base_env):
    control_env = dict(base_env)
    control_env.update(CONTROL_ENV_ADDITIONS)
    injected_env = dict(control_env)
    injected_env.update(INJECTED_ENV)
    argv = [git_path, "-C", LANE_ROOT, "rev-parse", "--git-dir"]
    baseline = run_bounded(argv, LANE_ROOT, control_env, CONTROL_TIMEOUT_S)
    injected = run_bounded(argv, LANE_ROOT, injected_env, CONTROL_TIMEOUT_S)
    baseline_ok = baseline["exit"] == 0 and baseline["stdout"].strip() != ""
    reflects = (POISON_PATH in injected["stdout"]
                or POISON_PATH in injected["stderr"]
                or injected["exit"] != baseline["exit"])
    return {"argv": argv, "baseline": baseline, "injected": injected,
            "baseline_ok": baseline_ok, "injected_reflects_poison": reflects,
            "effective": baseline_ok and injected["exit"] != 0 and reflects,
            "env_additions": dict(CONTROL_ENV_ADDITIONS),
            "env_delta": {"baseline": [], "injected": sorted(INJECTED_ENV)}}


def base_receipt():
    with open(SELF, "rb") as handle:
        tool_sha = sha256_bytes(handle.read())
    return {
        "schema": RECEIPT_SCHEMA, "tool": VERSION, "tool_sha256": tool_sha,
        "observed_at": utc_now(), "lane_root": LANE_ROOT, "fleet_root": FLEET_ROOT,
        "invocation": {"argv": list(sys.argv), "cwd": os.getcwd()},
        "environment": {
            "baseline_policy": "ambient with every GIT_* key removed, plus LC_ALL=C",
            "injected_policy": "baseline plus exactly the keys in injected_env",
            "injected_env": None, "env_delta_keys": None,
            "env_delta_matches_declared": None, "baseline_has_GIT_DIR": None,
            "ambient_git_keys_removed": [], "poison_path": POISON_PATH,
            "poison_path_exists": None, "ambient_env_dumped": False,
        },
        "sources": {}, "runs": {}, "comparison": {}, "positive_control": {},
        "mapping": {}, "result_reuse": "not_established",
        "result_reuse_reason": "content observation + static mapping do not "
        "establish environment, dependency, fixture or suite identity",
        "not_compared": ["leg execution and kill-rate outcomes",
                         "suite environment and dependencies",
                         "concurrent sibling movement"],
    }


def validate_manifest(document):
    if document.get("schema") != MANIFEST_SCHEMA:
        raise InvalidContext("invalid_manifest", "manifest schema is not " + MANIFEST_SCHEMA)
    legs = document.get("legs")
    if not isinstance(legs, list) or len(legs) != 6:
        raise InvalidContext("invalid_manifest", "manifest must carry exactly six legs")
    seen = set()
    for index, entry in enumerate(legs, 1):
        if not isinstance(entry, dict):
            raise InvalidContext("invalid_manifest", "leg {} is not an object".format(index))
        for key in ("leg", "repo", "path", "pinned_commit", "expected_sha256"):
            if not isinstance(entry.get(key), str) or not entry[key]:
                raise InvalidContext(
                    "invalid_manifest", "leg {} has no string {}".format(index, key))
        if entry["leg"] in seen:
            raise InvalidContext("invalid_manifest", "manifest repeats a leg")
        seen.add(entry["leg"])
        if not COMMIT_RE.fullmatch(entry["pinned_commit"]):
            raise InvalidContext("invalid_manifest", "leg {} pinned_commit not 40 hex".format(
                entry["leg"]))
        if not DIGEST_RE.fullmatch(entry["expected_sha256"]):
            raise InvalidContext("invalid_manifest", "leg {} sha256 not 64 hex".format(
                entry["leg"]))
    return legs


def evaluate(receipt):
    removed = sorted(key for key in os.environ if key.startswith("GIT_"))
    environment = receipt["environment"]
    environment["ambient_git_keys_removed"] = removed
    environment["poison_path_exists"] = os.path.lexists(POISON_PATH)
    if environment["poison_path_exists"]:
        raise InvalidContext("poison_path_exists",
                             "injected GIT_DIR target exists: " + POISON_PATH)
    if not os.path.isdir(FLEET_ROOT):
        raise InvalidContext("invalid_fleet_root", "fleet root is not a directory")

    probe_raw = read_lane_bytes(PROBE_REL)
    runner_raw = read_lane_bytes(RUNNER_REL)
    manifest_raw = read_lane_bytes(MANIFEST_REL)
    expected_raw = read_lane_bytes(EXPECTED_R13_REL)
    sources = receipt["sources"] = {
        "probe": {"path": PROBE_REL, "sha256": sha256_bytes(probe_raw)},
        "runner": {"path": RUNNER_REL, "sha256": sha256_bytes(runner_raw)},
        "manifest": {"path": MANIFEST_REL, "sha256": sha256_bytes(manifest_raw)},
        "expected_r13": {"path": EXPECTED_R13_REL,
                         "sha256": sha256_bytes(expected_raw)},
    }
    manifest_doc = parse_json(manifest_raw, MANIFEST_REL)
    expected_doc = parse_json(expected_raw, EXPECTED_R13_REL)
    manifest_legs = validate_manifest(manifest_doc)
    inputs = expected_doc.get("inputs")
    if not isinstance(inputs, dict):
        raise InvalidContext("invalid_expected", "expected.json has no inputs object")
    derived = manifest_doc.get("derived_from")
    if not isinstance(derived, dict):
        raise InvalidContext("invalid_manifest", "manifest has no derived_from object")
    probe_declared = inputs.get(PROBE_REL)
    derived_sha = derived.get("sha256")
    derived_path = derived.get("path")
    sources["probe"].update({
        "declared_sha256": probe_declared,
        "matches_declared": isinstance(probe_declared, str)
        and sources["probe"]["sha256"] == probe_declared,
    })
    sources["runner"].update({
        "manifest_declared_sha256": derived_sha,
        "matches_manifest_declaration": isinstance(derived_sha, str)
        and isinstance(derived_path, str) and derived_path.endswith(RUNNER_REL)
        and sources["runner"]["sha256"] == derived_sha,
    })

    try:
        runner_text = runner_raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidContext("invalid_utf8", RUNNER_REL + " is not UTF-8")
    receipt["mapping"] = mapping_block(parse_runner_mapping(runner_text), manifest_legs)

    python3_path = shutil.which("python3")
    git_path = shutil.which("git")
    if not python3_path:
        raise InvalidContext("missing_executable", "python3 is not on PATH")
    if not git_path:
        raise InvalidContext("missing_executable", "git is not on PATH")

    base_env = safe_env()
    injected_env = dict(base_env)
    injected_env.update(INJECTED_ENV)
    changed = {key for key, value in base_env.items()
               if key in injected_env and injected_env[key] != value}
    delta = sorted((set(base_env) ^ set(injected_env)) | changed)
    actual_injected = {key: injected_env[key] for key in delta}
    environment.update({
        "env_delta_keys": delta, "injected_env": actual_injected,
        "env_delta_matches_declared": delta == sorted(INJECTED_ENV)
        and actual_injected == INJECTED_ENV,
        "baseline_has_GIT_DIR": "GIT_DIR" in base_env,
    })

    argv = [python3_path, PROBE_REL, "--manifest", MANIFEST_REL, "--root", FLEET_ROOT]
    baseline_run = run_bounded(argv, LANE_ROOT, base_env, PROBE_TIMEOUT_S)
    injected_run = run_bounded(argv, LANE_ROOT, injected_env, PROBE_TIMEOUT_S)
    receipt["runs"] = {
        "argv": argv, "argv_equal": baseline_run["argv"] == injected_run["argv"],
        "cwd": LANE_ROOT, "cwd_equal": baseline_run["cwd"] == injected_run["cwd"],
        "env_delta": {"baseline": [], "injected": delta},
        "baseline": baseline_run, "injected": injected_run,
    }
    receipt["positive_control"] = positive_control_block(git_path, base_env)
    receipt["comparison"] = comparison_block(
        baseline_run, injected_run, sources["probe"]["sha256"]
    )


def decide(receipt):
    comparison = receipt.get("comparison") or {}
    control = receipt.get("positive_control") or {}
    mapping = receipt.get("mapping") or {}
    sources = receipt.get("sources") or {}
    environment = receipt.get("environment") or {}
    reasons = []
    if comparison.get("equal") is not True:
        reasons.append("injected observation differs from baseline after "
                       "excluding observed_at: {}".format(
                           comparison.get("error") or "normalized JSON mismatch"))
    if comparison.get("payload_tool_sha256_matches_disk") is not True:
        reasons.append("probe payload tool_sha256 does not match the disk digest")
    if environment.get("env_delta_matches_declared") is not True:
        reasons.append("environment delta is not exactly the declared GIT_DIR injection")
    if environment.get("baseline_has_GIT_DIR") is not False:
        reasons.append("baseline still carries GIT_DIR")
    if control.get("effective") is not True:
        reasons.append("git poison positive control is ineffective")
    if not (sources.get("probe") or {}).get("matches_declared"):
        reasons.append("probe source digest does not match its r13 declared digest")
    if not (sources.get("runner") or {}).get("matches_manifest_declaration"):
        reasons.append("runner source digest does not match the manifest declaration")
    if not mapping.get("all_match"):
        reasons.extend(mapping.get("reasons") or ["runner mapping mismatch"])
    if reasons:
        return "mismatch", 1, reasons
    return "ok", 0, []


def write_receipt(receipt):
    path = lane_path(OUTPUT_REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=".context-receipt.", suffix=".tmp", dir=os.path.dirname(path))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(receipt, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    return OUTPUT_REL


def main(argv):
    if argv:
        if len(argv) == 1 and argv[0] in ("-h", "--help"):
            sys.stdout.write(USAGE)
            return 0
        sys.stderr.write("capture-context.py: unexpected argument(s): {}\n".format(
            " ".join(argv)))
        sys.stderr.write(USAGE)
        return 64
    receipt = base_receipt()
    try:
        evaluate(receipt)
    except InvalidContext as exc:
        receipt.update({"status": "invalid_input", "exit": 2,
                        "error": {"kind": exc.kind, "message": str(exc)},
                        "reasons": [exc.kind + ": " + str(exc)]})
        try:
            path = write_receipt(receipt)
        except (InvalidContext, OSError) as write_exc:
            sys.stderr.write("capture-context.py: cannot write receipt: {}\n".format(
                write_exc))
            return 2
        print("CONTEXT: INVALID (kind={} receipt={} exit=2)".format(exc.kind, path))
        return 2
    status, code, reasons = decide(receipt)
    receipt.update({"status": status, "exit": code, "reasons": reasons})
    try:
        path = write_receipt(receipt)
    except (InvalidContext, OSError) as write_exc:
        sys.stderr.write("capture-context.py: cannot write receipt: {}\n".format(
            write_exc))
        return 2
    print("CONTEXT: {} (receipt={} exit={} probe-equal={} poison-control={} "
          "runner-mapping={})".format(
              status.upper(), path, code,
              (receipt.get("comparison") or {}).get("equal"),
              (receipt.get("positive_control") or {}).get("effective"),
              (receipt.get("mapping") or {}).get("all_match")))
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
