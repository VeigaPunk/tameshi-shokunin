#!/usr/bin/env python3
"""Reference parser for surface-census.sh --selftest output.

Designed for BashWitness to safely extract suite denominator, case outcomes,
and failing labels without fragile substring matching or false positives.
"""

import re
import sys
from typing import Dict, List, Optional, Tuple

CASE_RE = re.compile(
    r"^(?P<status>ok-case|bad-case|skip-case)\s+(?P<idx>\d{2})\s+(?P<name>[a-z0-9-]+)\s*(?P<rest>.*)$"
)
SUMMARY_PASS_RE = re.compile(r"^SELFTEST:\s+PASS\s+\((?P<total>\d+)\s+cases\)$")
SUMMARY_FAIL_RE = re.compile(
    r"^SELFTEST:\s+FAIL\s+\((?P<failures>\d+)/(?P<total>\d+)\s+cases\)$"
)

EXPECTED_DENOMINATOR = 16


class SelftestParseResult:
    def __init__(self):
        self.cases: List[Tuple[str, int, str, str]] = []
        self.ok_cases: List[Tuple[int, str]] = []
        self.bad_cases: List[Tuple[int, str]] = []
        self.skip_cases: List[Tuple[int, str]] = []
        self.summary_verdict: Optional[str] = None
        self.summary_failures: Optional[int] = None
        self.summary_total: Optional[int] = None
        self.integrity_errors: List[str] = []

    @property
    def is_valid(self) -> bool:
        return len(self.integrity_errors) == 0

    @property
    def failing_labels(self) -> List[str]:
        """Returns list of failing case names."""
        return [name for _, name in self.bad_cases]


def parse_selftest_output(stdout_text: str, exit_code: int) -> SelftestParseResult:
    res = SelftestParseResult()

    for line in stdout_text.splitlines():
        line = line.rstrip()
        # Diagnostic lines indented by '    | ' are explicitly skipped
        if line.startswith("    | ") or line.startswith("\t"):
            continue

        m_case = CASE_RE.match(line)
        if m_case:
            status = m_case.group("status")
            idx = int(m_case.group("idx"))
            name = m_case.group("name")
            rest = m_case.group("rest")
            res.cases.append((status, idx, name, rest))
            if status == "ok-case":
                res.ok_cases.append((idx, name))
            elif status == "bad-case":
                res.bad_cases.append((idx, name))
            elif status == "skip-case":
                res.skip_cases.append((idx, name))
            continue

        m_pass = SUMMARY_PASS_RE.match(line)
        if m_pass:
            res.summary_verdict = "PASS"
            res.summary_failures = 0
            res.summary_total = int(m_pass.group("total"))
            continue

        m_fail = SUMMARY_FAIL_RE.match(line)
        if m_fail:
            res.summary_verdict = "FAIL"
            res.summary_failures = int(m_fail.group("failures"))
            res.summary_total = int(m_fail.group("total"))
            continue

    # Integrity validations
    if res.summary_verdict is None:
        res.integrity_errors.append("Missing summary line (SELFTEST: PASS/FAIL)")

    if res.summary_total != EXPECTED_DENOMINATOR:
        res.integrity_errors.append(
            f"Denominator mismatch: summary reports {res.summary_total}, expected {EXPECTED_DENOMINATOR}"
        )

    if len(res.cases) != EXPECTED_DENOMINATOR:
        res.integrity_errors.append(
            f"Enumerated case count mismatch: parsed {len(res.cases)} cases, expected {EXPECTED_DENOMINATOR}"
        )

    if res.summary_failures is not None and len(res.bad_cases) != res.summary_failures:
        res.integrity_errors.append(
            f"Bad-case count mismatch: summary claims {res.summary_failures}, parsed {len(res.bad_cases)}"
        )

    if res.summary_verdict == "PASS":
        if exit_code != 0:
            res.integrity_errors.append(
                f"Exit code inconsistency: summary PASS but exit={exit_code}"
            )
        if len(res.bad_cases) != 0:
            res.integrity_errors.append("Summary PASS but bad-case lines present")
    elif res.summary_verdict == "FAIL":
        if exit_code != 1:
            res.integrity_errors.append(
                f"Exit code inconsistency: summary FAIL but exit={exit_code} (expected 1)"
            )
        if len(res.bad_cases) == 0:
            res.integrity_errors.append("Summary FAIL but zero bad-case lines parsed")

    return res


if __name__ == "__main__":
    content = sys.stdin.read()
    res = parse_selftest_output(content, exit_code=int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    print("Valid:", res.is_valid)
    print("Verdict:", res.summary_verdict)
    print("Cases:", len(res.cases))
    print("Failing labels:", res.failing_labels)
    if not res.is_valid:
        print("Integrity errors:", res.integrity_errors)
