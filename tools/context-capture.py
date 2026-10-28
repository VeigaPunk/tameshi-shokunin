#!/usr/bin/env python3
"""context-capture.py — round-15 retained context-receipt gate.

Question answered: does one retained round-14 context receipt, byte-pinned by
a caller-supplied digest, still reproduce the same verdict after every derived
fact is RE-DERIVED from the receipt's raw fields — or does the retained record
disagree with its own raw observation?

This is the promoted, active replacement for the archived round-14 context
gate `.ufo/evidence/round-14/capture-context.py`. It does not capture, does
not execute the probe or git, and does not read live lane inputs. Check mode
writes nothing; the only writes are --selftest fixtures under mkdtemp.
Frozen mode reads only the archived round-14 receipt named by the built-in
pin. The historical script and every round-12..14 byte remain untouched.

Modes:
  --check [--receipt FILE --expected FILE] [--json]
      Without receipt arguments, replay the frozen round-14 clean receipt
      (.ufo/evidence/round-14/context-receipt.json) against the literal pin in
      this tool: sha256 05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a,
      id context_consistent, exit 0.
      With --receipt and --expected, the receipt bytes must hash to
      expected.receipt_sha256 and the recomputed verdict must equal
      expected.id / expected.exit.
  --selftest
      Run the real CLI by subprocess against isolated synthetic fixtures under
      / the scratch root (tempfile.mkdtemp(dir=tempfile.gettempdir())), pinning literal expected ids and
      exits. Each subprocess reads its own tool source only to report
      tool_sha256; no live domain inputs or live lane path are read, and no
      temp tool copy is made. Fixtures are removed in a finally block.
  -h, --help
      Print usage.

Expected-pin schema `tameshi-context-expected-v1`, exactly four keys:
  {"schema": "tameshi-context-expected-v1",
   "receipt_sha256": "<64 lowercase hex>",
   "id": "<stable finding id or context_consistent>",
   "exit": 0 | 1 | 2}

Raw-field re-derivation (the stored derived booleans are never trusted):
  * comparison: both `runs.*.stdout` documents are parsed strictly (duplicate
    JSON keys rejected); the baseline document must be a six-leg ok
    pin-disposition-v1 document; the canonical payload is compared after
    removing ONLY the top-level observed_at; the comparable digests, equal,
    raw_stdout_equal, observed_at and error values are recomputed (digests and
    the payload flag are null on a recorded injected-run failure);
  * environment: injected_env must be exactly {"GIT_DIR": POISON_PATH} and
    env_delta_keys exactly ["GIT_DIR"]; baseline_has_GIT_DIR is False;
  * runs: argv/cwd equality and the env delta are recomputed from the raw
    baseline/injected run records;
  * positive control: baseline_ok, injected_reflects_poison and effective are
    recomputed from the raw exits/stdout/stderr;
  * sources: probe sha256 == declared_sha256 and runner sha256 ==
    manifest_declared_sha256 are recomputed as strings; match flags must be
    literal True;
  * mapping: all five per-leg checks, per-leg match, leg set/order equality and
    all_match are recomputed from the raw header/call/manifest/constant fields;
  * stored status/exit/reasons are compared with the recomputed verdict; a
    disagreement is itself a finding.

Stable finding IDs:
  context_consistent                exit 0, the only clean verdict
  missing_injected_environment      exit 1 (round-14 guardrail literal pair)
  environment_delta_mismatch        exit 1
  environment_baseline_git_dir      exit 1
  run_argv_mismatch                 exit 1
  run_cwd_mismatch                  exit 1
  run_env_delta_mismatch            exit 1
  comparison_tool_digest_mismatch   exit 1
  comparison_mismatch               exit 1
  positive_control_ineffective      exit 1
  probe_source_digest_mismatch      exit 1
  runner_source_digest_mismatch     exit 1
  mapping_mismatch                  exit 1
  receipt_verdict_mismatch          exit 1
  tool_declaration_mismatch         exit 1 (frozen mode only)
  expected_verdict_mismatch         exit 1
  receipt_missing                   exit 2
  receipt_unreadable                exit 2
  receipt_json_invalid              exit 2
  receipt_structure_invalid         exit 2
  baseline_unusable                 exit 2
  snapshot_tampered                 exit 2
  receipt_records_invalid_input     exit 2
  expected_missing                  exit 2
  expected_unreadable               exit 2
  expected_invalid                  exit 2
  internal_error                    exit 2
  usage_error                       exit 64

Exit map:
  0   clean: the pinned receipt reproduces the pinned clean verdict
  1   failed: a re-derived fact disagrees, the stored verdict disagrees, or the
      recomputed verdict does not match the expected id/exit pin. A pinned
      exit-1 retained mismatch that matches its pin still exits 1: the pin
      asserts the retained verdict, never a clean substrate.
  2   could-not-evaluate: missing/unreadable/malformed/structurally invalid
      receipt or expected pin, unusable baseline observation, snapshot digest
      mismatch, retained invalid-input record, or an unexpected internal error
  64  usage / could-not-evaluate invocation

Pinned-verdict precedence: `expected_verdict_mismatch` becomes the primary
finding and converts a clean 0 into 1; on an exit-1 or exit-2 result it is a
secondary finding and the primary class/exit is preserved. Tamper, malformed
and other could-not-evaluate results never become exit 1.

Bounded scope: the digest pin is the integrity authority; the tool's declared
tool_sha256 is reported, not treated as authentication. A passing check is not
proof that the historical commands were re-executed, nor a claim about
environment, dependency, fixture or suite identity. Each file is read once and
the pinned digest is compared with the same bytes that are parsed; no locking or
directory-integrity guarantee is claimed, and a concurrent writer is outside
this contract. The archived round-14 script is never imported and its
main/evaluate/write paths are never used.

Dependencies: python3 (stdlib). Frozen mode and --selftest read only the
configured archived receipt and synthetic temp fixtures. Explicit mode reads
the caller-selected receipt and expected JSON with the caller's permissions;
callers must select non-secret receipt/expected files. No credential probe is
executed and no ambient environment is dumped.
"""

import copy
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

VERSION = "context-capture.py r15 (tameshi-shokunin, 2026-10-20)"
SELF = os.path.realpath(__file__)
DEFAULT_LANE_ROOT = os.path.dirname(os.path.dirname(SELF))

RECEIPT_SCHEMA = "tameshi-round14-context-receipt-v1"
EXPECTED_SCHEMA = "tameshi-context-expected-v1"
RESULT_SCHEMA = "tameshi-context-gate-result-v1"
MAPPING_SCHEMA = "runner-leg-mapping-v1"
PROBE_SCHEMA = "pin-disposition-v1"

PROBE_REL = "tools/pin-disposition.py"
RUNNER_REL = "tools/mutate-and-run.sh"
MANIFEST_REL = ".ufo/evidence/round-13/pin-manifest.json"
EXPECTED_R13_REL = ".ufo/evidence/round-13/expected.json"

FROZEN_RECEIPT_REL = ".ufo/evidence/round-14/context-receipt.json"
FROZEN_RECEIPT_SHA256 = (
    "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a"
)
FROZEN_TOOL_SHA256 = (
    "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89"
)
FROZEN_EXPECTED_ID = "context_consistent"
FROZEN_EXPECTED_EXIT = 0

INJECTED_ENV = {"GIT_DIR": "/nonexistent/tameshi-round14-poison"}
POISON_PATH = INJECTED_ENV["GIT_DIR"]
CONTROL_ENV_ADDITIONS = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_TERMINAL_PROMPT": "0",
}

EXPECTED_SUFFIX = {
    "js-kimi-census": "JS",
    "bash-surface-census": "BASH",
    "bash-tsukuroi-census": "TSUKUROI",
    "bash-mado-verify": "MADO",
    "bash-checklist-run": "CHECKLIST",
    "js-claims-check": "CLAIMS",
}
CHECK_NAMES = (
    "header_matches_manifest",
    "pin_name_and_value_match_manifest",
    "rev_name_and_value_match_manifest",
    "leg_call_matches_manifest",
    "constant_names_match_leg",
)
NOT_COMPARED_LIMITS = (
    "leg execution and kill-rate outcomes",
    "suite environment and dependencies",
    "concurrent sibling movement",
)

HEX40 = re.compile(r"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")
OBSERVED_AT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
FINDING_ID = re.compile(r"^[a-z][a-z0-9_]{2,63}$")

RECEIPT_KEYS = frozenset(
    (
        "schema", "tool", "tool_sha256", "observed_at", "lane_root",
        "fleet_root", "invocation", "environment", "sources", "runs",
        "comparison", "positive_control", "mapping", "result_reuse",
        "result_reuse_reason", "not_compared", "status", "exit", "reasons",
    )
)
ENVIRONMENT_KEYS = frozenset(
    (
        "baseline_policy", "injected_policy", "injected_env", "env_delta_keys",
        "env_delta_matches_declared", "baseline_has_GIT_DIR",
        "ambient_git_keys_removed", "poison_path", "poison_path_exists",
        "ambient_env_dumped",
    )
)
RUN_KEYS = frozenset(("argv", "cwd", "exit", "stdout", "stderr"))
RUNS_KEYS = frozenset(
    ("argv", "argv_equal", "cwd", "cwd_equal", "env_delta", "baseline",
     "injected")
)
COMPARISON_KEYS = frozenset(
    (
        "exclusions", "normalization", "observed_at", "raw_stdout_equal",
        "baseline_comparable_sha256", "injected_comparable_sha256",
        "payload_tool_sha256_matches_disk", "equal", "error",
    )
)
POSITIVE_CONTROL_KEYS = frozenset(
    (
        "argv", "baseline", "injected", "baseline_ok",
        "injected_reflects_poison", "effective", "env_additions", "env_delta",
    )
)
SOURCE_ENTRY_KEYS = {
    "probe": frozenset(
        ("path", "sha256", "declared_sha256", "matches_declared")),
    "runner": frozenset(
        ("path", "sha256", "manifest_declared_sha256",
         "matches_manifest_declaration")),
    "manifest": frozenset(("path", "sha256")),
    "expected_r13": frozenset(("path", "sha256")),
}
SOURCE_PATHS = {
    "probe": PROBE_REL,
    "runner": RUNNER_REL,
    "manifest": MANIFEST_REL,
    "expected_r13": EXPECTED_R13_REL,
}
MAPPING_KEYS = frozenset(
    (
        "schema", "runner_path", "parsed", "call_scope",
        "declared_variable_table", "runner_leg_order", "manifest_leg_order",
        "leg_set_equal", "leg_order_equal", "legs", "all_match", "reasons",
    )
)
LEG_KEYS = frozenset(
    (
        "leg", "manifest", "declared_variable_suffix", "runner_header",
        "runner_call", "pin_value", "rev_value", "checks", "match",
    )
)
MANIFEST_ENTRY_KEYS = frozenset(
    ("repo", "path", "pinned_commit", "expected_sha256"))
HEADER_KEYS = frozenset(("leg", "repo", "path"))
CALL_KEYS = frozenset(
    ("leg", "repo", "path", "line", "pin_constant", "rev_constant",
     "table_constant")
)
EXPECTED_KEYS = frozenset(("schema", "receipt_sha256", "id", "exit"))
KNOWN_ARGUMENTS = frozenset(
    ("--check", "--selftest", "--json", "--receipt", "--expected", "-h",
     "--help"))

USAGE = """usage: context-capture.py --check [--receipt FILE --expected FILE] [--json]
       context-capture.py --selftest

Retained-receipt gate for the round-14 context observation. `--check` alone
replays the frozen clean receipt against its built-in digest/id/exit pin.
`--check --receipt FILE --expected FILE` pins the receipt sha256 and the exact
expected finding id/exit from an expected file.

The gate re-derives comparison, environment, run, positive-control, source and
runner-mapping facts from raw retained fields; stored status/exit/reasons and
summary booleans are never trusted. It does not capture, execute the probe,
read live lane inputs, or write during check; frozen mode reads only the
archived receipt named by the built-in pin. Explicit mode reads only the
caller-selected receipt and expected JSON with the caller's permissions; select
non-secret files. No credential probe is executed.

exit 0   clean retained receipt (id=context_consistent)
exit 1   re-derived or pinned-verdict mismatch (a matched exit-1 pin still
         reports the retained mismatch as exit 1)
exit 2   could-not-evaluate receipt/expected/snapshot/internal failure
exit 64  usage / could-not-evaluate invocation

expected schema (exactly four keys):
  {"schema": "tameshi-context-expected-v1",
   "receipt_sha256": "<64 lowercase hex>",
   "id": "<stable finding id or context_consistent>",
   "exit": 0 | 1 | 2}
"""


class ScratchRootUnusable(RuntimeError):
    """A set-but-unusable TMPDIR: could-not-evaluate, never a traceback (round 55)."""


def strict_scratch_root():
    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
    fallback to /tmp, preserving CR47 semantics), else the platform default."""
    import os as _os
    t = _os.environ.get("TMPDIR")
    if t:
        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
            raise ScratchRootUnusable(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()


class UsageError(Exception):
    pass


class CouldNotEvaluate(Exception):
    """A retained record that prevents the gate question being evaluated."""

    def __init__(self, finding_id, detail):
        super().__init__(detail)
        self.finding_id = finding_id
        self.detail = detail


# ------------------------------------------------------------------ utilities


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def tool_sha256():
    try:
        with open(SELF, "rb") as handle:
            return sha256_bytes(handle.read())
    except OSError:
        return None


def _no_duplicate_keys(pairs):
    record = {}
    for key, value in pairs:
        if key in record:
            raise ValueError("duplicate JSON key " + repr(key))
        record[key] = value
    return record


def parse_json_strict(raw, finding_id, label):
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise CouldNotEvaluate(finding_id, label + " is not UTF-8")
    try:
        document = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except (ValueError, RecursionError) as exc:
        raise CouldNotEvaluate(
            finding_id, "{} is not strict JSON: {}".format(label, exc))
    return document


def read_regular(path, missing_id, unreadable_id, label):
    try:
        info = os.stat(path)
    except FileNotFoundError:
        raise CouldNotEvaluate(missing_id, label + " is missing: " + path)
    except OSError as exc:
        raise CouldNotEvaluate(
            unreadable_id,
            "cannot stat {}: {}".format(label, exc.strerror or "I/O error"))
    if not stat.S_ISREG(info.st_mode):
        raise CouldNotEvaluate(unreadable_id, label + " is not a regular file")
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except FileNotFoundError:
        raise CouldNotEvaluate(missing_id, label + " is missing: " + path)
    except OSError as exc:
        raise CouldNotEvaluate(
            unreadable_id,
            "cannot read {}: {}".format(label, exc.strerror or "I/O error"))


def collect_finding(findings, finding_id, detail):
    for finding in findings:
        if finding["id"] == finding_id:
            finding["detail"] += "; " + detail
            return
    findings.append({"id": finding_id, "detail": detail})


# ------------------------------------------------------- structural coercion


def require_object(value, path, keys=None):
    if type(value) is not dict:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not an object")
    if keys is not None:
        missing = sorted(key for key in keys if key not in value)
        extra = sorted(key for key in value if key not in keys)
        if missing or extra:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "{} keys mismatch (missing={}, extra={})".format(
                    path, missing, extra))
    return value


def require_string(value, path, nonempty=True):
    if type(value) is not str or (nonempty and not value):
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "{} is not a non-empty string".format(path)
            if nonempty else "{} is not a string".format(path))
    return value


def require_bool(value, path):
    if type(value) is not bool:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not a literal boolean")
    return value


def require_int(value, path, allowed=None):
    if type(value) is not int:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not an integer")
    if allowed is not None and value not in allowed:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "{} value {} is outside {}".format(path, value, sorted(allowed)))
    return value


def require_list(value, path, length=None):
    if type(value) is not list:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not a list")
    if length is not None and len(value) != length:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "{} has {} entries, expected {}".format(path, len(value), length))
    return value


def require_strings(value, path, length=None):
    items = require_list(value, path, length)
    for index, item in enumerate(items):
        require_string(item, "{}[{}]".format(path, index))
    return items


def require_hex(value, path, pattern):
    require_string(value, path)
    if pattern.fullmatch(value) is None:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not canonical lowercase hex")
    return value


def require_observed_at(value, path):
    require_string(value, path)
    if OBSERVED_AT.fullmatch(value) is None:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", path + " is not a UTC timestamp")
    return value


def require_run(value, path):
    require_object(value, path, RUN_KEYS)
    require_strings(value["argv"], path + ".argv")
    require_string(value["cwd"], path + ".cwd")
    require_int(value["exit"], path + ".exit")
    require_string(value["stdout"], path + ".stdout", nonempty=False)
    require_string(value["stderr"], path + ".stderr", nonempty=False)
    return value


def require_env_delta(value, path):
    require_object(value, path, frozenset(("baseline", "injected")))
    require_strings(value["baseline"], path + ".baseline")
    require_strings(value["injected"], path + ".injected")
    return value


# --------------------------------------------------------- receipt structure


def validate_top(receipt):
    if type(receipt) is not dict:
        raise CouldNotEvaluate(
            "receipt_json_invalid", "receipt root is not an object")
    status = receipt.get("status")
    if status not in ("ok", "mismatch", "invalid_input"):
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.status is not ok/mismatch/invalid_input")
    keys = set(RECEIPT_KEYS)
    if status == "invalid_input":
        keys.add("error")
    require_object(receipt, "receipt", frozenset(keys))
    if receipt["schema"] != RECEIPT_SCHEMA:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.schema is not " + RECEIPT_SCHEMA)
    require_string(receipt["tool"], "receipt.tool")
    require_hex(receipt["tool_sha256"], "receipt.tool_sha256", HEX64)
    require_observed_at(receipt["observed_at"], "receipt.observed_at")
    require_string(receipt["lane_root"], "receipt.lane_root")
    require_string(receipt["fleet_root"], "receipt.fleet_root")
    if not os.path.isabs(receipt["lane_root"]):
        raise CouldNotEvaluate(
            "receipt_structure_invalid", "receipt.lane_root is not absolute")
    if not os.path.isabs(receipt["fleet_root"]):
        raise CouldNotEvaluate(
            "receipt_structure_invalid", "receipt.fleet_root is not absolute")
    if os.path.normpath(receipt["fleet_root"]) != os.path.dirname(
            os.path.normpath(receipt["lane_root"])):
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.fleet_root is not the parent of receipt.lane_root")
    invocation = require_object(
        receipt["invocation"], "receipt.invocation",
        frozenset(("argv", "cwd")))
    require_strings(invocation["argv"], "receipt.invocation.argv")
    require_string(invocation["cwd"], "receipt.invocation.cwd")
    if receipt["result_reuse"] != "not_established":
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.result_reuse is not not_established")
    require_string(receipt["result_reuse_reason"],
                   "receipt.result_reuse_reason")
    not_compared = require_strings(
        receipt["not_compared"], "receipt.not_compared")
    for limit in NOT_COMPARED_LIMITS:
        if limit not in not_compared:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "receipt.not_compared omits a configured limit")
    require_int(receipt["exit"], "receipt.exit", {0, 1, 2})
    require_strings(receipt["reasons"], "receipt.reasons")
    return status


def validate_environment(environment):
    if type(environment) is not dict:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", "receipt.environment is not an object")
    allowed = set(ENVIRONMENT_KEYS)
    missing = sorted((allowed - {"injected_env"}) - set(environment))
    extra = sorted(set(environment) - allowed)
    if missing or extra:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.environment keys mismatch (missing={}, extra={})".format(
                missing, extra))
    if "injected_env" in environment:
        injected = environment["injected_env"]
        if injected is not None and type(injected) is not dict:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "receipt.environment.injected_env is neither an object nor null")
        if type(injected) is dict:
            for key, value in injected.items():
                require_string(key, "environment.injected_env key")
                require_string(value, "environment.injected_env[{!r}]".format(key))
    require_string(environment["baseline_policy"], "environment.baseline_policy")
    require_string(environment["injected_policy"], "environment.injected_policy")
    require_strings(environment["env_delta_keys"], "environment.env_delta_keys")
    require_bool(environment["env_delta_matches_declared"],
                 "environment.env_delta_matches_declared")
    require_bool(environment["baseline_has_GIT_DIR"],
                 "environment.baseline_has_GIT_DIR")
    require_strings(environment["ambient_git_keys_removed"],
                    "environment.ambient_git_keys_removed")
    require_string(environment["poison_path"], "environment.poison_path")
    require_bool(environment["poison_path_exists"],
                 "environment.poison_path_exists")
    require_bool(environment["ambient_env_dumped"],
                 "environment.ambient_env_dumped")
    if environment["ambient_env_dumped"] is not False:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "receipt.environment declares an ambient environment dump")
    return environment


def validate_runs(runs):
    require_object(runs, "receipt.runs", RUNS_KEYS)
    require_strings(runs["argv"], "runs.argv")
    require_bool(runs["argv_equal"], "runs.argv_equal")
    require_string(runs["cwd"], "runs.cwd")
    require_bool(runs["cwd_equal"], "runs.cwd_equal")
    require_env_delta(runs["env_delta"], "runs.env_delta")
    require_run(runs["baseline"], "runs.baseline")
    require_run(runs["injected"], "runs.injected")
    return runs


def validate_comparison(comparison):
    require_object(comparison, "receipt.comparison", COMPARISON_KEYS)
    exclusions = require_strings(comparison["exclusions"],
                                 "comparison.exclusions")
    if exclusions != ["observed_at"]:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "comparison.exclusions is not exactly ['observed_at']")
    require_string(comparison["normalization"], "comparison.normalization")
    observed = require_object(
        comparison["observed_at"], "comparison.observed_at",
        frozenset(("baseline", "injected")))
    require_observed_at(observed["baseline"], "comparison.observed_at.baseline")
    if observed["injected"] is not None:
        require_observed_at(observed["injected"],
                            "comparison.observed_at.injected")
    require_bool(comparison["raw_stdout_equal"],
                 "comparison.raw_stdout_equal")
    if comparison["error"] is not None:
        require_string(comparison["error"], "comparison.error")
    for field in ("baseline_comparable_sha256", "injected_comparable_sha256"):
        if comparison[field] is None:
            if comparison["error"] is None:
                raise CouldNotEvaluate(
                    "receipt_structure_invalid",
                    "comparison.{} is null without a recorded error".format(field))
        else:
            require_hex(comparison[field], "comparison." + field, HEX64)
    payload_match = comparison["payload_tool_sha256_matches_disk"]
    if payload_match is None:
        if comparison["error"] is None:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "comparison.payload_tool_sha256_matches_disk is null without "
                "a recorded error")
    else:
        require_bool(payload_match,
                     "comparison.payload_tool_sha256_matches_disk")
    require_bool(comparison["equal"], "comparison.equal")
    return comparison


def validate_positive_control(control):
    require_object(control, "receipt.positive_control", POSITIVE_CONTROL_KEYS)
    require_strings(control["argv"], "positive_control.argv")
    require_run(control["baseline"], "positive_control.baseline")
    require_run(control["injected"], "positive_control.injected")
    require_bool(control["baseline_ok"], "positive_control.baseline_ok")
    require_bool(control["injected_reflects_poison"],
                 "positive_control.injected_reflects_poison")
    require_bool(control["effective"], "positive_control.effective")
    additions = require_object(
        control["env_additions"], "positive_control.env_additions")
    for key, value in additions.items():
        require_string(key, "positive_control.env_additions key")
        require_string(value, "positive_control.env_additions[{!r}]".format(key))
    require_env_delta(control["env_delta"], "positive_control.env_delta")
    return control


def validate_sources(sources):
    require_object(sources, "receipt.sources", frozenset(SOURCE_PATHS))
    for name, path in SOURCE_PATHS.items():
        entry = require_object(
            sources[name], "sources." + name, SOURCE_ENTRY_KEYS[name])
        if entry["path"] != path:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "sources.{} path is not {}".format(name, path))
        require_hex(entry["sha256"], "sources.{}.sha256".format(name), HEX64)
        if name == "probe":
            require_hex(entry["declared_sha256"],
                        "sources.probe.declared_sha256", HEX64)
            require_bool(entry["matches_declared"],
                         "sources.probe.matches_declared")
        elif name == "runner":
            require_hex(entry["manifest_declared_sha256"],
                        "sources.runner.manifest_declared_sha256", HEX64)
            require_bool(entry["matches_manifest_declaration"],
                         "sources.runner.matches_manifest_declaration")
    return sources


def validate_mapping(mapping):
    require_object(mapping, "receipt.mapping", MAPPING_KEYS)
    if mapping["schema"] != MAPPING_SCHEMA:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "mapping.schema is not " + MAPPING_SCHEMA)
    if mapping["runner_path"] != RUNNER_REL:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "mapping.runner_path is not " + RUNNER_REL)
    parsed = require_object(
        mapping["parsed"], "mapping.parsed",
        frozenset(("header_rows", "pin_constants", "rev_constants",
                   "leg_calls")))
    for key, value in parsed.items():
        require_int(value, "mapping.parsed." + key)
        if value != 6:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "mapping.parsed.{} is not 6".format(key))
    scope = require_object(
        mapping["call_scope"], "mapping.call_scope",
        frozenset(("function", "line_start", "call_count")))
    if scope["function"] != "run_regression":
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "mapping.call_scope.function is not run_regression")
    require_int(scope["line_start"], "mapping.call_scope.line_start")
    require_int(scope["call_count"], "mapping.call_scope.call_count")
    if scope["line_start"] < 1 or scope["call_count"] != 6:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", "mapping.call_scope is inconsistent")
    table = require_object(
        mapping["declared_variable_table"], "mapping.declared_variable_table")
    if table != EXPECTED_SUFFIX:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "mapping.declared_variable_table is not the configured six-leg table")
    runner_order = require_strings(
        mapping["runner_leg_order"], "mapping.runner_leg_order", 6)
    manifest_order = require_strings(
        mapping["manifest_leg_order"], "mapping.manifest_leg_order", 6)
    if len(set(runner_order)) != 6 or len(set(manifest_order)) != 6:
        raise CouldNotEvaluate(
            "receipt_structure_invalid", "mapping leg orders repeat a leg")
    require_bool(mapping["leg_set_equal"], "mapping.leg_set_equal")
    require_bool(mapping["leg_order_equal"], "mapping.leg_order_equal")
    require_bool(mapping["all_match"], "mapping.all_match")
    require_strings(mapping["reasons"], "mapping.reasons")
    legs = require_list(mapping["legs"], "mapping.legs", 6)
    seen = set()
    for index, leg in enumerate(legs):
        path = "mapping.legs[{}]".format(index)
        require_object(leg, path, LEG_KEYS)
        name = require_string(leg["leg"], path + ".leg")
        if name in seen:
            raise CouldNotEvaluate(
                "receipt_structure_invalid", "mapping repeats a leg")
        seen.add(name)
        if name not in manifest_order:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "mapping leg is not in manifest_leg_order")
        entry = require_object(
            leg["manifest"], path + ".manifest", MANIFEST_ENTRY_KEYS)
        require_string(entry["repo"], path + ".manifest.repo")
        require_string(entry["path"], path + ".manifest.path")
        require_hex(entry["pinned_commit"],
                    path + ".manifest.pinned_commit", HEX40)
        require_hex(entry["expected_sha256"],
                    path + ".manifest.expected_sha256", HEX64)
        suffix = require_string(leg["declared_variable_suffix"],
                                path + ".declared_variable_suffix")
        if suffix not in EXPECTED_SUFFIX.values():
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                path + ".declared_variable_suffix is not configured")
        header = leg["runner_header"]
        if header is not None:
            require_object(header, path + ".runner_header", HEADER_KEYS)
            for key in ("leg", "repo", "path"):
                require_string(header[key],
                               "{}.runner_header.{}".format(path, key))
        call = leg["runner_call"]
        if call is not None:
            require_object(call, path + ".runner_call", CALL_KEYS)
            for key in ("leg", "repo", "path", "pin_constant", "rev_constant",
                        "table_constant"):
                require_string(call[key],
                               "{}.runner_call.{}".format(path, key))
            if call["line"] is not None:
                require_int(call["line"], path + ".runner_call.line")
        if leg["pin_value"] is not None:
            require_hex(leg["pin_value"], path + ".pin_value", HEX64)
        if leg["rev_value"] is not None:
            require_hex(leg["rev_value"], path + ".rev_value", HEX40)
        checks = require_object(
            leg["checks"], path + ".checks", frozenset(CHECK_NAMES))
        for name_key, value in checks.items():
            require_bool(value, "{}.checks.{}".format(path, name_key))
        require_bool(leg["match"], path + ".match")
    if [leg["leg"] for leg in legs] != manifest_order:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "mapping.legs order does not match manifest_leg_order")
    return mapping


# ----------------------------------------------------- raw-field re-derivation


def embedded_json(text, finding_id, label):
    try:
        document = json.loads(text, object_pairs_hook=_no_duplicate_keys)
    except (ValueError, RecursionError) as exc:
        raise CouldNotEvaluate(
            finding_id, "{} is not strict JSON: {}".format(label, exc))
    return document


def validate_baseline_document(document):
    if type(document) is not dict:
        raise CouldNotEvaluate(
            "baseline_unusable", "baseline observation is not an object")
    if document.get("schema") != PROBE_SCHEMA or document.get("status") != "ok":
        raise CouldNotEvaluate(
            "baseline_unusable",
            "baseline observation is not an ok pin-disposition-v1 document")
    legs = document.get("legs")
    if type(legs) is not list or len(legs) != 6:
        raise CouldNotEvaluate(
            "baseline_unusable", "baseline observation does not carry six legs")
    for index, row in enumerate(legs):
        if type(row) is not dict:
            raise CouldNotEvaluate(
                "baseline_unusable",
                "baseline leg {} is not an object".format(index))
        if row.get("content_status") == "unavailable":
            raise CouldNotEvaluate(
                "baseline_unusable",
                "baseline leg {} is unavailable".format(index))
        pinned = row.get("pinned")
        if type(pinned) is not dict or pinned.get("status") != "verified":
            raise CouldNotEvaluate(
                "baseline_unusable",
                "baseline leg {} is not pinned/verified".format(index))
    observed = document.get("observed_at")
    if type(observed) is not str or OBSERVED_AT.fullmatch(observed) is None:
        raise CouldNotEvaluate(
            "baseline_unusable",
            "baseline observation has no top-level observed_at")
    return document


def canonical_payload(document):
    trimmed = dict(document)
    trimmed.pop("observed_at")
    return json.dumps(trimmed, sort_keys=True, separators=(",", ":"))


def recompute_environment(receipt, findings):
    environment = receipt["environment"]
    injected = environment.get("injected_env", "<absent>")
    if injected == "<absent>":
        collect_finding(
            findings, "missing_injected_environment",
            "receipt.environment.injected_env is absent")
    elif injected is None:
        collect_finding(
            findings, "missing_injected_environment",
            "receipt.environment.injected_env is null")
    else:
        if injected != INJECTED_ENV:
            collect_finding(
                findings, "environment_delta_mismatch",
                "injected_env is not exactly {}".format(sorted(INJECTED_ENV)))
        recomputed_delta_ok = injected == INJECTED_ENV
        if environment["env_delta_keys"] != sorted(INJECTED_ENV):
            collect_finding(
                findings, "environment_delta_mismatch",
                "env_delta_keys is not {}".format(sorted(INJECTED_ENV)))
            recomputed_delta_ok = False
        if environment["env_delta_matches_declared"] is not True:
            collect_finding(
                findings, "environment_delta_mismatch",
                "env_delta_matches_declared is not literal True")
        elif not recomputed_delta_ok:
            collect_finding(
                findings, "environment_delta_mismatch",
                "env_delta_matches_declared claims True but raw fields disagree")
    if environment["baseline_has_GIT_DIR"] is not False:
        collect_finding(
            findings, "environment_baseline_git_dir",
            "baseline_has_GIT_DIR is not literal False")
    if environment["poison_path"] != POISON_PATH:
        collect_finding(
            findings, "environment_delta_mismatch",
            "poison_path is not the bounded injection path")
    if environment["poison_path_exists"] is not False:
        collect_finding(
            findings, "environment_delta_mismatch",
            "poison_path_exists is not literal False")


def recompute_runs(receipt, findings):
    runs = receipt["runs"]
    baseline = runs["baseline"]
    injected = runs["injected"]
    argv_equal = baseline["argv"] == injected["argv"]
    cwd_equal = baseline["cwd"] == injected["cwd"]
    if baseline["argv"] != runs["argv"] or injected["argv"] != runs["argv"]:
        collect_finding(
            findings, "run_argv_mismatch",
            "runs.argv does not equal both raw run argvs")
    if runs["argv_equal"] is not True or not argv_equal:
        collect_finding(
            findings, "run_argv_mismatch",
            "argv_equal is not literal True for equal raw argvs")
    if baseline["cwd"] != runs["cwd"] or injected["cwd"] != runs["cwd"]:
        collect_finding(
            findings, "run_cwd_mismatch",
            "runs.cwd does not equal both raw run cwds")
    if runs["cwd_equal"] is not True or not cwd_equal:
        collect_finding(
            findings, "run_cwd_mismatch",
            "cwd_equal is not literal True for equal raw cwds")
    expected_delta = {"baseline": [], "injected": sorted(INJECTED_ENV)}
    if runs["env_delta"] != expected_delta:
        collect_finding(
            findings, "run_env_delta_mismatch",
            "runs.env_delta is not exactly {}".format(expected_delta))


def recompute_comparison(receipt, findings):
    runs = receipt["runs"]
    recorded = receipt["comparison"]
    probe_sha = receipt["sources"]["probe"]["sha256"]
    if runs["baseline"]["exit"] != 0:
        raise CouldNotEvaluate(
            "baseline_unusable",
            "baseline probe run exited {}".format(runs["baseline"]["exit"]))
    baseline = embedded_json(
        runs["baseline"]["stdout"], "baseline_unusable",
        "runs.baseline.stdout")
    validate_baseline_document(baseline)
    if runs["injected"]["exit"] != 0:
        injected = None
    else:
        try:
            injected = embedded_json(
                runs["injected"]["stdout"], "comparison_mismatch",
                "runs.injected.stdout")
        except CouldNotEvaluate:
            injected = None
    recomputed = {
        "raw_stdout_equal": (
            runs["baseline"]["stdout"] == runs["injected"]["stdout"]),
        "baseline_comparable_sha256": None,
        "injected_comparable_sha256": None,
        "payload_tool_sha256_matches_disk": None,
        "equal": False,
        "error": None,
        "observed_at": {
            "baseline": baseline.get("observed_at"),
            "injected": None,
        },
    }
    if type(injected) is not dict:
        recomputed["error"] = (
            "injected probe run produced no JSON document (exit={})".format(
                runs["injected"]["exit"]))
    elif "observed_at" not in injected:
        recomputed["error"] = "injected document has no top-level observed_at"
    else:
        recomputed["observed_at"]["injected"] = injected.get("observed_at")
        recomputed["payload_tool_sha256_matches_disk"] = (
            baseline.get("tool_sha256") == probe_sha
            and injected.get("tool_sha256") == probe_sha)
        baseline_text = canonical_payload(baseline)
        injected_text = canonical_payload(injected)
        recomputed["baseline_comparable_sha256"] = sha256_bytes(
            baseline_text.encode())
        recomputed["injected_comparable_sha256"] = sha256_bytes(
            injected_text.encode())
        recomputed["equal"] = baseline_text == injected_text

    # The digest declaration is checked before the general equality fields so
    # a payload mismatch keeps its own primary finding.
    if recorded["payload_tool_sha256_matches_disk"] is not (
            recomputed["payload_tool_sha256_matches_disk"]):
        collect_finding(
            findings, "comparison_tool_digest_mismatch",
            "payload_tool_sha256_matches_disk recorded {!r} but raw documents "
            "recompute {!r}".format(
                recorded["payload_tool_sha256_matches_disk"],
                recomputed["payload_tool_sha256_matches_disk"]))
    elif recomputed["payload_tool_sha256_matches_disk"] is False:
        collect_finding(
            findings, "comparison_tool_digest_mismatch",
            "raw documents do not both declare the probe source digest")
    for field in ("baseline", "injected"):
        if recorded["observed_at"][field] != recomputed["observed_at"][field]:
            collect_finding(
                findings, "comparison_mismatch",
                "recorded observed_at.{} {!r} != recomputed {!r}".format(
                    field, recorded["observed_at"][field],
                    recomputed["observed_at"][field]))
    if recorded["raw_stdout_equal"] is not recomputed["raw_stdout_equal"]:
        collect_finding(
            findings, "comparison_mismatch",
            "raw_stdout_equal recorded {!r} but raw stdout recomputes {!r}"
            .format(recorded["raw_stdout_equal"],
                    recomputed["raw_stdout_equal"]))
    for field in ("baseline_comparable_sha256",
                  "injected_comparable_sha256"):
        if recorded[field] != recomputed[field]:
            collect_finding(
                findings, "comparison_mismatch",
                "recorded {} {!r} != recomputed {!r}".format(
                    field, recorded[field], recomputed[field]))
    if recorded["equal"] is not recomputed["equal"]:
        collect_finding(
            findings, "comparison_mismatch",
            "equal recorded {!r} but raw observations recompute {!r}".format(
                recorded["equal"], recomputed["equal"]))
    if recorded["error"] != recomputed["error"]:
        collect_finding(
            findings, "comparison_mismatch",
            "recorded error {!r} != recomputed {!r}".format(
                recorded["error"], recomputed["error"]))
    if recomputed["equal"] is False:
        collect_finding(
            findings, "comparison_mismatch",
            "recomputed canonical observations are not equal")


def recompute_positive_control(control, findings):
    baseline = control["baseline"]
    injected = control["injected"]
    baseline_ok = baseline["exit"] == 0 and baseline["stdout"].strip() != ""
    reflects = (
        POISON_PATH in injected["stdout"]
        or POISON_PATH in injected["stderr"]
        or injected["exit"] != baseline["exit"])
    effective = baseline_ok and injected["exit"] != 0 and reflects
    problems = []
    if control["baseline_ok"] is not baseline_ok:
        problems.append(
            "baseline_ok recorded {!r} but raw run recomputes {!r}".format(
                control["baseline_ok"], baseline_ok))
    if control["injected_reflects_poison"] is not reflects:
        problems.append(
            "injected_reflects_poison recorded {!r} but raw run recomputes "
            "{!r}".format(control["injected_reflects_poison"], reflects))
    if control["effective"] is not effective:
        problems.append(
            "effective recorded {!r} but raw runs recompute {!r}".format(
                control["effective"], effective))
    if control["env_additions"] != CONTROL_ENV_ADDITIONS:
        problems.append("env_additions is not the configured control set")
    expected_delta = {"baseline": [], "injected": sorted(INJECTED_ENV)}
    if control["env_delta"] != expected_delta:
        problems.append("positive-control env_delta is not the bounded delta")
    if problems:
        collect_finding(
            findings, "positive_control_ineffective", "; ".join(problems))
    elif effective is False:
        collect_finding(
            findings, "positive_control_ineffective",
            "raw positive control is ineffective")


def recompute_sources(sources, findings):
    probe = sources["probe"]
    if probe["sha256"] != probe["declared_sha256"]:
        collect_finding(
            findings, "probe_source_digest_mismatch",
            "probe sha256 does not equal its declared digest")
    if probe["matches_declared"] is not True:
        collect_finding(
            findings, "probe_source_digest_mismatch",
            "matches_declared is not literal True")
    runner = sources["runner"]
    if runner["sha256"] != runner["manifest_declared_sha256"]:
        collect_finding(
            findings, "runner_source_digest_mismatch",
            "runner sha256 does not equal its manifest declaration")
    if runner["matches_manifest_declaration"] is not True:
        collect_finding(
            findings, "runner_source_digest_mismatch",
            "matches_manifest_declaration is not literal True")


def recompute_mapping(mapping, findings):
    legs = mapping["legs"]
    problems = []
    recomputed_matches = []
    for leg in legs:
        name = leg["leg"]
        manifest = leg["manifest"]
        canonical_suffix = EXPECTED_SUFFIX.get(name)
        stored_suffix = leg["declared_variable_suffix"]
        if canonical_suffix is None:
            problems.append(
                "leg {!r} is not a configured six-leg name".format(name))
        elif stored_suffix != canonical_suffix:
            problems.append(
                "leg {!r} declared_variable_suffix {!r} is not the canonical "
                "{!r}".format(name, stored_suffix, canonical_suffix))
        suffix = canonical_suffix
        header = leg["runner_header"]
        call = leg["runner_call"]
        checks = {check: False for check in CHECK_NAMES}
        if header is not None:
            checks["header_matches_manifest"] = (
                header["leg"] == name
                and header["repo"] == manifest["repo"]
                and header["path"] == manifest["path"])
        if call is not None and suffix is not None:
            checks["leg_call_matches_manifest"] = (
                call["leg"] == name
                and call["repo"] == manifest["repo"]
                and call["path"] == manifest["path"])
            checks["pin_name_and_value_match_manifest"] = (
                call["pin_constant"] == "PIN_" + suffix
                and leg["pin_value"] == manifest["expected_sha256"])
            checks["rev_name_and_value_match_manifest"] = (
                call["rev_constant"] == "REV_" + suffix
                and leg["rev_value"] == manifest["pinned_commit"])
            checks["constant_names_match_leg"] = (
                call["pin_constant"] == "PIN_" + suffix
                and call["rev_constant"] == "REV_" + suffix
                and call["table_constant"] == "TABLE_" + suffix)
        match = all(checks.values())
        recomputed_matches.append(match)
        for check in CHECK_NAMES:
            if leg["checks"][check] is not checks[check]:
                problems.append(
                    "leg {!r} check {!r} recorded {!r} but raw fields recompute "
                    "{!r}".format(name, check, leg["checks"][check],
                                  checks[check]))
        if leg["match"] is not match:
            problems.append(
                "leg {!r} match recorded {!r} but checks recompute {!r}"
                .format(name, leg["match"], match))
    runner_order = mapping["runner_leg_order"]
    manifest_order = mapping["manifest_leg_order"]
    leg_set_equal = set(runner_order) == set(manifest_order)
    leg_order_equal = runner_order == manifest_order
    if mapping["leg_set_equal"] is not leg_set_equal:
        problems.append(
            "leg_set_equal recorded {!r} but recomputes {!r}".format(
                mapping["leg_set_equal"], leg_set_equal))
    if mapping["leg_order_equal"] is not leg_order_equal:
        problems.append(
            "leg_order_equal recorded {!r} but recomputes {!r}".format(
                mapping["leg_order_equal"], leg_order_equal))
    all_match = (
        leg_set_equal and leg_order_equal
        and len(recomputed_matches) == 6 and all(recomputed_matches))
    if mapping["all_match"] is not all_match:
        problems.append(
            "all_match recorded {!r} but raw fields recompute {!r}".format(
                mapping["all_match"], all_match))
    if problems:
        collect_finding(findings, "mapping_mismatch", "; ".join(problems))
    elif all_match is False:
        collect_finding(
            findings, "mapping_mismatch",
            "recomputed runner mapping does not match the manifest")


def verify_recorded_verdict(receipt, findings):
    computed_exit = 1 if findings else 0
    computed_status = "mismatch" if findings else "ok"
    problems = []
    if receipt["status"] != computed_status:
        problems.append(
            "status recorded {!r} but raw fields recompute {!r}".format(
                receipt["status"], computed_status))
    if receipt["exit"] != computed_exit:
        problems.append(
            "exit recorded {!r} but raw fields recompute {!r}".format(
                receipt["exit"], computed_exit))
    if computed_exit == 0 and receipt["reasons"]:
        problems.append("clean raw fields carry stored reasons")
    if computed_exit == 1 and not receipt["reasons"]:
        problems.append("mismatched raw fields carry no stored reasons")
    if problems:
        collect_finding(
            findings, "receipt_verdict_mismatch", "; ".join(problems))
    code = 1 if findings else 0
    status = "mismatch" if findings else "ok"
    return status, code, findings


def validate_invalid_blocks(receipt):
    for name in ("sources", "runs", "comparison", "positive_control", "mapping"):
        if receipt[name] != {}:
            raise CouldNotEvaluate(
                "receipt_structure_invalid",
                "invalid_input receipt carries a non-empty " + name)
    if receipt["exit"] != 2:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "invalid_input receipt exit is not 2")
    error = require_object(
        receipt["error"], "receipt.error", frozenset(("kind", "message")))
    require_string(error["kind"], "receipt.error.kind")
    require_string(error["message"], "receipt.error.message")
    if not receipt["reasons"]:
        raise CouldNotEvaluate(
            "receipt_structure_invalid",
            "invalid_input receipt carries no reasons")


def check_receipt(receipt, frozen=False):
    status = validate_top(receipt)
    if status == "invalid_input":
        validate_invalid_blocks(receipt)
        return "invalid_input", 2, [
            {
                "id": "receipt_records_invalid_input",
                "detail": "retained receipt records a could-not-evaluate capture",
            }
        ]
    validate_environment(receipt["environment"])
    validate_runs(receipt["runs"])
    validate_comparison(receipt["comparison"])
    validate_positive_control(receipt["positive_control"])
    validate_sources(receipt["sources"])
    validate_mapping(receipt["mapping"])
    findings = []
    recompute_environment(receipt, findings)
    recompute_runs(receipt, findings)
    recompute_comparison(receipt, findings)
    recompute_positive_control(receipt["positive_control"], findings)
    recompute_sources(receipt["sources"], findings)
    recompute_mapping(receipt["mapping"], findings)
    if frozen and receipt["tool_sha256"] != FROZEN_TOOL_SHA256:
        collect_finding(
            findings, "tool_declaration_mismatch",
            "retained tool_sha256 {!r} is not the pinned historical "
            "declaration".format(receipt["tool_sha256"]))
    return verify_recorded_verdict(receipt, findings)


# ----------------------------------------------------------------- expected pin


def validate_expected(document, path):
    if type(document) is not dict:
        raise CouldNotEvaluate(
            "expected_invalid", path + " root is not an object")
    missing = sorted(key for key in EXPECTED_KEYS if key not in document)
    extra = sorted(key for key in document if key not in EXPECTED_KEYS)
    if missing or extra:
        raise CouldNotEvaluate(
            "expected_invalid",
            "{} keys mismatch (missing={}, extra={})".format(
                path, missing, extra))
    if document["schema"] != EXPECTED_SCHEMA:
        raise CouldNotEvaluate(
            "expected_invalid", path + " schema is not " + EXPECTED_SCHEMA)
    try:
        require_hex(document["receipt_sha256"], path + ".receipt_sha256", HEX64)
        require_string(document["id"], path + ".id")
        if FINDING_ID.fullmatch(document["id"]) is None:
            raise CouldNotEvaluate(
                "expected_invalid", path + ".id is not a stable finding id")
        require_int(document["exit"], path + ".exit", {0, 1, 2})
    except CouldNotEvaluate as exc:
        raise CouldNotEvaluate("expected_invalid", exc.detail)
    return document


def load_expected(path):
    raw = read_regular(path, "expected_missing", "expected_unreadable",
                       "expected file")
    document = parse_json_strict(raw, "expected_invalid", "expected file")
    return validate_expected(document, path)


# -------------------------------------------------------------------- verdict


def make_result(mode, status, finding_id, code, findings, receipt_path,
                receipt_sha, expected, digest_matches, expected_matches):
    return {
        "schema": RESULT_SCHEMA,
        "tool": VERSION,
        "tool_sha256": tool_sha256(),
        "mode": mode,
        "status": status,
        "id": finding_id,
        "exit": code,
        "findings": findings,
        "receipt": {
            "path": receipt_path,
            "sha256": receipt_sha,
            "expected_sha256": None if expected is None
            else expected["receipt_sha256"],
            "digest_matches": digest_matches,
        },
        "expected": None if expected is None else {
            "id": expected["id"],
            "exit": expected["exit"],
        },
        "verdict_matches_expected": expected_matches,
    }


def _one_line(value):
    """Fold CR/LF so retained text cannot forge a verdict line."""
    return str(value).replace("\r", "\\r").replace("\n", "\\n")


def emit(result, as_json):
    if as_json:
        sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
        return result["exit"]
    label = {"ok": "OK", "mismatch": "MISMATCH",
             "invalid_input": "INVALID"}[result["status"]]
    sys.stdout.write(
        "CONTEXT: {} (id={} receipt={} sha256={} exit={} findings={})\n".format(
            label, result["id"], _one_line(result["receipt"]["path"]),
            result["receipt"]["sha256"] or "<none>", result["exit"],
            len(result["findings"])))
    for finding in result["findings"]:
        sys.stdout.write(
            "FINDING {} {}\n".format(
                _one_line(finding["id"]), _one_line(finding["detail"])))
    return result["exit"]


def apply_expected(result, expected):
    """Compare the recomputed verdict with the pinned id/exit pair."""
    if result["expected"] is None:
        return result
    matches = (result["id"] == expected["id"]
               and result["exit"] == expected["exit"])
    result["verdict_matches_expected"] = matches
    if matches:
        return result
    detail = (
        "expected id={} exit={} but recomputed id={} exit={}".format(
            expected["id"], expected["exit"], result["id"], result["exit"]))
    if result["exit"] == 0:
        result["findings"].insert(
            0, {"id": "expected_verdict_mismatch", "detail": detail})
        result["id"] = "expected_verdict_mismatch"
        result["status"] = "mismatch"
        result["exit"] = 1
    else:
        collect_finding(result["findings"], "expected_verdict_mismatch",
                        detail)
    return result


def result_from_exception(exc, mode, receipt_path, receipt_sha, expected,
                          digest_matches):
    result = make_result(
        mode, "invalid_input", exc.finding_id, 2,
        [{"id": exc.finding_id, "detail": exc.detail}],
        receipt_path, receipt_sha, expected, digest_matches, None)
    return apply_expected(result, expected) if expected is not None else result


def run_check(options):
    frozen = options["receipt"] is None
    if frozen:
        receipt_path = FROZEN_RECEIPT_REL
        full_path = os.path.join(DEFAULT_LANE_ROOT, *FROZEN_RECEIPT_REL.split("/"))
        expected = {
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": FROZEN_RECEIPT_SHA256,
            "id": FROZEN_EXPECTED_ID,
            "exit": FROZEN_EXPECTED_EXIT,
        }
        mode = "frozen"
    else:
        receipt_path = options["receipt"]
        full_path = receipt_path
        expected = load_expected(options["expected"])
        mode = "explicit"

    raw = None
    try:
        raw = read_regular(full_path, "receipt_missing", "receipt_unreadable",
                           "receipt")
    except CouldNotEvaluate as exc:
        return result_from_exception(
            exc, mode, receipt_path, None, expected, None)
    actual_sha = sha256_bytes(raw)
    if actual_sha != expected["receipt_sha256"]:
        result = make_result(
            mode, "invalid_input", "snapshot_tampered", 2,
            [{
                "id": "snapshot_tampered",
                "detail": "receipt sha256 {} is not the pinned {}".format(
                    actual_sha, expected["receipt_sha256"]),
            }],
            receipt_path, actual_sha, expected, False, None)
        return apply_expected(result, expected)
    try:
        receipt = parse_json_strict(raw, "receipt_json_invalid", "receipt")
        status, code, findings = check_receipt(receipt, frozen=frozen)
    except CouldNotEvaluate as exc:
        return result_from_exception(
            exc, mode, receipt_path, actual_sha, expected, True)
    primary = findings[0]["id"] if findings else "context_consistent"
    result = make_result(
        mode, status, primary, code, findings, receipt_path, actual_sha,
        expected, True, None)
    return apply_expected(result, expected)


# ------------------------------------------------------------------- selftest

FIXTURE_PROBE_BYTES = b"#!/usr/bin/env python3\n# selftest fixture; never run\n"
FIXTURE_RUNNER_BYTES = b"#!/usr/bin/env bash\n# selftest fixture; never run\n"
FIXTURE_MANIFEST_BYTES = b'{"schema":"pin-manifest-v1","legs":[]}\n'
FIXTURE_EXPECTED_BYTES = b'{"inputs":{}}\n'
FIXTURE_TOOL_SHA = sha256_bytes(FIXTURE_PROBE_BYTES)
FIXTURE_LEGS = tuple(EXPECTED_SUFFIX)


def _fixture_commit(leg):
    return hashlib.sha256(("commit:" + leg).encode()).hexdigest()[:40]


def _fixture_digest(leg):
    return hashlib.sha256(("digest:" + leg).encode()).hexdigest()


def _fixture_probe_document(observed_at, tool_digest):
    return {
        "schema": PROBE_SCHEMA,
        "status": "ok",
        "observed_at": observed_at,
        "tool_sha256": tool_digest,
        "legs": [
            {
                "leg": leg,
                "content_status": "observed",
                "pinned": {"status": "verified"},
            }
            for leg in FIXTURE_LEGS
        ],
    }


def _fixture_canonical(document):
    trimmed = dict(document)
    trimmed.pop("observed_at")
    return json.dumps(trimmed, sort_keys=True, separators=(",", ":"))


def build_fixture_receipt():
    baseline_document = _fixture_probe_document(
        "2026-10-20T00:00:00Z", FIXTURE_TOOL_SHA)
    injected_document = _fixture_probe_document(
        "2026-10-20T00:00:01Z", FIXTURE_TOOL_SHA)
    baseline_text = json.dumps(
        baseline_document, sort_keys=True, separators=(",", ":"))
    injected_text = json.dumps(
        injected_document, sort_keys=True, separators=(",", ":"))
    comparable = sha256_bytes(_fixture_canonical(baseline_document).encode())
    lane = "/fixture/lane"
    fleet = "/fixture"
    probe_argv = [
        "/usr/bin/python3", PROBE_REL, "--manifest", MANIFEST_REL,
        "--root", fleet,
    ]
    control_argv = ["/usr/bin/git", "-C", lane, "rev-parse", "--git-dir"]
    rows = []
    for leg in FIXTURE_LEGS:
        suffix = EXPECTED_SUFFIX[leg]
        manifest = {
            "repo": "fixture-repo",
            "path": "scripts/" + leg + ".sh",
            "pinned_commit": _fixture_commit(leg),
            "expected_sha256": _fixture_digest(leg),
        }
        rows.append({
            "leg": leg,
            "manifest": manifest,
            "declared_variable_suffix": suffix,
            "runner_header": {
                "leg": leg,
                "repo": manifest["repo"],
                "path": manifest["path"],
            },
            "runner_call": {
                "leg": leg,
                "repo": manifest["repo"],
                "path": manifest["path"],
                "line": 100 + len(rows),
                "pin_constant": "PIN_" + suffix,
                "rev_constant": "REV_" + suffix,
                "table_constant": "TABLE_" + suffix,
            },
            "pin_value": manifest["expected_sha256"],
            "rev_value": manifest["pinned_commit"],
            "checks": {check: True for check in CHECK_NAMES},
            "match": True,
        })
    return {
        "schema": RECEIPT_SCHEMA,
        "tool": "context-capture.py r15 selftest fixture",
        "tool_sha256": "a" * 64,
        "observed_at": "2026-10-20T00:00:02Z",
        "lane_root": lane,
        "fleet_root": fleet,
        "invocation": {
            "argv": ["context-capture.py", "--selftest"],
            "cwd": lane,
        },
        "environment": {
            "baseline_policy": "ambient with every GIT_* key removed, plus LC_ALL=C",
            "injected_policy": "baseline plus exactly the keys in injected_env",
            "injected_env": dict(INJECTED_ENV),
            "env_delta_keys": sorted(INJECTED_ENV),
            "env_delta_matches_declared": True,
            "baseline_has_GIT_DIR": False,
            "ambient_git_keys_removed": [],
            "poison_path": POISON_PATH,
            "poison_path_exists": False,
            "ambient_env_dumped": False,
        },
        "sources": {
            "probe": {
                "path": PROBE_REL,
                "sha256": FIXTURE_TOOL_SHA,
                "declared_sha256": FIXTURE_TOOL_SHA,
                "matches_declared": True,
            },
            "runner": {
                "path": RUNNER_REL,
                "sha256": sha256_bytes(FIXTURE_RUNNER_BYTES),
                "manifest_declared_sha256": sha256_bytes(FIXTURE_RUNNER_BYTES),
                "matches_manifest_declaration": True,
            },
            "manifest": {
                "path": MANIFEST_REL,
                "sha256": sha256_bytes(FIXTURE_MANIFEST_BYTES),
            },
            "expected_r13": {
                "path": EXPECTED_R13_REL,
                "sha256": sha256_bytes(FIXTURE_EXPECTED_BYTES),
            },
        },
        "runs": {
            "argv": probe_argv,
            "argv_equal": True,
            "cwd": lane,
            "cwd_equal": True,
            "env_delta": {"baseline": [], "injected": sorted(INJECTED_ENV)},
            "baseline": {
                "argv": probe_argv,
                "cwd": lane,
                "exit": 0,
                "stdout": baseline_text,
                "stderr": "",
            },
            "injected": {
                "argv": probe_argv,
                "cwd": lane,
                "exit": 0,
                "stdout": injected_text,
                "stderr": "",
            },
        },
        "comparison": {
            "exclusions": ["observed_at"],
            "normalization": "top-level observed_at removed; canonical JSON compared",
            "observed_at": {
                "baseline": "2026-10-20T00:00:00Z",
                "injected": "2026-10-20T00:00:01Z",
            },
            "raw_stdout_equal": baseline_text == injected_text,
            "baseline_comparable_sha256": comparable,
            "injected_comparable_sha256": comparable,
            "payload_tool_sha256_matches_disk": True,
            "equal": True,
            "error": None,
        },
        "positive_control": {
            "argv": control_argv,
            "baseline": {
                "argv": control_argv,
                "cwd": lane,
                "exit": 0,
                "stdout": ".git\n",
                "stderr": "",
            },
            "injected": {
                "argv": control_argv,
                "cwd": lane,
                "exit": 128,
                "stdout": "",
                "stderr": "fatal: not a git repository: "
                          "'/nonexistent/tameshi-round14-poison'\n",
            },
            "baseline_ok": True,
            "injected_reflects_poison": True,
            "effective": True,
            "env_additions": dict(CONTROL_ENV_ADDITIONS),
            "env_delta": {"baseline": [], "injected": sorted(INJECTED_ENV)},
        },
        "mapping": {
            "schema": MAPPING_SCHEMA,
            "runner_path": RUNNER_REL,
            "parsed": {
                "header_rows": 6,
                "pin_constants": 6,
                "rev_constants": 6,
                "leg_calls": 6,
            },
            "call_scope": {
                "function": "run_regression",
                "line_start": 42,
                "call_count": 6,
            },
            "declared_variable_table": dict(EXPECTED_SUFFIX),
            "runner_leg_order": list(FIXTURE_LEGS),
            "manifest_leg_order": list(FIXTURE_LEGS),
            "leg_set_equal": True,
            "leg_order_equal": True,
            "legs": rows,
            "all_match": True,
            "reasons": [],
        },
        "result_reuse": "not_established",
        "result_reuse_reason": "selftest fixture: no execution or reuse claim",
        "not_compared": list(NOT_COMPARED_LIMITS),
        "status": "ok",
        "exit": 0,
        "reasons": [],
    }


SELFTEST_ENV = {
    "PATH": "/usr/bin:/bin",
    "LC_ALL": "C",
    "GIT_DIR": "/nonexistent/context-selftest-poison",
}


class SelftestHarness:
    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="context-capture-selftest-",
                                     dir=strict_scratch_root())
        self.passed = 0
        self.failed = []
        self.outputs = []
        self.counter = 0

    def case_dir(self, name):
        self.counter += 1
        path = os.path.join(self.root, "{:02d}-{}".format(self.counter, name))
        os.makedirs(path)
        return path

    def record(self, name, ok, detail):
        status = "OK" if ok else "FAIL"
        sys.stdout.write(
            "SELFTEST_CASE {} {} {}\n".format(name, status, detail))
        if ok:
            self.passed += 1
        else:
            self.failed.append(name)

    def run(self, argv, cwd):
        proc = subprocess.run(
            argv, cwd=cwd, env=SELFTEST_ENV, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
            text=True, check=False)
        self.outputs.append(proc.stdout)
        self.outputs.append(proc.stderr)
        return proc

    def check_case(self, name, receipt, expected_id, expected_exit,
                   receipt_bytes=None, write_receipt=True,
                   expected_override=None, write_expected=True,
                   expected_ids=None, expected_bytes=None,
                   expected_match=True):
        directory = self.case_dir(name)
        receipt_path = os.path.join(directory, "receipt.json")
        expected_path = os.path.join(directory, "expected.json")
        if receipt_bytes is None:
            receipt_bytes = (json.dumps(
                receipt, indent=2, sort_keys=True) + "\n").encode("utf-8")
        if write_receipt:
            with open(receipt_path, "wb") as handle:
                handle.write(receipt_bytes)
        if expected_bytes is not None:
            expected_document = None
        elif expected_override is None:
            expected_document = {
                "schema": EXPECTED_SCHEMA,
                "receipt_sha256": sha256_bytes(receipt_bytes),
                "id": expected_id,
                "exit": expected_exit,
            }
        else:
            expected_document = expected_override
        if write_expected:
            if expected_bytes is not None:
                with open(expected_path, "wb") as handle:
                    handle.write(expected_bytes)
            else:
                with open(expected_path, "w", encoding="utf-8") as handle:
                    json.dump(expected_document, handle, sort_keys=True)
                    handle.write("\n")
        proc = self.run(
            [sys.executable, "-I", SELF, "--check", "--receipt", receipt_path,
             "--expected", expected_path, "--json"],
            directory)
        observed_id = "<unparsed>"
        observed_exit = proc.returncode
        findings = None
        payload = None
        try:
            payload = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            payload = None
        if type(payload) is dict:
            observed_id = payload.get("id", "<missing>")
            observed_exit = payload.get("exit", proc.returncode)
            findings = payload.get("findings")
        ok = (
            proc.returncode == expected_exit
            and observed_exit == expected_exit
            and observed_id == expected_id
            and type(findings) is list
            and "Traceback" not in proc.stderr
        )
        if expected_exit == 0:
            ok = ok and findings == []
            ok = ok and type(payload) is dict
            ok = ok and payload.get("receipt", {}).get("sha256") == sha256_bytes(
                receipt_bytes)
        ids = [finding.get("id") for finding in (findings or [])
               if type(finding) is dict]
        if expected_match is not None:
            observed_match = (
                payload.get("verdict_matches_expected")
                if type(payload) is dict else None)
            ok = ok and observed_match is expected_match
            if expected_match:
                ok = ok and "expected_verdict_mismatch" not in ids
            else:
                ok = ok and "expected_verdict_mismatch" in ids
        else:
            ok = ok and "expected_verdict_mismatch" not in ids
        if expected_ids is not None:
            ok = ok and all(item in ids for item in expected_ids)
        self.record(
            name, ok,
            "expected={}/{} observed={}/{} exit={}".format(
                expected_id, expected_exit, observed_id, observed_exit,
                proc.returncode))
        if not ok:
            if proc.stderr.strip():
                sys.stdout.write(
                    "SELFTEST_STDERR {}: {}\n".format(
                        name, proc.stderr.strip()[:400]))
            if proc.stdout.strip():
                sys.stdout.write(
                    "SELFTEST_STDOUT {}: {}\n".format(
                        name, proc.stdout.strip()[:400]))

    def usage_case(self, name, argv):
        directory = self.case_dir(name)
        proc = self.run([sys.executable, "-I", SELF] + argv, directory)
        ok = (
            proc.returncode == 64
            and "id=usage_error" in proc.stderr
            and "Traceback" not in proc.stderr
        )
        self.record(
            name, ok,
            "expected=usage_error/64 observed_exit={}".format(proc.returncode))
        if not ok and proc.stderr.strip():
            sys.stdout.write(
                "SELFTEST_STDERR {}: {}\n".format(
                    name, proc.stderr.strip()[:400]))

    def finish(self):
        lane_leak = any(
            DEFAULT_LANE_ROOT in text for text in self.outputs)
        self.record(
            "hermetic-no-lane-path", not lane_leak,
            "default lane root absent from subprocess output"
            if not lane_leak else "subprocess output names the live lane root")
        entries = sorted(os.listdir(self.root))
        unexpected = [
            entry for entry in entries
            if not re.fullmatch(r"\d{2}-[a-z0-9-]+", entry)
        ]
        self.record(
            "hermetic-temp-only", not unexpected,
            "no unexpected temp-root entries" if not unexpected
            else "unexpected entries: {}".format(unexpected))
        shutil.rmtree(self.root, ignore_errors=True)
        total = self.passed + len(self.failed)
        if self.failed:
            sys.stdout.write(
                "SELFTEST: FAIL ({}/{} failed: {})\n".format(
                    len(self.failed), total, ", ".join(self.failed)))
            return 1
        sys.stdout.write("SELFTEST: PASS ({}/{})\n".format(self.passed, total))
        return 0


def run_selftest_cases(harness):
    base = build_fixture_receipt()

    def mutate(change):
        document = copy.deepcopy(base)
        change(document)
        return document

    clean = mutate(lambda document: None)
    clean_bytes = (json.dumps(
        clean, indent=2, sort_keys=True) + "\n").encode("utf-8")
    clean_digest = sha256_bytes(clean_bytes)
    harness.check_case("clean", clean, "context_consistent", 0,
                       receipt_bytes=clean_bytes)

    missing_env = mutate(
        lambda document: document["environment"].pop("injected_env"))
    harness.check_case(
        "missing-injected-env", missing_env, "missing_injected_environment", 1,
        expected_ids=["missing_injected_environment",
                      "receipt_verdict_mismatch"])

    harness.check_case(
        "tampered-before-semantic", missing_env, "snapshot_tampered", 2,
        expected_override={
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": clean_digest,
            "id": "context_consistent",
            "exit": 0,
        },
        expected_match=False)

    null_env = mutate(
        lambda document: document["environment"].update({"injected_env": None}))
    harness.check_case(
        "null-injected-env", null_env, "missing_injected_environment", 1)

    def comparison_raw_mismatch(document):
        injected = json.loads(document["runs"]["injected"]["stdout"])
        injected["status"] = "drift"
        document["runs"]["injected"]["stdout"] = json.dumps(
            injected, sort_keys=True, separators=(",", ":"))
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: raw observation differs"]
    harness.check_case(
        "comparison-raw-mismatch", mutate(comparison_raw_mismatch),
        "comparison_mismatch", 1)

    def comparison_observed_at_lie(document):
        document["comparison"]["observed_at"]["baseline"] = (
            "2020-01-01T00:00:00Z")
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: recorded observed_at differs"]
    harness.check_case(
        "comparison-observed-at-lie", mutate(comparison_observed_at_lie),
        "comparison_mismatch", 1)

    def payload_digest_lie(document):
        replacement = "0" * 64
        document["sources"]["probe"]["sha256"] = replacement
        document["sources"]["probe"]["declared_sha256"] = replacement
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: probe declaration differs"]
    harness.check_case(
        "payload-digest-lie", mutate(payload_digest_lie),
        "comparison_tool_digest_mismatch", 1)

    def injected_run_failed(document):
        document["runs"]["injected"]["exit"] = 128
        document["runs"]["injected"]["stdout"] = ""
        comparison = document["comparison"]
        comparison["observed_at"]["injected"] = None
        comparison["baseline_comparable_sha256"] = None
        comparison["injected_comparable_sha256"] = None
        comparison["payload_tool_sha256_matches_disk"] = None
        comparison["equal"] = False
        comparison["error"] = (
            "injected probe run produced no JSON document (exit=128)")
        comparison["raw_stdout_equal"] = False
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: injected run failed"]
    harness.check_case(
        "injected-run-failed", mutate(injected_run_failed),
        "comparison_mismatch", 1)

    def injected_deep_malformed(document):
        document["runs"]["injected"]["stdout"] = "[" * 6000 + "]" * 6000
        comparison = document["comparison"]
        comparison["observed_at"]["injected"] = None
        comparison["baseline_comparable_sha256"] = None
        comparison["injected_comparable_sha256"] = None
        comparison["payload_tool_sha256_matches_disk"] = None
        comparison["equal"] = False
        comparison["error"] = (
            "injected probe run produced no JSON document (exit=0)")
        comparison["raw_stdout_equal"] = False
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: injected document is unparsable"]
    harness.check_case(
        "injected-deep-malformed", mutate(injected_deep_malformed),
        "comparison_mismatch", 1)

    def control_ineffective(document):
        document["positive_control"]["injected"]["exit"] = 0
        document["positive_control"]["injected"]["stderr"] = ""
        document["positive_control"]["injected_reflects_poison"] = False
        document["positive_control"]["effective"] = False
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: control ineffective"]
    harness.check_case(
        "control-ineffective", mutate(control_ineffective),
        "positive_control_ineffective", 1)

    def control_flag_lie(document):
        document["positive_control"]["injected"]["exit"] = 0
        document["positive_control"]["injected"]["stderr"] = ""
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: control flags lie"]
    harness.check_case(
        "control-flag-lie", mutate(control_flag_lie),
        "positive_control_ineffective", 1)

    def control_exit_zero_poison(document):
        document["positive_control"]["injected"]["exit"] = 0
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = [
            "fixture: exit zero under a truthful poison marker"]
    harness.check_case(
        "control-exit-zero-poison", mutate(control_exit_zero_poison),
        "positive_control_ineffective", 1)

    def mapping_check_lie(document):
        document["mapping"]["legs"][0]["pin_value"] = "0" * 64
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: mapping check lies"]
    harness.check_case(
        "mapping-check-lie", mutate(mapping_check_lie), "mapping_mismatch", 1)

    mapping_failed = mutate(mapping_check_lie)
    mapping_failed_bytes = (json.dumps(
        mapping_failed, indent=2, sort_keys=True) + "\n").encode("utf-8")
    harness.check_case(
        "mapping-failed-wrong-pin", mapping_failed, "mapping_mismatch", 1,
        receipt_bytes=mapping_failed_bytes,
        expected_override={
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": sha256_bytes(mapping_failed_bytes),
            "id": "comparison_mismatch",
            "exit": 1,
        },
        expected_match=False,
        expected_ids=["mapping_mismatch", "expected_verdict_mismatch"])

    def mapping_suffix_swap(document):
        js = document["mapping"]["legs"][0]
        bash = document["mapping"]["legs"][1]
        js["declared_variable_suffix"] = bash["declared_variable_suffix"]
        js["pin_value"] = bash["pin_value"]
        js["rev_value"] = bash["rev_value"]
        js["runner_call"]["pin_constant"] = bash["runner_call"]["pin_constant"]
        js["runner_call"]["rev_constant"] = bash["runner_call"]["rev_constant"]
        js["runner_call"]["table_constant"] = (
            bash["runner_call"]["table_constant"])
    harness.check_case(
        "mapping-suffix-swap", mutate(mapping_suffix_swap),
        "mapping_mismatch", 1)

    def mapping_constant_swap(document):
        leg = document["mapping"]["legs"][0]
        other = document["mapping"]["legs"][1]
        leg["runner_call"]["rev_constant"] = (
            "REV_" + EXPECTED_SUFFIX[other["leg"]])
        leg["checks"]["rev_name_and_value_match_manifest"] = False
        leg["checks"]["constant_names_match_leg"] = False
        leg["match"] = all(leg["checks"].values())
        document["mapping"]["all_match"] = all(
            row["match"] for row in document["mapping"]["legs"])
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: equal-valued variable swap"]
    harness.check_case(
        "mapping-constant-swap", mutate(mapping_constant_swap),
        "mapping_mismatch", 1)

    def mapping_order_lie(document):
        document["mapping"]["runner_leg_order"] = list(
            reversed(document["mapping"]["runner_leg_order"]))
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: runner order lies"]
    harness.check_case(
        "mapping-order-lie", mutate(mapping_order_lie), "mapping_mismatch", 1)

    def probe_source_lie(document):
        document["sources"]["probe"]["declared_sha256"] = "1" * 64
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: probe declaration lies"]
    harness.check_case(
        "probe-source-lie", mutate(probe_source_lie),
        "probe_source_digest_mismatch", 1)

    def runner_source_lie(document):
        document["sources"]["runner"]["manifest_declared_sha256"] = "2" * 64
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: runner declaration lies"]
    harness.check_case(
        "runner-source-lie", mutate(runner_source_lie),
        "runner_source_digest_mismatch", 1)

    def probe_flag_false_equal(document):
        document["sources"]["probe"]["matches_declared"] = False
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: probe flag false with equal digest"]
    harness.check_case(
        "probe-flag-false-equal", mutate(probe_flag_false_equal),
        "probe_source_digest_mismatch", 1)

    def runner_flag_false_equal(document):
        document["sources"]["runner"]["matches_manifest_declaration"] = False
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: runner flag false with equal digest"]
    harness.check_case(
        "runner-flag-false-equal", mutate(runner_flag_false_equal),
        "runner_source_digest_mismatch", 1)

    truthy_matches = mutate(
        lambda document: document["sources"]["probe"].update(
            {"matches_declared": 1}))
    harness.check_case(
        "truthy-matches-declared", truthy_matches,
        "receipt_structure_invalid", 2)

    truthy_all_match = mutate(
        lambda document: document["mapping"].update({"all_match": "false"}))
    harness.check_case(
        "truthy-all-match", truthy_all_match,
        "receipt_structure_invalid", 2)

    bool_exit = mutate(lambda document: document.update({"exit": True}))
    harness.check_case("bool-exit", bool_exit, "receipt_structure_invalid", 2)

    widened_exclusions = mutate(
        lambda document: document["comparison"].update(
            {"exclusions": ["observed_at", "tool_sha256"]}))
    harness.check_case(
        "exclusions-widened", widened_exclusions,
        "receipt_structure_invalid", 2)

    comparison_container = mutate(
        lambda document: document.update({"comparison": []}))
    harness.check_case(
        "comparison-container", comparison_container,
        "receipt_structure_invalid", 2)

    harness.check_case(
        "duplicate-key", None, "receipt_json_invalid", 2,
        receipt_bytes=(
            '{"schema": "tameshi-round14-context-receipt-v1", '
            '"schema": "tameshi-round14-context-receipt-v1"}').encode())
    harness.check_case(
        "malformed-json", None, "receipt_json_invalid", 2,
        receipt_bytes=b"{")
    harness.check_case(
        "non-object-json", None, "receipt_json_invalid", 2,
        receipt_bytes=b"[]")
    harness.check_case(
        "invalid-utf8", None, "receipt_json_invalid", 2,
        receipt_bytes=b"\xff\xfe{")

    harness.check_case(
        "receipt-missing", None, "receipt_missing", 2,
        receipt_bytes=b"absent\n", write_receipt=False)

    harness.check_case(
        "snapshot-tampered", clean, "snapshot_tampered", 2,
        expected_override={
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": "0" * 64,
            "id": "context_consistent",
            "exit": 0,
        },
        expected_match=False)

    harness.check_case(
        "expected-missing", clean, "expected_missing", 2,
        write_expected=False, expected_match=None)

    harness.check_case(
        "expected-invalid", clean, "expected_invalid", 2,
        expected_override={
            "schema": "not-the-expected-schema",
            "receipt_sha256": "0" * 64,
            "id": "context_consistent",
            "exit": 0,
        },
        expected_match=None)

    harness.check_case(
        "expected-verdict-mismatch", clean, "expected_verdict_mismatch", 1,
        expected_override={
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": clean_digest,
            "id": "comparison_mismatch",
            "exit": 1,
        },
        expected_match=False)

    def stored_verdict_lie(document):
        document["status"] = "mismatch"
        document["exit"] = 1
        document["reasons"] = ["fixture: stored verdict does not match raw fields"]
    harness.check_case(
        "stored-verdict-lie", mutate(stored_verdict_lie),
        "receipt_verdict_mismatch", 1)

    invalid = {
        "schema": RECEIPT_SCHEMA,
        "tool": "context-capture.py r15 selftest fixture",
        "tool_sha256": "a" * 64,
        "observed_at": "2026-10-20T00:00:03Z",
        "lane_root": "/fixture/lane",
        "fleet_root": "/fixture",
        "invocation": {"argv": ["fixture"], "cwd": "/fixture/lane"},
        "environment": {
            "baseline_policy": "fixture",
            "injected_policy": "fixture",
            "injected_env": None,
            "env_delta_keys": None,
            "env_delta_matches_declared": None,
            "baseline_has_GIT_DIR": None,
            "ambient_git_keys_removed": [],
            "poison_path": None,
            "poison_path_exists": None,
            "ambient_env_dumped": False,
        },
        "sources": {},
        "runs": {},
        "comparison": {},
        "positive_control": {},
        "mapping": {},
        "result_reuse": "not_established",
        "result_reuse_reason": "fixture: retained invalid-input record",
        "not_compared": list(NOT_COMPARED_LIMITS),
        "status": "invalid_input",
        "exit": 2,
        "error": {"kind": "missing_input", "message": "fixture"},
        "reasons": ["missing_input: fixture"],
    }
    harness.check_case(
        "retained-invalid-input", invalid, "receipt_records_invalid_input", 2)

    harness.check_case(
        "expected-digest-invalid", clean, "expected_invalid", 2,
        expected_override={
            "schema": EXPECTED_SCHEMA,
            "receipt_sha256": "not-a-digest",
            "id": "context_consistent",
            "exit": 0,
        },
        expected_match=None)

    duplicate_expected = (
        '{"schema": "tameshi-context-expected-v1", '
        '"receipt_sha256": "' + clean_digest + '", '
        '"receipt_sha256": "' + clean_digest + '", '
        '"id": "context_consistent", "exit": 0}').encode("utf-8")
    harness.check_case(
        "expected-duplicate-key", clean, "expected_invalid", 2,
        receipt_bytes=clean_bytes, expected_bytes=duplicate_expected,
        expected_match=None)

    baseline_unusable = mutate(
        lambda document: document["runs"]["baseline"].update({"stdout": "{}"}))
    harness.check_case(
        "baseline-unusable", baseline_unusable, "baseline_unusable", 2)

    harness.usage_case("usage-no-args", [])
    harness.usage_case(
        "usage-receipt-without-expected", ["--check", "--receipt", "receipt.json"])
    harness.usage_case(
        "usage-expected-without-receipt", ["--check", "--expected", "expected.json"])
    harness.usage_case(
        "usage-receipt-final-missing",
        ["--check", "--expected", "expected.json", "--receipt"])
    harness.usage_case(
        "usage-receipt-flag-as-value",
        ["--check", "--expected", "expected.json", "--receipt", "--json"])
    harness.usage_case("usage-unknown-flag", ["--check", "--bogus"])
    harness.usage_case("usage-selftest-extra", ["--selftest", "--json"])


def run_selftest():
    harness = None
    try:
        harness = SelftestHarness()
        run_selftest_cases(harness)
        return harness.finish()
    except ScratchRootUnusable as exc:
        # One stderr line with the frozen grammar: the class is operator-visible,
        # the exception type never is, and stdout keeps no setup error. A stream
        # that refuses the line (/dev/full, closed pipe) must not change the class
        # from could-not-evaluate to a verdict (round 55, wave-2 F1).
        try:
            sys.stderr.write("context-capture.py: could-not-evaluate: {}\n".format(exc))
            sys.stderr.flush()
        except (OSError, ValueError):
            pass
        return 2
    except Exception as exc:  # setup failure is loud but never a traceback
        sys.stdout.write(
            "SELFTEST: FAIL (setup error: {}: {})\n".format(
                type(exc).__name__, exc))
        return 2
    finally:
        if harness is not None:
            shutil.rmtree(harness.root, ignore_errors=True)


# ------------------------------------------------------------------------ CLI


def parse_argv(argv):
    if not argv:
        raise UsageError("a mode is required")
    if argv in (["-h"], ["--help"]):
        return {"help": True}
    mode = None
    receipt = None
    expected = None
    as_json = False
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--check":
            if mode is not None:
                raise UsageError("mode given twice")
            mode = "check"
            index += 1
        elif argument == "--selftest":
            if mode is not None:
                raise UsageError("mode given twice")
            mode = "selftest"
            index += 1
        elif argument == "--json":
            if as_json:
                raise UsageError("--json given twice")
            as_json = True
            index += 1
        elif argument in ("--receipt", "--expected"):
            if index + 1 >= len(argv):
                raise UsageError(argument + " needs a value")
            value = argv[index + 1]
            if not value:
                raise UsageError(argument + " has an empty value")
            if value in KNOWN_ARGUMENTS:
                raise UsageError(
                    argument + " cannot take a recognized flag as its value: "
                    + value)
            index += 2
            if argument == "--receipt":
                if receipt is not None:
                    raise UsageError("--receipt given twice")
                receipt = value
            else:
                if expected is not None:
                    raise UsageError("--expected given twice")
                expected = value
        else:
            raise UsageError("unknown argument: " + argument)
    if mode is None:
        raise UsageError("a mode is required")
    if mode == "selftest":
        if receipt is not None or expected is not None or as_json:
            raise UsageError("--selftest takes no other arguments")
        return {"selftest": True}
    if (receipt is None) != (expected is None):
        raise UsageError("--receipt and --expected must be given together")
    return {
        "selftest": False,
        "json": as_json,
        "receipt": receipt,
        "expected": expected,
    }


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    try:
        options = parse_argv(argv)
    except UsageError as exc:
        sys.stderr.write(USAGE)
        sys.stderr.write(
            "context-capture.py: {}\nCONTEXT: USAGE_ERROR (id=usage_error "
            "exit=64)\n".format(exc))
        return 64
    if options.get("help"):
        sys.stdout.write(USAGE)
        return 0
    if options.get("selftest"):
        return run_selftest()
    try:
        return emit(run_check(options), options["json"])
    except CouldNotEvaluate as exc:
        result = result_from_exception(
            exc, "frozen" if options["receipt"] is None else "explicit",
            options["receipt"] or FROZEN_RECEIPT_REL, None, None, None)
        return emit(result, options["json"])
    except Exception as exc:  # fail closed, never traceback on retained data
        failure = CouldNotEvaluate(
            "internal_error", "{}: {}".format(type(exc).__name__, exc))
        result = result_from_exception(
            failure, "frozen" if options["receipt"] is None else "explicit",
            options["receipt"] or FROZEN_RECEIPT_REL, None, None, None)
        return emit(result, options["json"])


if __name__ == "__main__":
    raise SystemExit(main())
