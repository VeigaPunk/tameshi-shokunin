# Verdict: five new forged shapes survived frozen binding v4

Five of nine new shapes kept **63/63**, exit **0**, despite being newly forged command text that this probe never executed. Four shapes were killed at **0/63**, exit **1**. Every pristine and restored run kept **63/63**, exit **0**. No real entry was falsely rejected; no probe was inconclusive. All copied session files were restored to their exact original bytes.

Assigned axis: **calibration**. Probe axes: forged-call rejection, real-entry retention, and exact-byte restoration. This is a scoped input-mutation finding, not a judgment of C1. The frozen binder, C1 predicate, counter, and target were not changed.

## Evidence

Path abbreviations:

- `P=/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- `S=/fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New`
- `L=$S/repo`
- `B=$L/.ufo/evidence/round-31/coldread/bind-select-v4.py`

### Isolation and exact commands

All code ran with working directory `L`, except the clone/copy and hash/version commands, whose working directory was `S`. The scratch clone was detached at frozen revision `c111dab58b0a8d55e991bbd2efe3aad56717b95a`.

Executed from `S`:

```sh
df -h /fast && timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tameshi-shokunin repo && timeout 90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C repo checkout --detach c111dab58b0a8d55e991bbd2efe3aad56717b95a
```

Observed: `/fast` had 804G total, 629G used, 175G available, 79% used; clone completed; `HEAD is now at c111dab round-31: freeze C1 counter, binding v4, contract, base receipts`.

The real session directory was copied, never edited:

```sh
timeout 60 cp -a /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-23T06-27-20-968Z_01a16771-4d08-7011-958e-0f9940db87a7/TameshiR30A3 sessions-pristine
```

Observed: successful completion, no stdout or stderr.

Executed from `L`:

```sh
timeout --signal=TERM --kill-after=5s 240s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/probe-bind-v4-new.py
```

Observed: all nine result lines reported the counts in the table below and `restored_exact: true`; final output was `frozen_inputs_unchanged=true`. The command completed successfully. The retained harness SHA-256 is `03c93b9f077d01b49ffbf8959e83626c9aebebc02a1ae045a237f3c723330ebe`.

The harness used three independent local workers, with pristine → mutated → restored ordering inside each worker. Each shape had its own copied session directory. It changed only assistant Bash `arguments.command` fields, with JSON serialization of affected lines; call IDs, result messages, COLDREAD statements, reports, registry, and trace receipt content were left unchanged. Each shape changed 213 trace-recognized calls in 22 copied transcripts and covered all 211 distinct trace basenames named by the assembly. Coverage is enforced at `S/probe-bind-v4-new.py:153-154`; restoration is in the `finally` block at lines 181–191.

The frozen assembly contains absolute production trace paths. To avoid reading those instead of the clone's receipts, a separate fixture, `S/assembled-relocated.json`, changed only those path strings to clone-relative paths. The frozen assembly itself was not edited. Original assembly SHA-256: `f94929eb0f23335763fc42ffec71de83e8a4e19775c88900e74fd05fd1540eb2`; relocated fixture SHA-256: `83ce00fd90c8afe835c0b241889bd744fc25d259f5c790c88a5b4424eeb0760b`. Evidence: `S/relocation.json:2-6`, `S/probe-bind-v4-new.py:225-243`.

Here is one exact observed detector invocation, recorded at `S/shapes/literal_heredoc/mutated.run.json:2`:

```sh
timeout --signal=TERM --kill-after=2s 30s /usr/bin/python3 /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/repo/.ufo/evidence/round-31/coldread/bind-select-v4.py --repo /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/repo --assembled /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/assembled-relocated.json --registry /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/repo/.ufo/waves/round-30/wC/swarm-registry.json --sessions /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/shapes/literal_heredoc/sessions --prefix TameshiR30A3. --out /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/shapes/literal_heredoc/mutated.kept.json --receipt /fast/scratch/hyaku/tameshi-r31-seats/CtlBindV4New/shapes/literal_heredoc/mutated.receipt.json
```

All 27 expanded commands are retained at `S/shapes/<shape>/<phase>.run.json:2`, for `phase=pristine,mutated,restored`; observed exit/stdout/stderr are at lines 4–6. Within a shape the detector and inputs were identical across phases, except output filenames and the deliberately mutated/restored transcript bytes.

### Expected detector and observed outputs

Expected: pristine/restored **63 kept, exit 0**; every forged shape **0 kept, exit 1**. These expectations were not changed after observing results.

Actual stdout for every pristine/restored run and each surviving mutant:

```text
{"assembled": 63, "kept": 63, "excluded": 0}
```

Actual stdout for every killed mutant:

```text
{"assembled": 63, "kept": 0, "excluded": 63}
```

Stderr was empty for all 27 detector runs. Examples: `S/shapes/literal_heredoc/mutated.run.json:4-9`, `S/shapes/echo_full_call/mutated.run.json:4-9`, and `S/shapes/echo_full_call/restored.run.json:4-9`.

In the table, `X` means the exact named trace path and `A` means that receipt's shell-quoted argv tokens. Shape construction is at `S/probe-bind-v4-new.py:59-82`. Exact original and mutated commands, original transcript filename/line, call ID, and affected trace names are preserved in each shape's `mutations.json`.

| New shape | Forged command shape | Kept/63 | Wrongly kept entries | Exit | Verdict |
|---|---|---:|---|---:|---|
| `echo_full_call` | `echo python3 tools/trace-inputs.py --out X -- A` | 0/63 | None | 1 | killed |
| `python_c_string` | `python3 -c "print(<quoted full call>)"` | 0/63 | None | 1 | killed |
| `literal_heredoc` | Literal `cat` heredoc whose body contains the full call | 63/63 | All E01–E63 below | 0 | survived |
| `split_simple_commands` | `python3 -c pass --out X; python3 tools/trace-inputs.py -- A` | 0/63 | None | 1 | killed |
| `python_c_script_argument` | `python3 -c tools/trace-inputs.py --out X -- A; :` | 63/63 | All E01–E63 below | 0 | survived |
| `false_and_branch` | `false && python3 tools/trace-inputs.py --out X -- A; :` | 63/63 | All E01–E63 below | 0 | survived |
| `uncalled_function` | Full call inside a function definition that is never called | 63/63 | All E01–E63 below | 0 | survived |
| `quoted_separator_argument` | `printf '%s\n' literal ';' python3 tools/trace-inputs.py --out X -- A` | 63/63 | All E01–E63 below | 0 | survived |
| `changed_traced_argv` | Full call, but child argv changed to `python3 -c pass R31_DIFFERENT_ARGV` | 0/63 | None | 1 | killed |

Per-row output evidence: `S/shapes/<shape>/mutated.run.json:4-9`. For each survivor, the complete kept-entry list is at lines 10–263 of that file and the seat/trace bindings are in `mutated.receipt.json`. For each killed shape, `kept_entries` is empty; the first exclusion reason is `trace-without-executed-bash-call:ColdA01:ColdA01-1-1.json,ColdA01-1-2.json,ColdA01-1-3.json,ColdA01-1-4.json,ColdA01-1-5.json,ColdA01-1-6.json` (`S/shapes/echo_full_call/mutated.run.json:22-23`).

### Which entries were wrongly kept

E01–E63 are one-based entry positions in the frozen assembly, not unique section numbers. Repeated starts with different seats remain separate entries. Every survivor kept this entire set. `S/entry-index.json:1` preserves the full ordered headings and seat labels; its first joint-seat entry is at lines 16–23.

| Entry positions | Seat | Starts, in order |
|---|---|---|
| E01–E03 | ColdA01; E03 also names ColdB11 | 131, 375, 827 |
| E04–E06 | ColdA02 | 858, 921, 933 |
| E07–E09 | ColdA03 | 965, 1021, 1164 |
| E10–E12 | ColdA04 | 1212, 1246, 1272 |
| E13–E15 | ColdA05 | 1281, 1302, 1380 |
| E16–E18 | ColdA06 | 1479, 1499, 1517 |
| E19–E21 | ColdA07 | 1548, 1563, 1609 |
| E22–E24 | ColdA08 | 1754, 1806, 1814 |
| E25–E27 | ColdA09 | 1846, 1905, 1925 |
| E28–E30 | ColdA10 | 1938, 1964, 2104 |
| E31 | ColdA11 | 2132 |
| E32–E34 | ColdB01 | 375, 827, 858 |
| E35–E37 | ColdB02 | 921, 933, 965 |
| E38–E40 | ColdB03 | 1021, 1164, 1212 |
| E41–E43 | ColdB04 | 1246, 1272, 1281 |
| E44–E46 | ColdB05 | 1302, 1380, 1479 |
| E47–E49 | ColdB06 | 1499, 1517, 1548 |
| E50–E52 | ColdB07 | 1563, 1609, 1754 |
| E53–E55 | ColdB08 | 1806, 1814, 1846 |
| E56–E58 | ColdB09 | 1905, 1925, 1938 |
| E59–E61 | ColdB10 | 1964, 2104, 2132 |
| E62–E63 | ColdB11 | 131, 375 |

**Real false rejects: none in this fixture.** Every `pristine.run.json` has `kept=63`, `excluded=0`, and an empty `excluded_entries` array. Thus there is no rejected real entry or rejection reason to explain. This does not claim retention for untested data.

### Why the five shapes survive

The observed retention is detector output. The shell-semantics explanations below are source-based **[INFERENCE]**; no forged command was submitted for execution. Original result text was intentionally retained in the copied transcript, not presented as output from the replacement command.

1. **Literal heredoc.** The script invocation is data supplied to `cat`, not a shell command. v4 splits on newlines and inspects the body as a separate command without tracking heredocs (`B:74-78,96-103`). The exact first mutation is at `S/shapes/literal_heredoc/mutations.json:3-10`.
2. **Python `-c` argument.** Python treats `tools/trace-inputs.py` as source text after `-c`, not as a script path. v4 skips option tokens and then credits that token as a script (`B:130-135`). The final `:`, also present in the forged command, permits overall shell success without a trace run. Exact first mutation: `S/shapes/python_c_script_argument/mutations.json:3-10`.
3. **False `&&` branch.** The trace command is unreachable after `false`. v4 splits at `&&` and accepts its right-hand segment without considering reachability (`B:96-103`). Exact first mutation: `S/shapes/false_and_branch/mutations.json:3-10`.
4. **Uncalled function.** Defining a function does not execute its body. Newline splitting treats the body as an executed command without tracking function scope (`B:96-103`). Exact first mutation: `S/shapes/uncalled_function/mutations.json:3-10`.
5. **Quoted separator.** The `';'` token is an argument to `printf`; no second shell command exists. POSIX shlex removes its quotes, and v4 then classifies the resulting `;` string as a separator (`B:74,98-100`). Exact first mutation: `S/shapes/quoted_separator_argument/mutations.json:3-10`.

These cases retain matching receipt rev and argv, unique call IDs, and later non-error results. Their survival is therefore not the earlier error-result, reused-ID, result-before-call, comment-only, or different-tool control. The observed argv-mismatch kill also shows that a named output alone is not sufficient under v4.

### Exact restoration and hashes

Every shape saves original bytes before mutation and restores them in `finally`, then invokes the same bounded detector again (`S/probe-bind-v4-new.py:158-203`). Complete per-file SHA-256 maps are retained as `before-hashes.json`, `mutated-hashes.json`, and `restored-hashes.json` in each shape directory.

The manifest digest is SHA-256 of the sorted compact JSON map from relative filename to byte SHA-256 (`S/probe-bind-v4-new.py:50-56`). **All nine before/restored manifest digests were identical:**

```text
c8695ac5ac4eca083c4f3a51f2a0ccfa6155f9c0876702afa952cdc9c2ec17d4
```

| Shape | Mutated manifest SHA-256 |
|---|---|
| `echo_full_call` | `fc798718634d536bb846522d249c3fa0402c2c69b68d5c7eb76bca5d69229047` |
| `python_c_string` | `1cd4807dd757f40776092d2f09dbf0581d7546d13f8ad6209ff7454c7310453c` |
| `literal_heredoc` | `af563dd4e7660d3d0b82c684d68a42bb0abeb263f5b9c15c7cf3659c49edc45e` |
| `split_simple_commands` | `09f724babce560cfb709eedbc9ba19fd8108747ef4132d2a08276b8cfc93ca10` |
| `python_c_script_argument` | `5ccabdfe420c3a00babecef33ba8c2e970d379724c1221817af3919960aedb6d` |
| `false_and_branch` | `349c06894291ff69decac6fcffbde4094ce9c4e493c29e821bc33cc01d2f0ba6` |
| `uncalled_function` | `bc08ef7e7eeb2e326d39e358f8a70ff9b36dcfb2400d080d8345a913ef6fe041` |
| `quoted_separator_argument` | `d82b031ec60ca3b153079f21805139228580af708fb5a065313dfb30bb953c37` |
| `changed_traced_argv` | `84695dfb0455323daa29108c15cc525895173b223a7b1cb136d3800f7575af01` |

Example manifest/verdict evidence: `S/shapes/literal_heredoc/result.json:539-546,813`. Full evidence for every shape is also in `S/results.json`.

For `TameshiR30A3.ColdA01.jsonl`, the literal-heredoc before → mutated → restored byte hashes were:

```text
d4645d63c31c936be9f66da290650c31372bca006a8cc2d3756e6425918fcdd5
702d8fa0417aa74511179ad6da8fea778e8ef1c6f8db7ada067133f133c8924a
d4645d63c31c936be9f66da290650c31372bca006a8cc2d3756e6425918fcdd5
```

The binder, original assembly, and registry hashes were unchanged before/after (`S/results.json:2-12`):

| Frozen input | Before = after SHA-256 |
|---|---|
| binding v4 | `dd8bb39309cb337b4b0e6703657198fc88655ce4b498de2ad3f637e04030b87f` |
| original round-30 assembly | `f94929eb0f23335763fc42ffec71de83e8a4e19775c88900e74fd05fd1540eb2` |
| round-30 registry | `28562c5dc820f0932cbd027154f4f6ef6a98aac8da0babadeb8e1e4dbba02db8` |

The production binder's initial read-only SHA-256 matched the clone's binder. No production content was edited except this assigned report. No sibling scratch directory, fleet index, jj command, gate, C1 run, subagent, model, or alternate orchestration runtime was used. All subprocesses completed and were waited for; no process tree remains from this probe and no process was killed. No tools were installed or upgraded. Observed versions: Python 3.14.8; Git 2.56.0.

## Smallest safe correction

Leave frozen v4 and the round-31 predicate/target unchanged. Record these five survivors as coverage findings and qualify any interpretation of a kept count: v4's lexical binding is not sufficient evidence that the trace invocation actually executed. Preserve the observed real-data retention and four successful rejections alongside that limitation.

If a later, separately versioned binder claims execution, it would need to distinguish quoted operators, heredoc data, function bodies, Python `-c` operands, and unreachable branches rather than treating every matching token segment as an executed command. That is a future design requirement, not a patch or a claim that static parsing alone establishes execution.
