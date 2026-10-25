seat: CritJudge04

# Round-45 w2 — C1 falsify review of S049, S063, S086 (non-author)

Ledger read at commit `ad5942c6e9858af19d00000b58439b321ddfa62b`
(`.ufo/evidence/round-45/freshness/ledger.json`), snapshots read from that same commit, rows read
from `corpus/SOURCES.md`. Authors (not me): S049 `ExecRows06`, S063 `ExecRows10`, S086 `ExecRows15`.
Scratch dir `/tmp/tameshi-r45-CritJudge04/`. Lane checkout untouched except this report file.
No tool installs or upgrades (stock `curl`, `python3`, `sha256sum`, `git show`); no pacman/uv/npx/cargo action.

## Verdicts

S049 agree — reviewer CritJudge04 — live fetch sha256 `587938d2…` equals entry `raw_sha256` and the gunzipped snapshot; the quote is body text in the Popen Constructor `preexec_fn` Note (same "Using the subprocess Module" section, ~15.9 KB after the anchor's run() env paragraph) and states that the `env` parameter, not `preexec_fn`, modifies the child's environment, which supports the teaches claim, and the anchor's own run() env sentence is itself still present in the live bytes.
S063 agree — reviewer CritJudge04 — live fetch sha256 `a43b6eff…` equals entry and snapshot; the quote is the `GIT_CEILING_DIRECTORIES` definition under ENVIRONMENT VARIABLES → "The Git Repository", exactly where the anchor places it, and the same paragraph adds that the ceiling "will not exclude … a GIT_DIR set on the command line or in the environment", supporting the ceiling-bounds-the-walk / no-identity-check teaches.
S086 agree — reviewer CritJudge04 — live tarball sha256 `adb78e13…` and sha512 `28Cobrc…` (gitHead `00aa7bdc…`) equal the entry and the row's integrity pin; the quote is the eight-value `MutantStatus` enum at member `package/src/mutation-testing-report-schema.json:88-93` exactly as anchored, and `:7` `required: ["schemaVersion", "thresholds", "files"]` plus `:41` `required: ["id", "mutatorName", "location", "status"]` both survive, so the eight-statuses and top-level-required teaches hold.

No dispute. The three rows are genuinely re-verified against live bytes.

## sha256 comparisons (live now / entry / committed snapshot)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S049.live 'https://docs.python.org/3/library/subprocess.html'   # rc=0
587938d256dede9dc64c5f543ab3f19c74e42abd5de648056697701f199adf71  S049.live
entry raw_sha256 : 587938d256dede9dc64c5f543ab3f19c74e42abd5de648056697701f199adf71
git show ad5942c:.ufo/evidence/round-45/freshness/sources/S049.raw.gz | gunzip -c | sha256sum
587938d256dede9dc64c5f543ab3f19c74e42abd5de648056697701f199adf71  -
=> equal (byte-identical live bytes)

$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S063.live 'https://git-scm.com/docs/git'   # rc=0
a43b6eff834ea2eb2f4134c7be57a11c8b26d5a9884e5b331f6d5b99ea1a2f0e  S063.live
entry raw_sha256 : a43b6eff834ea2eb2f4134c7be57a11c8b26d5a9884e5b331f6d5b99ea1a2f0e
snapshot (git show ad5942c:…/S063.raw.gz | gunzip -c | sha256sum)
a43b6eff834ea2eb2f4134c7be57a11c8b26d5a9884e5b331f6d5b99ea1a2f0e  -
=> equal

$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o S086.live 'https://registry.npmjs.org/mutation-testing-report-schema/-/mutation-testing-report-schema-3.9.0.tgz'   # rc=0
adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280  S086.live
entry raw_sha256 : adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280
snapshot (git show ad5942c:…/S086.raw.gz | gunzip -c | sha256sum)
adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280  -
=> equal; sha512-b64 of live tarball = 28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==
   (equals the row's anchor pin), package.json version 3.9.0, gitHead 00aa7bdc1da9df9f474e363cd70041ef4d389b4e (equals anchor)
```

Independent predicate re-run (seat helper, not a measurement), on my own fetched bytes via `--snapdir`:

```
$ for id in S049 S063 S086; do python3 .ufo/evidence/round-45/freshness/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 \
    --check /tmp/tameshi-r45-CritJudge04/$id.json --snapdir /tmp/tameshi-r45-CritJudge04; done
CHECK S049 verified ok
CHECK S063 verified ok
CHECK S086 verified ok
exit=0
```
Quote lengths: S049 21 tokens, S063 25 tokens, S086 21 tokens. None of the three quotes occurs in its
row's own source/scope/anchor/teaches cells (`quote-in-own-cells: False` for all three).

## Located context

### S049 — `corpus/SOURCES.md:58`
Row: scope "Python subprocess.run env argument semantics …"; anchor "Using the subprocess Module,
run() env paragraph; Python 3.15.0 docs served 2026-10-20"; teaches "Explicit env mappings define
child environment rather than merely documenting an intended injection …".

Quote at char 20266 of the extracted text, inside the **Popen Constructor** subsection (heading
`Popen Constructor ¶` / `class subprocess. Popen (…)` at char 12565), in the `preexec_fn` parameter's
Note:

> … Warning The preexec_fn parameter is NOT SAFE to use in the presence of threads in your application.
> The child process could deadlock before exec is called. **Note If you need to modify the environment
> for the child use the env parameter rather than doing it in a preexec_fn .** The start_new_session
> and process_group parameters should take the place of code using preexec_fn to call os.setsid() …

The anchor's own run() env paragraph is at char 4364 and is still present verbatim in the live bytes:

> … If env is not None , it must be a mapping that defines the environment variables for the new
> process; these are used instead of the default behavior of inheriting the current process'
> environment. It is passed directly to Popen . …

The run() docs themselves forward to the Popen constructor ("These options, along with all of the
other options, are described in more detail in the Popen constructor documentation"), so the quoted
Note documents the same `env` parameter the row's scope names.

Observation (not a dispute): the entry's quote is not the anchor's paragraph but the Popen
Constructor Note ~15.9 KB later. `ExecRows06.md` records why: the literal run() env sentence yields
`CHECK S049 invalid overlap 1` under the frozen overlap rule (that sentence shares only
`environment` with scope+anchor+teaches; `env` is 3 chars and excluded). The row is nevertheless
fresh — I verified the anchor sentence myself in today's live bytes — so the row counts.

### S063 — `corpus/SOURCES.md:72`
Row: scope "git's upward repository-discovery walk and the environment variables that redirect or
bound it"; anchor 'ENVIRONMENT VARIABLES, "The Git Repository" @ page last updated in 2.56.0';
teaches "discovery walks parent directories and environment variables override it, so a ceiling
bounds the walk but is no identity check, and an inherited GIT_DIR redirects every `git -C`".

Headings in the extracted text: `Environment Variables` at 28986, `The Git Repository` at 30036,
`GIT_DIR` at 30350, `GIT_CEILING_DIRECTORIES` at 31939; quote at 32028.

> … GIT_CEILING_DIRECTORIES This should be a colon-separated list of absolute paths. If set, **it is a
> list of directories that Git should not chdir up into while looking for a repository directory
> (useful for excluding slow-loading network directories)**. It will not exclude the current working
> directory or a GIT_DIR set on the command line or in the environment. Normally, Git has to read
> the entries in this list and resolve any symlink …

and, two paragraphs earlier, the GIT_DIR sentence that carries the "redirects every `git -C`" part:

> GIT_DIR If the GIT_DIR environment variable is set then it specifies a path to use instead of the
> default .git for the base of the repository. The --git-dir command-line option also sets this value.

with the `-C` option itself defined as "Run as if git was started in <path> instead of the current
working directory." The quote is body prose in the anchor's exact subsection, not a title/nav/table
fragment, and it states the walk-bounding rule the teaches cell asserts; the immediately following
sentence in the same paragraph supplies the "no identity check / env override" clause.

### S086 — `corpus/SOURCES.md:95`
Row: scope "the released 3.9.0 report schema as an integrity-pinned npm artifact, not the
master-branch file S002 tracks"; anchor `package/src/mutation-testing-report-schema.json:7 … :41 …
:88-93 …`; teaches "the released schema requires schemaVersion, thresholds and files at the top
level and gives every mutant one of eight named statuses …".

Member `package/src/mutation-testing-report-schema.json` (353 lines) in the live tarball:

```
7   "required": ["schemaVersion", "thresholds", "files"],
41                "required": ["id", "mutatorName", "location", "status"],
88                  "status": {
89                    "type": "string",
90                    "title": "MutantStatus",
91                    "description": "Result of the mutation.",
92                    "enum": ["Killed", "Survived", "NoCoverage", "CompileError", "RuntimeError", "Timeout", "Ignored", "Pending"]
93                  },
```
Quote at char 2828 of the member's normalized text (single occurrence), immediately preceded by the
`static` mutant property and followed by `statusReason` — i.e. the enum is a mutant property exactly
as the anchor says. All three anchored line numbers match the live member.

Observation: the S086 quote string is textually identical to S002's ledger quote. S002 tracks the
master-branch `report-schema/…/mutation-testing-report-schema.json`, a different artifact; the string
is independently located in the 3.9.0 member at :88-93 and is not in S086's own cells, so this is not
a copied-from-row violation, but the duplication is worth knowing when the two rows are read together.

## Notes on the reviewed entries

- S049 live page now self-identifies as "Python 3.15.1 documentation" while the anchor says
  "Python 3.15.0 docs served 2026-10-20"; the floating `/3/` URL moved one patch release, and the
  anchored paragraph is unchanged. Not a freshness defect, recorded for calibration.
- All three live fetches were single attempts, HTTP 200 (curl exit 0), no redirect handling needed.
