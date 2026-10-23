# ReviewBindV4 — code review of round-31 cold-read binding v4

Seat: TameshiR31.ReviewBindV4 (read-only review; no production files touched).
Target: `.ufo/evidence/round-31/coldread/bind-select-v4.py` (363 lines, frozen at lane commit
c111dab) vs its docstring, vs `.ufo/evidence/round-30/coldread/bind-select-v3.py` (diffed in my
scratch clone), and vs `.ufo/evidence/round-30/coldread/audit-bound-wC.py`.
Method: line-by-line read of all three files, then ~70 behavioral probes run against a scratch copy
at `/fast/scratch/hyaku/tameshi-r31-seats/ReviewBindV4/` importing only `traced_commands`,
`argv_matches`, `assistant_has` (pure functions; the frozen file was never executed or modified).
Bash semantics cross-checked against `bash` on this host; shlex is Python 3.14.8.

Verdict first: v4 is materially stricter than v3 and satisfies the round-30 audit's three
conditions, but the shell tokeniser is a *syntax-level* matcher with no heredoc, substitution,
line-continuation, or control-structure awareness. I found concrete false-accepts (the worst:
heredoc bodies credited as executions, quoted `';'` fabricating phantom commands, spaced fd
duplications/syntax errors credited) and a large false-reject class (every launch path not on the
wrapper whitelist: `then`/`do` bodies, `bash -c` strings, `$( )`, subshells, `sudo`, `time`,
`stdbuf`, `nice -n 5`, `env --`, `timeout --`, …) plus a fatal parse quirk: a shlex `#` comment
eats its newline, so any commented line merges the next line into the current segment and the
following command is silently invisible. Findings are ordered by severity.

## False accepts (credit for something bash does not do)

### FA-1 (highest): heredoc bodies are credited as executed commands — lines 74-104
`shlex` has no heredoc notion. `cat <<EOF` lexes as `['cat','<<EOF']`; `_strip_redirections`
(line 148-151) drops `<<EOF`, and every following line of the heredoc *body* is re-lexed as a
separate command. Probe:

    'cat <<EOF\npython trace-inputs.py --out seat-1.json\nEOF' -> [('seat-1.json', [])]

Bash feeds that `python …` line to `cat`'s stdin; nothing executes it. A forged transcript need
only contain one real bash call like the above plus a planted `seat-1.json` receipt (rev + argv
`[]`) to bind a trace that was never produced. Same for `<<-`, `<< 'EOF'`, and heredoc bodies
containing whole pipelines. Correction: pre-scan for heredoc introducers (`<<-?\s*['"]?\w+`) per
line and mask body lines until the delimiter, or refuse to credit segments originating inside a
heredoc span.

### FA-2: quoted separator tokens fabricate a second "command" — lines 97-103
`set(t) <= SEPARATOR_CHARS` splits on the *token text* ';', '||', '&', '\n' even when shlex
delivered them as quoted words (`posix=True` strips the quote marks but leaves a pure-punctuation
word). Probe:

    "python trace-inputs.py --out seat-1.json -- junk ';' trace-inputs.py --out seat-2.json"
      -> [('seat-1.json', ['junk']), ('seat-2.json', [])]

Bash passes `;` as a literal argv string to the real run; `seat-2.json` is never executed, yet v4
emits a traced pair for it — combined with a forged receipt this binds a non-existent run. Also
worth noting the inverse already verified: `-- a 'x;y' b` (separator char inside a mixed word) is
correctly kept as one token; only *pure* separator words are misread. Correction: have shlex tell
quoted words apart — e.g. keep quotes (`posix=False`) and re-tokenise words, or run a small custom
scanner that splits only on unquoted separators.

### FA-3: `command -v`/`-V` never execute, yet `_program` unwraps `command` — line 114
`command -v python` prints a path; it executes nothing. The generic env-style option loop
(lines 114-117) skips `-v` and treats the following token as the program. A forged
`command -v trace-inputs.py --out B` (exit 0, usually no `isError`) plus a receipt binds.
`nice`/`nohup`/`exec` inherit the same option loop: `nice -n 5 python …` is a *false reject*
('5' lands as program), and `exec -a x python …` is a false reject; those belong below, but the
`command` case is a true false-accept because `-v`/`-V` suppress execution entirely.
Correction: give `command` its own branch that refuses to unwrap when the next token is `-v`/`-V`.

### FA-4: spaced redirect + `&` merge credits syntax-error lines — lines 84-94
Merge rule 1 collapses `[X>, &, N]` into nothing for *any* redirect token ending in `>`/`<`,
including the spaced form `2> &1`, which bash treats as "redirect to file `&1`" only if it is the
last word — followed by more words it is a syntax error, and plain `> &` is a syntax error
outright (`bash -c 'echo a > & python -c "print(1)"'` → exit 2, nothing ran). Probes:

    'python trace-inputs.py --out seat-1.json 2> &1'          -> [('seat-1.json', [])]   # bash: file &1 or syntax err
    'echo a > & python trace-inputs.py --out seat-1.json'     -> [('seat-1.json', [])]   # bash: exit 2, never ran

Rule 2 (`&` before a `>`-leading token) likewise merges `cmd1 & >>x`, where bash parses `&` as a
background terminator followed by a redirect-only command. Only matters where `isError` is absent
or the line still ran something; direction is over-credit. Correction: apply rule 1 only when the
`&` is *glued* to the redirect (`2>&1` lexes `['2>','&','1']` — the `2>` token proves adjacency is
already required for the fd digit, so also require `tokens` had no whitespace, i.e. merge only
`N>`/`>` immediately followed by `&` immediately followed by a digit in the raw string — simplest
correct fix is to recognise the literal patterns `>&N`/`<&N`/`>&-` in the raw text, not reassemble
from tokens).

### FA-5: `timeout` with no duration is credited — lines 118-123
`timeout python trace-inputs.py --out seat-1.json` → `[('seat-1.json', [])]`; real GNU timeout
prints "invalid time interval 'python'", exit 125, never runs the script. The DURATION_RE check is
optional. Correction: require a duration token after `timeout` options (if the next non-option
token is not DURATION_RE, do not unwrap).

### FA-6: `x=$(python trace-inputs.py --out B)` credits basename `B)` — lines 74-104, 172
`(` is not in `punctuation_chars`, so `x=$(python` is one word matching WRAP_RE and `B)` is the
`--out` value token. Probe: `x=$(python trace-inputs.py --out seat-1.json)` →
`[('seat-1.json)', [])]`. The real file written is `seat-1.json`; the credited basename carries a
`)`. Narrow because the entry's trace basename must equal `seat-1.json)` — `own`'s
`splitext(...).split('.')[-1]` gives `json)`, which still starts with `seat-`, so `own` admits it
(lines 319-320). A forger naming a receipt `seat-1.json)` binds it to a real run that wrote
`seat-1.json`. Correction: strip trailing `)`/` ` /`}`…` from token ends when reassembling
substitutions, or reject `--out` values containing `(` `)` backtick as un-tokenisable.

### FA-7: mid-word `#` truncates the token in shlex but not in bash — lines 74-78
shlex treats an unquoted `#` *anywhere* in a word as a comment start (Python 3.14 verified:
`'echo a#b; python …'` lexes to `['echo','a']` — everything after `#` is gone; bash echoes `a#b`
and runs the second command). Dual use: FR for real commands after a `#` inside a token
(`--out seat-1.json#v2`), and a narrow FA — `--out seat-1.json#frag` writes `seat-1.json#frag` in
bash but is credited as basename `seat-1.json`. Correction: same as FA-2 — identify comment onset
only at unquoted word-start, i.e. custom scan or two-pass lexing per line.

### FA-8 (documented but worth recording): wildcard/expansion argv tokens void the argv check — lines 189-200
`argv_matches` treats any traced token containing `$`, backtick, or `~` as matching *any single*
recorded token, and any token containing `*?[ ` as matching *one or more* recorded tokens. So the
forged command `python trace-inputs.py --out seat-1.json -- $x '*'` matches receipt argv
`['any','a','b','c']` — argv comparison adds no binding strength once the command uses an
expansion. The docstring states this openly (lines 17-19), so it is a known design concession, but
note the asymmetry it creates: an honest command with `-- ${ARGS[@]}` binds against *any* receipt
argv of the right length, including a planted one. Also `a~b`/`foo~` mid-word tildes are wildcarded
though bash never expands them there. No correction requested (documented); flagged as residual
risk.

## False rejects (executions the binder cannot see)

### FR-1 (highest, broad class): every launch path outside the whitelist is invisible — lines 107-136
`_program` only unwraps `VAR=`, `env`-family, `timeout`, `command`, `exec`, `nice`, `nohup`.
Verified invisible executions (each is a *real* bash run of trace-inputs.py that yields no traced
pair):

    'if true; then python trace-inputs.py --out B; fi'        -> []   # 'then' segment heads its own seg
    'while read l; do python trace-inputs.py --out B; done'   -> []
    'for i in 1 2; do python trace-inputs.py --out B; done'   -> []
    'echo `python trace-inputs.py --out B`'                    -> []   # backtick word is opaque
    'echo $(python trace-inputs.py --out B)'                   -> []   # $( glued to echo's word... actually merged
    'bash -c "python trace-inputs.py --out B"'                 -> []   # nested shell string opaque
    '{ python trace-inputs.py --out B; }' / '( … )'            -> []   # brace/paren heads
    '! python trace-inputs.py --out B'                         -> []   # negation word
    'time python trace-inputs.py --out B'                      -> []   # 'time' not whitelisted
    'sudo/stdbuf/watch/parallel/chrt/ionice/taskset python …'  -> []   # all launchers break unwrap
    'X=1 python $(echo trace-inputs.py) --out B'               -> []   # program produced by substitution
    'env -C /tmp python trace-inputs.py --out B'               -> []   # -C takes an arg, loop lands on '/tmp'
    'env -- python trace-inputs.py --out B'                    -> []   # '--' becomes the argv cut (line 157)
    'timeout -- 5 python trace-inputs.py --out B'              -> []   # same '--' cut
    'nice -n 5 python trace-inputs.py --out B'                 -> []   # '-n' consumes nothing; '5' lands as program
    'python -X dev trace-inputs.py --out B'                    -> []   # option-arg swallow: 'dev' taken as script
    'python trace-\<newline>inputs.py --out B'                 -> []   # line continuation splits the word
    'cmd --out B' where command list-encoded as JSON list      -> []   # str(cmd) of a list is "[...]" glue

The `then`/`do` case is the most likely real-world hit: any seat that wraps its run in a shell
conditional or loop produces a transcript v4 cannot bind, and the *reason string* will blame the
trace (`trace-without-executed-bash-call`), not the grammar gap. `bash -c`/`sh -c` strings are the
second most likely. Correction that stays conservative: treat `then`, `do`, `else`, `elif`, `!`,
`{`, `(` as segment separators, and add `time`, `sudo`, `stdbuf`, `command -p` to the unwrap table
(option-arity per tool). Nested `bash -c`/`sh -c` strings could be recursively fed back through
`traced_commands` on the dequoted word — bounded depth 1.

### FR-2: a `#` comment eats its newline — the next line's command is merged — lines 74-78
With `commenters='#'` and `\n` removed from `lex.whitespace`, shlex's comment reader consumes the
newline itself; the comment does not terminate at end-of-line. Probe:

    'echo x # comment\npython trace-inputs.py --out seat-1.json' -> tokens [echo, x, python, trace-inputs.py, --out, seat-1.json] -> traced []

The `python` run lands *inside the `echo` segment* — silently invisible. Any real transcript whose
command has a `#`-comment line followed by the actual run is rejected; worse, a comment anywhere
merges *both* lines' tokens into one segment (here it also contaminates `echo`'s args — mostly
harmless, but a comment line ending in `--out B` followed by another line could even produce a
spurious credit on the wrong segment). Correction: split `cmd` on newlines before lexing, lex each
line separately, then split each line's token stream at separators (newlines are already literal
punctuation tokens, so this is a one-line change: iterate `str(cmd).split('\n')`).

### FR-3: pure quoted separator words split real argv — lines 97-103
Inverse of FA-2: `--out B -- a ';' b` → argv `['a']` (bash: `['a',';','b']`), so the receipt argv
never matches and a genuine run is rejected. Same for quoted `'|'`, `'&&'`, `'\n'` args.
Correction: same fix as FA-2 (quote-aware splitting).

### FR-4: backslash-newline continuations split words — lines 74-78
shlex with `whitespace=' \t\r'` does not join `\<newline>` continuations: `'python trace-\\\ninputs.py'`
→ tokens `['python','trace-\\','inputs.py','--out','B']` → `[]`. Bash joins them and runs.
Correction: `cmd = cmd.replace('\\\n', '')` before lexing (safe: inside double quotes bash also
joins; inside single quotes `\<newline>` is literal backslash+newline, a corner case).

### FR-5: malformed transcript shapes abort the whole run — lines 225-241
`(c.get('arguments') or {}).get('command', '')` at line 241 crashes when `arguments` is a truthy
non-dict (verified: `arguments: "python …"` → `AttributeError` propagates out of `assistant_has`,
out of `main` — the entire binding run dies). Same for a `content` that is a truthy non-list
(string content → iterating chars → `c.get` crash) or a `message` that is a non-dict truthy value
(line 225 `m.get('role')`). v3 had the `content`/`message` exposure already (it iterated
`m.get('content')` identically), but the `arguments`-string crash is new in v4 because v3 only
`json.dumps`ed the value. All are fail-closed (run dies, exit ≠ 0) yet one corrupt line in one
seat transcript blocks every entry. Correction: `args = c.get('arguments')`; guard
`isinstance(args, dict)` before `.get`, and `m`/`content` isinstance checks.

### FR-6: first post-call result must be non-error; later ok result does not rescue — lines 244-249
`later and not later[0][1]` requires the *first* result after the call to be clean. A harness that
emits an error result then a corrected result under the same call id is rejected. The docstring
("a toolResult with the same id that comes AFTER the call and is not marked isError", line 15)
reads as "exists a later non-error result", which the code does not implement — doc/code mismatch
in the stricter direction; probably intended (single-result-per-id model), but flag the wording.
Also `bool(m.get('isError'))` (line 226) treats the *string* `"false"` as error — verified
(`isError='false'` → excluded); harness-dependent.

### FR-7: `seen_ids` counts tool calls in *any* message role — lines 228-231
The id-uniqueness counter runs before the `role != 'assistant'` skip, so a user/system message
that embeds a `toolCall` with the same id (e.g. transcript echo of the call) invalidates the
genuine assistant call — verified (`t11` fixture → `[]`). Conservative direction, but it means
id reuse by non-assistant content silently unbinds real evidence.

### FR-8: first-hit transcript wins; traces split across retry sessions never bind — lines 307-314
`for tp in cands: … if hit: break` stops at the first transcript containing the COLDREAD needle.
A seat whose session rotated (`seat.jsonl`, `seat-2.jsonl`) and ran some traces in each file binds
only the traces present in the first hit file. Also `prefix`/`seat` are interpolated raw into
`glob.glob` patterns (lines 307-308); a registry seat containing `*?[` would widen the candidate
glob — config-controlled, noted only.

## Docstring-vs-code deltas (calibration notes, low severity)

- Lines 10-11: docstring names only `VAR=value`, `env [-u X]`, `timeout [opts] DURATION`; code
  also unwraps `command`, `exec`, `nice`, `nohup` and lets `env` consume *any* `-`-options and
  `VAR=` tokens (code strictly more permissive than documented).
- Line 15: see FR-6 — code requires the *first* post-call result non-error; wording implies any.
- Line 8: "an id that no other tool call in the transcript reuses" — code counts tool calls in
  non-assistant messages too (FR-7); doc does not limit to assistant calls, so arguably consistent.
- Line 16: "the trace receipt file … exists under --repo" — line 327 honours *absolute* entry
  trace paths verbatim, so an entry naming `/abs/path` escapes `--repo` entirely (inherited from
  v3's report-path logic, new for trace receipts). Same for report paths at line 288 (inherited).
- Line 19: "Unquoted fd duplications (2>&1) and redirections are not argv" — verified true for
  attached `2>&1`, `>&2`, `&>f`, `<<<`, `>f`, `2>f` (both in argv position and trailing); the
  spaced forms (`2> &1`, `> &`) are also stripped but see FA-4 for what that hides.
- v3 docstring retained verbatim (lines 25-29) still says "trace basename appears in an
  assistant-authored tool call whose arguments also name trace-inputs.py" — no longer the
  operative rule; a skimmer could misread v4's actual condition. Cosmetic.

## Confirmed correct (no action)

- `2>&1`/`>&2`/`&>f` attached forms tokenise `['2>','&','1']` / `['&','>f']` and are stripped
  cleanly — verified in argv position too (`-- a 2>&1 b` → argv `['a','b']`).
- `&&`, `||`, `|`, `|&`, `;`, `&`, newlines all split segments correctly; `a|b` inside words splits
  (`|` is punctuation). `true && python …` → credited.
- Quoted/escaped separators inside mixed words (`'a&b'`, `'x;y'`, `a\&b`, `"B # c"`) never split —
  only pure-separator words misbehave (FA-2/FR-3).
- `#` inside quotes and mid-token after quote removal is literal; `--out 'seat-1.json'` fine.
- Wrapper chains nest (`FOO=1 env X=2 timeout -s KILL 5 python3.11 …` → credited); `timeout -sKILL`,
  `env -u FOO` two-token forms correct; `python -u/-E -s`, `python3.11`, `./trace-inputs.py`,
  `/opt/x/trace-inputs.py`, `/tmp/../x/trace-inputs.py` all match basename correctly.
- `xtrace-inputs.py`, `bash`/`py`/`sh` as program, `--out` after `--`, and `command -v python`
  *alone* (no `--out`) produce no spurious credit.
- Duplicate call ids excluded (both-call-same-id fixture → `[]`); result-before-call-only → `[]`;
  isError result → `[]`; missing isError → credited; needle in tool-call args counts as hit;
  needle in *user* text does not; session id captured from `type=='session'` line.
- `argv_matches` DP: exact/shorter/longer correct; glob run-matching is greedy-with-backtrack and
  correct for `a*`/`?`/`[ab]`/unmatched-literal-self. Two divergences from real pathname expansion:
  `fnmatchcase` has no POSIX `[[:alpha:]]` (real-expanded arg rejected — FR) and `*` matches
  `a/b` (bash `*` cannot cross `/` — FA); both marginal.
- Pilot claim in docstring verified: `.ufo/evidence/round-31/coldread/pilot/v4-on-r30-real-receipt.json`
  exists and reports `{assembled: 63, kept: 63, excluded: 0}`.

## Audit-equivalence delta (v4 vs `audit-bound-wC.py`)

Audit uses `results.setdefault(cid)` — the *first-seen* result for the id must be post-call and
non-error. v4 requires only the first *post-call* result to be non-error, so a call carrying a
bogus pre-call result plus a real post-call one is credited by v4 but FAILs the audit (fixture
`t4`: v4 → `[('seat-1.json', ['x'])]`). v4 is otherwise a strict superset of the audit (adds
tokenised execution proof, id uniqueness, argv/rev receipt checks). One line of the audit remains
strictly stricter; whether pre-call garbage results should void credit is a policy call the frozen
contract does not settle.

## Verification gaps

- Transcript probes used synthetic JSONL fixtures shaped to the schema the code expects
  (`type=='message'`, `content[]` with `type=='toolCall'`/`text`, `role=='toolResult'` +
  `toolCallId`). If real host transcripts wrap calls differently (e.g. `toolCalls` array or
  `function_call`), both v3 and v4 read zero calls — inherited blind spot, not introduced here.
- `traced_commands` was probed on ~70 command strings; the set is adversarial but not exhaustive
  of bash grammar (no `case`, `coproc`, `(( ))`, `select` probes — all predictably FR-1-class).
- Did not re-run the pilot or the frozen counter (read-only seat; the pilot receipt was inspected,
  not regenerated).

## Tool installs

None. All work used system Python 3.14.8 / bash / coreutils already on the host.

Report: .ufo/waves/round-31/w1/ReviewBindV4.md
