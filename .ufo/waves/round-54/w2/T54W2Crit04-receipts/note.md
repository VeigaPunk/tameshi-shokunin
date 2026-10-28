# The scratch-root contract — three arms, one exit class (round 54)

Every lane tool that allocates scratch through a `strict_scratch_root()` helper
shares one contract. Before round 53 the helpers were seven near-copies of the
same fifteen lines and only some of their callers mapped the failure to the
documented class; round 54 makes the mapping uniform and this note is the rule
the seven tools and their registry rows now name.

## Three arms

| Arm | `TMPDIR` | Behaviour | Exit class |
|---|---|---|---|
| unset | absent | the platform default (`tempfile.gettempdir()`) is used | — |
| empty | `""` | **unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278) and the platform default applies | — |
| unusable | a path that is not a writable directory | the tool refuses before it allocates: the value is named, the class is printed, nothing falls back to `/tmp` | **2, could-not-evaluate** |

The empty arm is not a convenience. The reference implementation reads
`for envname in 'TMPDIR', 'TEMP', 'TMP': dirname = _os.getenv(envname); if dirname:
dirlist.append(dirname)` (S278 `_candidate_tempdir_list`:163-165), so an empty
`TMPDIR` never becomes a candidate directory; the documented list also starts at
"the directory named by the TMPDIR environment variable" and then falls through
(S279). A tool that treated `""` as a path would try to allocate under the
working directory — a silent, wrong scratch root — which is why the arm is
declared rather than left to whatever `os.path.isdir("")` happens to return.

The standard fixes only the variable's meaning, not its empty-string handling:
`TMPDIR` "shall represent a pathname of a directory made available for programs
that need a place to create temporary files" (S277). The empty arm is therefore
a lane declaration that follows the resolver the lane actually calls, and the
registry rows say so.

## Why the class is uniform

A set-but-unusable `TMPDIR` is an environment fact, not a failed measurement: the
gate did not run, so no verdict may be printed and the exit class is
could-not-evaluate (2), never 1 (a verdict of "differs"/"failed") and never a
traceback. Round 53 removed the silent `/tmp` fallback in seven tools and its
own closure spot-check routed the residue: four of the seven still raised an
uncaught `RuntimeError` from the self-test path (rc 1 with a traceback of the
message), so the class existed in three tools and not in four (routed defect
R53.6). Round 54 gives each of the four a `ScratchRootUnusable(RuntimeError)`
subclass raised by the helper and caught at the entry point, printing one line
that names the value and the class.

## What measures it

`python3 .ufo/evidence/round-54/c2/measure.py` runs each of the seven tools'
self-tests under three `TMPDIR` states (unusable, empty, usable) and reads the
registry rows: 7/7 exit 2 with the naming line and no traceback, 7/7 exit 0 on
the empty arm, 7/7 exit 0 on a usable root with no `mkdir` under `/tmp` under
`strace`, and 7/7 rows carrying the `scratch_root` cell. The counter's blind
spot is stated in the contract: it sees the self-test path, not every branch a
tool might use to allocate scratch.

## Falsifier

A tool that returns 0 after printing the could-not-evaluate line (control
CTL_EXIT0), or that names the class without the value, fails the counter. A
tool that regains a `dir="/tmp"` literal fails the round-53 monitor and the C2
`tmp_mkdirs` arm together.
