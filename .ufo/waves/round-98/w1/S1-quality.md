# R98S1 — QUALITY criterion draft

> Draft by seat R98S1 (scribe). Next free number at `HEAD` is **177** (the committed file's
> last numbered item is 176; `git show HEAD:corpus/QUALITY.md | grep -E '^1[0-9][0-9]\. '`
> ends at 176). Append after 176 in the file's voice.

177. A control's graded code is **measurement-derived**: the value a control driver compares
    against its expectation is the process result the state claims to run, never a constant
    typed beside it. A driver conforms only when every static `add(...)` site's recorded code
    resolves to a runner call (`sh`, `git`, `run`, `subprocess.run`) — directly
    (`p.returncode` where `p = run(...)`) or through the last assignment of the name before the
    call (resolution is linear in source order and scope-blind) — or as the first element of
    `code, out = run(...)`; a direct constant, a name whose last assignment is a constant, a
    loop variable, a plain call, or a `returncode` attribute on a value whose last assignment
    is not a runner call is unmeasured. Able to fail: the round-97 driver at `d32043ec` prints
    `CONTROL_ASSERT sites=15 measured=14 literal=1 unmeasured=1`, exit 1, and names line 156
    (`c2-nowork-absent`, whose committed receipt carries outer `rc=0` while the wrapped
    `git grep` returns 1); the repaired driver prints `sites=15 measured=15 literal=0
    unmeasured=0`, exit 0; the audit's twelve selftest arms include a literal-through-a-name
    arm and a fake-`returncode` arm (`--selftest` 12/12). The measure is the audit's
    classification of the site, not a proof that no constant reaches it: resolution is
    linear and scope-blind (a nested-scope assignment is the last one in source order and is
    what the resolver reads), the runner set is matched by call name (a locally defined
    `run`/`sh`/`git` counts as a runner), and the expectation is data and is not covered by
    the criterion. (`lessons/round-98.md`; round-97 spot-check D-2; S012.)
