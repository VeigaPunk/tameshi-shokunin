#!/usr/bin/env python3
"""verify.py — round-15 integrated L1 verification runner (tameshi-shokunin).

One command:

    python3 .ufo/evidence/round-15/verify.py --rev REV

REV must name the committed revision carrying the final maintained context
gate (tools/context-capture.py, pinned source sha256 c4a1d165...601726).
BASELINE a9cf4da...7df0 carries the archived round-14 probe; PREFIX bca5deb
carries the pre-fix maintained gate (sha256 0ed784e0...c61edc) used only for
same-path old-vs-new oracle contrast. All gate inputs are committed blobs or
byte-pinned frozen copies under this round's own evidence directory; no
historical round-12..14 byte is read from the worktree as authority, none is
written, and no sibling gate or live historical capture is invoked.

Sequence (every subprocess stdout/stderr/exit retained in verification.json):

  1.  Resolve REV, BASELINE and PREFIX; assert tools/context-capture.py at REV
      and at PREFIX match their pinned source sha256 values, and the two
      round-14 receipts match their pinned content digests.
  2.  Historical integrity: archived script, receipts, runner, SHONEN.md and
      the outside closure note compare byte-equal baseline-vs-REV; runner and
      frozen round-12 summary match their published digests; the
      round-12/13/14 evidence trees show no diff.
  3.  Persist expected.json BEFORE any gate run: every input/source sha256
      and every expected literal exit/finding pair. Exclusive-create only.
  4.  Copy the two immutable round-14 receipts into own round-15 frozen
      directories (frozen/context-clean/, frozen/context-missing-env/) with a
      tameshi-context-expected-v1 pin file each; a third frozen fixture
      (frozen/mapping-suffix/) holds the mapping-suffix-swap mutation whose
      stored verdict stays clean while raw leg-0 BASH constants contradict
      the declared mapping. Existing frozen files are digest-verified, never
      silently overwritten.
  5.  Same-path --selftest contrast: baseline historical probe bytes and REV
      gate bytes each written to the SAME temp script path
      <scratch>/lane/tools/candidate.py (the lane/tools layout keeps the
      tool's own DEFAULT_LANE_ROOT distinct from its selftest mkdtemp
      fixtures, so the hermetic-no-lane-path check reads truthfully) and
      invoked with the SAME argv; only file bytes differ. Expected: old
      exits 64 (unsupported argument), new exits 0 with SELFTEST: PASS (n/n).
  6.  Same-path usage-class proof: PREFIX gate bytes then REV gate bytes at
      the SAME temp path with the SAME argv
      '--check --expected <valid pin file> --receipt --json'. The pre-fix
      parser consumes --json as the --receipt value and reports
      receipt_missing/exit 2; the fixed parser rejects a recognized flag as
      an option value and reports usage_error/exit 64. No file named --json
      may be created.
  7.  Frozen gate runs: the actual registered tools/context-capture.py is
      invoked once in built-in frozen mode ('--check --json', no receipt
      arguments) so the gate resolves its own lane root through the
      registered path; then explicit --receipt/--expected runs against REV
      bytes at the same temp path: frozen clean (exit0, context_consistent),
      frozen missing-env (exit1, missing_injected_environment), tampered
      scratch copy (exit2, snapshot_tampered), usage error (exit64,
      usage_error). Temp-script invocations are copied-source runs, never
      claimed as the registered path.
  8.  Failure-backed mapping oracle: the same mutated receipt at the same
      temp path under PREFIX then REV bytes. The literal oracle is
      exit 1 with primary id mapping_mismatch. PREFIX fails the oracle
      (its false-clean recompute is flipped only by the expected pin into
      expected_verdict_mismatch/1); REV satisfies it (mapping_mismatch/1).
  9.  measure.py --rev BASELINE -> before.json, --rev REV -> after.json.
 10.  Source census end receipt -> sources-after.json.
 11.  verification.json (first attempt) or verification-N.json (later
      attempts; attempt-N/ carries that run's expected/before/after/
      sources-after receipts while the shared frozen/ inputs stay immutable)
      collects every command and check; exit 0 only when all observed
      outcomes equal their pinned expectations. Unexpected outcomes are
      recorded and produce a nonzero exit after receipts write; scratch is
      removed in a finally.

This runner never executes retained receipt argv, never opens the historical
probe's main/evaluate paths, and never claims environment or dependency
independence beyond these literal observations.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / ".ufo" / "evidence" / "round-15"

BASELINE = "a9cf4da78f2514c7bedd91a850a88590009d7df0"
PREFIX_REV = "bca5deb"  # pre-fix maintained gate commit; resolved at run time

TOOL_REL = "tools/context-capture.py"
HISTORICAL_SCRIPT_REL = ".ufo/evidence/round-14/capture-context.py"
CLEAN_RECEIPT_REL = ".ufo/evidence/round-14/context-receipt.json"
MISSING_ENV_RECEIPT_REL = ".ufo/evidence/round-14/context-missing-env.json"
RUNNER_REL = "tools/mutate-and-run.sh"
FROZEN_SUMMARY_REL = ".ufo/evidence/round-12/BashWitness/summary.json"
SHONEN_REL = "SHONEN.md"
CLOSURE_NOTE_REL = "corpus/lessons/round-14-verifier-spotcheck.md"
MEASURE_REL = ".ufo/evidence/round-15/measure.py"
VERIFY_REL = ".ufo/evidence/round-15/verify.py"
CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
EXPECTED_SCHEMA = "tameshi-context-expected-v1"
RESULT_SCHEMA = "tameshi-context-gate-result-v1"

# Final maintained gate source identity (round-15 w2, committed by L1).
PIN_TOOL_SHA256 = (
    "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726")
# Pre-fix gate source at PREFIX_REV (old-half oracle bytes).
PIN_PREFIX_TOOL_SHA256 = (
    "0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc")
PIN_CLEAN_RECEIPT_SHA256 = (
    "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a")
PIN_MISSING_ENV_RECEIPT_SHA256 = (
    "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208")
# Published in corpus/lessons/round-14-verifier-spotcheck.md.
PIN_RUNNER_SHA256 = (
    "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5")
PIN_SUMMARY_SHA256 = (
    "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9")

# Files that must be byte-identical between BASELINE and REV.
PRESERVE_PATHS = (
    HISTORICAL_SCRIPT_REL,
    CLEAN_RECEIPT_REL,
    MISSING_ENV_RECEIPT_REL,
    RUNNER_REL,
    SHONEN_REL,
    CLOSURE_NOTE_REL,
)

CHECKS = []
SCRATCH = None
COMMAND_TIMEOUT = 300
ID_TOKEN_RE = re.compile(r"id=([a-z_]+)")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def git(*argv):
    # GIT_* keys are stripped so an ambient injection cannot redirect the
    # lane's own git reads (round-14 lesson: GIT_DIR poisoning is real).
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(
        ["git", "-C", str(ROOT), *argv], stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
        timeout=COMMAND_TIMEOUT)


def git_blob(rev, path):
    proc = git("show", "{}:{}".format(rev, path))
    if proc.returncode != 0:
        return None
    return proc.stdout


def resolve_rev(rev):
    proc = git("rev-parse", "--verify", "--quiet", rev + "^{commit}")
    text = proc.stdout.decode("ascii", "replace").strip()
    if proc.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", text):
        return None
    return text


def record_check(name, passed, detail, **extra):
    entry = {"name": name, "passed": bool(passed), "detail": detail}
    entry.update(extra)
    CHECKS.append(entry)
    print("{}: {} {}".format(
        name, "PASS" if passed else "FAIL", detail), flush=True)
    return passed


def run_command(name, argv, cwd, expected_exit, env=None,
                expected_id=None, stdout_token=None, stderr_token=None,
                stdout_is_result_json=False,
                expected_verdict_match=None, forbid_traceback=True):
    """Run one command; retain full stdout/stderr/exit in CHECKS.

    expected_id matches the JSON result id when stdout_is_result_json, else
    the 'id=<token>' marker in stdout/stderr text. expected_verdict_match
    asserts the result's verdict_matches_expected flag when not None.
    """
    argv = [str(a) for a in argv]
    proc = subprocess.run(
        argv, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=COMMAND_TIMEOUT)
    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")
    result_doc = None
    observed_id = None
    observed_match = None
    if stdout_is_result_json:
        try:
            result_doc = json.loads(stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result_doc = None
        if type(result_doc) is dict:
            observed_id = result_doc.get("id")
            observed_match = result_doc.get("verdict_matches_expected")
    if observed_id is None:
        token = ID_TOKEN_RE.search(stdout) or ID_TOKEN_RE.search(stderr)
        if token:
            observed_id = token.group(1)
    ok = proc.returncode == expected_exit
    if expected_id is not None:
        ok = ok and observed_id == expected_id
        if stdout_is_result_json:
            ok = ok and type(result_doc) is dict
            ok = ok and result_doc.get("exit") == expected_exit
            ok = ok and result_doc.get("schema") == RESULT_SCHEMA
    if expected_verdict_match is not None:
        ok = ok and observed_match == expected_verdict_match
    if stdout_token is not None:
        ok = ok and stdout_token in stdout
    if stderr_token is not None:
        ok = ok and stderr_token in stderr
    if forbid_traceback:
        ok = ok and "Traceback" not in stderr
    entry = {
        "name": name,
        "kind": "command",
        "argv": argv,
        "cwd": str(cwd),
        "expected_exit": expected_exit,
        "observed_exit": proc.returncode,
        "expected_id": expected_id,
        "observed_id": observed_id,
        "expected_verdict_match": expected_verdict_match,
        "observed_verdict_match": observed_match,
        "stdout": stdout,
        "stderr": stderr,
        "passed": bool(ok),
        "detail": "expected exit={} id={} observed exit={} id={}".format(
            expected_exit, expected_id, proc.returncode, observed_id),
    }
    CHECKS.append(entry)
    print("{}: {} exit={} (expected {})".format(
        name, "PASS" if ok else "FAIL", proc.returncode, expected_exit),
        flush=True)
    return proc, result_doc, ok


def write_exclusive(path, text):
    """Create-only write; a pre-existing receipt is never overwritten."""
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(text)
    except FileExistsError:
        raise SystemExit(
            "verify.py: refusing to overwrite existing receipt {}".format(
                path))


def write_json_exclusive(path, document):
    write_exclusive(path, json.dumps(document, indent=2, sort_keys=True) + "\n")


def write_frozen_input(path, data, expected_sha256):
    """Idempotent immutable input: create once, else verify identical digest."""
    if path.exists():
        existing = path.read_bytes()
        if sha256_bytes(existing) != expected_sha256:
            raise SystemExit(
                "verify.py: frozen input {} digest {} is not the pinned "
                "{}".format(path, sha256_bytes(existing), expected_sha256))
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)
    return True


def tool_env():
    """Child environment: ambient minus every GIT_* key, LC_ALL pinned."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C"
    return env


def expected_document(expected_id, expected_exit, receipt_sha256):
    return {
        "schema": EXPECTED_SCHEMA,
        "receipt_sha256": receipt_sha256,
        "id": expected_id,
        "exit": expected_exit,
    }


def build_mapping_suffix_fixture(clean_data):
    """Clone the clean receipt and swap mapping leg0 suffix/constants to BASH.

    Raw mapping fields are edited; stored checks/match/all_match/status stay
    clean, so a stored-verdict-trusting recompute reports context_consistent
    while a raw re-derivation reports mapping_mismatch.
    """
    document = json.loads(clean_data.decode("utf-8"))
    leg = document["mapping"]["legs"][0]
    leg["declared_variable_suffix"] = "BASH"
    leg["runner_call"]["pin_constant"] = "PIN_BASH"
    leg["runner_call"]["rev_constant"] = "REV_BASH"
    leg["runner_call"]["table_constant"] = "TABLE_BASH"
    return (json.dumps(document, indent=2, sort_keys=True)
            + "\n").encode("utf-8")


def main():
    global SCRATCH
    parser = argparse.ArgumentParser(
        description="Round-15 integrated L1 verification runner.")
    parser.add_argument(
        "--rev", required=True,
        help="committed revision carrying the final tools/context-capture.py")
    args = parser.parse_args()

    # Never overwrite a prior run's receipts: the failed first artifacts stay
    # inspectable at the root/attempt-1 level; later attempts land in
    # attempt-N/ with the verdict receipt named verification-N.json.
    destination = EVIDENCE / "verification.json"
    serial = 1
    while destination.exists():
        serial += 1
        destination = EVIDENCE / "verification-{}.json".format(serial)
    artifact_dir = (EVIDENCE if serial == 1
                    else EVIDENCE / "attempt-{}".format(serial))
    try:
        try:
            run_verification(args.rev, artifact_dir)
        except SystemExit as exc:  # write refusals still retain a receipt
            record_check(
                "runner-write-refusal", False,
                "SystemExit: {}".format(exc))
        except Exception as exc:  # retain receipts even on unexpected failure
            record_check(
                "runner-internal-error", False,
                "{}: {}".format(type(exc).__name__, exc))
        failures = [entry["name"] for entry in CHECKS if not entry["passed"]]
        payload = {
            "schema": "tameshi-round15-verification-v1",
            "runner": VERIFY_REL,
            "requested_rev": args.rev,
            "attempt": serial,
            "artifact_dir": str(artifact_dir.relative_to(ROOT)),
            "receipt_file": destination.name,
            "baseline_revision": BASELINE,
            "prefix_revision": PREFIX_REV,
            "checks": CHECKS,
            "failed_checks": failures,
            "passed": not failures,
            "scope": ("retained-receipt gate replay on committed bytes; no "
                      "live historical capture, no receipt argv execution, "
                      "no sibling gate"),
        }
        write_json_exclusive(destination, payload)
        return 0 if not failures else 1
    finally:
        if SCRATCH is not None:
            shutil.rmtree(str(SCRATCH), ignore_errors=True)


def run_verification(rev, artifact_dir):
    global SCRATCH
    env = tool_env()

    # ------------------------------------------------------------ 1. resolve
    revision = resolve_rev(rev)
    record_check(
        "rev-resolves", revision is not None,
        "rev {!r} resolved to {}".format(rev, revision or "<none>"))
    if revision is None:
        return
    baseline = resolve_rev(BASELINE)
    record_check(
        "baseline-resolves", baseline == BASELINE,
        "baseline {}".format(baseline or "<unresolved>"))
    prefix = resolve_rev(PREFIX_REV)
    record_check(
        "prefix-resolves", prefix is not None,
        "prefix {!r} resolved to {}".format(
            PREFIX_REV, prefix or "<none>"))

    # ------------------------------------------------- 2. source/content pins
    tool_bytes = git_blob(revision, TOOL_REL)
    tool_sha = sha256_bytes(tool_bytes) if tool_bytes is not None else None
    record_check(
        "tool-source-pin", tool_sha == PIN_TOOL_SHA256,
        "{}@{} sha256={} pinned={}".format(
            TOOL_REL, revision, tool_sha, PIN_TOOL_SHA256),
        path=TOOL_REL, observed_sha256=tool_sha,
        expected_sha256=PIN_TOOL_SHA256)
    prefix_bytes = (git_blob(prefix, TOOL_REL) if prefix else None)
    prefix_sha = (sha256_bytes(prefix_bytes)
                  if prefix_bytes is not None else None)
    record_check(
        "prefix-source-pin", prefix_sha == PIN_PREFIX_TOOL_SHA256,
        "{}@{} sha256={} pinned={}".format(
            TOOL_REL, prefix or PREFIX_REV, prefix_sha,
            PIN_PREFIX_TOOL_SHA256),
        path=TOOL_REL, observed_sha256=prefix_sha,
        expected_sha256=PIN_PREFIX_TOOL_SHA256)

    # Keep every later phase reachable: on a missing/mismatched REV blob the
    # pin check above already records a failure, and commands run against an
    # explicit placeholder so their expected-mismatch is retained rather than
    # skipping independent evidence.
    tool_run_bytes = (tool_bytes if tool_bytes is not None
                      else b"# unavailable tool blob at REV\n")
    prefix_run_bytes = (prefix_bytes if prefix_bytes is not None
                        else b"# unavailable tool blob at PREFIX\n")

    historical_bytes = git_blob(revision, HISTORICAL_SCRIPT_REL)
    historical_sha = (sha256_bytes(historical_bytes)
                      if historical_bytes is not None else None)
    baseline_historical = git_blob(baseline, HISTORICAL_SCRIPT_REL)
    baseline_historical_sha = (sha256_bytes(baseline_historical)
                               if baseline_historical is not None else None)
    record_check(
        "historical-script-pin",
        historical_sha is not None
        and historical_sha == baseline_historical_sha,
        "historical script sha256={} baseline={}".format(
            historical_sha, baseline_historical_sha),
        path=HISTORICAL_SCRIPT_REL, observed_sha256=historical_sha,
        expected_sha256=baseline_historical_sha)

    receipt_bytes = {}
    for rel, sha_pin in (
            (CLEAN_RECEIPT_REL, PIN_CLEAN_RECEIPT_SHA256),
            (MISSING_ENV_RECEIPT_REL, PIN_MISSING_ENV_RECEIPT_SHA256)):
        data = git_blob(revision, rel)
        sha = sha256_bytes(data) if data is not None else None
        record_check(
            "receipt-pin-" + Path(rel).stem, sha == sha_pin,
            "{} sha256={} pinned={}".format(rel, sha, sha_pin),
            path=rel, observed_sha256=sha, expected_sha256=sha_pin)
        if sha == sha_pin:
            receipt_bytes[rel] = data

    # ------------------------------------------------ 3. integrity vs baseline
    for rel in PRESERVE_PATHS:
        before = git_blob(baseline, rel)
        after = git_blob(revision, rel)
        record_check(
            "integrity-" + rel,
            before is not None and after is not None and before == after,
            "baseline sha256={} rev sha256={}".format(
                sha256_bytes(before) if before is not None else None,
                sha256_bytes(after) if after is not None else None),
            path=rel)
    runner = git_blob(revision, RUNNER_REL)
    record_check(
        "runner-published-digest",
        runner is not None and sha256_bytes(runner) == PIN_RUNNER_SHA256,
        "runner sha256={} published={}".format(
            sha256_bytes(runner) if runner is not None else None,
            PIN_RUNNER_SHA256))
    summary = git_blob(revision, FROZEN_SUMMARY_REL)
    record_check(
        "frozen-summary-published-digest",
        summary is not None and sha256_bytes(summary) == PIN_SUMMARY_SHA256,
        "summary sha256={} published={}".format(
            sha256_bytes(summary) if summary is not None else None,
            PIN_SUMMARY_SHA256))
    diff = git("diff", "--name-only", baseline, revision, "--",
               ".ufo/evidence/round-12", ".ufo/evidence/round-13",
               ".ufo/evidence/round-14")
    changed = [line for line in
               diff.stdout.decode("utf-8", "replace").splitlines()
               if line.strip()]
    record_check(
        "historical-evidence-unchanged",
        diff.returncode == 0 and not changed,
        "changed paths: {}".format(changed if changed else "none"),
        changed_paths=changed)

    # ----------------------------------------------- 4. frozen inputs + oracle
    clean_data = receipt_bytes.get(CLEAN_RECEIPT_REL)
    mapping_fixture = (build_mapping_suffix_fixture(clean_data)
                       if clean_data is not None else None)
    mapping_fixture_sha = (sha256_bytes(mapping_fixture)
                           if mapping_fixture is not None else None)

    frozen_written = {}
    frozen_specs = [
        ("clean", CLEAN_RECEIPT_REL, "context_consistent", 0,
         PIN_CLEAN_RECEIPT_SHA256),
        ("missing-env", MISSING_ENV_RECEIPT_REL,
         "missing_injected_environment", 1, PIN_MISSING_ENV_RECEIPT_SHA256),
        ("mapping-suffix", None, "mapping_mismatch", 1, mapping_fixture_sha),
    ]
    for key, rel, expected_id, expected_exit, sha_pin in frozen_specs:
        data = (receipt_bytes.get(rel) if rel is not None
                else mapping_fixture)
        if data is None or sha_pin is None:
            record_check("frozen-input-" + key, False,
                         "receipt bytes unavailable for " + key)
            continue
        directory = EVIDENCE / "frozen" / ("context-" + key
                                           if key != "mapping-suffix"
                                           else key)
        receipt_path = directory / "receipt.json"
        expected_path = directory / "expected.json"
        expected = expected_document(expected_id, expected_exit, sha_pin)
        expected_bytes = (
            json.dumps(expected, sort_keys=True) + "\n").encode("utf-8")
        write_frozen_input(receipt_path, data, sha_pin)
        write_frozen_input(expected_path, expected_bytes,
                           sha256_bytes(expected_bytes))
        frozen_written[key] = {
            "receipt": str(receipt_path.resolve()),
            "expected": str(expected_path.resolve()),
            "receipt_sha256": sha_pin,
            "expected_sha256": sha256_bytes(expected_bytes),
        }

    expected_payload = {
        "schema": "tameshi-round15-expected-v1",
        "requested_rev": rev,
        "resolved_revision": revision,
        "baseline_revision": baseline,
        "prefix_revision": prefix,
        "source_sha256": {
            TOOL_REL: PIN_TOOL_SHA256,
            TOOL_REL + "@prefix": PIN_PREFIX_TOOL_SHA256,
            HISTORICAL_SCRIPT_REL: historical_sha,
            RUNNER_REL: PIN_RUNNER_SHA256,
            FROZEN_SUMMARY_REL: PIN_SUMMARY_SHA256,
        },
        "receipt_inputs": {
            CLEAN_RECEIPT_REL: {
                "sha256": PIN_CLEAN_RECEIPT_SHA256,
                "expected_id": "context_consistent", "expected_exit": 0},
            MISSING_ENV_RECEIPT_REL: {
                "sha256": PIN_MISSING_ENV_RECEIPT_SHA256,
                "expected_id": "missing_injected_environment",
                "expected_exit": 1},
            "frozen/mapping-suffix/receipt.json": {
                "sha256": mapping_fixture_sha,
                "expected_id": "mapping_mismatch", "expected_exit": 1},
        },
        "frozen_inputs": frozen_written,
        "expected_commands": {
            "selftest-historical-unsupported": {"exit": 64},
            "selftest-new": {"exit": 0, "stdout_token": "SELFTEST: PASS ("},
            "usage-proof-old": {"exit": 2, "id": "receipt_missing"},
            "usage-proof-new": {"exit": 64, "stderr_token": "id=usage_error"},
            "gate-clean": {"exit": 0, "id": "context_consistent"},
            "gate-missing-env": {"exit": 1,
                                 "id": "missing_injected_environment"},
            "gate-tampered-snapshot": {"exit": 2, "id": "snapshot_tampered",
                                       "verdict_matches_expected": False},
            "gate-usage": {"exit": 64, "stderr_token": "id=usage_error"},
            "mapping-oracle-old": {"exit": 1,
                                   "id": "expected_verdict_mismatch",
                                   "oracle_satisfied": False},
            "mapping-oracle-new": {"exit": 1, "id": "mapping_mismatch",
                                   "verdict_matches_expected": True,
                                   "oracle_satisfied": True},
            "gate-frozen-builtin": {"exit": 0, "id": "context_consistent",
                                    "verdict_matches_expected": True},
            "measure-before": {"exit": 0},
            "measure-after": {"exit": 0},
            "sources-census": {"exit": 0},
        },
    }
    artifact_dir.mkdir(parents=True, exist_ok=True)
    write_json_exclusive(artifact_dir / "expected.json", expected_payload)

    # -------------------------------------- 5. same-path --selftest contrast
    scratch = Path(tempfile.mkdtemp(prefix="tameshi-r15-verify-"))
    SCRATCH = scratch
    tool_path = scratch / "lane" / "tools" / "candidate.py"
    tool_path.parent.mkdir(parents=True)
    selftest_argv = [sys.executable, "-I", str(tool_path), "--selftest"]
    if baseline_historical is None:
        record_check("selftest-historical-unsupported", False,
                     "baseline historical bytes unavailable")
    else:
        tool_path.write_bytes(baseline_historical)
        run_command(
            "selftest-historical-unsupported", selftest_argv, scratch, 64,
            env=env, stderr_token="unexpected argument")
    tool_path.write_bytes(tool_run_bytes)
    record_check(
        "selftest-same-path-same-argv",
        sha256_bytes(tool_path.read_bytes()) == tool_sha,
        "path={} argv identical; only file bytes differ "
        "(old sha256={} new sha256={})".format(
            tool_path, baseline_historical_sha, tool_sha),
        path=str(tool_path))
    proc, _, _ = run_command(
        "selftest-new", selftest_argv, scratch, 0, env=env,
        stdout_token="SELFTEST: PASS (")
    pass_match = re.search(
        r"SELFTEST: PASS \((\d+)/(\d+)\)",
        proc.stdout.decode("utf-8", "replace"))
    record_check(
        "selftest-new-full-count",
        pass_match is not None
        and pass_match.group(1) == pass_match.group(2),
        "summary {}".format(
            pass_match.group(0) if pass_match else "<missing>"))

    # ------------------------- 6. same-path usage-class proof (prefix -> rev)
    usage_dir = scratch / "usage-proof"
    usage_dir.mkdir()
    usage_expected = expected_document(
        "context_consistent", 0, "0" * 64)
    usage_expected_path = usage_dir / "expected.json"
    usage_expected_path.write_text(
        json.dumps(usage_expected, sort_keys=True) + "\n", encoding="utf-8")
    usage_argv = [sys.executable, "-I", str(tool_path), "--check",
                  "--expected", str(usage_expected_path), "--receipt",
                  "--json"]
    tool_path.write_bytes(prefix_run_bytes)
    run_command(
        "usage-proof-old", usage_argv, scratch, 2, env=env,
        expected_id="receipt_missing")
    record_check(
        "usage-proof-no-json-file",
        not (scratch / "--json").exists(),
        "no file named --json created in scratch cwd")
    tool_path.write_bytes(tool_run_bytes)
    run_command(
        "usage-proof-new", usage_argv, scratch, 64, env=env,
        stderr_token="id=usage_error")

    # ------------------------------------------- 7. frozen gate runs (rev)

    # Registered-path frozen mode: exercises the built-in pin and lane-root
    # resolution of the actual maintained tool (not the temp copy).
    worktree_tool = ROOT / TOOL_REL
    worktree_sha = (sha256_bytes(worktree_tool.read_bytes())
                    if worktree_tool.exists() else None)
    record_check(
        "registered-tool-source-pin", worktree_sha == PIN_TOOL_SHA256,
        "worktree {} sha256={} pinned={}".format(
            TOOL_REL, worktree_sha, PIN_TOOL_SHA256),
        path=TOOL_REL, observed_sha256=worktree_sha,
        expected_sha256=PIN_TOOL_SHA256)
    proc, frozen_doc, _ = run_command(
        "gate-frozen-builtin",
        [sys.executable, str(worktree_tool), "--check", "--json"],
        ROOT, 0, env=env, expected_id="context_consistent",
        stdout_is_result_json=True, expected_verdict_match=True)
    if type(frozen_doc) is dict:
        receipt_info = frozen_doc.get("receipt") or {}
        record_check(
            "frozen-builtin-inputs",
            frozen_doc.get("mode") == "frozen"
            and receipt_info.get("path") == CLEAN_RECEIPT_REL
            and receipt_info.get("sha256") == PIN_CLEAN_RECEIPT_SHA256
            and receipt_info.get("digest_matches") is True,
            "mode={} receipt={} sha256={} digest_matches={}".format(
                frozen_doc.get("mode"), receipt_info.get("path"),
                receipt_info.get("sha256"),
                receipt_info.get("digest_matches")),
            receipt=receipt_info)
    tool_path.write_bytes(tool_run_bytes)
    check_argv = [sys.executable, "-I", str(tool_path), "--check"]
    if "clean" in frozen_written:
        run_command(
            "gate-clean",
            check_argv + ["--receipt", frozen_written["clean"]["receipt"],
                          "--expected", frozen_written["clean"]["expected"],
                          "--json"],
            scratch, 0, env=env, expected_id="context_consistent",
            stdout_is_result_json=True, expected_verdict_match=True)
    if "missing-env" in frozen_written:
        run_command(
            "gate-missing-env",
            check_argv + ["--receipt",
                          frozen_written["missing-env"]["receipt"],
                          "--expected",
                          frozen_written["missing-env"]["expected"],
                          "--json"],
            scratch, 1, env=env, expected_id="missing_injected_environment",
            stdout_is_result_json=True, expected_verdict_match=True)
    # Tampered snapshot: scratch-only mutation of the pinned clean receipt;
    # the expected pin still declares the honest clean pair, so the gate must
    # refuse at integrity (snapshot_tampered/2) and mark the pin unmatched.
    if clean_data is not None:
        tampered = scratch / "tampered-snapshot"
        tampered.mkdir()
        tampered_receipt = (clean_data[:256]
                            + bytes([clean_data[256] ^ 0x01])
                            + clean_data[257:])
        (tampered / "receipt.json").write_bytes(tampered_receipt)
        tampered_expected = expected_document(
            "context_consistent", 0, PIN_CLEAN_RECEIPT_SHA256)
        (tampered / "expected.json").write_text(
            json.dumps(tampered_expected, sort_keys=True) + "\n",
            encoding="utf-8")
        record_check(
            "tampered-input-differs",
            sha256_bytes(tampered_receipt) != PIN_CLEAN_RECEIPT_SHA256,
            "tampered sha256={} pinned={}".format(
                sha256_bytes(tampered_receipt), PIN_CLEAN_RECEIPT_SHA256))
        run_command(
            "gate-tampered-snapshot",
            check_argv + ["--receipt", str(tampered / "receipt.json"),
                          "--expected", str(tampered / "expected.json"),
                          "--json"],
            scratch, 2, env=env, expected_id="snapshot_tampered",
            stdout_is_result_json=True, expected_verdict_match=False)
    # Usage class on the final source: --receipt without --expected.
    run_command(
        "gate-usage",
        [sys.executable, "-I", str(tool_path), "--check", "--receipt",
         "receipt.json"],
        scratch, 64, env=env, stderr_token="id=usage_error")

    # ------------------------- 8. mapping oracle (prefix -> rev, same path)
    if "mapping-suffix" in frozen_written:
        mapping_argv = check_argv + [
            "--receipt", frozen_written["mapping-suffix"]["receipt"],
            "--expected", frozen_written["mapping-suffix"]["expected"],
            "--json"]
        oracle_satisfied = {}
        tool_path.write_bytes(prefix_run_bytes)
        proc, doc, _ = run_command(
            "mapping-oracle-old", mapping_argv, scratch, 1, env=env,
            expected_id="expected_verdict_mismatch",
            stdout_is_result_json=True)
        oracle_satisfied["old"] = bool(
            proc.returncode == 1 and type(doc) is dict
            and doc.get("id") == "mapping_mismatch")
        record_check(
            "mapping-oracle-old-status",
            oracle_satisfied["old"] is False,
            "literal oracle (exit1+id mapping_mismatch) on prefix "
            "source: {} (expected fail)".format(
                "pass" if oracle_satisfied["old"] else "fail"),
            oracle_status="fail" if not oracle_satisfied["old"]
            else "pass")
        tool_path.write_bytes(tool_run_bytes)
        proc, doc, _ = run_command(
            "mapping-oracle-new", mapping_argv, scratch, 1, env=env,
            expected_id="mapping_mismatch", stdout_is_result_json=True,
            expected_verdict_match=True)
        oracle_satisfied["new"] = bool(
            proc.returncode == 1 and type(doc) is dict
            and doc.get("id") == "mapping_mismatch")
        record_check(
            "mapping-oracle-discriminates",
            oracle_satisfied.get("old") is False
            and oracle_satisfied.get("new") is True,
            "oracle old={} new={} (only checker source differs)".format(
                "FAIL/1" if not oracle_satisfied.get("old") else "PASS/0",
                "PASS/0" if oracle_satisfied.get("new") else "FAIL/1"),
            oracle_statuses=oracle_satisfied)

    # ------------------------------------------------------------- 9. measure
    measure_path = ROOT / MEASURE_REL
    measure_blob = git_blob(revision, MEASURE_REL)
    worktree_measure = (measure_path.read_bytes()
                        if measure_path.exists() else None)
    record_check(
        "measure-script-pin",
        measure_blob is not None and worktree_measure is not None
        and measure_blob == worktree_measure,
        "worktree measure.py {} revision blob".format(
            "equals" if measure_blob == worktree_measure
            else "differs from"),
        path=MEASURE_REL,
        observed_sha256=(sha256_bytes(worktree_measure)
                         if worktree_measure else None))
    proc, _, _ = run_command(
        "measure-before",
        [sys.executable, str(measure_path), "--rev", baseline], ROOT, 0,
        env=env)
    write_exclusive(artifact_dir / "before.json",
                    proc.stdout.decode("utf-8", "replace"))
    before_doc = None
    try:
        before_doc = json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        before_doc = None
    proc, _, _ = run_command(
        "measure-after",
        [sys.executable, str(measure_path), "--rev", revision], ROOT, 0,
        env=env)
    write_exclusive(artifact_dir / "after.json",
                    proc.stdout.decode("utf-8", "replace"))
    after_doc = None
    try:
        after_doc = json.loads(proc.stdout.decode("utf-8", "replace"))
    except ValueError:
        after_doc = None
    for label, doc, expects in (
            ("before", before_doc, {
                "context_capture_present": 0,
                "runner_sha256_matches_round14_published": 1,
                "frozen_summary_sha256_matches_round14_published": 1,
                "recorded_cases": 6,
                "calibration_restraint_score": 6}),
            ("after", after_doc, {
                "context_capture_present": 1,
                "context_capture_sha256": PIN_TOOL_SHA256,
                "context_gate_active_classification": 1,
                "context_standalone_selftest_present": 1,
                "context64_explicit_class": 1,
                "disposition64_explicit_class": 1,
                "explicit64_classes_declared": 2,
                "runner_sha256_matches_round14_published": 1,
                "frozen_summary_sha256_matches_round14_published": 1,
                "recorded_cases": 6,
                "calibration_restraint_score": 6})):
        if not type(doc) is dict:
            record_check("measure-{}-fields".format(label), False,
                         "measure output is not a JSON document")
            continue
        bad = {key: (doc.get(key), want) for key, want in expects.items()
               if doc.get(key) != want}
        record_check(
            "measure-{}-fields".format(label), not bad,
            "mismatches {}".format(bad) if bad else "all pinned fields match",
            observed={key: doc.get(key) for key in expects})
    if type(after_doc) is dict:
        hist = after_doc.get("historical_evidence") or {}
        record_check(
            "measure-historical-preserved",
            hist.get("all_baseline_bytes_preserved") == 1,
            "all_baseline_bytes_preserved={} changed={}".format(
                hist.get("all_baseline_bytes_preserved"),
                hist.get("changed_or_missing")))

    # ----------------------------------------------- 10. source census end
    census_argv = [CENSUS_TOOL, "validate", "--root",
                   "/home/vgpnk/Projects/shokunin", "tameshi"]
    proc, _, _ = run_command("sources-census", census_argv, ROOT, 0, env=env)
    census_stdout = proc.stdout.decode("utf-8", "replace")
    record_check(
        "sources-census-ok-line",
        any(line.startswith("tameshi\tok\t")
            for line in census_stdout.splitlines()),
        "ok line {}".format(
            "present" if "tameshi\tok" in census_stdout else "absent"))
    write_json_exclusive(artifact_dir / "sources-after.json", {
        "command": census_argv,
        "exit": proc.returncode,
        "stdout": census_stdout,
        "stderr": proc.stderr.decode("utf-8", "replace"),
        "revision": revision,
        "observation": ("Captured at round-15 verification end after round15 "
                        "writes; warnings preserved, not suppressed."),
    })


if __name__ == "__main__":
    raise SystemExit(main())
