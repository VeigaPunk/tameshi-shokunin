#!/usr/bin/env python3
"""bash-witness-study.py — declared-witness classification of the pinned
bash-surface-census mutation leg (tameshi-shokunin, round 12, seat BashWitness).

What this tool does
-------------------
declare   materialize the pinned target from the kagi git object store, extract
          the embedded defect spec from tools/mutate-and-run.sh, and write the
          frozen declared-witness TSV (one row per defect: the selftest case
          labels that the mutation should turn red, or NONE) plus
          declaration.json carrying every input digest.  Refuses to overwrite an
          existing declared.tsv.
run       refuse unless declared.tsv matches its recorded digest, then execute
          the pinned mutation CLI sweep (tools/mutate-and-run.sh, all 10
          defects, suite `bash "$MUTANT" --selftest`) and classify every defect
          killed-on-witness / accidental / survived / inconclusive.  Refuses
          unless the runner exits 0/1, prints a terminal DONE/DEGRADED line, an
          anchored CONTROL: GREEN line, and a restore line whose before/after
          target digest equals the pinned target.  Writes summary.json
          (per-defect rows, classifier digest) and a full manifest.json over
          every evidence file.
count     recompute the retained sweep from results.tsv, the mutant artifacts
          and the raw case logs, compare every row/count/status with
          summary.json, and refuse a mismatch.  Prints recomputed rows only.
rerun     re-check digests, refuse on tamper, run a fresh sweep into
          rerun-<stamp>/ with its own summary.json, preserve the committed
          summary, extend the full manifest, and compare classifications with
          the committed summary.
check     require the full manifest and validate every committed digest plus
          exact file-set equality (unlisted, missing, unsafe and malformed
          entries refuse); a modified declared.tsv (or any other covered file)
          refuses with a named error before any classification.
selftest  hermetic fixtures for the parser, classifier, result table, manifest
          and summary tamper paths.

Exit codes: 0 ok/clean · 1 failed (tamper, mismatch, inconclusive) ·
            2 cannot evaluate (missing inputs, pin mismatch, runner SETUP) ·
            64 usage.

Classification rule (declared before the sweep)
-----------------------------------------------
* killed-on-witness — the mutant's run is red with the full selftest
  denominator (16 declared cases) and at least one pre-declared witness case
  failed.
* accidental — red with the full denominator and no pre-declared witness case
  failed (including every defect declared NONE).
* survived — green with the full denominator and zero failing cases.
* inconclusive — anything else: missing SELFTEST line, denominator != 16,
  ok+bad+skip != 16, skip labels other than the two expected verbs skips,
  skip set differing from the control's, runner verdict INCONCLUSIVE.
The declared total is 16; on a host without the-janitor on PATH the two verbs
cases are recorded as skip-case rows (14 exercised + 2 skipped) — skipped
checks are never counted as executed.

Disclosure — this is a declared-witness mapping, NOT a blind preregistration
---------------------------------------------------------------------------
The mapping below was authored from the pinned target's selftest and the
embedded spec, but the author had prior exposure to recorded aggregate outcomes
of this leg before declaring: the recorded kill-rate header of
tools/mutate-and-run.sh, the corpus/README.md coverage row for
mutation-case-kagi-census.md, the SOURCES.md S033 row, and the recorded
TABLE_BASH per-defect KILLED/SURVIVED entries (surfaced by a pin grep).  No
per-defect *witness* classification of this leg existed before this run; the
mapping is hashed before execution and is never rewritten after results.

Environment scrub: every child process drops inherited `GIT_*` variables, then
sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. The sweep
environment additionally removes THE_JANITOR_BIN, SQLITE3_BIN, CENSUS_BREAK,
DEEP and ONEPASSWORD_BROWSER_SUPPORT (each is read by the pinned gate and can
change behavior). The resolved `the-janitor`/`sqlite3` PATH facts are recorded
in summary.json, and a `the-janitor` found on PATH refuses the sweep so the
selftest cannot reach a real op/custody surface. REV_BASH must be an exact
40-hex git id and materialization runs `git show --end-of-options`.

Usage errors exit 64 (the probe contract), not argparse's default 2.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EVIDENCE_DEFAULT = REPO / ".ufo" / "evidence" / "round-12" / "BashWitness"
RUNNER = REPO / "tools" / "mutate-and-run.sh"
KAGI_DEFAULT = REPO.parent / "kagi-shokunin"
TARGET_GIT_PATH = "corpus/surface-census.sh"
TARGET_NAME = "pristine.sh"
SPEC_NAME = "bash-surface-census.spec"
DECLARED_NAME = "declared.tsv"
DECLARATION_NAME = "declaration.json"
SUMMARY_NAME = "summary.json"
MANIFEST_NAME = "manifest.json"
SWEEP_DIR = "sweep"
LABEL = "bash-surface-census"
SUITE = 'bash "$MUTANT" --selftest'
DECLARED_TOTAL = 16
EXPECTED_CASE_LABELS = (
    "clean", "mode-drift", "asset-gone", "runtime-absent", "undeclared-file",
    "crosscheck-disagree", "symlink-swap", "sqlite-magic",
    "sqlite-magic-prefix-only", "sqlite-unavailable", "required-table-gone",
    "row-floor", "malformed-row", "fused-shape-row", "verbs-sandboxed",
    "verbs-break-injection",
)
EXPECTED_SKIP_LABELS = ("verbs-sandboxed", "verbs-break-injection")
SCRUB_ENV = ("THE_JANITOR_BIN", "SQLITE3_BIN", "CENSUS_BREAK", "DEEP",
             "ONEPASSWORD_BROWSER_SUPPORT")
EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64

# ---------------------------------------------------------------------------
# declared witness mapping (frozen; authored from the pinned selftest + spec)
# ---------------------------------------------------------------------------
# Each row: defect id -> (witness case labels or None for NONE, rationale).
# Case labels are the selftest's `(ok|bad|skip)-case NN <name>` names.
DECLARED_WITNESSES = (
    ("B1", ("undeclared-file",),
     "verify_unlisted early-return flips to `-ne 0`, so the SURFACE UNLISTED "
     "sweep is skipped whenever scan dirs exist (pristine.sh:241). Only "
     "`undeclared-file` plants an undeclared child in a declared scan dir and "
     "asserts exit 1 + token SURFACE UNLISTED; the clean tree has no unlisted "
     "child, so no other case's pass condition depends on the sweep."),
    ("B2", ("clean", "runtime-absent"),
     "rows_min `-ge`->`-gt` (pristine.sh:435) breaks the equality boundary "
     "got==floor. The intact-db cases pin that boundary (part rows 1 vs floor "
     "1): `clean` (exit 0 + SURFACE OK) and `runtime-absent` (exit 0). "
     "`row-floor` exercises 0<1, which fails under both operators, so it "
     "cannot witness this change."),
    ("B3", ("crosscheck-disagree", "clean"),
     "crosscheck `!=`->`==` (pristine.sh:229) flags agreement instead of "
     "disagreement. `crosscheck-disagree` builds baseline 644 vs census 600 "
     "and asserts exit 1 + SURFACE CROSSCHECK (mutant passes silently); "
     "`clean` carries baseline 600 == census 600 and asserts exit 0 (mutant "
     "flags it). Both cases drive the mutated branch."),
    ("B4", ("symlink-swap",),
     "the symlink guard is deleted (pristine.sh:200-204), so the declared-exec "
     "symlink falls through to the live-kind check and prints SURFACE DIVERGED "
     "(live symlink) instead of SURFACE LINK. `symlink-swap` asserts exit 1 + "
     "token SURFACE LINK. No other case creates a symlink."),
    ("B5", None,
     "the exec-bit arm is deleted (pristine.sh:214-217). NONE: no selftest case "
     "creates a declared-exec path that is a regular file without the execute "
     "bit — the only exec path (.local/bin/the-janitor) is created 755, and "
     "`symlink-swap` is intercepted by the earlier symlink guard. Fixture-"
     "absent arm: no assertion can witness this mutation."),
    ("B6", ("clean", "runtime-absent"),
     "magic compare `head -c ${#value}+1` -> `${#value}` (pristine.sh:371) "
     "makes the 15-byte read no longer match the 16-byte expected file, so the "
     "positive magic path fails on the real sqlite header (`SQLite format "
     "3\\0`): `clean` and `runtime-absent` assert exit 0 there. Note "
     "`sqlite-magic-prefix-only` (the case built for the NUL contract) still "
     "passes under the mutant — a 15-byte read still differs from the 16-byte "
     "expected — so it cannot witness this change."),
    ("B7", ("sqlite-unavailable",),
     "N_UNVERIFIED += 2 (pristine.sh:405-406) changes only the summary count; "
     "the three sqlite-dependent shape rows print unverified=6 instead of 3. "
     "`sqlite-unavailable` is the only case asserting the DRIFT line token "
     "`unverified=3`."),
    ("B8", ("malformed-row", "fused-shape-row"),
     "die() exits 1 instead of 2 (pristine.sh:85). The two refusal cases that "
     "assert exit 2 go red: `malformed-row` (bad kind) and `fused-shape-row` "
     "(too many fields). Both route through die()."),
    ("B9", ("asset-gone", "runtime-absent"),
     "the missing-path class test flips `runtime`->`asset` (pristine.sh:191), "
     "swapping GONE (failure) and ABSENT (not a failure) for missing paths. "
     "`asset-gone` asserts exit 1 + SURFACE GONE for the missing asset (mutant "
     "prints ABSENT, exit 0); `runtime-absent` asserts exit 0 for the missing "
     "runtime file (mutant prints GONE, exit 1)."),
    ("B10", None,
     "the CLEAN summary's ok= argument becomes $N_ABSENT (pristine.sh:862). "
     "NONE: no selftest case asserts the CLEAN summary line's ok= field; the "
     "`clean` case's token SURFACE OK is matched by per-path SURFACE OK lines, "
     "which the mutation does not touch."),
)

DISCLOSURE = (
    "declared-witness mapping, not a blind preregistration: before declaring, "
    "the author had seen recorded aggregate outcomes of this leg — the "
    "recorded kill-rate header of tools/mutate-and-run.sh, the "
    "corpus/README.md coverage row for mutation-case-kagi-census.md, the "
    "SOURCES.md S033 row, and the recorded TABLE_BASH per-defect "
    "KILLED/SURVIVED entries surfaced by a pin grep. No per-defect witness "
    "classification of this leg existed before this run."
)

CASE_RE = re.compile(r"^(ok-case|bad-case|skip-case)\s+(\d+)\s+(\S+)")
FINAL_RE = re.compile(r"^SELFTEST: (PASS|FAIL) \((\d+)(?:/(\d+))? cases\)\s*$")
PIN_RE = re.compile(r"^(PIN_BASH)=([0-9a-f]{64})$", re.M)
REV_RE = re.compile(r"^(REV_BASH)=([0-9a-f]{40})$", re.M)
HEREDOC_RE = re.compile(r'^\s*cat >"\$d/bash-surface-census\.spec" <<\'EOT\'$')
SPEC_LINE_RE = re.compile(r"^@(defect|old|new)(?: (.*))?$")
UNESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}


class Cannot(Exception):
    """could-not-evaluate: missing input, pin mismatch, runner SETUP."""


class Fail(Exception):
    """definite negative finding: tamper, mismatch, inconclusive run."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot(f"unreadable {path}: {exc}") from exc


def read_text_lossy(path: Path) -> str:
    """Suite logs are target output; decode with replacement (never crash)."""
    try:
        return path.read_bytes().decode("utf-8", "replace")
    except OSError as exc:
        raise Cannot(f"unreadable {path}: {exc}") from exc


def utc_stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def unescape(text: str, where: str) -> str:
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        if i + 1 >= len(text):
            raise Cannot(f"{where}: trailing backslash in spec literal")
        nxt = text[i + 1]
        if nxt not in UNESCAPES:
            raise Cannot(f"{where}: unknown escape '\\{nxt}' in spec literal")
        out.append(UNESCAPES[nxt])
        i += 2
    return "".join(out)


def runner_pins(text: str) -> dict:
    pins = {}
    for pattern in (PIN_RE, REV_RE):
        pins.update({m.group(1): m.group(2) for m in pattern.finditer(text)})
    missing = [k for k in ("PIN_BASH", "REV_BASH") if k not in pins]
    if missing:
        raise Cannot(f"runner is missing pin constant(s): {', '.join(missing)}")
    return pins


def extract_spec(runner_text: str) -> str:
    lines = runner_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if HEREDOC_RE.match(line):
            start = i + 1
            break
    if start is None:
        raise Cannot("runner has no bash-surface-census.spec heredoc")
    for j in range(start, len(lines)):
        if lines[j] == "EOT":
            return "\n".join(lines[start:j]) + "\n"
    raise Cannot("bash-surface-census.spec heredoc is unterminated")


def parse_spec(text: str) -> list:
    defects, cur = [], None
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        m = SPEC_LINE_RE.match(raw)
        if not m:
            raise Cannot(f"spec line {lineno}: not a directive")
        kind, rest = m.group(1), m.group(2) or ""
        if kind == "defect":
            if "|" not in rest:
                raise Cannot(f"spec line {lineno}: @defect without ' | '")
            ident, desc = rest.split("|", 1)
            cur = {"id": ident.strip(), "desc": desc.strip(), "old": None, "new": None}
            defects.append(cur)
        else:
            if cur is None:
                raise Cannot(f"spec line {lineno}: @{kind} before any @defect")
            if cur[kind] is not None:
                raise Cannot(f"spec line {lineno}: duplicate @{kind} for {cur['id']}")
            cur[kind] = unescape(rest, f"spec line {lineno}")
    for d in defects:
        if d["old"] is None or d["new"] is None:
            raise Cannot(f"spec defect {d['id']}: missing @old or @new")
    ids = [d["id"] for d in defects]
    duplicates = sorted({ident for ident in ids if ids.count(ident) > 1})
    if duplicates:
        raise Cannot(f"spec duplicate defect id(s): {', '.join(duplicates)}")
    return defects


def spec_precheck(defects: list, target_text: str) -> dict:
    """Non-blocking sanity record; the runner's own count==1 gate is authoritative."""
    non_unique = []
    for d in defects:
        count = target_text.count(d["old"])
        if count != 1:
            non_unique.append({"id": d["id"], "count": count})
    return {
        "checked": True,
        "defects": len(defects),
        "all_unique": not non_unique,
        "non_unique": non_unique,
    }


def git_clean_env() -> dict:
    """Remove inherited Git settings, then pin safe configuration sources."""
    env = {name: value for name, value in os.environ.items()
           if not name.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    return env


def materialize_target(kagi: Path, rev: str) -> bytes:
    if not re.fullmatch(r"[0-9a-f]{40}", rev or ""):
        raise Cannot(f"revision is not an exact 40-hex git id: {rev!r}")
    if not (kagi / ".git").exists() and not (kagi / ".jj").exists():
        raise Cannot(f"kagi object store not found at {kagi}")
    proc = subprocess.run(
        ["git", "-C", str(kagi), "show", "--end-of-options",
         f"{rev}:{TARGET_GIT_PATH}"],
        capture_output=True, check=False, env=git_clean_env())
    if proc.returncode != 0:
        raise Cannot(f"git show {rev}:{TARGET_GIT_PATH} failed: "
                     f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout


def declared_rows() -> list:
    rows = []
    for ident, witness, rationale in DECLARED_WITNESSES:
        rows.append((ident, "NONE" if witness is None else ",".join(witness), rationale))
    return rows


def declared_tsv_text(meta: dict) -> str:
    lines = [
        "# bash-witness-study — declared witness mapping (frozen before the sweep)",
        f"# seat: BashWitness · round: round-12 · leg: {LABEL} (pinned)",
        f"# target: {TARGET_NAME} sha256={meta['target_sha256']} "
        f"(kagi-shokunin@{meta['rev']} {TARGET_GIT_PATH})",
        f"# spec:   {SPEC_NAME} sha256={meta['spec_sha256']} "
        f"(heredoc of tools/mutate-and-run.sh sha256={meta['runner_sha256']})",
        f"# suite:  {SUITE} · declared total {DECLARED_TOTAL} cases "
        f"(2 verbs cases skip when the-janitor is absent)",
        "# rule: killed-on-witness iff a full-denominator red run fails >=1 declared",
        "#       case; accidental iff red with none; survived iff green with the",
        "#       full denominator; inconclusive otherwise.",
        "# kind: declared-witness mapping, NOT a blind preregistration (disclosure",
        "#       in declaration.json and the evidence README).",
        "# fields: defect<TAB>witness<TAB>rationale   (witness = comma list or NONE)",
    ]
    for ident, witness, rationale in declared_rows():
        lines.append(f"{ident}\t{witness}\t{rationale}")
    return "\n".join(lines) + "\n"


def parse_declared_tsv(text: str) -> dict:
    mapping = {}
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw or raw.startswith("#"):
            continue
        fields = raw.split("\t")
        if len(fields) != 3:
            raise Cannot(f"declared.tsv line {lineno}: expected 3 tab fields")
        ident, witness, rationale = fields
        if witness == "NONE":
            mapping[ident] = None
        else:
            mapping[ident] = tuple(w.strip() for w in witness.split(",") if w.strip())
        if not rationale.strip():
            raise Cannot(f"declared.tsv line {lineno}: empty rationale")
    if not mapping:
        raise Cannot("declared.tsv has no rows")
    return mapping


def declared_expected() -> dict:
    return {ident: (tuple(witness) if witness is not None else None)
            for ident, witness, _ in DECLARED_WITNESSES}


# ------------------------------------------------------------------ classifier

def parse_case_lines(log_text: str) -> dict:
    ok, bad, skip = [], [], []
    numbers = []
    total = failures = None
    selftest_line = None
    last_nonempty = None
    selftest_at = None
    for index, raw in enumerate(log_text.splitlines()):
        if raw.strip():
            last_nonempty = index
        m = CASE_RE.match(raw)
        if m:
            kind, num, name = m.group(1), int(m.group(2)), m.group(3)
            {"ok-case": ok, "bad-case": bad, "skip-case": skip}[kind].append(name)
            numbers.append(num)
            continue
        m = FINAL_RE.match(raw)
        if m:
            selftest_line = raw.strip()
            selftest_at = index
            if m.group(1) == "PASS":
                total, failures = int(m.group(2)), 0
            else:
                failures = int(m.group(2))
                total = int(m.group(3)) if m.group(3) is not None else None
    return {
        "ok": ok, "bad": bad, "skip": skip, "numbers": numbers,
        "total": total, "failures": failures, "selftest_line": selftest_line,
        "selftest_terminal": selftest_at is not None and selftest_at == last_nonempty,
    }


def run_problems(runinfo: dict, control: dict) -> list:
    """Completeness problems shared by the control and every mutant run."""
    reasons = []
    if runinfo["selftest_line"] is None:
        reasons.append("no-selftest-line")
    elif not runinfo["selftest_terminal"]:
        reasons.append("selftest-line-not-terminal")
    if runinfo["total"] != DECLARED_TOTAL:
        reasons.append(f"denominator={runinfo['total']}!=declared-{DECLARED_TOTAL}")
    if runinfo["total"] is not None:
        accounted = len(runinfo["ok"]) + len(runinfo["bad"]) + len(runinfo["skip"])
        if accounted != runinfo["total"]:
            reasons.append(f"case-accounting={accounted}!=total-{runinfo['total']}")
    if runinfo["total"] is not None:
        if sorted(runinfo["numbers"]) != list(range(1, runinfo["total"] + 1)):
            reasons.append("incomplete-case-numbering")
    if runinfo["skip"] and sorted(runinfo["skip"]) != sorted(EXPECTED_SKIP_LABELS):
        reasons.append("unexpected-skip-label:" + ",".join(runinfo["skip"]))
    if sorted(runinfo["skip"]) != sorted(control["skip"]):
        reasons.append("skip-set-differs-from-control")
    observed = runinfo["ok"] + runinfo["bad"] + runinfo["skip"]
    duplicates = sorted({label for label in observed if observed.count(label) > 1})
    if duplicates:
        reasons.append("duplicate-case-label:" + ",".join(duplicates))
    if set(observed) != set(EXPECTED_CASE_LABELS):
        missing = sorted(set(EXPECTED_CASE_LABELS) - set(observed))
        extra = sorted(set(observed) - set(EXPECTED_CASE_LABELS))
        reasons.append("catalog-mismatch:missing=" + (",".join(missing) or "-")
                       + ";extra=" + (",".join(extra) or "-"))
    if runinfo["failures"] is not None:
        if runinfo["failures"] != len(runinfo["bad"]):
            reasons.append(f"failure-count={runinfo['failures']}"
                           f"!=bad-case-count={len(runinfo['bad'])}")
        exit_code = runinfo.get("exit")
        if exit_code is not None and (runinfo["failures"] > 0) != (exit_code != 0):
            reasons.append(f"exit={exit_code} inconsistent with "
                           f"failures={runinfo['failures']}")
    return reasons


def classify(defect_id, verdict, runinfo, control, witnesses) -> tuple:
    reasons = run_problems(runinfo, control)
    if reasons:
        return "inconclusive", reasons
    if verdict == "SURVIVED":
        if runinfo["failures"] != 0 or runinfo["bad"]:
            return "inconclusive", ["green-with-failing-cases"]
        return "survived", []
    if verdict == "INCONCLUSIVE":
        return "inconclusive", ["runner-inconclusive"]
    if verdict != "KILLED":
        return "inconclusive", [f"unknown-verdict:{verdict}"]
    # verdict == KILLED: red with the full denominator
    if not runinfo["bad"]:
        return "inconclusive", ["red-without-failing-cases"]
    if witnesses is None:
        return "accidental", ["declared-NONE"]
    hit = [label for label in witnesses if label in runinfo["bad"]]
    if hit:
        return "killed-on-witness", []
    return "accidental", ["no-declared-witness-failed"]


# -------------------------------------------------------------------- helpers

def load_declaration(evidence: Path) -> dict:
    path = evidence / DECLARATION_NAME
    if not path.is_file():
        raise Cannot(f"missing {path} — run `declare` first")
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise Cannot(f"unreadable {path}: {exc}") from exc


def verify_declared_digest(evidence: Path, declaration: dict) -> str:
    """Named refusal before any classification when declared.tsv was modified."""
    path = evidence / DECLARED_NAME
    if not path.is_file():
        raise Cannot(f"missing {path}")
    actual = sha256_file(path)
    committed = declaration.get("declared", {}).get("sha256")
    if actual != committed:
        raise Fail(f"TAMPER {DECLARED_NAME} sha256={actual} committed={committed}")
    return actual


def ensure_target_and_spec(evidence: Path, declaration: dict, kagi: Path) -> dict:
    inputs = declaration.get("inputs", {})
    target = evidence / TARGET_NAME
    spec = evidence / SPEC_NAME
    facts = {}

    expected_target = inputs.get("target", {}).get("sha256")
    rev = inputs.get("target", {}).get("rev")
    if target.is_file():
        actual = sha256_file(target)
        if actual != expected_target:
            raise Fail(f"TAMPER {TARGET_NAME} sha256={actual} committed={expected_target}")
    else:
        if not rev:
            raise Cannot(f"missing {TARGET_NAME} and no revision recorded")
        data = materialize_target(kagi, rev)
        actual = sha256_bytes(data)
        if actual != expected_target:
            raise Fail(f"materialized target sha256={actual} != committed={expected_target}")
        target.write_bytes(data)
    facts["target_sha256"] = actual

    expected_spec = inputs.get("spec", {}).get("sha256")
    if spec.is_file():
        actual = sha256_file(spec)
        if actual != expected_spec:
            raise Fail(f"TAMPER {SPEC_NAME} sha256={actual} committed={expected_spec}")
    else:
        actual = sha256_bytes(extract_spec(read_text(RUNNER)).encode("utf-8"))
        if actual != expected_spec:
            raise Fail(f"re-extracted spec sha256={actual} != committed={expected_spec}")
        spec.write_bytes(extract_spec(read_text(RUNNER)).encode("utf-8"))
    facts["spec_sha256"] = actual

    runner_sha = sha256_file(RUNNER)
    committed_runner = inputs.get("runner", {}).get("sha256")
    if runner_sha != committed_runner:
        raise Cannot(f"runner-drift tools/mutate-and-run.sh sha256={runner_sha} "
                     f"committed={committed_runner}")
    facts["runner_sha256"] = runner_sha

    pins = runner_pins(read_text(RUNNER))
    if pins["PIN_BASH"] != expected_target:
        raise Cannot(f"pin-mismatch PIN_BASH={pins['PIN_BASH']} "
                     f"declared-target={expected_target}")
    facts["pin_bash"] = pins["PIN_BASH"]
    facts["rev_bash"] = pins["REV_BASH"]
    return facts


def sweep_env() -> dict:
    env = git_clean_env()
    for name in SCRUB_ENV:
        env.pop(name, None)
    return env


def env_facts() -> dict:
    return {
        "scrubbed": ["GIT_*", *SCRUB_ENV],
        "the_janitor_on_path": shutil.which("the-janitor"),
        "sqlite3_on_path": shutil.which("sqlite3"),
        "path": os.environ.get("PATH", ""),
    }


def run_sweep(evidence: Path, rundir: Path, timeout: int, tail: int) -> dict:
    janitor = shutil.which("the-janitor")
    if janitor is not None:
        raise Cannot(f"the-janitor is on PATH ({janitor}) — refusing to run real "
                     f"op/custody probes; run on a host without it")
    rundir.mkdir(parents=True, exist_ok=False)
    argv = [
        "bash", str(RUNNER),
        "--target", str(evidence / TARGET_NAME),
        "--defects", str(evidence / SPEC_NAME),
        "--suite", SUITE,
        "--workdir", str(rundir),
        "--label", LABEL,
        "--timeout", str(timeout),
        "--tail", str(tail),
    ]
    proc = subprocess.run(argv, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env=sweep_env(), check=False)
    log = proc.stdout.decode("utf-8", "replace")
    (rundir / "cli.log").write_text(log, encoding="utf-8")
    (rundir / "cli.exit").write_text(f"{proc.returncode}\n", encoding="utf-8")
    return {
        "argv": argv,
        "exit": proc.returncode,
        "cli_log": f"{rundir.name}/cli.log",
        "cli_log_sha256": sha256_bytes(log.encode("utf-8")),
        "control_green": re.search(r"^CONTROL: GREEN ", log, re.M) is not None,
        "restore_ok": re.search(r"^MUTATE_RESTORE: OK ", log, re.M) is not None,
        "restore_line": next((l for l in log.splitlines()
                              if l.startswith("MUTATE_RESTORE: ")), None),
        "done_line": next((l for l in log.splitlines()
                           if l.startswith("MUTATE: ")), None),
    }


def collect_results(rundir: Path, declared: dict, control: dict) -> tuple:
    results = rundir / "results.tsv"
    if not results.is_file():
        raise Cannot(f"missing {results} — sweep did not produce a results table")
    lines = read_text_lossy(results).splitlines()
    header = "id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc"
    if not lines or lines[0] != header:
        raise Cannot(f"{results}: unexpected header "
                     f"{lines[0] if lines else '<empty>'!r}")
    # control_record keeps the report-facing `skip_labels`; run_problems reads
    # the normalized `skip` view (same shape as parse_case_lines output).
    control = {"skip": control.get("skip", control.get("skip_labels", []))}
    known = [d[0] for d in DECLARED_WITNESSES]
    if set(declared) != set(known):
        raise Cannot("declared.tsv rows differ from the frozen DECLARED_WITNESSES ids")
    rows, seen = [], set()
    for lineno, raw in enumerate(lines, 1):
        if lineno == 1 or not raw.strip():
            continue
        fields = raw.split("\t")
        if len(fields) != 6:
            raise Cannot(f"results.tsv line {lineno}: expected 6 tab fields")
        ident, verdict, exit_code, dur_ms, mutant_sha, desc = fields
        if ident in seen:
            raise Cannot(f"results.tsv duplicate defect id {ident}")
        if ident not in known:
            raise Cannot(f"results.tsv unknown defect id {ident}")
        if ident not in declared:
            raise Cannot(f"declared.tsv has no row for defect {ident}")
        try:
            exit_int, dur_int = int(exit_code), int(dur_ms)
        except ValueError as exc:
            raise Cannot(f"results.tsv line {lineno}: non-integer field: {exc}") from exc
        expected_verdict = ("SURVIVED" if exit_int == 0 else
                            "INCONCLUSIVE" if exit_int in (124, 126, 127) else "KILLED")
        if verdict != expected_verdict:
            raise Fail(f"RESULTS {ident} verdict={verdict} but exit={exit_int} "
                       f"implies {expected_verdict}")
        mutant_path = rundir / f"mutant-{ident}.{TARGET_NAME}"
        if not mutant_path.is_file():
            raise Cannot(f"missing mutant artifact {mutant_path}")
        actual_mutant_sha = sha256_file(mutant_path)
        if actual_mutant_sha != mutant_sha:
            raise Fail(f"MUTANT {ident} sha256={actual_mutant_sha} "
                       f"results.tsv={mutant_sha}")
        log_path = rundir / "evidence" / f"{ident}.out"
        if not log_path.is_file():
            raise Cannot(f"missing raw log {log_path}")
        info = parse_case_lines(read_text_lossy(log_path))
        info["exit"] = exit_int
        witnesses = declared.get(ident)
        classification, reasons = classify(ident, verdict, info, control, witnesses)
        rows.append({
            "defect": ident,
            "desc": desc,
            "runner_verdict": verdict,
            "exit": exit_int,
            "duration_ms": dur_int,
            "mutant_sha256": mutant_sha,
            "declared_witness": list(witnesses) if witnesses else [],
            "declared_witness_none": witnesses is None,
            "failing_labels": info["bad"],
            "ok_labels": info["ok"],
            "skipped_labels": info["skip"],
            "denominator": info["total"],
            "failures": info["failures"],
            "selftest_line": info["selftest_line"],
            "exercised": len(info["ok"]) + len(info["bad"]),
            "skipped": len(info["skip"]),
            "classification": classification,
            "classification_reasons": reasons,
            "raw_log": f"{rundir.name}/evidence/{ident}.out",
            "raw_log_sha256": sha256_file(log_path),
        })
        seen.add(ident)
    missing = [ident for ident in known if ident not in seen]
    if missing:
        raise Cannot(f"results.tsv lacks declared defect(s): {', '.join(missing)}")
    if len(rows) != len(known):
        raise Cannot(f"results.tsv has {len(rows)} rows, expected {len(known)}")
    return rows, seen


def control_record(rundir: Path) -> dict:
    path = rundir / "evidence" / "control.out"
    if not path.is_file():
        raise Cannot(f"missing control log {path}")
    info = parse_case_lines(read_text_lossy(path))
    return {
        "exit": 0,
        "denominator": info["total"],
        "failures": info["failures"],
        "exercised": len(info["ok"]) + len(info["bad"]),
        "skipped": len(info["skip"]),
        "skip_labels": info["skip"],
        "ok_labels": info["ok"],
        "failing_labels": info["bad"],
        "numbers": info["numbers"],
        "selftest_line": info["selftest_line"],
        "selftest_terminal": info["selftest_terminal"],
        "raw_log": f"{rundir.name}/evidence/control.out",
        "raw_log_sha256": sha256_file(path),
    }


def control_problems(control: dict) -> list:
    view = {
        "ok": control["ok_labels"], "bad": control["failing_labels"],
        "skip": control["skip_labels"], "numbers": control["numbers"],
        "total": control["denominator"], "failures": control["failures"],
        "exit": control["exit"],
        "selftest_line": control["selftest_line"],
        "selftest_terminal": control["selftest_terminal"],
    }
    return run_problems(view, view)


def cannot_counts() -> dict:
    ids = [d[0] for d in DECLARED_WITNESSES]
    return {
        "killed_on_witness": 0, "accidental": 0, "survived": 0,
        "inconclusive": len(ids), "total": len(ids), "witness_classified": 0,
        "declared_none": [d[0] for d in DECLARED_WITNESSES if d[1] is None],
        "unresolved": ids,
    }


def counts(rows: list) -> dict:
    tally = {"killed_on_witness": 0, "accidental": 0, "survived": 0, "inconclusive": 0}
    for row in rows:
        tally[row["classification"].replace("-", "_")] += 1
    declared_none = [r["defect"] for r in rows if r["declared_witness_none"]]
    unresolved = [r["defect"] for r in rows if r["classification"] == "inconclusive"]
    tally["total"] = len(rows)
    tally["witness_classified"] = (tally["killed_on_witness"] + tally["accidental"]
                                   + tally["survived"])
    tally["declared_none"] = declared_none
    tally["unresolved"] = unresolved
    return tally


def write_json(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def build_summary(evidence: Path, declaration: dict, declared_sha: str, facts: dict,
                  sweep: dict, control: dict, rows: list, status: str) -> dict:
    return {
        "study": "bash-witness-study",
        "seat": "BashWitness",
        "round": "round-12",
        "leg": LABEL,
        "generated_at": utc_stamp(),
        "status": status,
        "tool": {
            "path": str(Path(__file__).resolve()),
            "sha256": sha256_file(Path(__file__).resolve()),
        },
        "declaration": {
            "path": DECLARED_NAME,
            "sha256": declared_sha,
            "kind": declaration.get("kind"),
            "disclosure": declaration.get("disclosure"),
        },
        "inputs": declaration.get("inputs"),
        "suite": {
            "command": SUITE,
            "declared_total": DECLARED_TOTAL,
            "expected_skip_labels": list(EXPECTED_SKIP_LABELS),
        },
        "environment": env_facts(),
        "sweep": sweep,
        "control": control,
        "rows": rows,
        "counts": counts(rows),
        "classification_rule": (
            "killed-on-witness: full-denominator red with >=1 declared case failed; "
            "accidental: full-denominator red with none; survived: full-denominator "
            "green with zero failures; inconclusive: missing/odd denominator, "
            "unexpected or control-divergent skip labels, runner INCONCLUSIVE"
        ),
        "facts": facts,
    }


def manifest_files(root: Path) -> list:
    """Every regular file under root except the manifest itself and temp writes."""
    names = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel == MANIFEST_NAME or rel.endswith(".tmp"):
            continue
        names.append(rel)
    return names


def write_manifest(root: Path) -> dict:
    covered = manifest_files(root)
    manifest = {
        "created_at": utc_stamp(),
        "files": {name: sha256_file(root / name) for name in covered},
    }
    write_json(root / MANIFEST_NAME, manifest)
    return manifest


# ------------------------------------------------------------------- commands

def cmd_declare(args) -> int:
    evidence = Path(args.evidence)
    evidence.mkdir(parents=True, exist_ok=True)
    if (evidence / DECLARED_NAME).exists():
        raise Fail(f"{DECLARED_NAME} already exists — declarations are frozen; "
                   f"re-declaring requires a fresh evidence directory")
    runner_text = read_text(RUNNER)
    pins = runner_pins(runner_text)
    spec_text = extract_spec(runner_text)
    defects = parse_spec(spec_text)
    ids = [d["id"] for d in defects]
    if len(defects) != len(DECLARED_WITNESSES):
        raise Fail(f"spec has {len(defects)} defects, declaration has "
                   f"{len(DECLARED_WITNESSES)}")
    if ids != [d[0] for d in DECLARED_WITNESSES]:
        raise Fail(f"spec ids {ids} != declared ids "
                   f"{[d[0] for d in DECLARED_WITNESSES]}")

    data = materialize_target(Path(args.kagi), pins["REV_BASH"])
    target_sha = sha256_bytes(data)
    if target_sha != pins["PIN_BASH"]:
        raise Fail(f"materialized target sha256={target_sha} != PIN_BASH={pins['PIN_BASH']}")
    (evidence / TARGET_NAME).write_bytes(data)
    (evidence / SPEC_NAME).write_text(spec_text, encoding="utf-8")

    spec_sha = sha256_bytes(spec_text.encode("utf-8"))
    runner_sha = sha256_file(RUNNER)
    precheck = spec_precheck(defects, data.decode("utf-8"))
    meta = {"target_sha256": target_sha, "spec_sha256": spec_sha,
            "runner_sha256": runner_sha, "rev": pins["REV_BASH"]}
    tsv = declared_tsv_text(meta)
    (evidence / DECLARED_NAME).write_text(tsv, encoding="utf-8")
    declared_sha = sha256_bytes(tsv.encode("utf-8"))

    declaration = {
        "study": "bash-witness-study",
        "seat": "BashWitness",
        "round": "round-12",
        "created_at": utc_stamp(),
        "kind": "declared-witness mapping (not a blind preregistration)",
        "disclosure": DISCLOSURE,
        "declared": {
            "path": DECLARED_NAME,
            "sha256": declared_sha,
            "rows": len(DECLARED_WITNESSES),
            "none_rows": [d[0] for d in DECLARED_WITNESSES if d[1] is None],
        },
        "inputs": {
            "target": {
                "path": TARGET_NAME,
                "sha256": target_sha,
                "source": f"git -C {Path(args.kagi)} show {pins['REV_BASH']}:{TARGET_GIT_PATH}",
                "rev": pins["REV_BASH"],
                "pin": pins["PIN_BASH"],
            },
            "spec": {
                "path": SPEC_NAME,
                "sha256": spec_sha,
                "source": f"heredoc of {RUNNER} (lines around the "
                          f"bash-surface-census.spec marker), defects={len(defects)}",
                "defects": ids,
            },
            "runner": {"path": str(RUNNER), "sha256": runner_sha},
            "suite": {"command": SUITE, "declared_total": DECLARED_TOTAL,
                      "expected_skip_labels": list(EXPECTED_SKIP_LABELS)},
        },
        "spec_precheck": precheck,
        "environment_at_declare": env_facts(),
    }
    write_json(evidence / DECLARATION_NAME, declaration)
    print(f"WITNESS_DECLARE: wrote {evidence / DECLARED_NAME}")
    print(f"WITNESS_DECLARE: declared.tsv sha256={declared_sha} rows={len(DECLARED_WITNESSES)}")
    print(f"WITNESS_DECLARE: target sha256={target_sha} (pin {pins['PIN_BASH']})")
    print(f"WITNESS_DECLARE: spec sha256={spec_sha} defects={len(defects)}")
    print(f"WITNESS_DECLARE: runner sha256={runner_sha}")
    print(f"WITNESS_DECLARE: spec precheck all_unique={precheck['all_unique']} "
          f"non_unique={precheck['non_unique']}")
    print("WITNESS_DECLARE: declaration.json sha256="
          f"{sha256_file(evidence / DECLARATION_NAME)}")
    return EXIT_OK


def _prepare(args) -> tuple:
    evidence = Path(args.evidence)
    declaration = load_declaration(evidence)
    declared_sha = verify_declared_digest(evidence, declaration)
    declared = parse_declared_tsv(read_text(evidence / DECLARED_NAME))
    facts = ensure_target_and_spec(evidence, declaration, Path(args.kagi))
    return evidence, declaration, declared_sha, declared, facts


def _cannot_summary(evidence: Path, declaration: dict, declared_sha: str, facts: dict,
                    sweep: dict, control: dict, problems: list, note: str,
                    outdir: Path | None = None) -> int:
    outdir = outdir or evidence
    summary = build_summary(evidence, declaration, declared_sha, facts, sweep, control,
                            [], "could-not-evaluate")
    summary["counts"] = cannot_counts()
    summary["unresolved_reasons"] = problems
    write_json(outdir / SUMMARY_NAME, summary)
    write_manifest(outdir)
    print(f"WITNESS_RUN: could-not-evaluate — {note}: {', '.join(problems)}")
    print(f"WITNESS_RUN: summary {outdir / SUMMARY_NAME}")
    return EXIT_CANNOT


def _execute_sweep(evidence: Path, declaration: dict, declared_sha: str, declared: dict,
                   facts: dict, rundir: Path, args,
                   outdir: Path | None = None) -> int:
    outdir = outdir or evidence
    sweep = run_sweep(evidence, rundir, args.timeout, args.tail)
    if sweep["exit"] not in (0, 1):
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               {"exit": sweep["exit"], "status": "runner-refused"},
                               [f"runner-exit={sweep['exit']}"],
                               "runner did not complete (setup/usage refusal)",
                               outdir=outdir)
    done = sweep.get("done_line") or ""
    if not (done.startswith("MUTATE: DONE ") or done.startswith("MUTATE: DEGRADED ")):
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               {"exit": sweep["exit"], "status": "done-line-missing"},
                               ["done-line-missing"],
                               f"runner verdict line missing: {done or '<none>'}",
                               outdir=outdir)
    if (sweep["exit"] == 0) != done.startswith("MUTATE: DONE "):
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               {"exit": sweep["exit"], "status": "done-line-exit-mismatch"},
                               ["done-line-exit-mismatch"],
                               f"exit={sweep['exit']} with {done}", outdir=outdir)
    if not sweep["control_green"]:
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               {"exit": None, "status": "control-not-green"},
                               ["control-not-green"], "control not green",
                               outdir=outdir)
    control = control_record(rundir)
    problems = control_problems(control)
    if problems:
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               control, problems, "control incomplete", outdir=outdir)
    expected_restore = (f"MUTATE_RESTORE: OK (target-sha256 "
                        f"before={facts['target_sha256']} "
                        f"after={facts['target_sha256']} ")
    restore = sweep.get("restore_line") or ""
    if not restore.startswith(expected_restore):
        return _cannot_summary(evidence, declaration, declared_sha, facts, sweep,
                               control, ["restore-line-mismatch"],
                               f"restore proof missing/mismatched: "
                               f"{restore or '<none>'}", outdir=outdir)
    rows, _ = collect_results(rundir, declared, control)
    status = "degraded" if any(r["classification"] == "inconclusive" for r in rows) else "complete"
    summary = build_summary(evidence, declaration, declared_sha, facts, sweep, control,
                            rows, status)
    write_json(outdir / SUMMARY_NAME, summary)
    write_manifest(outdir)
    tally = summary["counts"]
    print(f"WITNESS_RUN: {status} — killed_on_witness={tally['killed_on_witness']} "
          f"accidental={tally['accidental']} survived={tally['survived']} "
          f"inconclusive={tally['inconclusive']} total={tally['total']}")
    print(f"WITNESS_RUN: control denominator={control['denominator']} "
          f"exercised={control['exercised']} skipped={control['skipped']}")
    print(f"WITNESS_RUN: summary {outdir / SUMMARY_NAME}")
    return EXIT_FAIL if status == "degraded" else EXIT_OK


def cmd_run(args) -> int:
    evidence, declaration, declared_sha, declared, facts = _prepare(args)
    rundir = evidence / SWEEP_DIR
    if rundir.exists():
        raise Fail(f"{rundir} exists — use `rerun` for a fresh sweep")
    return _execute_sweep(evidence, declaration, declared_sha, declared, facts, rundir, args)


def cmd_rerun(args) -> int:
    evidence, declaration, declared_sha, declared, facts = _prepare(args)
    committed_path = evidence / SUMMARY_NAME
    prior = json.loads(read_text(committed_path)) if committed_path.is_file() else None
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    rundir = evidence / f"rerun-{stamp}"
    if rundir.exists():
        raise Fail(f"{rundir} exists")
    rc = _execute_sweep(evidence, declaration, declared_sha, declared, facts, rundir,
                        args, outdir=rundir)
    fresh_path = rundir / SUMMARY_NAME
    if not fresh_path.is_file():
        print("WITNESS_RERUN: no fresh summary; committed summary preserved")
        return rc
    # The rerun artifacts extend the evidence set; re-anchor the full manifest.
    write_manifest(evidence)
    fresh = json.loads(read_text(fresh_path))
    print(f"WITNESS_RERUN: committed summary preserved at {committed_path}")
    if prior is None:
        print("WITNESS_RERUN: no committed summary to compare; fresh sweep retained")
        return rc
    prior_map = {r["defect"]: r["classification"] for r in prior.get("rows", [])}
    fresh_map = {r["defect"]: r["classification"] for r in fresh.get("rows", [])}
    domains = sorted(set(prior_map) | set(fresh_map))
    agree = [d for d in domains if prior_map.get(d) == fresh_map.get(d)]
    deviations = [d for d in domains if prior_map.get(d) != fresh_map.get(d)]
    print(f"WITNESS_RERUN: agreement {len(agree)}/{len(domains)} rows; "
          f"deviations={deviations or 'none'}")
    if deviations and rc == EXIT_OK:
        rc = EXIT_FAIL
    return rc


def cmd_count(args) -> int:
    evidence = Path(args.evidence)
    declaration = load_declaration(evidence)
    declared_sha = verify_declared_digest(evidence, declaration)
    declared = parse_declared_tsv(read_text(evidence / DECLARED_NAME))
    if declared != declared_expected():
        raise Fail("DECLARED mapping differs from the frozen DECLARED_WITNESSES rows")
    summary_path = evidence / SUMMARY_NAME
    if not summary_path.is_file():
        raise Cannot(f"missing {summary_path} — run the sweep first")
    try:
        summary = json.loads(read_text(summary_path))
    except json.JSONDecodeError as exc:
        raise Cannot(f"unreadable {summary_path}: {exc}") from exc
    if summary.get("declaration", {}).get("sha256") != declared_sha:
        raise Fail(f"TAMPER {SUMMARY_NAME} declaration-linkage "
                   f"sha256={summary.get('declaration', {}).get('sha256')} "
                   f"declared={declared_sha}")
    status = summary.get("status")
    if status == "could-not-evaluate":
        reasons = summary.get("unresolved_reasons", [])
        print(f"count\tcould-not-evaluate\t{', '.join(reasons) or '-'}")
        return EXIT_CANNOT
    rundir = evidence / SWEEP_DIR
    control = control_record(rundir)
    problems = control_problems(control)
    if problems:
        raise Cannot("control incomplete: " + ", ".join(problems))
    rows, _ = collect_results(rundir, declared, control)
    stored_rows = {r.get("defect"): r for r in summary.get("rows", [])}
    fresh_rows = {r["defect"]: r for r in rows}
    if set(stored_rows) != set(fresh_rows):
        raise Fail(f"COUNT summary/raw mismatch row ids: stored={sorted(stored_rows)} "
                   f"recomputed={sorted(fresh_rows)}")
    compare = ("runner_verdict", "exit", "duration_ms", "mutant_sha256",
               "declared_witness", "declared_witness_none", "failing_labels",
               "ok_labels", "skipped_labels", "denominator", "failures",
               "selftest_line", "exercised", "skipped", "classification",
               "classification_reasons", "raw_log", "raw_log_sha256")
    for ident in sorted(fresh_rows):
        for key in compare:
            stored = stored_rows[ident].get(key)
            fresh = fresh_rows[ident].get(key)
            if stored != fresh:
                raise Fail(f"COUNT summary/raw mismatch {ident}.{key}: "
                           f"stored={stored!r} recomputed={fresh!r}")
    tally = counts(rows)
    stored_counts = summary.get("counts", {})
    for key in ("killed_on_witness", "accidental", "survived", "inconclusive",
                "total", "witness_classified", "declared_none", "unresolved"):
        if stored_counts.get(key) != tally[key]:
            raise Fail(f"COUNT summary/raw mismatch counts.{key}: "
                       f"stored={stored_counts.get(key)!r} recomputed={tally[key]!r}")
    expected_status = "degraded" if tally["unresolved"] else "complete"
    if status != expected_status:
        raise Fail(f"COUNT summary/raw mismatch status: stored={status!r} "
                   f"recomputed={expected_status!r}")
    print(f"declared\t{declared_sha}\t{evidence / DECLARED_NAME}")
    print(f"control\texit={control['exit']}\tdenominator={control['denominator']}"
          f"\texercised={control['exercised']}\tskipped={control['skipped']}"
          f"\tskip={','.join(control['skip_labels']) or '-'}")
    for row in rows:
        declared_w = ",".join(row["declared_witness"]) if row["declared_witness"] else "NONE"
        failed = ",".join(row["failing_labels"]) or "-"
        print(f"row\t{row['defect']}\t{row['runner_verdict']}\texit={row['exit']}"
              f"\tdeclared={declared_w}\tfailed={failed}"
              f"\tdenominator={row['denominator']}\texercised={row['exercised']}"
              f"\tskipped={row['skipped']}\tclass={row['classification']}")
    print(f"counts\tkilled_on_witness={tally['killed_on_witness']}"
          f"\taccidental={tally['accidental']}\tsurvived={tally['survived']}"
          f"\tinconclusive={tally['inconclusive']}\ttotal={tally['total']}"
          f"\twitness_classified={tally['witness_classified']}")
    print(f"declared_none\t{','.join(tally['declared_none']) or 'none'}")
    print(f"unresolved\t{','.join(tally['unresolved']) or 'none'}")
    return EXIT_FAIL if tally["unresolved"] else EXIT_OK


def cmd_check(args) -> int:
    evidence = Path(args.evidence)
    declaration = load_declaration(evidence)
    problems = []
    covered = set()
    declared_sha = verify_declared_digest(evidence, declaration)
    covered.add(DECLARED_NAME)
    declared = parse_declared_tsv(read_text(evidence / DECLARED_NAME))
    if declared != declared_expected():
        problems.append("DECLARED mapping differs from the frozen DECLARED_WITNESSES rows")
    inputs = declaration.get("inputs", {})
    for key, name in (("target", TARGET_NAME), ("spec", SPEC_NAME)):
        path = evidence / name
        if not path.is_file():
            raise Cannot(f"missing {path}")
        actual = sha256_file(path)
        committed = inputs.get(key, {}).get("sha256")
        covered.add(name)
        if actual != committed:
            problems.append(f"TAMPER {name} sha256={actual} committed={committed}")
    try:
        runner_sha = sha256_file(RUNNER)
    except OSError as exc:
        runner_sha = None
        problems.append(f"MISSING runner {RUNNER}: {exc}")
    committed_runner = inputs.get("runner", {}).get("sha256")
    covered.add("tools/mutate-and-run.sh")
    if runner_sha is not None and runner_sha != committed_runner:
        problems.append(f"DRIFT tools/mutate-and-run.sh sha256={runner_sha} "
                        f"committed={committed_runner}")
    summary_path = evidence / SUMMARY_NAME
    summary = None
    if summary_path.is_file():
        try:
            summary = json.loads(read_text(summary_path))
        except json.JSONDecodeError as exc:
            raise Cannot(f"unreadable {summary_path}: {exc}") from exc
        covered.add(SUMMARY_NAME)
        if summary.get("declaration", {}).get("sha256") != declared_sha:
            problems.append(f"TAMPER {SUMMARY_NAME} declaration-linkage "
                            f"sha256={summary.get('declaration', {}).get('sha256')} "
                            f"declared={declared_sha}")
    else:
        problems.append(f"MISSING {SUMMARY_NAME}")
    manifest_path = evidence / MANIFEST_NAME
    if not manifest_path.is_file():
        raise Cannot(f"missing {manifest_path} — the full manifest is mandatory")
    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError as exc:
        raise Cannot(f"unreadable {manifest_path}: {exc}") from exc
    listed = manifest.get("files")
    if not isinstance(listed, dict) or not listed:
        raise Fail(f"{MANIFEST_NAME}: files map is empty or malformed")
    required = [DECLARATION_NAME, DECLARED_NAME, TARGET_NAME, SPEC_NAME, SUMMARY_NAME]
    if summary is not None and summary.get("status") in ("complete", "degraded"):
        required.extend([f"{SWEEP_DIR}/results.tsv",
                         f"{SWEEP_DIR}/evidence/control.out",
                         f"{SWEEP_DIR}/cli.log", f"{SWEEP_DIR}/cli.exit"])
        required.extend(f"{SWEEP_DIR}/evidence/{ident}.out" for ident in declared)
    missing_required = [name for name in required if name not in listed]
    if missing_required:
        problems.append("MANIFEST incomplete (missing required): "
                        + ", ".join(missing_required))
    present = set(manifest_files(evidence))
    for name in sorted(present - set(listed)):
        problems.append(f"UNLISTED {name}")
    root = evidence.resolve()
    for name in sorted(listed):
        digest = listed[name]
        if not isinstance(name, str) or Path(name).is_absolute():
            problems.append(f"UNSAFE {name!r}")
            continue
        path = evidence / name
        try:
            path.resolve().relative_to(root)
        except (ValueError, OSError):
            problems.append(f"UNSAFE {name}")
            continue
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            problems.append(f"MALFORMED {name} sha256={digest!r}")
            continue
        if not path.is_file():
            problems.append(f"MISSING {name} (manifest sha256={digest})")
            continue
        actual = sha256_file(path)
        if actual != digest:
            problems.append(f"TAMPER {name} sha256={actual} committed={digest}")
        covered.add(name)
    if problems:
        for problem in problems:
            print(f"WITNESS_CHECK: {problem}")
        print(f"WITNESS_CHECK: FAIL ({len(problems)} problems; "
              f"{len(covered)} files covered)")
        return EXIT_FAIL
    print(f"WITNESS_CHECK: CLEAN (declared.tsv sha256={declared_sha}, "
          f"{len(covered)} files covered, {len(listed)} manifest entries)")
    return EXIT_OK


def cmd_selftest(args) -> int:
    cases = failed = 0

    def check(name: str, ok: bool) -> None:
        nonlocal cases, failed
        cases += 1
        if ok:
            print(f"  check {name:<44} ok")
        else:
            failed += 1
            print(f"  check {name:<44} FAIL")

    private_root = Path(tempfile.mkdtemp(
        prefix="bash-witness-selftest-private.", dir="/tmp"))
    assert private_root.resolve(strict=True) == private_root
    root = None
    try:
        root = Path(tempfile.mkdtemp(
            prefix="bash-witness-selftest.", dir=private_root))
        assert root.resolve(strict=True) == root
        # A hostile inherited Git selection must not redirect either child Git
        # invocation to the canary repository. Both launch paths are exercised
        # with GIT_DIR and GIT_WORK_TREE exported and distinct fixture repos.
        def fixture_repo(name: str, contents: bytes) -> tuple:
            repo = root / name
            repo.mkdir()
            target = repo / TARGET_GIT_PATH
            target.parent.mkdir(parents=True)
            target.write_bytes(contents)
            safe_env = git_clean_env()
            subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null",
                 "-C", str(repo), "init", "--quiet"],
                check=True, env=safe_env,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null",
                 "-C", str(repo), "add", "--", TARGET_GIT_PATH],
                check=True, env=safe_env,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null",
                 "-C", str(repo), "-c", "user.name=fixture",
                 "-c", "user.email=fixture@example.invalid", "commit",
                 "--quiet", "-m", "fixture"],
                check=True, env=safe_env,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            revision = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True, capture_output=True, env=safe_env,
            ).stdout.decode("ascii").strip()
            return repo, revision

        materialize_ok = sweep_ok = False
        saved_runner = RUNNER
        saved_which = shutil.which
        saved_env = {
            name: os.environ.get(name)
            for name in ("GIT_DIR", "GIT_WORK_TREE", "WITNESS_CANARY_REPO")
        }
        try:
            fixture, revision = fixture_repo(
                "git-fixture", b"fixture target bytes\n")
            canary, _ = fixture_repo("git-canary", b"canary target bytes\n")
            probe_runner = root / "git-canary-runner.sh"
            probe_runner.write_text(
                "#!/bin/bash\n"
                "set -eu\n"
                "git -C \"$WITNESS_CANARY_REPO\" rev-parse --show-toplevel\n",
                encoding="utf-8")
            os.environ["GIT_DIR"] = str(canary / ".git")
            os.environ["GIT_WORK_TREE"] = str(canary)
            os.environ["WITNESS_CANARY_REPO"] = str(fixture)

            try:
                materialize_ok = (
                    materialize_target(fixture, revision)
                    == b"fixture target bytes\n")
            except (Cannot, OSError, subprocess.SubprocessError):
                materialize_ok = False

            globals()["RUNNER"] = probe_runner
            shutil.which = lambda name: None if name == "the-janitor" else saved_which(name)
            try:
                sweep = run_sweep(root / "canary-evidence",
                                  root / "canary-sweep", 30, 4)
                sweep_ok = (
                    sweep["exit"] == 0
                    and str(fixture) in
                    (root / "canary-sweep" / "cli.log").read_text(encoding="utf-8")
                    and str(canary) not in
                    (root / "canary-sweep" / "cli.log").read_text(encoding="utf-8")
                )
            except (Cannot, OSError, subprocess.SubprocessError):
                sweep_ok = False
        except (OSError, subprocess.SubprocessError):
            materialize_ok = sweep_ok = False
        finally:
            globals()["RUNNER"] = saved_runner
            shutil.which = saved_which
            for name, value in saved_env.items():
                if value is None:
                    os.environ.pop(name, None)
                else:
                    os.environ[name] = value
        check("GIT_DIR/GIT_WORK_TREE cannot redirect materialization",
              materialize_ok)
        check("GIT_DIR/GIT_WORK_TREE cannot redirect sweep",
              sweep_ok)

        # spec extraction + parse on a synthetic runner
        runner = (
            "#!/bin/bash\n"
            "PIN_BASH=" + "a" * 64 + "\n"
            "REV_BASH=" + "b" * 40 + "\n"
            '  cat >"$d/bash-surface-census.spec" <<\'EOT\'\n'
            "@defect X1 | target.sh:10\n"
            "@old foo\n"
            "@new bar\n"
            "EOT\n"
            "  cat >\"$d/other.spec\" <<'EOT'\n@defect Z | z\n@old z\n@new y\nEOT\n"
        )
        spec = extract_spec(runner)
        check("extract_spec picks the census heredoc",
              spec == "@defect X1 | target.sh:10\n@old foo\n@new bar\n")
        defects = parse_spec(spec)
        check("parse_spec id/desc/literals",
              defects == [{"id": "X1", "desc": "target.sh:10", "old": "foo", "new": "bar"}])
        check("runner_pins reads both constants",
              runner_pins(runner) == {"PIN_BASH": "a" * 64, "REV_BASH": "b" * 40})
        short_pin = runner.replace("PIN_BASH=" + "a" * 64, "PIN_BASH=" + "a" * 40)
        try:
            runner_pins(short_pin)
            check("runner_pins refuses a short PIN_BASH", False)
        except Cannot as exc:
            check("runner_pins refuses a short PIN_BASH with a named error",
                  "PIN_BASH" in str(exc))
        check("unescape maps \\n", unescape("a\\nb", "t") == "a\nb")
        check("spec_precheck flags a non-unique literal",
              spec_precheck([{"id": "X", "old": "o", "new": ""}], "foo")["all_unique"] is False)

        catalog = EXPECTED_CASE_LABELS

        def synth_log(bad=(), skip=EXPECTED_SKIP_LABELS, omit=(), total=16,
                      summary=None):
            lines = []
            for number, name in enumerate(catalog, 1):
                if number > total or number in omit:
                    continue
                if name in skip:
                    lines.append(f"skip-case {number:02d} {name:<34} "
                                 f"substrate-absent (handler not on PATH)")
                elif name in bad:
                    lines.append(f"bad-case {number:02d} {name:<34} want exit=0 "
                                 f"token=SURFACE OK got exit=1")
                    lines.append("    | diagnostic dump: ok-case 99 nested, not a label")
                else:
                    lines.append(f"ok-case  {number:02d} {name:<34} exit=0")
            if summary is None:
                summary = (f"SELFTEST: FAIL ({len(bad)}/{total} cases)" if bad
                           else f"SELFTEST: PASS ({total} cases)")
            if summary:
                lines.append(summary)
            return "\n".join(lines) + "\n"

        control_info = parse_case_lines(synth_log())
        control = {"skip": control_info["skip"]}
        check("control log: 14 exercised + 2 expected skips + terminal 16",
              control_info["skip"] == list(EXPECTED_SKIP_LABELS)
              and len(control_info["ok"]) == 14 and control_info["total"] == 16
              and control_info["selftest_terminal"]
              and control_problems({
                  "ok_labels": control_info["ok"], "failing_labels": control_info["bad"],
                  "skip_labels": control_info["skip"], "numbers": control_info["numbers"],
                  "denominator": control_info["total"], "failures": control_info["failures"],
                  "exit": 0,
                  "selftest_line": control_info["selftest_line"],
                  "selftest_terminal": control_info["selftest_terminal"]}) == [])
        red = parse_case_lines(synth_log(bad=("clean",)))
        check("dump lines never count as labels",
              red["bad"] == ["clean"] and len(red["ok"]) == 13)
        check("killed-on-witness when a declared case fails",
              classify("B", "KILLED", red, control, ("clean",)) == ("killed-on-witness", []))
        check("accidental when no declared case fails",
              classify("B", "KILLED", parse_case_lines(synth_log(bad=("mode-drift",))),
                       control, ("clean",))[0] == "accidental")
        check("declared NONE red is accidental",
              classify("B", "KILLED", red, control, None)[0] == "accidental")
        green = parse_case_lines(synth_log())
        check("green with full denominator survives",
              classify("B", "SURVIVED", green, control, ("clean",)) == ("survived", []))
        check("no SELFTEST line is inconclusive",
              classify("B", "KILLED",
                       parse_case_lines(synth_log(bad=("clean",), summary="")),
                       control, ("clean",))[0] == "inconclusive")
        check("non-terminal SELFTEST line is inconclusive",
              classify("B", "KILLED",
                       parse_case_lines(synth_log(bad=("clean",)) + "trailing noise\n"),
                       control, ("clean",))[0] == "inconclusive")
        check("odd denominator is inconclusive",
              classify("B", "KILLED",
                       parse_case_lines(synth_log(bad=("clean",), total=15)),
                       control, ("clean",))[0] == "inconclusive")
        check("incomplete numbering is inconclusive",
              classify("B", "KILLED",
                       parse_case_lines(synth_log(bad=("clean",), omit=(7,))),
                       control, ("clean",))[0] == "inconclusive")
        check("unexpected skip label is inconclusive",
              classify("B", "KILLED",
                       parse_case_lines(synth_log(bad=("clean",),
                                                  skip=("mode-drift", "verbs-sandboxed"))),
                       control, ("clean",))[0] == "inconclusive")
        check("green with failing cases is inconclusive",
              classify("B", "SURVIVED",
                       parse_case_lines(synth_log(bad=("clean",),
                                                  summary="SELFTEST: PASS (16 cases)")),
                       control, ("clean",))[0] == "inconclusive")
        check("runner INCONCLUSIVE is inconclusive",
              classify("B", "INCONCLUSIVE", red, control, ("clean",))[0] == "inconclusive")
        try:
            parse_spec("@defect X | a\n@old o\n@new n\n"
                       "@defect X | b\n@old p\n@new q\n")
            check("duplicate spec id refuses", False)
        except Cannot as exc:
            check("duplicate spec id refuses", "duplicate" in str(exc))
        no_den = parse_case_lines(synth_log(bad=("clean",),
                                            summary="SELFTEST: FAIL (1 cases)"))
        check("FAIL without denominator is inconclusive, not a crash",
              no_den["total"] is None
              and classify("B", "KILLED", no_den, control, ("clean",))[0] == "inconclusive")
        check("unknown verdict is inconclusive",
              classify("B", "FLIPPED", red, control, ("clean",))[0] == "inconclusive")
        dup_log = synth_log().replace("SELFTEST: PASS",
                                      "bad-case 01 clean\nSELFTEST: PASS")
        dup_info = parse_case_lines(dup_log)
        check("duplicate case label is inconclusive",
              "duplicate-case-label:clean" in run_problems(dup_info, control)
              and classify("B", "KILLED", dup_info, control, ("clean",))[0]
              == "inconclusive")
        pass_red = parse_case_lines(synth_log(bad=("clean",),
                                              summary="SELFTEST: PASS (16 cases)"))
        check("PASS summary with a bad case is inconclusive",
              classify("B", "KILLED", pass_red, control, ("clean",))[0]
              == "inconclusive")
        red_exit0 = dict(red)
        red_exit0["exit"] = 0
        check("KILLED with exit 0 is inconclusive",
              classify("B", "KILLED", red_exit0, control, ("clean",))[0]
              == "inconclusive")
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                build_parser().parse_args(["no-such-mode"])
            check("usage error exits 64", False)
        except SystemExit as exc:
            check("usage error exits 64", exc.code == EXIT_USAGE)

        # declared.tsv round-trip + tamper refusal on a synthetic evidence dir
        evidence = root / "evidence"
        evidence.mkdir()
        tsv = declared_tsv_text({"target_sha256": "a" * 64, "spec_sha256": "b" * 64,
                                 "runner_sha256": "c" * 64, "rev": "d" * 64})
        (evidence / DECLARED_NAME).write_text(tsv, encoding="utf-8")
        mapping = parse_declared_tsv(tsv)
        check("declared.tsv round-trip keeps NONE rows",
              mapping.get("B5") is None and mapping.get("B1") == ("undeclared-file",))
        digest = sha256_bytes(tsv.encode("utf-8"))
        declaration = {"declared": {"sha256": digest}}
        check("untampered declared.tsv verifies",
              verify_declared_digest(evidence, declaration) == digest)
        (evidence / DECLARED_NAME).write_text(tsv + "# planted\n", encoding="utf-8")
        try:
            verify_declared_digest(evidence, declaration)
            check("planted tamper refuses", False)
        except Fail as exc:
            check("planted tamper refuses with a named error",
                  "TAMPER declared.tsv" in str(exc))

        # result-table re-evaluation fixtures
        def build_sweep(base: Path):
            ev = base / "evidence"
            ev.mkdir(parents=True, exist_ok=False)
            (ev / "control.out").write_text(synth_log(), encoding="utf-8")
            rows = ["id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc"]
            for ident in declared_expected():
                mutant = base / f"mutant-{ident}.{TARGET_NAME}"
                mutant.write_text(f"mutant {ident}\n", encoding="utf-8")
                (ev / f"{ident}.out").write_text(synth_log(), encoding="utf-8")
                rows.append(f"{ident}\tSURVIVED\t0\t1\t{sha256_file(mutant)}\t"
                            f"{ident} desc")
            (base / "results.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
            return base, control_record(base), rows

        srd, sctl, srows = build_sweep(root / "sweep-fixture")
        frows, _ = collect_results(srd, declared_expected(), sctl)
        check("collect_results recomputes ten survived rows",
              len(frows) == 10
              and all(r["classification"] == "survived" for r in frows))

        def write_rows(lines):
            (srd / "results.tsv").write_text("\n".join(lines) + "\n",
                                             encoding="utf-8")

        write_rows(srows + [srows[1]])
        try:
            collect_results(srd, declared_expected(), sctl)
            check("duplicate result id refuses", False)
        except Cannot as exc:
            check("duplicate result id refuses", "duplicate" in str(exc))
        write_rows(srows)
        unknown = list(srows)
        fields = unknown[-1].split("\t")
        fields[0] = "Z9"
        unknown[-1] = "\t".join(fields)
        write_rows(unknown)
        try:
            collect_results(srd, declared_expected(), sctl)
            check("unknown result id refuses", False)
        except Cannot as exc:
            check("unknown result id refuses", "unknown" in str(exc))
        write_rows(srows)
        flipped = list(srows)
        fields = flipped[1].split("\t")
        fields[1] = "KILLED"
        flipped[1] = "\t".join(fields)
        write_rows(flipped)
        try:
            collect_results(srd, declared_expected(), sctl)
            check("verdict/exit mismatch refuses", False)
        except Fail as exc:
            check("verdict/exit mismatch refuses", "verdict" in str(exc))
        write_rows(srows)
        (srd / f"mutant-B1.{TARGET_NAME}").write_text("tampered\n", encoding="utf-8")
        try:
            collect_results(srd, declared_expected(), sctl)
            check("mutant digest mismatch refuses", False)
        except Fail as exc:
            check("mutant digest mismatch refuses", "MUTANT B1" in str(exc))

        # full-manifest check fixture
        cev = root / "check-evidence"
        cev.mkdir()
        ctsv = declared_tsv_text({"target_sha256": "a" * 64,
                                  "spec_sha256": "b" * 64,
                                  "runner_sha256": "c" * 64,
                                  "rev": "d" * 40})
        (cev / DECLARED_NAME).write_text(ctsv, encoding="utf-8")
        cdigest = sha256_bytes(ctsv.encode("utf-8"))
        ctarget = b"#!/bin/bash\nexit 0\n"
        cspec = b"@defect B1 | x\n@old o\n@new n\n"
        (cev / TARGET_NAME).write_bytes(ctarget)
        (cev / SPEC_NAME).write_bytes(cspec)
        write_json(cev / DECLARATION_NAME, {
            "declared": {"sha256": cdigest},
            "inputs": {
                "target": {"sha256": sha256_bytes(ctarget)},
                "spec": {"sha256": sha256_bytes(cspec)},
                "runner": {"sha256": sha256_file(RUNNER)},
            },
        })
        write_json(cev / SUMMARY_NAME, {
            "status": "could-not-evaluate",
            "declaration": {"sha256": cdigest},
            "unresolved_reasons": ["fixture"],
            "counts": cannot_counts(),
            "rows": [],
        })
        write_manifest(cev)
        cns = argparse.Namespace(evidence=str(cev))

        def run_check():
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cmd_check(cns)
            return rc, buf.getvalue()

        crc, cout = run_check()
        check("check CLEAN on a full-manifest fixture",
              crc == EXIT_OK and "CLEAN" in cout)
        (cev / MANIFEST_NAME).unlink()
        try:
            run_check()
            check("missing manifest refuses", False)
        except Cannot as exc:
            check("missing manifest refuses", "mandatory" in str(exc))
        write_manifest(cev)
        manifest = json.loads(read_text(cev / MANIFEST_NAME))
        del manifest["files"][SUMMARY_NAME]
        write_json(cev / MANIFEST_NAME, manifest)
        crc, cout = run_check()
        check("pruned manifest is not CLEAN",
              crc == EXIT_FAIL and "MANIFEST incomplete" in cout
              and "UNLISTED summary.json" in cout)
        write_manifest(cev)
        (cev / SUMMARY_NAME).write_text(
            (cev / SUMMARY_NAME).read_text(encoding="utf-8") + " ",
            encoding="utf-8")
        crc, cout = run_check()
        check("summary tamper is detected",
              crc == EXIT_FAIL and "TAMPER summary.json" in cout)

        # count re-evaluation fixture
        qev = root / "count-evidence"
        qev.mkdir()
        qtsv = declared_tsv_text({"target_sha256": "a" * 64,
                                  "spec_sha256": "b" * 64,
                                  "runner_sha256": "c" * 64,
                                  "rev": "d" * 40})
        (qev / DECLARED_NAME).write_text(qtsv, encoding="utf-8")
        qdigest = sha256_bytes(qtsv.encode("utf-8"))
        write_json(qev / DECLARATION_NAME, {
            "declared": {"sha256": qdigest},
            "inputs": {},
        })
        qsweep, qctl, _ = build_sweep(qev / SWEEP_DIR)
        qrows, _ = collect_results(qsweep, declared_expected(), qctl)
        qsummary = build_summary(
            qev, {"kind": "declared-witness mapping (not a blind preregistration)",
                  "declared": {"sha256": qdigest}, "inputs": {}}, qdigest,
            {"target_sha256": "a" * 64},
            {"exit": 0, "cli_log": "sweep/cli.log"}, qctl, qrows, "complete")
        check("summary preserves top-level exposed declaration kind",
              qsummary["declaration"]["kind"] ==
              "declared-witness mapping (not a blind preregistration)")
        write_json(qev / SUMMARY_NAME, qsummary)
        qns = argparse.Namespace(evidence=str(qev))
        qbuf = io.StringIO()
        with contextlib.redirect_stdout(qbuf):
            qrc = cmd_count(qns)
        qout = qbuf.getvalue()
        check("count recomputes rows and matches summary",
              qrc == EXIT_OK and "witness_classified=10" in qout
              and "unresolved\tnone" in qout)
        qsummary["rows"][0]["classification"] = "killed-on-witness"
        qsummary["counts"] = counts(qsummary["rows"])
        write_json(qev / SUMMARY_NAME, qsummary)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_count(qns)
            check("count refuses summary/raw mismatch", False)
        except Fail as exc:
            check("count refuses summary/raw mismatch", "mismatch" in str(exc))

        print(f"WITNESS_SELFTEST: {cases - failed}/{cases} pass")
        if failed == 0:
            print("VERDICT: PASS")
            return EXIT_OK
        print("VERDICT: FAIL")
        return EXIT_FAIL
    finally:
        if root is not None:
            assert root.resolve(strict=True) == root
            shutil.rmtree(root, ignore_errors=True)
        assert private_root.resolve(strict=True) == private_root
        shutil.rmtree(private_root, ignore_errors=True)


class UsageParser(argparse.ArgumentParser):
    """argparse's default usage exit is 2; the probe contract uses 64."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = UsageParser(
        prog="bash-witness-study.py",
        description="declared-witness classification of the pinned "
                    "bash-surface-census mutation leg")
    parser.add_argument("--evidence", default=str(EVIDENCE_DEFAULT),
                        help=f"evidence directory (default: {EVIDENCE_DEFAULT})")
    parser.add_argument("--kagi", default=str(KAGI_DEFAULT),
                        help=f"kagi-shokunin repo (default: {KAGI_DEFAULT})")
    sub = parser.add_subparsers(dest="mode", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        # SUPPRESS keeps the top-level value when the subcommand omits the option,
        # so both `--evidence X declare` and `declare --evidence X` work.
        sp.add_argument("--evidence", default=argparse.SUPPRESS, help=argparse.SUPPRESS)
        sp.add_argument("--kagi", default=argparse.SUPPRESS, help=argparse.SUPPRESS)

    for name, help_text in (
        ("declare", "freeze the declared-witness TSV + declaration.json"),
        ("run", "execute the pinned sweep and classify every defect"),
        ("rerun", "re-run a fresh sweep against the static declarations"),
        ("count", "print classified rows, counts and unresolved (read-only)"),
        ("check", "verify every committed digest; named refusal on tamper"),
        ("selftest", "hermetic fixtures for the parser and classifier"),
    ):
        sp = sub.add_parser(name, help=help_text)
        add_common(sp)
        if name in ("run", "rerun"):
            sp.add_argument("--timeout", type=int, default=300,
                            help="seconds per suite run (default: 300)")
            sp.add_argument("--tail", type=int, default=4,
                            help="runner output tail lines per run (default: 4)")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handlers = {"declare": cmd_declare, "run": cmd_run, "rerun": cmd_rerun,
                "count": cmd_count, "check": cmd_check, "selftest": cmd_selftest}
    try:
        return handlers[args.mode](args)
    except Fail as exc:
        print(f"WITNESS_STUDY: {exc}", file=sys.stderr)
        return EXIT_FAIL
    except Cannot as exc:
        print(f"WITNESS_STUDY: CANNOT-EVALUATE ({exc})", file=sys.stderr)
        return EXIT_CANNOT


if __name__ == "__main__":
    sys.exit(main())
