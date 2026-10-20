#!/usr/bin/env python3
"""Assemble the round-17 cold-read ledger (v2) from seat cold-read reports.

Input (contract C / R16-C2b): each seat report is a markdown file carrying
EXACTLY ONE fenced ```json block of schema `tameshi-coldread-report-v2`:

    {"seat": str,
     "skill_sha256": "<64-hex sha256 of the page blob the seat read>",
     "read_rev": "<40-hex lane commit the seat's clone was at>",
     "sections": [{"start": int, "heading": str,
                   "class": "instruction"|"record",
                   "verdict": "executed-ok"|"verified-record"|"gap-minor"|
                              "gap-blocking"|"wrong-expectation"|
                              "not-executed",
                   "blocking_gaps": [], "wrong_expectations": [],
                   "minor_gaps": [], "commands_executed": [], "opened": [],
                   "inputs": {"<lane-rel path>": "<sha256>"},
                   "external_inputs": {"<abs|repo@rev:path>": "<sha256>"},
                   "traces": ["<trace receipt path>"]}]}

Page resolution: the page is `SKILL.md` in --repo at the report's read_rev;
its sha256 must equal the report's skill_sha256. If SKILL.md at that rev does
not match, the whole tree at read_rev is scanned (git ls-tree + cat-file
--batch) for any blob whose content sha256 equals skill_sha256. No match ->
the report is rejected (page-sha-mismatch). An unresolvable read_rev is also a
rejection.

Validation (a failing report is REJECTED, listed in _meta.reports_rejected,
and forces exit 1; other reports still assemble):
  zero or several ```json blocks, unparsable JSON, "schema" present and not
  tameshi-coldread-report-v2, missing/invalid seat|skill_sha256|read_rev|
  sections, unknown verdict/class, non-list gap/command/trace fields,
  non-dict inputs/external_inputs, non-64-hex digests, start that is not a
  section start (heading line, or 1 for the preamble) of the resolved page,
  or a heading that mismatches the page's heading text at that start.

Round-17 hardening (R05 §5 A4/A5 + L1 follow-ups 1–2):
  - A4 trace binding: every traces[] path must resolve against the repo
    worktree (absolute receipts are taken as given), carry schema
    tameshi-trace-inputs-v1, rev == read_rev, and empty live_lane_reads; its
    `inputs`/`external` maps are unioned into the section's maps, and a path
    declared with two different sha256 is rejected as `trace-conflict:<path>`.
    An observation that ran commands without any receipt is rejected
    (`trace-receipt-missing`).
  - read_rev is validated for EVERY report (resolves to a commit in --repo),
    before the page cache; a page sha cited at a rev that does not contain it
    is rejected (`page-not-at-read_rev`).
  - Exempt inputs: `SKILL.md` and the in-flight round-17 ledger are dropped
    from `inputs` (recorded per entry as `inputs_dropped`) so a page edit or
    the assembler's own output cannot manufacture input-drift.
  - Canonical inputs: absolute, `./`-prefixed, `.`/`..`-component, `.git`-
    component or empty-component keys are `noncanonical-input` rejections.
  - A5 external/lane separation (w2 F3): an `external_inputs` key must be an
    absolute path or `repo@rev:path`; any form that realpath-resolves under
    the lane root (absolute path, `<lane-abs-or-name>@<rev>:…` repo spec, or
    symlinked path) is rejected `external-input-lane`.
  - Fail-closed grouping: failing observations (verdict gap-blocking,
    wrong-expectation, not-executed, or any blocking_gaps/wrong_expectations)
    are kept in their own entries so a clean observation cannot launder them
    during aggregation (R05 F1; the measure vetoes).
  - Zero resolved reports (no files or every report rejected) exits 1 with a
    message instead of emitting an empty ledger as success.
  - Every git subprocess runs with all GIT_* variables scrubbed, so an
    exported GIT_DIR/GIT_WORK_TREE cannot redirect reads or writes to another
    repository (the round-17 lane-clobber incident).

Sectionizer (same rule as round-16 measure/assemble and contract C): a
section runs from a #/##/### heading line outside ``` fences through the line
before the next such heading; lines before the first heading form a preamble
bucket (start 1, heading ""). Section sha256 covers the section's lines
joined by "\\n" after stripping trailing whitespace-only lines.

Merging (contract C): observations for the same (skill_sha256, start) merge
into ONE ledger entry only when their `inputs` maps are identical; otherwise
each distinct inputs map keeps its own entry. To keep scalar entry fields
faithful, grouping also keys on external_inputs and read_rev (a stricter
condition than required — the contract's "only when inputs agree" is
honoured). Within a group: verdict = strictest observation
(wrong-expectation > gap-blocking > not-executed > gap-minor >
verified-record > executed-ok) after the v1 downgrade rule (executed-ok /
verified-record carrying minor_gaps counts as gap-minor); class =
"instruction" when any observation says so; gap/command fields are summed
list lengths; seats/reports/traces are order-preserving unions.

Ledger output (schema `tameshi-coldread-ledger-v2`): v1 entry fields
(skill_sha256, start, end, heading, sha256, class, verdict,
blocking_gaps:int, wrong_expectations:int, minor_gaps:int,
commands_executed_count:int, seats, reports) plus read_rev, inputs,
external_inputs, traces.

CLI:
  assemble.py --reports DIR_OR_GLOB... [--repo DIR] [--out FILE]
              [--expect-skill-sha SHA] [--selftest]

Exits: 0 ledger written and every bucket of the --expect-skill-sha page (or of
every observed page when the flag is absent) is covered by some entry, with no
rejected report; 1 a bucket uncovered (uncovered headings are printed) or a
report rejected; 2 invalid invocation (argparse or operational errors).
Stdlib only.
"""
import argparse
import contextlib
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# .ufo/evidence/round-17/coldread -> lane root is four levels up.
DEFAULT_REPO = os.path.realpath(os.path.join(HERE, "..", "..", "..", ".."))
DEFAULT_OUT = os.path.join(HERE, "ledger.json")
PAGE_PATH = "SKILL.md"

LEDGER_SCHEMA = "tameshi-coldread-ledger-v2"
REPORT_SCHEMA = "tameshi-coldread-report-v2"
HEADING_RE = re.compile(r"^#{1,3}(?:\s|$)")
FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
JSON_FENCE_RE = re.compile(r"^`{3,}\s*json\s*$", re.IGNORECASE)
FENCE_CLOSE_RE = re.compile(r"^`{3,}\s*$")
HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
CLASSES = ("instruction", "record")
# Round-17 hardening (R05 §5 A4/A5, L1 follow-up):
#  - trace receipts bind their inputs into the entry; conflicts reject.
#  - the page and the in-flight ledger never gate credit as inputs (F6/F10).
#  - failing observations are kept in their own entries (F1 fail-closed).
TRACE_SCHEMA = "tameshi-trace-inputs-v1"
DROPPED_INPUT_KEYS = (
    "SKILL.md",
    ".ufo/evidence/round-17/coldread/ledger.json",
)
FAILING_VERDICTS = ("gap-blocking", "wrong-expectation", "not-executed")
# Strictness order carried from the v1 assembler; index 0 is strictest.
VERDICTS = [
    "wrong-expectation",
    "gap-blocking",
    "not-executed",
    "gap-minor",
    "verified-record",
    "executed-ok",
]
VERDICT_RANK = {v: i for i, v in enumerate(VERDICTS)}
RELAXING = ("verified-record", "executed-ok")


class Reject(Exception):
    """One report fails validation; the report is rejected, assembly goes on."""


class AsmError(Exception):
    """Fatal operational error (repo unusable, expected page needed but
    unresolvable, output unwritable)."""


# ---------------------------------------------------------------- sections
def sectionize(text):
    """Split page text into sections per the contract rule.

    Returns [{start, end, heading, sha256}]; 1-based, end inclusive. sha256 is
    over the section's lines joined by "\\n" after stripping trailing
    whitespace-only lines.
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    in_fence = False
    fence_marker = ""
    headings = []
    for i, line in enumerate(lines, 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]
            elif marker[0] == fence_marker:
                in_fence = False
            continue
        if not in_fence and HEADING_RE.match(line):
            headings.append(i)
    bounds = []
    if not headings:
        if lines:
            bounds.append((1, len(lines), ""))
        return _mksections(lines, bounds)
    if headings[0] > 1:
        bounds.append((1, headings[0] - 1, ""))
    for idx, h in enumerate(headings):
        end = headings[idx + 1] - 1 if idx + 1 < len(headings) else len(lines)
        bounds.append((h, end, lines[h - 1]))
    return _mksections(lines, bounds)


def _mksections(lines, bounds):
    out = []
    for start, end, heading in bounds:
        body = lines[start - 1 : end]
        while body and not body[-1].strip():
            body.pop()
        out.append(
            {
                "start": start,
                "end": end,
                "heading": heading,
                "sha256": hashlib.sha256(
                    "\n".join(body).encode("utf-8")
                ).hexdigest(),
            }
        )
    return out


# --------------------------------------------------------------------- git
def _git_env():
    """Environment for git subprocesses with every GIT_* variable removed.

    A stray GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE in the caller's environment
    overrides `-C` and makes git read or write a different repository. R17
    incident: a selftest run with GIT_DIR exported clobbered the live lane's
    HEAD/index. Never inherit those variables.
    """
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo] + list(args),
        capture_output=True,
        env=_git_env(),
    )


def rev_ok(repo, rev):
    r = _git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    return r.returncode == 0


def resolve_commit(repo, rev):
    r = _git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if r.returncode != 0:
        return None
    return r.stdout.decode("ascii", "replace").strip()


def blob_at(repo, rev, path):
    """Bytes of the blob rev:path, or None.

    Uses `cat-file blob`, never `git show REV:path`: `show` prints a tree and
    exits 0 for a directory, so a directory input would masquerade as content.
    """
    r = _git(repo, "cat-file", "blob", "%s:%s" % (rev, path))
    return r.stdout if r.returncode == 0 else None


def find_blob_by_sha256(repo, rev, target_sha):
    """Scan the tree at rev for a blob whose content sha256 is target_sha.

    Returns (path, bytes) or None. Uses one `cat-file --batch` process.
    """
    r = _git(repo, "ls-tree", "-r", "--full-tree", "-z", rev)
    if r.returncode != 0:
        return None
    blobs = []
    for rec in r.stdout.split(b"\0"):
        if not rec:
            continue
        meta, _, path = rec.partition(b"\t")
        parts = meta.split(b" ")
        if len(parts) >= 3 and parts[1] == b"blob":
            blobs.append((parts[2].decode("ascii"), path.decode("utf-8", "replace")))
    if not blobs:
        return None
    try:
        proc = subprocess.Popen(
            ["git", "-C", repo, "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=_git_env(),
        )
    except OSError:
        return None
    found = None
    try:
        for oid, path in blobs:
            try:
                proc.stdin.write(oid.encode("ascii") + b"\n")
                proc.stdin.flush()
            except (BrokenPipeError, OSError):
                break
            header = proc.stdout.readline().split()
            if len(header) < 3 or header[1] != b"blob":
                break
            try:
                size = int(header[2])
            except ValueError:
                break
            data = proc.stdout.read(size)
            proc.stdout.read(1)  # trailing newline after content
            if hashlib.sha256(data).hexdigest() == target_sha:
                found = (path, data)
                break
    finally:
        try:
            proc.stdin.close()
        except OSError:
            pass
        proc.wait()
    return found


def resolve_page(repo, rev, skill_sha):
    """Return (path, text, sections) for the page whose sha256 is skill_sha at
    rev, or None."""
    data = blob_at(repo, rev, PAGE_PATH)
    if data is not None and hashlib.sha256(data).hexdigest() == skill_sha:
        path = PAGE_PATH
    else:
        hit = find_blob_by_sha256(repo, rev, skill_sha)
        if hit is None:
            return None
        path, data = hit
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("utf-8", "replace")
    return (path, text, sectionize(text))


# ------------------------------------------------------------------ reports
def extract_json_blocks(text):
    """Return the payloads of every closed ```json fenced block."""
    lines = text.split("\n")
    blocks = []
    i = 0
    while i < len(lines):
        if JSON_FENCE_RE.match(lines[i].strip()):
            j = i + 1
            body = []
            while j < len(lines) and not FENCE_CLOSE_RE.match(lines[j]):
                body.append(lines[j])
                j += 1
            if j < len(lines):
                blocks.append("\n".join(body))
                i = j + 1
                continue
        i += 1
    return blocks


def _is_hex(s, n):
    return isinstance(s, str) and re.match(
        r"^[0-9a-fA-F]{%d}$" % n, s
    ) is not None


def _check_digest_map(v, name, start):
    if not isinstance(v, dict):
        raise Reject("section start=%s: '%s' must be an object" % (start, name))
    for k, val in v.items():
        if not isinstance(k, str) or not k:
            raise Reject(
                "section start=%s: '%s' has a non-string/empty key"
                % (start, name)
            )
        if not _is_hex(val, 64):
            raise Reject(
                "section start=%s: '%s[%s]' is not a 64-hex sha256"
                % (start, name, k)
            )
        v[k] = val.lower()


def _check_str_list(v, name, start):
    if not isinstance(v, list):
        raise Reject("section start=%s: '%s' must be a list" % (start, name))
    for item in v:
        if not isinstance(item, str):
            raise Reject(
                "section start=%s: '%s' must be a list of strings"
                % (start, name)
            )


def canonical_path_reason(key):
    """Why `key` is not a canonical lane-relative path, or None.

    Matches measure.py's canonical_lane_path: no absolute, no `./`-prefix,
    no `.`, `..` or `.git` components, no empty components, no NUL, and the
    key must encode as UTF-8.
    """
    if not isinstance(key, str) or not key:
        return "empty"
    if "\0" in key:
        return "nul"
    try:
        key.encode("utf-8")
    except UnicodeEncodeError:
        return "non-utf8"
    if key.startswith("/"):
        return "absolute"
    if key.startswith("./"):
        return "dot-prefixed"
    parts = key.split("/")
    if any(p == ".." for p in parts):
        return "parent-component"
    if any(p == "." for p in parts):
        return "dot-component"
    if any(p == ".git" for p in parts):
        return "git-component"
    if any(p == "" for p in parts):
        return "empty-component"
    return None


def is_failing(obs):
    """Fail-closed classification (R05 §3 step 2, §5 A1).

    Failing observations stay in their own ledger entries so an aggregation
    step cannot launder them behind a clean observation with the same inputs.
    """
    return (
        obs["verdict"] in FAILING_VERDICTS
        or bool(obs["blocking_gaps"])
        or bool(obs["wrong_expectations"])
    )


def trace_receipt_path(repo, spec):
    """Resolve a traces[] entry: lane-relative against the repo worktree,
    absolute as given (receipts may have been emitted to /tmp)."""
    if os.path.isabs(spec):
        return os.path.realpath(spec)
    return os.path.realpath(os.path.join(repo, spec))


def load_trace_receipt(repo, spec, read_rev):
    """Load one tameshi-trace-inputs-v1 receipt; any defect raises Reject."""
    path = trace_receipt_path(repo, spec)
    if not os.path.isfile(path):
        raise Reject("trace-receipt-missing:%s" % spec)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise Reject("trace-receipt-unreadable:%s: %s" % (spec, e))
    if not isinstance(data, dict):
        raise Reject("trace-receipt-unreadable:%s: not an object" % spec)
    if data.get("schema") != TRACE_SCHEMA:
        raise Reject(
            "trace-receipt-schema:%s: %r != %s"
            % (spec, data.get("schema"), TRACE_SCHEMA)
        )
    if data.get("rev") != read_rev:
        raise Reject(
            "trace-rev-mismatch:%s: receipt rev %r != read_rev %s"
            % (spec, data.get("rev"), read_rev)
        )
    if data.get("live_lane_reads"):
        raise Reject(
            "trace-live-lane-read:%s: %d live-lane read(s) recorded"
            % (spec, len(data["live_lane_reads"]))
        )
    out = {"path": path}
    for field in ("inputs", "external"):
        raw = data.get(field) or {}
        if not isinstance(raw, dict):
            raise Reject(
                "trace-receipt-malformed:%s: '%s' must be an object"
                % (spec, field)
            )
        clean = {}
        for k, v in raw.items():
            if not isinstance(k, str) or not k:
                raise Reject(
                    "trace-receipt-malformed:%s: '%s' has a "
                    "non-string/empty key" % (spec, field)
                )
            if not _is_hex(v, 64):
                raise Reject(
                    "trace-receipt-malformed:%s: '%s[%s]' is not a 64-hex "
                    "sha256" % (spec, field, k)
                )
            clean[k] = v.lower()
        out[field] = clean
    return out


def merge_receipt_map(target, incoming, spec, dropped):
    """Union a receipt's digests into a section map.

    Exempt keys (the page, the in-flight ledger) are dropped and recorded in
    `dropped`; a path present in both maps with differing sha256 is
    `trace-conflict`; the same path with the same sha256 is idempotent.
    """
    for k, v in incoming.items():
        if k in DROPPED_INPUT_KEYS:
            dropped.add(k)
            continue
        if k in target and target[k] != v:
            raise Reject(
                "trace-conflict:%s: receipt %s declares %s, section "
                "declares %s" % (k, spec, v[:12], target[k][:12])
            )
        target[k] = v


def check_external_lane(repo, externals, start):
    """R05 A5 + w2 F3: no external_inputs key may name the live lane.

    Allowed key shapes are an absolute path or `repo@rev:path`. A key names
    the lane when:
      - it is an absolute path whose realpath resolves under the lane root,
      - it is `spec@rev:path` whose spec's realpath resolves under the lane
        root (absolute specs are taken as given; relative specs resolve
        against the lane's parent directory, i.e. the fleet root, so the
        lane's own directory name is caught), or
      - it is anything else that realpath-resolves under the lane root.
    Symlinks are resolved throughout (`os.path.realpath`).
    """
    root = os.path.realpath(repo)
    fleet = os.path.dirname(root)
    for k in externals:
        lane_key = False
        if "@" in k and ":" in k and k.index("@") < k.rindex(":"):
            # repo@rev:path — check the repo spec for lane naming.
            spec = k[: k.index("@")]
            base = spec if spec.startswith("/") else os.path.join(fleet, spec)
            real = os.path.realpath(base)
            lane_key = real == root or real.startswith(root + os.sep)
        elif k.startswith("/"):
            real = os.path.realpath(k)
            lane_key = real == root or real.startswith(root + os.sep)
        elif "@" in k or ":" in k:
            # Malformed repo@rev:path (e.g. `x@y` without `:`).
            raise Reject(
                "section start=%s: external-input-shape:%s" % (start, k)
            )
        else:
            # Plain relative key: lane if it resolves inside the lane.
            real = os.path.realpath(os.path.join(root, k))
            lane_key = real.startswith(root + os.sep)
            if not lane_key:
                raise Reject(
                    "section start=%s: external-input-shape:%s" % (start, k)
                )
        if lane_key:
            raise Reject(
                "section start=%s: external-input-lane:%s" % (start, k)
            )


def apply_trace_binding(repo, s, read_rev, cache):
    """A4 + L1 (4): drop exempt keys, then bind trace receipts into inputs."""
    dropped = set()
    for k in list(s["inputs"]):
        if k in DROPPED_INPUT_KEYS:
            dropped.add(k)
            del s["inputs"][k]
    if s["commands_executed"] and not s["traces"]:
        raise Reject(
            "trace-receipt-missing: start=%s ran %d command(s) without a "
            "trace receipt" % (s["start"], len(s["commands_executed"]))
        )
    for spec in s["traces"]:
        rec = cache.get(spec)
        if rec is None:
            rec = load_trace_receipt(repo, spec, read_rev)
            cache[spec] = rec
        merge_receipt_map(s["inputs"], rec["inputs"], spec, dropped)
        merge_receipt_map(
            s["external_inputs"], rec["external"], spec, dropped
        )
    for k in s["inputs"]:
        why = canonical_path_reason(k)
        if why is not None:
            raise Reject(
                "section start=%s: noncanonical-input:%s (%s)"
                % (s["start"], k, why)
            )
    check_external_lane(repo, s["external_inputs"], s["start"])
    if dropped:
        s["inputs_dropped"] = sorted(dropped)
    return s



def load_report(path):
    """Parse one v2 report file. Returns the payload dict or raises Reject."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        raise Reject("unreadable: %s" % e)
    blocks = extract_json_blocks(text)
    if not blocks:
        raise Reject("no ```json block found")
    if len(blocks) > 1:
        raise Reject("%d ```json blocks found; exactly one required"
                     % len(blocks))
    try:
        data = json.loads(blocks[0])
    except json.JSONDecodeError as e:
        raise Reject("json block does not parse: %s" % e)
    if not isinstance(data, dict):
        raise Reject("json block is not an object")
    if "schema" in data and data["schema"] != REPORT_SCHEMA:
        raise Reject("wrong schema %r" % data["schema"])
    seat = data.get("seat")
    if not isinstance(seat, str) or not seat:
        raise Reject("missing/invalid 'seat'")
    skill_sha = data.get("skill_sha256")
    if not _is_hex(skill_sha, 64):
        raise Reject("missing/invalid 'skill_sha256' (64-hex required)")
    data["skill_sha256"] = skill_sha.lower()
    read_rev = data.get("read_rev")
    if not _is_hex(read_rev, 40):
        raise Reject("missing/invalid 'read_rev' (40-hex required)")
    data["read_rev"] = read_rev.lower()
    sections = data.get("sections")
    if not isinstance(sections, list):
        raise Reject("missing/invalid 'sections' (list required)")
    for s in sections:
        if not isinstance(s, dict):
            raise Reject("non-object entry in sections")
        start = s.get("start")
        if not isinstance(start, int) or isinstance(start, bool):
            raise Reject("section without integer 'start'")
        for k in ("heading", "verdict", "class"):
            if not isinstance(s.get(k), str):
                raise Reject(
                    "section start=%s missing string '%s'" % (start, k)
                )
        if s["verdict"] not in VERDICT_RANK:
            raise Reject(
                "section start=%s invalid verdict %r" % (start, s["verdict"])
            )
        if s["class"] not in CLASSES:
            raise Reject(
                "section start=%s invalid class %r" % (start, s["class"])
            )
        for k in ("blocking_gaps", "wrong_expectations", "minor_gaps",
                  "commands_executed", "opened"):
            if s.get(k) is not None:
                _check_str_list(s[k], k, start)
            else:
                s[k] = []
        if s.get("traces") is not None:
            _check_str_list(s["traces"], "traces", start)
        else:
            s["traces"] = []
        s["inputs"] = s.get("inputs") or {}
        _check_digest_map(s["inputs"], "inputs", start)
        s["external_inputs"] = s.get("external_inputs") or {}
        _check_digest_map(
            s["external_inputs"], "external_inputs", start
        )
    return data


def effective_verdict(o):
    """v1 downgrade rule: a relaxing verdict carrying minor_gaps counts as
    gap-minor."""
    if o["verdict"] in RELAXING and o.get("minor_gaps"):
        return "gap-minor"
    return o["verdict"]


def canon(d):
    return json.dumps(d, sort_keys=True, separators=(",", ":"))


# ------------------------------------------------------------------ assembly
def discover_reports(specs):
    """Expand --reports args: dirs -> sorted *.md, files -> themselves, other
    strings -> glob patterns."""
    paths = []
    for spec in specs:
        if os.path.isdir(spec):
            hits = sorted(glob.glob(os.path.join(spec, "*.md")))
        elif os.path.isfile(spec):
            hits = [spec]
        else:
            hits = sorted(glob.glob(spec))
        paths.extend(hits)
    seen = set()
    return [
        p
        for p in paths
        if os.path.isfile(p) and not (p in seen or seen.add(p))
    ]


def assemble(repo, report_paths):
    """Parse reports, resolve pages, merge entries.

    Returns (entries, meta, pages) where pages maps skill_sha256 -> page
    record {rev, path, sections, by_start, first_line}; meta carries
    rejected/loaded reports, seats and the observed read_revs.
    """
    pages = {}  # skill_sha -> {rev, path, sections, by_start, first_line}
    rejected = []
    loaded = []
    seats_seen = []
    revs_seen = []
    groups = {}  # (skill_sha, start, inputs_key, ext_key, rev) -> [obs]
    order = []

    for path in report_paths:
        try:
            rep = load_report(path)
        except Reject as e:
            rejected.append({"report": path, "reason": str(e)})
            continue
        sha = rep["skill_sha256"]
        rev = rep["read_rev"]
        # F1 (w2 review): validate read_rev for EVERY report, before the page
        # cache — a cached page must not launder an unresolvable read point.
        if not rev_ok(repo, rev):
            rejected.append(
                {
                    "report": path,
                    "seat": rep["seat"],
                    "reason": "read_rev %s unresolvable in repo" % rev,
                }
            )
            continue
        page = pages.get(sha)
        if page is None:
            resolved = resolve_page(repo, rev, sha)
            if resolved is None:
                rejected.append(
                    {
                        "report": path,
                        "seat": rep["seat"],
                        "reason": "page-sha-mismatch: no blob at rev %s "
                        "has sha256 %s" % (rev, sha),
                    }
                )
                continue
            ppath, ptext, psecs = resolved
            page = {
                "sha256": sha,
                "rev": rev,
                "path": ppath,
                "sections": psecs,
                "by_start": {s["start"]: s for s in psecs},
                "first_line": ptext.split("\n", 1)[0] if ptext else "",
            }
            pages[sha] = page
        elif page["rev"] != rev:
            # Same page sha cited at another rev: the blob must exist at the
            # cited read point too (same sha => identical text, so the cached
            # section map stays valid).
            if resolve_page(repo, rev, sha) is None:
                rejected.append(
                    {
                        "report": path,
                        "seat": rep["seat"],
                        "reason": "page-not-at-read_rev: no blob at rev %s "
                        "has sha256 %s" % (rev, sha),
                    }
                )
                continue
        # Validate section starts/headings against this page.
        bad = None
        for s in rep["sections"]:
            sec = page["by_start"].get(s["start"])
            if sec is None:
                bad = (
                    "start=%s is not a section start of the page at "
                    "skill_sha256 %s" % (s["start"], sha)
                )
                break
            want, got = sec["heading"], s["heading"]
            ok = got == want or (
                want == ""
                and s["start"] == 1
                and got in ("", page["first_line"])
            )
            if not ok:
                bad = (
                    "heading mismatch at start=%d: report %r != page %r"
                    % (s["start"], got, want)
                )
                break
        if bad is not None:
            rejected.append(
                {"report": path, "seat": rep["seat"], "reason": bad}
            )
            continue
        try:
            cache = {}
            for s in rep["sections"]:
                apply_trace_binding(repo, s, rev, cache)
        except Reject as e:
            rejected.append(
                {"report": path, "seat": rep["seat"], "reason": str(e)}
            )
            continue
        loaded.append(path)
        if rep["seat"] not in seats_seen:
            seats_seen.append(rep["seat"])
        if rev not in revs_seen:
            revs_seen.append(rev)
        for s in rep["sections"]:
            key = (
                sha,
                s["start"],
                canon(s["inputs"]),
                canon(s["external_inputs"]),
                rev,
                is_failing(s),
            )
            if key not in groups:
                groups[key] = []
                order.append(key)
            obs = dict(s)
            obs["_seat"] = rep["seat"]
            obs["_report"] = path
            groups[key].append(obs)

    entries = []
    for key in order:
        sha, start, _ik, _ek, rev, _failing = key
        obslist = groups[key]
        sec = pages[sha]["by_start"][start]
        best = min(
            obslist, key=lambda o: VERDICT_RANK[effective_verdict(o)]
        )
        cls = (
            "instruction"
            if any(o["class"] == "instruction" for o in obslist)
            else obslist[0]["class"]
        )
        entry = {
            "skill_sha256": sha,
            "start": start,
            "end": sec["end"],
            "heading": sec["heading"],
            "sha256": sec["sha256"],
            "class": cls,
            "verdict": effective_verdict(best),
            "blocking_gaps": sum(len(o["blocking_gaps"]) for o in obslist),
            "wrong_expectations": sum(
                len(o["wrong_expectations"]) for o in obslist
            ),
            "minor_gaps": sum(len(o["minor_gaps"]) for o in obslist),
            "commands_executed_count": sum(
                len(o["commands_executed"]) for o in obslist
            ),
            "read_rev": rev,
            "inputs": obslist[0]["inputs"],
            "external_inputs": obslist[0]["external_inputs"],
            "traces": [],
            "seats": [],
            "reports": [],
        }
        dropped = set()
        for o in obslist:
            dropped.update(o.get("inputs_dropped") or [])
            for t in o["traces"]:
                if t not in entry["traces"]:
                    entry["traces"].append(t)
            if o["_seat"] not in entry["seats"]:
                entry["seats"].append(o["_seat"])
            if o["_report"] not in entry["reports"]:
                entry["reports"].append(o["_report"])
        if dropped:
            entry["inputs_dropped"] = sorted(dropped)
        if not entry["traces"]:
            del entry["traces"]
        entries.append(entry)

    meta = {
        "repo": repo,
        "pages": {
            sha: {
                "rev": p["rev"],
                "path": p["path"],
                "buckets": len(p["sections"]),
            }
            for sha, p in pages.items()
        },
        "reports_loaded": loaded,
        "reports_rejected": rejected,
        "seats": seats_seen,
        "read_revs": revs_seen,
    }
    return entries, meta, pages


def coverage(entries, page):
    """Buckets of `page` (a pages-dict value) covered by some entry."""
    have = {
        (e["skill_sha256"], e["start"]) for e in entries
    }
    sha = page["sha256"]
    missing = [
        s for s in page["sections"] if (sha, s["start"]) not in have
    ]
    return missing


def resolve_expected_page(repo, expect_sha, pages, revs):
    """Find the page identified by --expect-skill-sha. Reuses already
    resolved pages; otherwise scans each observed read_rev, then HEAD."""
    if expect_sha in pages:
        return pages[expect_sha]
    for rev in list(revs) + ["HEAD"]:
        if not rev_ok(repo, rev):
            continue
        resolved = resolve_page(repo, rev, expect_sha)
        if resolved is not None:
            ppath, ptext, psecs = resolved
            return {
                "sha256": expect_sha,
                "rev": rev,
                "path": ppath,
                "sections": psecs,
                "by_start": {s["start"]: s for s in psecs},
                "first_line": ptext.split("\n", 1)[0] if ptext else "",
            }
    return None


def print_summary(out_path, result, uncovered):
    meta = result["_meta"]
    print("ledger written: %s (%d entries)" % (out_path, len(result["entries"])))
    for e in result["entries"]:
        print(
            "  %5d-%-5d %-16s %-18s %s"
            % (
                e["start"],
                e["end"],
                e["class"],
                e["verdict"],
                (e["heading"] or "(preamble)")[:72],
            )
        )
    if meta["reports_rejected"]:
        print("rejected reports:")
        for r in meta["reports_rejected"]:
            print("  %s: %s" % (r["report"], r["reason"]))
    else:
        print("rejected reports: none")
    if uncovered is None:
        print("coverage: not evaluated (expected page unresolvable)")
    else:
        total = uncovered["total"]
        covered = uncovered["covered"]
        which = uncovered["skill_sha256"]
        print(
            "coverage: %d/%d buckets covered (skill %s)"
            % (covered, total, which[:12] if which else "all-observed")
        )
        if uncovered["missing"]:
            print("uncovered buckets:")
            for s in uncovered["missing"]:
                print(
                    "  start=%d %s" % (s["start"], s["heading"] or "(preamble)")
                )
        else:
            print("uncovered buckets: none")


# ------------------------------------------------------------------- selftest
def _selftest():
    import io

    fence = "```"
    failures = []

    def check(name, cond, detail=""):
        if not cond:
            failures.append(name)
        print("  [%s] %s %s" % ("ok" if cond else "FAIL", name, detail))

    def run_git(repo, *args):
        r = subprocess.run(
            ["git", "-C", repo] + list(args),
            capture_output=True,
            text=True,
            env=_git_env(),
        )
        if r.returncode != 0:
            raise RuntimeError("git %s failed: %s" % (args, r.stderr))
        return r.stdout

    def mkreport(seat, sha, rev, secs):
        return (
            "# report prose\n\nline\n" + fence + "json\n"
            + json.dumps(
                {
                    "seat": seat,
                    "skill_sha256": sha,
                    "read_rev": rev,
                    "sections": secs,
                }
            )
            + "\n" + fence + "\ntrailing prose\n"
        )

    skill_text = (
        "preamble line 1\n"
        "preamble line 2\n"
        "## Alpha\n"
        "body a\n"
        + fence + "\n# not a heading\n" + fence + "\n"
        "## Beta\n"
        "body b\n"
        "### Gamma\n"
        "body g\n"
        "\n"
    )
    skill_sha = hashlib.sha256(skill_text.encode()).hexdigest()
    secs = sectionize(skill_text)
    check("section count", len(secs) == 4, "got %d" % len(secs))
    check(
        "preamble/alpha starts",
        secs[0]["start"] == 1 and secs[1]["start"] == 3,
    )
    check(
        "alpha spans fenced #",
        secs[1]["end"] == 7,
        "end=%s" % secs[1]["end"],
    )

    with tempfile.TemporaryDirectory(
        prefix="assemble-v2-selftest-"
    ) as td:
        repo = os.path.join(td, "repo")
        os.makedirs(repo)
        run_git(repo, "init", "-q")
        run_git(repo, "config", "user.email", "selftest@example.invalid")
        run_git(repo, "config", "user.name", "selftest")
        # rev_old: different SKILL.md (used for the sha-mismatch rejection).
        with open(os.path.join(repo, "SKILL.md"), "w") as f:
            f.write("old unrelated page\n")
        run_git(repo, "add", "SKILL.md")
        run_git(repo, "commit", "-qm", "old")
        rev_old = run_git(repo, "rev-parse", "HEAD").strip()
        # rev_new: the real page.
        with open(os.path.join(repo, "SKILL.md"), "w") as f:
            f.write(skill_text)
        run_git(repo, "add", "SKILL.md")
        run_git(repo, "commit", "-qm", "page")
        rev_new = run_git(repo, "rev-parse", "HEAD").strip()

        # Trace receipts live in the repo worktree (lane-relative specs).
        trace_dir = os.path.join(repo, "traces")
        os.makedirs(trace_dir, exist_ok=True)

        def write_receipt(name, rev=None, schema=TRACE_SCHEMA,
                          live_lane_reads=None, **kw):
            payload = {
                "schema": schema,
                "rev": rev_new if rev is None else rev,
                "inputs": kw.get("inputs", {}),
                "external": kw.get("external", {}),
            }
            if live_lane_reads is not None:
                payload["live_lane_reads"] = live_lane_reads
            with open(os.path.join(trace_dir, name), "w") as f:
                json.dump(payload, f)

        write_receipt("t1.json", inputs={"tools/second.py": "d" * 64})
        write_receipt("t2.json", inputs={"tools/second.py": "d" * 64})
        write_receipt("bad-schema.json", schema="not-a-trace")
        write_receipt("old-rev.json", rev=rev_old)
        write_receipt(
            "live-lane.json",
            live_lane_reads={os.path.join(repo, "SKILL.md"): "a" * 64},
        )
        write_receipt("no-live-lane.json", live_lane_reads={})

        heads = {s["start"]: s["heading"] for s in secs}
        heads[1] = ""

        def sec(start, verdict, cls="record", **kw):
            s = {
                "start": start,
                "heading": (
                    kw.pop("heading")
                    if "heading" in kw
                    else heads[start]
                ),
                "class": cls,
                "verdict": verdict,
                "blocking_gaps": kw.pop("blocking_gaps", []),
                "wrong_expectations": kw.pop("wrong_expectations", []),
                "minor_gaps": kw.pop("minor_gaps", []),
                "commands_executed": kw.pop("commands_executed", []),
                "opened": kw.pop("opened", []),
            }
            if "inputs" in kw:
                s["inputs"] = kw.pop("inputs")
            if "external_inputs" in kw:
                s["external_inputs"] = kw.pop("external_inputs")
            if "traces" in kw:
                s["traces"] = kw.pop("traces")
            return s

        I1 = {"tools/evidence-disposition.py": "a" * 64}
        I2 = {"tools/evidence-disposition.py": "b" * 64}
        E1 = {"/tmp/outside.txt": "c" * 64}
        out = os.path.join(td, "ledger.json")

        # ---- happy path: full coverage, merge on equal inputs
        r1 = os.path.join(td, "r1.md")
        with open(r1, "w") as f:
            f.write(
                mkreport(
                    "SeatA",
                    skill_sha,
                    rev_new,
                    [
                        sec(1, "verified-record",
                            minor_gaps=["m1"], opened=["SKILL.md"]),
                        sec(3, "gap-minor", "instruction",
                            commands_executed=["c1", "c2"],
                            inputs=I1, external_inputs=E1,
                            traces=["traces/t1.json"]),
                    ],
                )
            )
        r2 = os.path.join(td, "r2.md")
        with open(r2, "w") as f:
            f.write(
                mkreport(
                    "SeatB",
                    skill_sha,
                    rev_new,
                    [
                        sec(3, "executed-ok", "record",
                            inputs=I1, external_inputs=E1,
                            traces=["traces/t2.json"]),
                        sec(8, "executed-ok"),
                        sec(10, "not-executed"),
                    ],
                )
            )
        buf = io.StringIO()
        code = main(
            [
                "--reports", td, "--repo", repo, "--out", out,
                "--expect-skill-sha", skill_sha,
            ],
            stdout=buf,
        )
        check("happy path exit 0", code == 0, "got %d" % code)
        led = json.load(open(out))
        check("ledger schema", led["schema"] == LEDGER_SCHEMA)
        check("4 entries", len(led["entries"]) == 4,
              "got %d" % len(led["entries"]))
        e_alpha = [e for e in led["entries"] if e["start"] == 3][0]
        check(
            "merge on equal inputs (seats)",
            e_alpha["seats"] == ["SeatA", "SeatB"],
            str(e_alpha["seats"]),
        )
        check(
            "strictest verdict wins",
            e_alpha["verdict"] == "gap-minor",
            e_alpha["verdict"],
        )
        check("class disagreement -> instruction",
              e_alpha["class"] == "instruction")
        check("counts summed",
              e_alpha["commands_executed_count"] == 2
              and e_alpha["blocking_gaps"] == 0)
        check(
            "inputs unioned from trace receipts",
            e_alpha["inputs"]
            == dict(I1, **{"tools/second.py": "d" * 64}),
            str(e_alpha["inputs"]),
        )
        check("external_inputs kept", e_alpha["external_inputs"] == E1)
        check("read_rev kept", e_alpha["read_rev"] == rev_new)
        check("traces union", e_alpha["traces"] == ["traces/t1.json", "traces/t2.json"])
        e_pre = [e for e in led["entries"] if e["start"] == 1][0]
        check(
            "minor_gaps downgrade verified-record -> gap-minor",
            e_pre["verdict"] == "gap-minor",
            e_pre["verdict"],
        )
        check("entry sha256 matches sectionizer",
              e_alpha["sha256"] == secs[1]["sha256"]
              and e_alpha["end"] == secs[1]["end"])

        # ---- inputs disagreement keeps both entries
        r3 = os.path.join(td, "r3.md")
        with open(r3, "w") as f:
            f.write(
                mkreport(
                    "SeatC",
                    skill_sha,
                    rev_new,
                    [sec(3, "executed-ok", "instruction", inputs=I2)],
                )
            )
        code = main(
            [
                "--reports", r1, r2, r3, "--repo", repo, "--out", out,
                "--expect-skill-sha", skill_sha,
            ],
            stdout=io.StringIO(),
        )
        check("split run exit 0", code == 0, "got %d" % code)
        led = json.load(open(out))
        alphas = [e for e in led["entries"] if e["start"] == 3]
        check("inputs disagreement keeps both", len(alphas) == 2,
              "got %d" % len(alphas))
        check(
            "split entries keep own inputs",
            sorted(canon(a["inputs"]) for a in alphas)
            == sorted([
                canon(I2),
                canon(dict(I1, **{"tools/second.py": "d" * 64})),
            ]),
        )

        # ---- failing observation stays a separate entry (R05 F1)
        r4 = os.path.join(td, "r4.md")
        with open(r4, "w") as f:
            f.write(
                mkreport(
                    "SeatD",
                    skill_sha,
                    rev_new,
                    [sec(3, "gap-blocking", "record",
                         blocking_gaps=["g1"], inputs=I1,
                         traces=["traces/t1.json"])],
                )
            )
        code = main(
            [
                "--reports", r1, r2, r3, r4, "--repo", repo, "--out", out,
                "--expect-skill-sha", skill_sha,
            ],
            stdout=io.StringIO(),
        )
        check("failing-separation run exit 0", code == 0, "got %d" % code)
        led = json.load(open(out))
        alphas = [e for e in led["entries"] if e["start"] == 3]
        check("failing entry kept separate", len(alphas) == 3,
              "got %d" % len(alphas))
        winners = [a for a in alphas if a["verdict"] == "gap-blocking"]
        clean = [a for a in alphas if a["verdict"] == "gap-minor"]
        check(
            "failing entry visible and clean entry intact",
            len(winners) == 1 and len(clean) == 1
            and winners[0]["seats"] == ["SeatD"]
            and clean[0]["seats"] == ["SeatA", "SeatB"],
        )

        # ---- rejection cases (each forces exit 1)
        rej_dir = os.path.join(td, "rej")
        os.makedirs(rej_dir)

        def rej_case(name, body):
            p = os.path.join(rej_dir, name + ".md")
            with open(p, "w") as f:
                f.write(body)
            c = main(
                ["--reports", p, "--repo", repo, "--out", out],
                stdout=io.StringIO(),
            )
            led2 = json.load(open(out))
            reasons = [
                r2_["reason"] for r2_ in led2["_meta"]["reports_rejected"]
            ]
            check(
                "reject: " + name,
                c == 1 and len(reasons) == 1,
                "code=%d reasons=%s" % (c, reasons),
            )
            return reasons[0] if reasons else ""

        rej_case("zero-blocks", "# prose only\nno json here\n")
        rej_case(
            "two-blocks",
            fence + "json\n{}\n" + fence + "\n" + fence + "json\n{}\n"
            + fence + "\n",
        )
        rej_case(
            "bad-json",
            fence + "json\n{not json\n" + fence + "\n",
        )
        rej_case(
            "wrong-schema",
            mkreport("S", skill_sha, rev_new, [])
            .replace(
                '{"seat":',
                '{"schema": "nope", "seat":',
                1,
            ),
        )
        rej_case(
            "bad-verdict",
            mkreport(
                "S", skill_sha, rev_new,
                [dict(sec(1, "totally-fine"))],
            ),
        )
        rej_case(
            "bad-class",
            mkreport(
                "S", skill_sha, rev_new,
                [dict(sec(1, "executed-ok", "both"))],
            ),
        )
        rej_case(
            "bad-start",
            mkreport(
                "S", skill_sha, rev_new,
                [sec(2, "executed-ok", heading="preamble line 2")],
            ),
        )
        rej_case(
            "bad-heading",
            mkreport(
                "S", skill_sha, rev_new,
                [sec(3, "executed-ok", "instruction", heading="## WRONG")],
            ),
        )
        rej_case(
            "sha-mismatch",
            mkreport(
                "S", skill_sha, rev_old, [sec(1, "executed-ok", heading="")],
            ),
        )
        rej_case(
            "bad-read_rev",
            mkreport(
                "S", skill_sha, "0" * 40, [sec(1, "executed-ok", heading="")],
            ),
        )
        bad_inputs = dict(sec(1, "executed-ok"))
        bad_inputs["inputs"] = {"tools/x.py": "not-a-sha"}
        rej_case(
            "bad-input-sha",
            mkreport("S", skill_sha, rev_new, [bad_inputs]),
        )
        bad_rev_fmt = mkreport(
            "S", skill_sha, rev_new, [sec(1, "executed-ok", heading="")]
        ).replace(rev_new, "deadbeef", 1)
        rej_case("read_rev-not-40hex", bad_rev_fmt)

        # ---- hardening: trace binding (A4), canonical inputs, A5
        r = rej_case(
            "trace-missing",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"],
                          traces=["traces/absent.json"])]),
        )
        check("reason trace-receipt-missing",
              r.startswith("trace-receipt-missing"), r)
        r = rej_case(
            "trace-schema",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"],
                          traces=["traces/bad-schema.json"])]),
        )
        check("reason trace-receipt-schema",
              r.startswith("trace-receipt-schema"), r)
        r = rej_case(
            "trace-rev",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"],
                          traces=["traces/old-rev.json"])]),
        )
        check("reason trace-rev-mismatch",
              r.startswith("trace-rev-mismatch"), r)
        r = rej_case(
            "trace-conflict",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"],
                          inputs={"tools/second.py": "e" * 64},
                          traces=["traces/t1.json"])]),
        )
        check("reason trace-conflict",
              r.startswith("trace-conflict"), r)
        r = rej_case(
            "commands-without-trace",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"])]),
        )
        check("reason commands-without-trace",
              r.startswith("trace-receipt-missing"), r)
        r = rej_case(
            "absolute-input",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          inputs={"/etc/passwd": "a" * 64})]),
        )
        check("reason absolute input",
              "noncanonical-input" in r and "absolute" in r, r)
        r = rej_case(
            "parent-input",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          inputs={"tools/../x.py": "a" * 64})]),
        )
        check("reason parent input",
              "noncanonical-input" in r and "parent-component" in r, r)
        r = rej_case(
            "external-lane",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          external_inputs={
                              os.path.join(repo, "SKILL.md"): "a" * 64,
                          })]),
        )
        check("reason external-input-lane",
              "external-input-lane" in r, r)

        # ---- exempt keys are dropped from inputs (page, in-flight ledger)
        drop_inputs = {
            "SKILL.md": "a" * 64,
            ".ufo/evidence/round-17/coldread/ledger.json": "b" * 64,
            "tools/kept.py": "c" * 64,
        }
        rd = os.path.join(td, "rd.md")
        with open(rd, "w") as f:
            f.write(
                mkreport(
                    "SeatE", skill_sha, rev_new,
                    [sec(1, "executed-ok", inputs=drop_inputs)],
                )
            )
        code = main(
            ["--reports", rd, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        e_pre = [e for e in led["entries"] if e["start"] == 1][0]
        check(
            "exempt inputs dropped",
            e_pre["inputs"] == {"tools/kept.py": "c" * 64}
            and e_pre.get("inputs_dropped") == sorted(DROPPED_INPUT_KEYS)
            and led["_meta"]["reports_rejected"] == [],
            str(e_pre.get("inputs")),
        )
        # The same keys arriving from a trace receipt are also dropped.
        write_receipt(
            "page.json",
            inputs={"SKILL.md": "a" * 64, "tools/kept.py": "c" * 64},
        )
        rp2 = os.path.join(td, "rp2.md")
        with open(rp2, "w") as f:
            f.write(
                mkreport(
                    "SeatF", skill_sha, rev_new,
                    [sec(1, "executed-ok", commands_executed=["c"],
                         traces=["traces/page.json"])],
                )
            )
        code = main(
            ["--reports", rp2, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        e_pre = [e for e in led["entries"] if e["start"] == 1][0]
        check(
            "receipt-side page input dropped",
            code == 1
            and e_pre["inputs"] == {"tools/kept.py": "c" * 64}
            and e_pre.get("inputs_dropped") == ["SKILL.md"],
            str(e_pre.get("inputs")),
        )

        # ---- GIT_* variables must not redirect reads/writes
        decoy = os.path.join(td, "decoy")
        os.makedirs(decoy)
        run_git(decoy, "init", "-q")
        run_git(decoy, "config", "user.email", "selftest@example.invalid")
        run_git(decoy, "config", "user.name", "selftest")
        with open(os.path.join(decoy, "d.txt"), "w") as f:
            f.write("decoy\n")
        run_git(decoy, "add", "d.txt")
        run_git(decoy, "commit", "-qm", "decoy")
        decoy_head = run_git(decoy, "rev-parse", "HEAD").strip()
        saved = {
            k: os.environ.get(k) for k in ("GIT_DIR", "GIT_WORK_TREE")
        }
        os.environ["GIT_DIR"] = os.path.join(decoy, ".git")
        os.environ["GIT_WORK_TREE"] = decoy
        try:
            got = resolve_commit(repo, "HEAD")
            code = main(
                ["--reports", r1, "--repo", repo, "--out", out],
                stdout=io.StringIO(),
            )
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        led = json.load(open(out))
        check("GIT_* scrubbed for reads", got == rev_new, str(got))
        check(
            "GIT_* scrubbed inside main",
            code == 1 and led["_meta"]["reports_rejected"] == [],
            "code=%d rejected=%d"
            % (code, len(led["_meta"]["reports_rejected"])),
        )
        check(
            "decoy repo untouched",
            run_git(decoy, "rev-parse", "HEAD").strip() == decoy_head,
        )

        # ---- w2 review follow-up cases ----------------------------------
        # F1: read_rev validated for every report, before the page cache.
        bogus = os.path.join(td, "bogus.md")
        with open(bogus, "w") as f:
            f.write(
                mkreport(
                    "SeatBogus", skill_sha, "1" * 40,
                    [sec(1, "executed-ok", heading="")],
                )
            )
        code = main(
            ["--reports", r1, bogus, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        reasons = led["_meta"]["reports_rejected"]
        check(
            "cached-sha report still rev-checked (valid,bogus)",
            code == 1 and len(reasons) == 1
            and "unresolvable" in reasons[0]["reason"],
            "code=%d reasons=%s" % (code, reasons),
        )
        code = main(
            ["--reports", bogus, r1, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        reasons = led["_meta"]["reports_rejected"]
        check(
            "cached-sha report still rev-checked (bogus,valid)",
            code == 1 and len(reasons) == 1
            and "unresolvable" in reasons[0]["reason"],
            "code=%d reasons=%s" % (code, reasons),
        )
        # Same page sha cited at a rev that does not contain it.
        bogus2 = os.path.join(td, "bogus2.md")
        with open(bogus2, "w") as f:
            f.write(
                mkreport(
                    "SeatBogus2", skill_sha, rev_old,
                    [sec(1, "executed-ok", heading="")],
                )
            )
        code = main(
            ["--reports", r1, bogus2, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        reasons = led["_meta"]["reports_rejected"]
        check(
            "page-not-at-read_rev rejection",
            code == 1 and len(reasons) == 1
            and reasons[0]["reason"].startswith("page-not-at-read_rev"),
            "code=%d reasons=%s" % (code, reasons),
        )

        # live_lane_reads: non-empty rejects, empty dict accepted.
        r = rej_case(
            "trace-live-lane",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok", commands_executed=["c"],
                          traces=["traces/live-lane.json"])]),
        )
        check("reason trace-live-lane-read",
              r.startswith("trace-live-lane-read"), r)
        ok_ll = os.path.join(td, "okll.md")
        with open(ok_ll, "w") as f:
            f.write(
                mkreport(
                    "SeatLL", skill_sha, rev_new,
                    [sec(1, "executed-ok", commands_executed=["c"],
                         traces=["traces/no-live-lane.json"])],
                )
            )
        code = main(
            ["--reports", ok_ll, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        check(
            "empty live_lane_reads accepted",
            code == 1 and led["_meta"]["reports_rejected"] == [],
            "code=%d" % code,
        )

        # external_inputs naming the lane in any form.
        r = rej_case(
            "external-lane-abs-repo",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          external_inputs={
                              repo + "@%s:SKILL.md" % rev_new: "a" * 64,
                          })]),
        )
        check("reason abs-repo@rev lane",
              "external-input-lane" in r, r)
        r = rej_case(
            "external-lane-rel-repo",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          external_inputs={
                              "repo@%s:SKILL.md" % rev_new: "a" * 64,
                          })]),
        )
        check("reason rel-repo@rev lane",
              "external-input-lane" in r, r)
        link = os.path.join(td, "lane-link")
        if not os.path.exists(link):
            os.symlink(repo, link)
        r = rej_case(
            "external-lane-symlink",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          external_inputs={
                              link + "/SKILL.md": "a" * 64,
                          })]),
        )
        check("reason symlink lane",
              "external-input-lane" in r, r)
        # A sibling name (not the lane) under the fleet root is accepted.
        os.makedirs(os.path.join(td, "sibling"), exist_ok=True)
        sib = os.path.join(td, "sib.md")
        with open(sib, "w") as f:
            f.write(
                mkreport(
                    "SeatSib", skill_sha, rev_new,
                    [sec(1, "executed-ok",
                         external_inputs={
                             "sibling@%s:x" % "0" * 40: "a" * 64,
                         })],
                )
            )
        code = main(
            ["--reports", sib, "--repo", repo, "--out", out],
            stdout=io.StringIO(),
        )
        led = json.load(open(out))
        check(
            "non-lane repo@rev external accepted",
            code == 1 and led["_meta"]["reports_rejected"] == [],
            "code=%d" % code,
        )

        # `.` input components rejected like `..`.
        r = rej_case(
            "dot-input",
            mkreport("S", skill_sha, rev_new,
                     [sec(1, "executed-ok",
                          inputs={"tools/./x.py": "a" * 64})]),
        )
        check("reason dot-component",
              "noncanonical-input" in r and "dot-component" in r, r)

        # Zero resolved reports -> exit 1 with a message.
        bufz = io.StringIO()
        code = main(
            [
                "--reports", os.path.join(td, "nomatch-*.md"),
                "--repo", repo, "--out", out,
            ],
            stdout=bufz,
        )
        check(
            "zero reports exit 1",
            code == 1 and "no reports resolved" in bufz.getvalue(),
            "code=%d out=%s" % (code, bufz.getvalue().strip()[-60:]),
        )
        bufz = io.StringIO()
        code = main(
            ["--reports", bogus, "--repo", repo, "--out", out],
            stdout=bufz,
        )
        check(
            "all-rejected exits 1",
            code == 1 and "no reports resolved" in bufz.getvalue(),
            "code=%d" % code,
        )

        # ---- coverage gap -> exit 1 with uncovered headings printed
        buf2 = io.StringIO()
        code = main(
            [
                "--reports", r1, "--repo", repo, "--out", out,
                "--expect-skill-sha", skill_sha,
            ],
            stdout=buf2,
        )
        check("coverage gap exit 1", code == 1, "got %d" % code)
        check(
            "uncovered headings printed",
            "## Beta" in buf2.getvalue() and "### Gamma" in buf2.getvalue(),
        )
        # preamble-heading tolerance: "" and the first line both accepted.
        rp = os.path.join(td, "rp.md")
        with open(rp, "w") as f:
            f.write(
                mkreport(
                    "SeatP", skill_sha, rev_new,
                    [
                        sec(1, "verified-record", heading="preamble line 1"),
                        sec(3, "executed-ok", "instruction", inputs=I1),
                        sec(8, "executed-ok"),
                        sec(10, "executed-ok"),
                    ],
                )
            )
        code = main(
            [
                "--reports", rp, "--repo", repo, "--out", out,
                "--expect-skill-sha", skill_sha,
            ],
            stdout=io.StringIO(),
        )
        check("preamble first-line heading tolerated", code == 0,
              "got %d" % code)

        # ---- unresolvable --expect-skill-sha -> exit 1
        buf3 = io.StringIO()
        code = main(
            [
                "--reports", r1, "--repo", repo, "--out", out,
                "--expect-skill-sha", "f" * 64,
            ],
            stdout=buf3,
        )
        check("unresolvable expected page exit 1", code == 1,
              "got %d" % code)

    if failures:
        print("SELFTEST: FAIL (%d checks)" % len(failures))
        return 1
    print("SELFTEST: all checks passed")
    return 0


# ----------------------------------------------------------------------- main
def main(argv=None, stdout=None):
    out = stdout or sys.stdout
    p = argparse.ArgumentParser(
        description="Assemble the tameshi round-17 cold-read ledger (v2) "
        "from seat reports."
    )
    p.add_argument(
        "--reports",
        nargs="+",
        metavar="DIR_OR_GLOB",
        help="report directories (globbed for *.md), report files, or glob "
        "patterns",
    )
    p.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help="lane git repo used to resolve pages at read_rev "
        "(default: the lane containing this script)",
    )
    p.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help="ledger output path (default: ledger.json next to this script)",
    )
    p.add_argument(
        "--expect-skill-sha",
        metavar="SHA",
        help="sha256 of the page whose every bucket must be covered "
        "(default: require coverage of every observed page)",
    )
    p.add_argument(
        "--selftest",
        action="store_true",
        help="run built-in synthetic self-test and exit",
    )
    a = p.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.reports:
        p.error("--reports is required")
    if a.expect_skill_sha and not HEX64_RE.match(a.expect_skill_sha):
        p.error("--expect-skill-sha must be a 64-hex sha256")
    if a.expect_skill_sha:
        a.expect_skill_sha = a.expect_skill_sha.lower()

    report_paths = discover_reports(a.reports)
    try:
        entries, meta, pages = assemble(a.repo, report_paths)
    except OSError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    return _finish(a, out, entries, meta, pages)


def _finish(a, out, entries, meta, pages):
    expect = a.expect_skill_sha
    uncovered = None
    missing_all = False
    if expect:
        page = pages.get(expect) or resolve_expected_page(
            a.repo, expect, pages, meta["read_revs"]
        )
        if page is None:
            missing_all = True
        else:
            missing = coverage(entries, page)
            uncovered = {
                "skill_sha256": expect,
                "total": len(page["sections"]),
                "covered": len(page["sections"]) - len(missing),
                "missing": missing,
            }
    else:
        missing = []
        total = 0
        for sha, page in pages.items():
            total += len(page["sections"])
            missing += coverage(entries, page)
        uncovered = {
            "skill_sha256": None,
            "total": total,
            "covered": total - len(missing),
            "missing": missing,
        }

    result = {
        "schema": LEDGER_SCHEMA,
        "entries": entries,
        "_meta": dict(
            meta,
            expect_skill_sha=expect,
            uncovered=(
                [
                    {"start": s["start"], "heading": s["heading"]}
                    for s in uncovered["missing"]
                ]
                if uncovered
                else "expected-page-unresolvable"
            ),
            reports_resolved=len(meta["reports_loaded"]),
        ),
    }
    try:
        os.makedirs(
            os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True
        )
        tmp = a.out + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            f.write("\n")
        os.replace(tmp, a.out)
    except OSError as e:
        print("ERROR: cannot write %s: %s" % (a.out, e), file=sys.stderr)
        return 2

    with contextlib.redirect_stdout(out):
        if missing_all:
            print(
                "ledger written: %s (%d entries)" % (a.out, len(entries))
            )
            print(
                "expected page %s could not be resolved; all buckets "
                "uncovered" % expect
            )
        else:
            print_summary(a.out, result, uncovered)
    if not meta["reports_loaded"]:
        with contextlib.redirect_stdout(out):
            print(
                "no reports resolved: 0 loaded, %d rejected — refusing to "
                "emit an empty ledger as success"
                % len(meta["reports_rejected"])
            )
        return 1
    failed = bool(meta["reports_rejected"]) or missing_all
    if uncovered is not None:
        failed = failed or bool(uncovered["missing"])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
