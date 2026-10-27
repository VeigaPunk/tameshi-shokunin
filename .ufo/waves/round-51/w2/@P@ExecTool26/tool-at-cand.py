#!/usr/bin/env python3
"""witness-metadata.py — bounded companion-metadata gate for the frozen
round-12 BashWitness declaration.

The round-12 producer (tools/bash-witness-study.py:787) wrote the nested
declaration.kind from declaration["declared"]["kind"], a field that does not
exist; the explicit frozen kind lives at declaration.json's top level
(:6).  The frozen summary therefore records declaration.kind = null.  This
gate does not rewrite those bytes.  It validates a NEW companion metadata
file that:

  * anchors sha256 of the three declaration inputs the checker reads
    (summary.json, declaration.json, declared.tsv) both in the companion
    and in this tool (a companion that carries its own digests alone would
    be self-certifying);
  * separately digest-pins and reads the rerun summary as a raw historical
    observation: it remains outside normalized scope, with its
    declaration.kind = null named and uncorrected;
  * carries the normalized declaration.kind as the literal frozen top-level
    kind, never an invented label and never a null-as-blind downgrade;
  * preserves the frozen disclosure byte-for-byte and records
    prior_exposure = true / blind = false;
  * records the original nested null as a historical fact, not as
    authority.

Integrity before comparison: all four pinned files are resolved, hashed and
read into memory before any exit-1 comparison; the companion digest map is
then checked against the tool's pinned literals; parsing uses the exact
hashed bytes (no second read).

Exit codes:
  0  metadata_consistent
  1  metadata_inconsistent
  2  input_unavailable or snapshot_tampered

Modes:
  --check     validate the companion against the live lane (read-only)
  --selftest  run the CLI over isolated tempfile fixtures and assert the
              literal expected IDs/exits in SELFTEST_CASES
  --emit      print the companion object built from the pinned constants to
              stdout (construction helper; reads and writes nothing)

No mode writes inside the lane.  The only writes are the isolated fixture
tree created by --selftest under tempfile.mkdtemp() and removed in a
finally block.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

# ---------------------------------------------------------------------------
# Pinned literals.  These are the authority, not the companion file.
# ---------------------------------------------------------------------------

SCHEMA = "tameshi-witness-metadata/v1"
GENERATED_FOR = "round-13"
DEFAULT_COMPANION_REL = ".ufo/evidence/round-13/witness-metadata.json"

LANE_ROOT = Path(__file__).resolve().parent.parent

PINNED_INPUTS = (
    (
        "summary",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ),
    (
        "declaration",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ),
    (
        "declared",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ),
)
PINNED_BY_NAME = {name: (rel, digest) for name, rel, digest in PINNED_INPUTS}
DECLARED_BASENAME = "declared.tsv"

EXPECTED_KIND = "declared-witness mapping (not a blind preregistration)"
EXPECTED_DISCLOSURE = (
    "declared-witness mapping, not a blind preregistration: before declaring, "
    "the author had seen recorded aggregate outcomes of this leg \u2014 the "
    "recorded kill-rate header of tools/mutate-and-run.sh, the "
    "corpus/README.md coverage row for mutation-case-kagi-census.md, the "
    "SOURCES.md S033 row, and the recorded TABLE_BASH per-defect "
    "KILLED/SURVIVED entries surfaced by a pin grep. No per-defect witness "
    "classification of this leg existed before this run."
)
EXPECTED_DISCLOSURE_SHA256 = (
    "ec6e5be711945a84e1148819a12d7897386c319a2544b8b0829b4bd74af9b2f0"
)
ORIGINAL_NESTED_SOURCE = "summary.json#/declaration/kind"
HISTORICAL_NESTED_STATE = "historical-null-preserved"

EXPECTED_VERDICT_ID = "metadata_consistent"
EXPECTED_VERDICT_EXIT = 0

# Historical facts copied from the frozen JSON.  They are validated against
# the digest-pinned documents, never against the live tools on disk: C2 must
# not depend on the C1 runner/tool staying byte-identical.
PRODUCER_TOOL_PATH = "tools/bash-witness-study.py"
PRODUCER_TOOL_SHA256 = (
    "249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a"
)
HISTORICAL_RUNNER_PATH = "tools/mutate-and-run.sh"
HISTORICAL_RUNNER_SHA256 = (
    "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5"
)

# The second frozen null observation stays outside normalized scope but is
# digest-anchored and read as a raw historical observation: this companion
# repairs only the canonical summary's normalized kind and leaves the rerun
# summary's declaration.kind = null uncorrected.  Silence would hide it.
RERUN_SUMMARY_REL = (
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json"
)
RERUN_SUMMARY_SHA256 = (
    "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0"
)
UNCOVERED_DISPOSITION = "named-residual-uncorrected"

HEX64 = re.compile(r"[0-9a-f]{64}")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def build_companion() -> dict:
    """Build the companion object from the pinned constants.

    Deterministic: no timestamp, no host state, no frozen-file reads.
    """
    return {
        "schema": SCHEMA,
        "generated_for": GENERATED_FOR,
        "purpose": (
            "Digest-anchored normalized metadata for the frozen round-12 "
            "BashWitness declaration; frozen round-12 bytes are not "
            "rewritten."
        ),
        "expected": {
            "id": EXPECTED_VERDICT_ID,
            "exit": EXPECTED_VERDICT_EXIT,
        },
        "frozen_declaration": {
            name: {"path": rel, "sha256": digest}
            for name, rel, digest in PINNED_INPUTS
        },
        "producer": {
            "path": PRODUCER_TOOL_PATH,
            "sha256": PRODUCER_TOOL_SHA256,
            "source": "summary.json#/tool",
            "checked_live": False,
            "note": (
                "Historical producer identity of the frozen observation; the "
                "gate does not live-hash tools/bash-witness-study.py."
            ),
        },
        "historical_runner": {
            "path": HISTORICAL_RUNNER_PATH,
            "sha256": HISTORICAL_RUNNER_SHA256,
            "source": "declaration.json#/inputs/runner",
            "checked_live": False,
            "note": (
                "Historical pin source for C1; the gate does not live-hash "
                "tools/mutate-and-run.sh."
            ),
        },
        "scope": {
            "covered_null_observations": [
                {
                    "path": PINNED_BY_NAME["summary"][0],
                    "sha256": PINNED_BY_NAME["summary"][1],
                    "field": "declaration.kind",
                    "value": None,
                }
            ],
            "uncovered_null_observations": [
                {
                    "path": RERUN_SUMMARY_REL,
                    "sha256": RERUN_SUMMARY_SHA256,
                    "field": "declaration.kind",
                    "value": None,
                    "disposition": UNCOVERED_DISPOSITION,
                    "integrity": "sha256-anchored-and-reverified",
                }
            ],
        },
        "declaration": {
            "kind": EXPECTED_KIND,
            "kind_source": "declaration.json#/kind (explicit frozen top-level field)",
            "disclosure": EXPECTED_DISCLOSURE,
            "disclosure_sha256": EXPECTED_DISCLOSURE_SHA256,
            "disclosure_source": (
                "declaration.json#/disclosure, byte-equal to "
                "summary.json#/declaration/disclosure"
            ),
            "prior_exposure": True,
            "blind": False,
        },
        "original_nested": {
            "source": ORIGINAL_NESTED_SOURCE,
            "value": None,
            "state": HISTORICAL_NESTED_STATE,
            "note": (
                "The frozen summary records kind=null because the producer "
                "read declared.kind; the companion kind above is additive "
                "metadata. The null remains a historical fact and is never "
                "reused as authority."
            ),
        },
        "frozen_bytes_rewritten": False,
        "measured_claim_unchanged": True,
    }


# ---------------------------------------------------------------------------
# Verdicts and strict input handling
# ---------------------------------------------------------------------------


class Failure(Exception):
    def __init__(self, verdict_id: str, reason: str, exit_code: int, detail: str = ""):
        super().__init__(reason)
        self.verdict_id = verdict_id
        self.reason = reason
        self.exit_code = exit_code
        self.detail = detail


SNAPSHOT_TAMPER_REASONS = frozenset(
    {
        "companion_inputs_mismatch",
        "companion_path_mismatch",
        "companion_digest_invalid",
        "companion_digest_unpinned",
    }
)


def _fail(reason: str, exit_code: int = 1, detail: str = "") -> None:
    if exit_code == 1:
        verdict_id = "metadata_inconsistent"
    elif exit_code == 2 and (
        reason.endswith("_digest_mismatch") or reason in SNAPSHOT_TAMPER_REASONS
    ):
        verdict_id = "snapshot_tampered"
    else:
        verdict_id = "input_unavailable"
    raise Failure(verdict_id, reason, exit_code, detail)


class _DuplicateKey(ValueError):
    pass


def _reject_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise _DuplicateKey(f"duplicate JSON key: {key!r}")
        seen[key] = value
    return seen


def _reject_constant(token: str):
    raise ValueError(f"non-finite JSON constant: {token}")


def parse_json_object(raw: bytes, label: str) -> dict:
    """Strict JSON object parse over already-hashed bytes."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _fail(f"{label}_json_invalid", 2, "not valid UTF-8")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except (ValueError, json.JSONDecodeError):
        _fail(f"{label}_json_invalid", 2, "malformed JSON")
    if not isinstance(value, dict):
        _fail(f"{label}_json_not_object", 2, "top-level JSON value is not an object")
    return value


def load_json_object(path: Path, label: str) -> dict:
    """Read once, then strict-parse the same bytes."""
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        _fail(f"{label}_missing", 2, str(path))
    except OSError as exc:
        _fail(f"{label}_unreadable", 2, f"{path}: {exc.strerror or exc}")
    return parse_json_object(raw, label)


def validate_relative_path(rel: str, label: str) -> PurePosixPath:
    """Reject absolute paths, empty values and '..' segments."""
    if not isinstance(rel, str) or not rel:
        _fail("path_rejected", 2, f"{label}: empty path")
    pure = PurePosixPath(rel)
    if pure.is_absolute():
        _fail("path_rejected", 2, f"{label}: absolute path")
    if any(part == ".." for part in pure.parts):
        _fail("path_rejected", 2, f"{label}: parent traversal")
    return pure


def safe_input_path(lane_root: Path, rel: str, label: str) -> Path:
    """Resolve a companion-declared relative path without escaping the lane.

    Rejects absolute paths, '..' segments, symlink components and
    non-regular files.  Missing files are input_unavailable.
    """
    pure = validate_relative_path(rel, label)
    current = lane_root
    for part in pure.parts:
        current = current / part
        try:
            st = os.lstat(current)
        except FileNotFoundError:
            _fail("input_missing", 2, f"{label}: {rel}")
        except OSError as exc:
            _fail("input_unreadable", 2, f"{label}: {rel}: {exc.strerror or exc}")
        if stat.S_ISLNK(st.st_mode):
            _fail("path_rejected", 2, f"{label}: symlink component {current}")
    if not stat.S_ISREG(os.lstat(current).st_mode):
        _fail("path_rejected", 2, f"{label}: not a regular file {current}")
    resolved = current.resolve()
    try:
        resolved.relative_to(lane_root.resolve())
    except ValueError:
        _fail("path_rejected", 2, f"{label}: resolves outside lane root")
    return resolved


# ---------------------------------------------------------------------------
# Core check
# ---------------------------------------------------------------------------


ALL_PINNED = tuple(PINNED_INPUTS) + (
    ("rerun_summary", RERUN_SUMMARY_REL, RERUN_SUMMARY_SHA256),
)


def run_check(lane_root: Path, companion_path: Path) -> dict:
    lane = lane_root.resolve()
    if not lane.is_dir():
        _fail("lane_root_unavailable", 2, str(lane_root))

    # Companion path: regular file only; symlinks are rejected.  An explicit
    # --companion may live outside the lane (direct old-null red probe), but
    # the result reports the resolved lane root and in-lane status.
    try:
        companion_stat = os.lstat(companion_path)
    except FileNotFoundError:
        _fail("companion_missing", 2, str(companion_path))
    except OSError as exc:
        _fail("companion_unreadable", 2, f"{companion_path}: {exc.strerror or exc}")
    if stat.S_ISLNK(companion_stat.st_mode):
        _fail("companion_path_rejected", 2, "symlink companion")
    if not stat.S_ISREG(companion_stat.st_mode):
        _fail("companion_path_rejected", 2, "not a regular file")
    companion = load_json_object(companion_path, "companion")

    # ---- INTEGRITY FIRST: hash every file this checker reads before any
    # exit-1 comparison.  A tampered byte must never be masked by a companion
    # semantic defect.  The exact hashed bytes are parsed below, never
    # re-read from disk.
    input_bytes = {}
    resolved_inputs = {}
    for name, rel, pinned_digest in ALL_PINNED:
        path = safe_input_path(lane, rel, name)
        try:
            raw = path.read_bytes()
        except OSError as exc:
            _fail("input_unreadable", 2, f"{name}: {exc.strerror or exc}")
        actual = _sha256_bytes(raw)
        if actual != pinned_digest:
            _fail(f"{name}_digest_mismatch", 2, f"{name}: {actual} != {pinned_digest}")
        input_bytes[name] = raw
        resolved_inputs[name] = path

    # ---- schema and companion digest manifest -----------------------------
    if companion.get("schema") != SCHEMA:
        _fail("schema_mismatch", 1, f"expected {SCHEMA!r}")
    if companion.get("generated_for") != GENERATED_FOR:
        _fail("generated_for_mismatch", 1, f"expected {GENERATED_FOR!r}")

    expected = companion.get("expected")
    if not isinstance(expected, dict):
        _fail("expected_record_missing", 1)
    if expected.get("id") != EXPECTED_VERDICT_ID:
        _fail("expected_id_mismatch", 1, repr(expected.get("id")))
    if type(expected.get("exit")) is not int or expected.get("exit") != EXPECTED_VERDICT_EXIT:
        _fail("expected_exit_mismatch", 1, repr(expected.get("exit")))

    frozen = companion.get("frozen_declaration")
    if not isinstance(frozen, dict):
        _fail("companion_inputs_mismatch", 2, "frozen_declaration is not an object")
    expected_names = [name for name, _rel, _digest in PINNED_INPUTS]
    if sorted(frozen) != sorted(expected_names):
        _fail(
            "companion_inputs_mismatch",
            2,
            f"expected exactly {expected_names}, observed {sorted(frozen)}",
        )

    for name, rel, pinned_digest in PINNED_INPUTS:
        entry = frozen.get(name)
        if not isinstance(entry, dict):
            _fail("companion_inputs_mismatch", 2, f"{name}: entry is not an object")
        declared_path = entry.get("path")
        validate_relative_path(declared_path, name)
        if declared_path != rel:
            _fail("companion_path_mismatch", 2, f"{name}: {declared_path!r} != {rel!r}")
        recorded = entry.get("sha256")
        if not isinstance(recorded, str) or not HEX64.fullmatch(recorded):
            _fail("companion_digest_invalid", 2, f"{name}: missing or non-hex digest")
        if recorded != pinned_digest:
            _fail("companion_digest_unpinned", 2, f"{name}: companion digest is not the pinned value")

    # ---- parse the exact hashed bytes -------------------------------------
    summary = parse_json_object(input_bytes["summary"], "summary")
    declaration = parse_json_object(input_bytes["declaration"], "declaration")
    rerun_summary = parse_json_object(input_bytes["rerun_summary"], "rerun_summary")

    # ---- historical identities and explicit null scope (no live tool hash) --
    summary_tool = summary.get("tool")
    if not isinstance(summary_tool, dict) or summary_tool.get("sha256") != PRODUCER_TOOL_SHA256:
        _fail("producer_identity_mismatch", 1, "summary.json#/tool")
    producer = companion.get("producer")
    if not isinstance(producer, dict):
        _fail("producer_missing", 1)
    if producer.get("path") != PRODUCER_TOOL_PATH or producer.get("sha256") != PRODUCER_TOOL_SHA256:
        _fail("producer_identity_mismatch", 1, "companion.producer")
    if producer.get("checked_live") is not False:
        _fail("producer_checked_live_invalid", 1)

    declaration_runner = declaration.get("inputs", {}).get("runner") if isinstance(
        declaration.get("inputs"), dict
    ) else None
    if not isinstance(declaration_runner, dict) or declaration_runner.get("sha256") != HISTORICAL_RUNNER_SHA256:
        _fail("runner_identity_mismatch", 1, "declaration.json#/inputs/runner")
    historical_runner = companion.get("historical_runner")
    if not isinstance(historical_runner, dict):
        _fail("runner_missing", 1)
    if (
        historical_runner.get("path") != HISTORICAL_RUNNER_PATH
        or historical_runner.get("sha256") != HISTORICAL_RUNNER_SHA256
    ):
        _fail("runner_identity_mismatch", 1, "companion.historical_runner")
    if historical_runner.get("checked_live") is not False:
        _fail("runner_checked_live_invalid", 1)

    scope = companion.get("scope")
    if not isinstance(scope, dict):
        _fail("scope_missing", 1)
    covered = scope.get("covered_null_observations")
    if not isinstance(covered, list) or len(covered) != 1:
        _fail("scope_covered_mismatch", 1)
    covered_entry = covered[0]
    if not isinstance(covered_entry, dict) or (
        covered_entry.get("path") != PINNED_BY_NAME["summary"][0]
        or covered_entry.get("sha256") != PINNED_BY_NAME["summary"][1]
        or covered_entry.get("field") != "declaration.kind"
        or "value" not in covered_entry
        or covered_entry.get("value") is not None
    ):
        _fail("scope_covered_mismatch", 1)
    uncovered = scope.get("uncovered_null_observations")
    if not isinstance(uncovered, list) or len(uncovered) != 1:
        _fail("scope_uncovered_missing", 1)
    uncovered_entry = uncovered[0]
    if not isinstance(uncovered_entry, dict) or (
        uncovered_entry.get("path") != RERUN_SUMMARY_REL
        or uncovered_entry.get("sha256") != RERUN_SUMMARY_SHA256
        or uncovered_entry.get("field") != "declaration.kind"
        or "value" not in uncovered_entry
        or uncovered_entry.get("value") is not None
        or uncovered_entry.get("disposition") != UNCOVERED_DISPOSITION
        or uncovered_entry.get("integrity") != "sha256-anchored-and-reverified"
    ):
        _fail("scope_uncovered_mismatch", 1)

    # The scoped-out rerun null was already hashed and parsed from the exact
    # pinned bytes above, before any exit-1 comparison.
    rerun_declaration = rerun_summary.get("declaration")
    if not isinstance(rerun_declaration, dict):
        _fail("rerun_declaration_missing", 1)
    if rerun_declaration.get("kind") is not None:
        _fail("rerun_nested_not_null", 1)
    if rerun_declaration.get("disclosure") != EXPECTED_DISCLOSURE:
        _fail("rerun_disclosure_mismatch", 1)
    if rerun_declaration.get("sha256") != PINNED_BY_NAME["declared"][1]:
        _fail("rerun_declared_binding_mismatch", 1)

    # ---- frozen top-level kind and disclosure -----------------------------
    if declaration.get("kind") != EXPECTED_KIND:
        _fail("top_level_kind_invalid", 1, repr(declaration.get("kind")))

    source_disclosure = declaration.get("disclosure")
    if not isinstance(source_disclosure, str) or not source_disclosure.strip():
        _fail("source_disclosure_missing", 1)
    if source_disclosure != EXPECTED_DISCLOSURE:
        _fail("source_disclosure_mismatch", 1)
    if _sha256_text(source_disclosure) != EXPECTED_DISCLOSURE_SHA256:
        _fail("source_disclosure_digest_mismatch", 1)

    summary_declaration = summary.get("declaration")
    if not isinstance(summary_declaration, dict):
        _fail("summary_declaration_missing", 1)
    if "kind" not in summary_declaration:
        _fail("original_nested_missing", 1)
    if summary_declaration["kind"] is not None:
        _fail("original_nested_not_null", 1)
    if summary_declaration.get("disclosure") != source_disclosure:
        _fail("summary_disclosure_mismatch", 1)
    if summary_declaration.get("path") != DECLARED_BASENAME:
        _fail("declared_path_mismatch", 1, "summary.declaration.path")
    if summary_declaration.get("sha256") != PINNED_BY_NAME["declared"][1]:
        _fail("declared_binding_mismatch", 1, "summary.declaration.sha256")

    declared_block = declaration.get("declared")
    if not isinstance(declared_block, dict):
        _fail("declaration_inputs_missing", 1)
    if declared_block.get("path") != DECLARED_BASENAME:
        _fail("declared_path_mismatch", 1, "declaration.declared.path")
    if declared_block.get("sha256") != PINNED_BY_NAME["declared"][1]:
        _fail("declared_binding_mismatch", 1, "declaration.declared.sha256")

    # ---- companion declaration semantics ----------------------------------
    comp_decl = companion.get("declaration")
    if not isinstance(comp_decl, dict):
        _fail("declaration_missing", 1)
    if "kind" not in comp_decl:
        _fail("normalized_kind_missing", 1)
    comp_kind = comp_decl["kind"]
    if comp_kind is None:
        _fail("normalized_kind_null", 1)
    if not isinstance(comp_kind, str):
        _fail("normalized_kind_invalid", 1)
    if comp_kind != EXPECTED_KIND:
        _fail("normalized_kind_mismatch", 1, repr(comp_kind))

    if comp_decl.get("kind_source") != "declaration.json#/kind (explicit frozen top-level field)":
        _fail("kind_source_invalid", 1)

    if "disclosure" not in comp_decl:
        _fail("disclosure_missing", 1)
    comp_disclosure = comp_decl["disclosure"]
    if not isinstance(comp_disclosure, str) or not comp_disclosure.strip():
        _fail("disclosure_missing", 1)
    if comp_disclosure != EXPECTED_DISCLOSURE:
        _fail("disclosure_mismatch", 1)
    if comp_decl.get("disclosure_sha256") != EXPECTED_DISCLOSURE_SHA256:
        _fail("disclosure_digest_mismatch", 1)
    if comp_decl.get("disclosure_source") != (
        "declaration.json#/disclosure, byte-equal to "
        "summary.json#/declaration/disclosure"
    ):
        _fail("disclosure_source_invalid", 1)

    if "prior_exposure" not in comp_decl:
        _fail("prior_exposure_missing", 1)
    if comp_decl["prior_exposure"] is not True:
        _fail("prior_exposure_invalid", 1)
    if "blind" not in comp_decl:
        _fail("blind_missing", 1)
    if comp_decl["blind"] is not False:
        _fail("blind_upgrade_rejected", 1)

    original_nested = companion.get("original_nested")
    if not isinstance(original_nested, dict):
        _fail("original_nested_missing", 1)
    if original_nested.get("source") != ORIGINAL_NESTED_SOURCE:
        _fail("original_nested_source_invalid", 1)
    if "value" not in original_nested:
        _fail("original_nested_value_missing", 1)
    if original_nested["value"] is not None:
        _fail("original_nested_not_null", 1)
    if original_nested.get("state") != HISTORICAL_NESTED_STATE:
        _fail("original_nested_state_invalid", 1)

    if companion.get("frozen_bytes_rewritten") is not False:
        _fail("frozen_bytes_claim_invalid", 1)
    if companion.get("measured_claim_unchanged") is not True:
        _fail("measured_claim_invalid", 1)

    # No unmodeled keys or values: the companion is exactly the canonical
    # object built from pinned constants.  This closes silent extras such as
    # declaration.preregistration = "blind" or original_nested.authoritative.
    if companion != build_companion():
        _fail("companion_noncanonical", 1)

    try:
        companion_path.resolve().relative_to(lane)
        companion_in_lane = True
    except ValueError:
        companion_in_lane = False

    return {
        "id": EXPECTED_VERDICT_ID,
        "reason": "ok",
        "exit": EXPECTED_VERDICT_EXIT,
        "lane_root": str(lane),
        "companion": str(companion_path),
        "companion_in_lane": companion_in_lane,
        "inputs_verified": [name for name, _rel, _digest in ALL_PINNED],
        "normalized_kind": comp_kind,
    }


def emit_result(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return
    print(
        "WITNESS_METADATA: {id} reason={reason} exit={exit} companion={companion} "
        "inputs={inputs}".format(
            id=result["id"],
            reason=result["reason"],
            exit=result["exit"],
            companion=result.get("companion", "-"),
            inputs=",".join(result.get("inputs_verified", [])) or "-",
        )
    )
    detail = result.get("detail")
    if detail:
        print(f"WITNESS_METADATA_DETAIL: {detail}")


# ---------------------------------------------------------------------------
# Selftest: CLI over isolated fixtures, literal expected IDs/exits
# ---------------------------------------------------------------------------

SELFTEST_CASES = (
    {
        "case": "corrected-companion-green",
        "expected_id": "metadata_consistent",
        "expected_reason": "ok",
        "expected_exit": 0,
        "setup": "green",
    },
    {
        "case": "old-null-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "normalized_kind_null",
        "expected_exit": 1,
        "setup": "old-null",
    },
    {
        "case": "expected-record-missing-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "expected_record_missing",
        "expected_exit": 1,
        "setup": "expected-record-missing",
    },
    {
        "case": "rerun-scope-omitted-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "scope_uncovered_missing",
        "expected_exit": 1,
        "setup": "rerun-scope-omitted",
    },
    {
        "case": "producer-checked-live-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "producer_checked_live_invalid",
        "expected_exit": 1,
        "setup": "producer-checked-live",
    },
    {
        "case": "extra-blind-key-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "companion_noncanonical",
        "expected_exit": 1,
        "setup": "extra-blind-key",
    },
    {
        "case": "tamper-rerun-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "rerun_summary_digest_mismatch",
        "expected_exit": 2,
        "setup": "tamper-rerun",
    },
    {
        "case": "tamper-plus-companion-defect-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "rerun_summary_digest_mismatch",
        "expected_exit": 2,
        "setup": "tamper-plus-companion-defect",
    },
    {
        "case": "tamper-declaration-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "declaration_digest_mismatch",
        "expected_exit": 2,
        "setup": "tamper-declaration",
    },
    {
        "case": "symlink-input-red",
        "expected_id": "input_unavailable",
        "expected_reason": "path_rejected",
        "expected_exit": 2,
        "setup": "symlink-input",
    },
    {
        "case": "symlink-companion-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_path_rejected",
        "expected_exit": 2,
        "setup": "symlink-companion",
    },
    {
        "case": "lane-root-missing-red",
        "expected_id": "input_unavailable",
        "expected_reason": "lane_root_unavailable",
        "expected_exit": 2,
        "setup": "lane-root-missing",
    },
    {
        "case": "nan-companion-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_json_invalid",
        "expected_exit": 2,
        "setup": "nan-companion",
    },
    {
        "case": "non-object-companion-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_json_not_object",
        "expected_exit": 2,
        "setup": "non-object-companion",
    },
    {
        "case": "invalid-utf8-companion-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_json_invalid",
        "expected_exit": 2,
        "setup": "invalid-utf8-companion",
    },
    {
        "case": "wrong-schema-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "schema_mismatch",
        "expected_exit": 1,
        "setup": "wrong-schema",
    },
    {
        "case": "frozen-manifest-not-object-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "companion_inputs_mismatch",
        "expected_exit": 2,
        "setup": "frozen-manifest-not-object",
    },
    {
        "case": "companion-path-mismatch-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "companion_path_mismatch",
        "expected_exit": 2,
        "setup": "companion-path-mismatch",
    },
    {
        "case": "producer-missing-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "producer_missing",
        "expected_exit": 1,
        "setup": "producer-missing",
    },
    {
        "case": "runner-mismatch-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "runner_identity_mismatch",
        "expected_exit": 1,
        "setup": "runner-mismatch",
    },
    {
        "case": "frozen-flag-rewritten-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "frozen_bytes_claim_invalid",
        "expected_exit": 1,
        "setup": "frozen-flag-rewritten",
    },
    {
        "case": "wrong-kind-short-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "normalized_kind_mismatch",
        "expected_exit": 1,
        "setup": "wrong-kind-short",
    },
    {
        "case": "wrong-kind-blind-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "normalized_kind_mismatch",
        "expected_exit": 1,
        "setup": "wrong-kind-blind",
    },
    {
        "case": "absent-disclosure-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "disclosure_missing",
        "expected_exit": 1,
        "setup": "absent-disclosure",
    },
    {
        "case": "disclosure-mismatch-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "disclosure_mismatch",
        "expected_exit": 1,
        "setup": "disclosure-mismatch",
    },
    {
        "case": "blind-upgrade-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "blind_upgrade_rejected",
        "expected_exit": 1,
        "setup": "blind-upgrade",
    },
    {
        "case": "prior-exposure-missing-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "prior_exposure_missing",
        "expected_exit": 1,
        "setup": "prior-exposure-missing",
    },
    {
        "case": "nested-null-omitted-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "original_nested_value_missing",
        "expected_exit": 1,
        "setup": "nested-null-omitted",
    },
    {
        "case": "nested-null-rewritten-red",
        "expected_id": "metadata_inconsistent",
        "expected_reason": "original_nested_not_null",
        "expected_exit": 1,
        "setup": "nested-null-rewritten",
    },
    {
        "case": "tamper-summary-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "summary_digest_mismatch",
        "expected_exit": 2,
        "setup": "tamper-summary",
    },
    {
        "case": "tamper-declared-before-kind-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "declared_digest_mismatch",
        "expected_exit": 2,
        "setup": "tamper-declared-wrong-kind",
    },
    {
        "case": "missing-companion-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_missing",
        "expected_exit": 2,
        "setup": "missing-companion",
    },
    {
        "case": "malformed-json-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_json_invalid",
        "expected_exit": 2,
        "setup": "malformed-json",
    },
    {
        "case": "duplicate-key-red",
        "expected_id": "input_unavailable",
        "expected_reason": "companion_json_invalid",
        "expected_exit": 2,
        "setup": "duplicate-key",
    },
    {
        "case": "missing-input-red",
        "expected_id": "input_unavailable",
        "expected_reason": "input_missing",
        "expected_exit": 2,
        "setup": "missing-input",
    },
    {
        "case": "path-escape-red",
        "expected_id": "input_unavailable",
        "expected_reason": "path_rejected",
        "expected_exit": 2,
        "setup": "path-escape",
    },
    {
        "case": "extra-input-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "companion_inputs_mismatch",
        "expected_exit": 2,
        "setup": "extra-input",
    },
    {
        "case": "missing-digest-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "companion_digest_invalid",
        "expected_exit": 2,
        "setup": "missing-digest",
    },
    {
        "case": "unpinned-digest-red",
        "expected_id": "snapshot_tampered",
        "expected_reason": "companion_digest_unpinned",
        "expected_exit": 2,
        "setup": "unpinned-digest",
    },
)


def _copy_pinned_inputs(fixture_root: Path) -> None:
    for name, rel, _digest in PINNED_INPUTS:
        source = LANE_ROOT / rel
        target = fixture_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
    rerun_source = LANE_ROOT / RERUN_SUMMARY_REL
    rerun_target = fixture_root / RERUN_SUMMARY_REL
    rerun_target.parent.mkdir(parents=True, exist_ok=True)
    rerun_target.write_bytes(rerun_source.read_bytes())


def _write_companion(fixture_root: Path, companion: dict) -> Path:
    path = fixture_root / DEFAULT_COMPANION_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(companion, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def _prepare_fixture(fixture_root: Path, setup: str) -> None:
    _copy_pinned_inputs(fixture_root)
    companion = build_companion()

    if setup == "missing-companion":
        return
    if setup == "malformed-json":
        path = fixture_root / DEFAULT_COMPANION_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not valid json\n", encoding="utf-8")
        return
    if setup == "duplicate-key":
        path = fixture_root / DEFAULT_COMPANION_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            '{"schema": "tameshi-witness-metadata/v1", '
            '"schema": "tameshi-witness-metadata/v1"}\n',
            encoding="utf-8",
        )
        return
    if setup == "nan-companion":
        path = fixture_root / DEFAULT_COMPANION_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"schema": NaN}\n', encoding="utf-8")
        return
    if setup == "non-object-companion":
        path = fixture_root / DEFAULT_COMPANION_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[]\n", encoding="utf-8")
        return
    if setup == "invalid-utf8-companion":
        path = fixture_root / DEFAULT_COMPANION_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\xff\xfe{")
        return

    if setup == "old-null":
        companion["declaration"]["kind"] = None
    elif setup == "expected-record-missing":
        del companion["expected"]
    elif setup == "rerun-scope-omitted":
        del companion["scope"]["uncovered_null_observations"]
    elif setup == "producer-checked-live":
        companion["producer"]["checked_live"] = True
    elif setup == "extra-blind-key":
        companion["declaration"]["preregistration"] = "blind"
    elif setup == "wrong-kind-short":
        companion["declaration"]["kind"] = "declared-witness mapping"
    elif setup == "wrong-kind-blind":
        companion["declaration"]["kind"] = "blind preregistration"
    elif setup == "absent-disclosure":
        del companion["declaration"]["disclosure"]
    elif setup == "disclosure-mismatch":
        companion["declaration"]["disclosure"] += " (rewritten)"
    elif setup == "blind-upgrade":
        companion["declaration"]["blind"] = True
    elif setup == "prior-exposure-missing":
        del companion["declaration"]["prior_exposure"]
    elif setup == "nested-null-omitted":
        del companion["original_nested"]["value"]
    elif setup == "nested-null-rewritten":
        companion["original_nested"]["value"] = EXPECTED_KIND
    elif setup == "path-escape":
        companion["frozen_declaration"]["summary"]["path"] = "../summary.json"
    elif setup == "extra-input":
        companion["frozen_declaration"]["extra"] = {
            "path": ".ufo/evidence/round-12/BashWitness/extra.json",
            "sha256": "0" * 64,
        }
    elif setup == "missing-digest":
        del companion["frozen_declaration"]["declared"]["sha256"]
    elif setup == "unpinned-digest":
        companion["frozen_declaration"]["declared"]["sha256"] = "0" * 64
    elif setup == "tamper-declared-wrong-kind":
        companion["declaration"]["kind"] = "blind preregistration"
    elif setup == "tamper-plus-companion-defect":
        companion["producer"]["checked_live"] = True
    elif setup == "wrong-schema":
        companion["schema"] = "not-the-schema"
    elif setup == "frozen-manifest-not-object":
        companion["frozen_declaration"] = []
    elif setup == "companion-path-mismatch":
        companion["frozen_declaration"]["summary"]["path"] = (
            ".ufo/evidence/round-12/BashWitness/other.json"
        )
    elif setup == "producer-missing":
        del companion["producer"]
    elif setup == "runner-mismatch":
        companion["historical_runner"]["sha256"] = "1" * 64
    elif setup == "frozen-flag-rewritten":
        companion["frozen_bytes_rewritten"] = True
    elif setup not in (
        "green",
        "tamper-summary",
        "missing-input",
        "tamper-rerun",
        "tamper-declaration",
        "symlink-input",
        "symlink-companion",
        "lane-root-missing",
    ):
        raise SystemExit(f"unknown selftest setup: {setup}")

    _write_companion(fixture_root, companion)

    if setup == "tamper-summary":
        summary = fixture_root / PINNED_BY_NAME["summary"][0]
        with summary.open("ab") as handle:
            handle.write(b" ")
    elif setup == "tamper-declared-wrong-kind":
        declared = fixture_root / PINNED_BY_NAME["declared"][0]
        with declared.open("ab") as handle:
            handle.write(b" ")
    elif setup == "tamper-rerun":
        rerun = fixture_root / RERUN_SUMMARY_REL
        with rerun.open("ab") as handle:
            handle.write(b" ")
    elif setup == "tamper-plus-companion-defect":
        rerun = fixture_root / RERUN_SUMMARY_REL
        with rerun.open("ab") as handle:
            handle.write(b" ")
    elif setup == "tamper-declaration":
        declaration_file = fixture_root / PINNED_BY_NAME["declaration"][0]
        with declaration_file.open("ab") as handle:
            handle.write(b" ")
    elif setup == "symlink-input":
        declared = fixture_root / PINNED_BY_NAME["declared"][0]
        declared.unlink()
        os.symlink(fixture_root / PINNED_BY_NAME["summary"][0], declared)
    elif setup == "symlink-companion":
        companion_path = fixture_root / DEFAULT_COMPANION_REL
        real_companion = companion_path.with_name("real-companion.json")
        companion_path.rename(real_companion)
        os.symlink(real_companion.name, companion_path)
    elif setup == "missing-input":
        (fixture_root / PINNED_BY_NAME["declared"][0]).unlink()


def run_selftest() -> int:
    # Frozen sources are read-only inputs to the fixtures; fail setup loudly
    # if the lane does not hold the pinned bytes.
    for name, rel, pinned_digest in PINNED_INPUTS:
        path = LANE_ROOT / rel
        try:
            actual = _sha256_bytes(path.read_bytes())
        except OSError as exc:
            print(f"SELFTEST: SETUP_FAIL {name} unreadable: {exc}")
            return 2
        if actual != pinned_digest:
            print(f"SELFTEST: SETUP_FAIL {name} digest {actual} != {pinned_digest}")
            return 2
    rerun_source = LANE_ROOT / RERUN_SUMMARY_REL
    try:
        rerun_actual = _sha256_bytes(rerun_source.read_bytes())
    except OSError as exc:
        print(f"SELFTEST: SETUP_FAIL rerun_summary unreadable: {exc}")
        return 2
    if rerun_actual != RERUN_SUMMARY_SHA256:
        print(
            "SELFTEST: SETUP_FAIL rerun_summary digest "
            f"{rerun_actual} != {RERUN_SUMMARY_SHA256}"
        )
        return 2

    temp_root = Path(tempfile.mkdtemp(prefix="witness-metadata-selftest-"))
    failures = 0
    try:
        tool = Path(__file__).resolve()
        for index, case in enumerate(SELFTEST_CASES, start=1):
            fixture_root = temp_root / f"{index:02d}-{case['case']}"
            fixture_root.mkdir(parents=True)
            _prepare_fixture(fixture_root, case["setup"])
            if case["setup"] == "lane-root-missing":
                shutil.rmtree(fixture_root)
            try:
                proc = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        str(tool),
                        "--check",
                        "--lane-root",
                        str(fixture_root),
                        "--json",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
            except subprocess.TimeoutExpired:
                print(
                    f"SELFTEST_CASE {case['case']} expected="
                    f"{case['expected_id']}/{case['expected_reason']}/"
                    f"{case['expected_exit']} observed=timeout FAIL"
                )
                failures += 1
                continue
            observed_id = observed_reason = "<unparsed>"
            observed_exit = proc.returncode
            try:
                payload = json.loads(proc.stdout.strip().splitlines()[-1])
                observed_id = payload.get("id", "<missing>")
                observed_reason = payload.get("reason", "<missing>")
                observed_exit = payload.get("exit", proc.returncode)
            except (ValueError, IndexError):
                pass
            ok = (
                proc.returncode == case["expected_exit"]
                and observed_exit == case["expected_exit"]
                and observed_id == case["expected_id"]
                and observed_reason == case["expected_reason"]
                and "Traceback" not in proc.stderr
            )
            status = "OK" if ok else "FAIL"
            print(
                f"SELFTEST_CASE {case['case']} expected="
                f"{case['expected_id']}/{case['expected_reason']}/"
                f"{case['expected_exit']} observed="
                f"{observed_id}/{observed_reason}/{observed_exit} exit="
                f"{proc.returncode} {status}"
            )
            if not ok:
                failures += 1
                if proc.stderr.strip():
                    print(f"SELFTEST_STDERR {case['case']}: {proc.stderr.strip()[:400]}")
                if proc.stdout.strip():
                    print(f"SELFTEST_STDOUT {case['case']}: {proc.stdout.strip()[:400]}")
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    # The frozen lane bytes must be unchanged by the selftest.
    for name, rel, pinned_digest in PINNED_INPUTS:
        path = LANE_ROOT / rel
        try:
            actual = _sha256_bytes(path.read_bytes())
        except OSError:
            actual = "<unreadable>"
        if actual != pinned_digest:
            print(f"SELFTEST: FROZEN_MUTATED {name} {actual}")
            failures += 1
    rerun_source = LANE_ROOT / RERUN_SUMMARY_REL
    try:
        rerun_actual = _sha256_bytes(rerun_source.read_bytes())
    except OSError:
        rerun_actual = "<unreadable>"
    if rerun_actual != RERUN_SUMMARY_SHA256:
        print(f"SELFTEST: FROZEN_MUTATED rerun_summary {rerun_actual}")
        failures += 1

    total = len(SELFTEST_CASES)
    if failures:
        print(f"SELFTEST: FAIL {total - failures}/{total}")
        return 1
    print(f"SELFTEST: PASS {total}/{total}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="witness-metadata.py",
        description=(
            "Bounded companion-metadata gate for the frozen round-12 "
            "BashWitness declaration."
        ),
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate the companion metadata")
    mode.add_argument("--selftest", action="store_true", help="run isolated CLI fixtures")
    mode.add_argument("--emit", action="store_true", help="print the companion object to stdout")
    parser.add_argument(
        "--lane-root",
        default=str(LANE_ROOT),
        help="lane root used to resolve companion-declared relative paths",
    )
    parser.add_argument(
        "--companion",
        default=None,
        help=(
            "companion path; relative paths resolve under --lane-root "
            f"(default: {DEFAULT_COMPANION_REL})"
        ),
    )
    parser.add_argument("--json", action="store_true", help="emit one JSON result object")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.emit:
        print(json.dumps(build_companion(), indent=2, ensure_ascii=False))
        return 0
    if args.selftest:
        return run_selftest()

    lane_root = Path(args.lane_root)
    if args.companion is None:
        companion_path = lane_root / DEFAULT_COMPANION_REL
    else:
        companion_path = Path(args.companion)
        if not companion_path.is_absolute():
            companion_path = lane_root / companion_path

    try:
        result = run_check(lane_root, companion_path)
    except Failure as failure:
        result = {
            "id": failure.verdict_id,
            "reason": failure.reason,
            "exit": failure.exit_code,
            "companion": str(companion_path),
            "detail": failure.detail,
        }
    except Exception as exc:  # fail closed, never traceback
        result = {
            "id": "input_unavailable",
            "reason": "unexpected_exception",
            "exit": 2,
            "companion": str(companion_path),
            "detail": f"{type(exc).__name__}: {exc}",
        }

    emit_result(result, args.json)
    return result["exit"]


if __name__ == "__main__":
    sys.exit(main())
