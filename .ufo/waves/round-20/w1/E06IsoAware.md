# E06 — aware-vs-naive timestamp semantics

## Finding

**Agree:** the receipt-window checker requires an aware ISO-8601 interval. Python 3.15.0 documentation, section **“Aware and naive objects”** (accessed **2026-10-21**), states: “A naive object does not contain enough information to unambiguously locate itself relative to other date/time objects.” (17 words.) Source: <https://docs.python.org/3/library/datetime.html#aware-and-naive-objects>

The checker at `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-20/stage/receipt-window.py` converts a trailing `Z` to `+00:00`, parses with `datetime.fromisoformat`, and returns `None` when `dt.tzinfo is None` (lines 34–46). `require_interval` rejects an endpoint that parses to `None` with “measurement_interval start/end must be aware ISO-8601” (lines 50–58). For instruments with different frozen and installed hashes, the gate compares receipt endpoints against the edit-window bounds (lines 189–195). A naive wall-clock timestamp has no offset to determine which instant it denotes; assuming UTC, local time, or another zone would be an external interpretation. It therefore cannot establish whether measurement occurred before/after an instrument-window boundary, so the checker rejects it before those comparisons. A sandbox comparison also confirmed Python raises `TypeError` if a naive `datetime` is compared directly with an aware one; the checker avoids that comparison by rejecting naive values first.

## Commands and observed outputs

- Read `https://docs.python.org/3/library/datetime.html`: page title was **“datetime — Basic date and time types — Python 3.15.0 documentation”**; section **“Aware and naive objects”** contained the quoted passage and explained that UTC/local/other-zone interpretation of a naive object is up to the program.
- Searched the staged checker for `def parse_ts|tzinfo is None|aware ISO-8601|start is after end`: observed `parse_ts` at line 34; the naive guard at line 44; the aware-ISO-8601 rejection at line 55; and interval-order rejection at line 57. A second search for `measurement_interval|windows\[|start <=|end >|start <|end <=` located endpoint parsing at line 160 and frozen/installed window checks at lines 189–195.
- Exact sandbox command:
  ```sh
  cd "$(mktemp -d /tmp/e06isoaware.XXXX)" && python3 - <<'EOF'
  from datetime import datetime, timezone
  n = datetime.fromisoformat("2026-10-21T07:40:18")
  a = datetime.fromisoformat("2026-10-21T07:40:18+00:00")
  print("naive tzinfo:", n.tzinfo, "| aware tzinfo:", a.tzinfo)
  try:
      n < a
      print("comparison: OK (unexpected)")
  except TypeError as e:
      print("comparison TypeError:", e)
  print("aware same wall clock, +14h zone instant delta hours:", (datetime.fromisoformat("2026-10-21T07:40:18-14:00") - a).total_seconds()/3600)
  EOF
  ```
  Output:
  ```text
  naive tzinfo: None | aware tzinfo: UTC
  comparison TypeError: can't compare offset-naive and offset-aware datetimes
  aware same wall clock, +14h zone instant delta hours: 14.0
  ```
  The final line demonstrates that the same wall-clock value can represent a different instant when supplied a different offset; it is an illustrative sandbox calculation, not a separate checker test.

## Defects and scope

No defect observed in the assigned aware-vs-naive behavior. The staged checker bytes were read only; no lane production files were edited, and no tools were installed.