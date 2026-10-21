#!/usr/bin/env python3
"""Builds .ufo/waves/round-21/spec1.json (tameshi round 21, wave 1 BUILD)."""
import json
from pathlib import Path

L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
F = "/home/vgpnk/Projects/shokunin"
W = f"{L}/.ufo/waves/round-21/w1"
GOD = "/skill:godspeed\n" + Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
BASE = "33d03b716d3edcf1d8656d46d6df61801d232c52"

CONTEXT = f"""# Goal
tameshi round 21 (hyaku), wave 1 BUILD (advisory). Lane repo {L} (jj-colocated; branch master; frozen base {BASE}). The L1 (TameshiR21) holds the planner seat and is the ONLY integrator/committer. Stagnation nudge fires (depth 8 = calibration 8 = saturation line; no capability since round 15), so this is a frontier/capability round with two declared claims, frozen and committed BEFORE this dispatch at {BASE}:
- C1 operability: kill the 18 round-18 guard survivors in four owning tool selftests. Frozen population/ruler: {L}/.ufo/evidence/round-21/c1-mutants.json and c1-survivors.py. Baseline at 08175c6: killed 0/18, survived 18, all pristine controls green. Counting: `python3 {L}/.ufo/evidence/round-21/c1-survivors.py --repo <repo> --rev <rev> [--only ID,ID] --json` (it clones <repo> at <rev> privately; never writes <repo>).
- C2 coverage + capability: frontier F5 (hermetic environment normalization, {L}/corpus/README.md:82) -> Core. Frozen contract {L}/.ufo/evidence/round-21/c2-contract.json, counter c2-count.py; baseline 0/9 classified, no tool, no entry. Target: tools/env-diff.py with --selftest, receipt `.ufo/evidence/round-21/f5/receipt.json` (schema in the contract), knowledge entry `corpus/knowledge/hermetic-env-differential.md` whose `source:` header cites a mined S### row opened this round.
No-harm monitors (not claims): depth command D recorded_cases=8; calibration monitor `python3 .ufo/evidence/round-20/coldread/measure.py --repo R --rev REV --explain` = 61/61 credited, restraint 8 at {BASE}. That monitor is input-keyed: editing tools/*.py, corpus/SOURCES.md, README, PROVINCE, QUALITY or tools/registry.json UNCREDITS sections (L1 simulation: trace-inputs edit -> 46/61). Never edit SKILL.md or SHONEN.md.

# F5 profile protocol (shared by the env-diff tool and the independent surface probes)
Surface = one gate file materialised from git (`git -C {F}/<repo> show <rev>:<path>`) to R/target.<mjs|sh> where R is a fresh `mktemp -d /tmp/tameshi-r21-envdiff.XXXXXX` with R/home and R/tmp. Run `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w <env-prefix> <node|bash> /tmp/w/target.<ext> --selftest`, timeout 600 s. Profiles (exact): host = invoking env minus every GIT_* variable (env -u ...); clean = `env -i PATH=$PATH HOME=/tmp/w/home TMPDIR=/tmp/w/tmp LANG=C LC_ALL=C TZ=UTC`; clean_repeat = clean again in a fresh R; tz = clean but TZ=Pacific/Chatham; locale = clean but LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8; home = clean but HOME=/nonexistent; columns = clean plus COLUMNS=20 LINES=5 TERM=dumb. Tuple = (exit, sha256(stdout), sha256(stderr)), normalization "none". Classification: clean!=clean_repeat -> nondeterministic; all equal clean -> invariant; else env-sensitive with sensitive_to = sorted differing profiles. Pins (repo rev path blob_sha256) are exactly the 9 surfaces in c2-contract.json.

# Isolation and bounds (binding)
- Read-only everywhere except: (a) your Report file; (b) files your item names under {W}/ ; (c) your own scratch under /tmp/tameshi-r21-<YourName>-*. Never write the lane working tree outside {W}, never run git/jj mutating commands in {L} (no add/commit/checkout/stash/reset/jj anything); never touch the lane .git index, the fleet repo {F} (except reading), sibling repos, .ufo/state, MANIFEST.json, ~/.omp, ~/.gitconfig.
- Writers (executors that change lane files) work ONLY in a private clone: `git clone -q --no-hardlinks {L} /tmp/tameshi-r21-<YourName>-x/fleet/tameshi-shokunin && git -C <clone> checkout -q --detach {BASE}`, plus read-only symlinks /tmp/tameshi-r21-<YourName>-x/fleet/<sibling> -> {F}/<sibling> for every other fleet entry. Commit inside the clone (identity `-c user.name=seat -c user.email=seat@local`) so rulers can take --rev; deliver `git -C <clone> diff {BASE} <your-commit> > {W}/patches/<YourName>.patch` and name the clone commit in the report. The L1 integrates; you never patch the lane.
- Selftests / gates that run git or write files run only in scratch clones or bwrap sandboxes; scrub GIT_* from the environment; hostile git config/hook fixtures must live under a private temp dir and be activated only through per-process env/argv inside the fixture.
- Leaf seats: no subagents, no background jobs, no swarms (an executor may spawn at most one read-only labrat). Never message agent://all; message TameshiR21 only for a blocker.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths in every tool call.
- Tooling: read /home/vgpnk/.omp/agent/RULES.md first; installs via official channels only; ALL pacman transactions are PAUSED host-wide (no pacman -S/-Sy/-Syu/-U/-R; use uv tool / npx / official binary in ~/.local/bin, or report); record tool+version+channel+reason. Never pass a model parameter.
- Honesty: an unrun check has not passed; report exact commands, exit codes and output excerpts; mark inference [INFERENCE]; do not prettify failures.
# Report
One Markdown report at the absolute Report path: verdict line first (done / partial / blocked), then findings, exact commands with exit codes, evidence paths, disagreements and defects."""

def item(name, role, body, axes):
    return {"name": name, "role": role, "axes": axes, "prompt": GOD + "\n" + body.strip() + "\n"}

C1 = {
 "MB03": "bash-witness-study.py GIT_ env scrub narrowed to GIT_DIR/GIT_WORK_TREE only (a kill needs an inherited GIT_* variable other than those two, e.g. GIT_INDEX_FILE or GIT_OBJECT_DIRECTORY, that would corrupt/redirect the fixture repo)",
}
items = []
def ex(name, ids, desc):
    items.append(item(name, "executor", f"""
# Target
C1 writer for mutants {ids} in {L}/.ufo/evidence/round-21/c1-mutants.json. {desc}
# Change
In your private clone (context: Writers), add the smallest discriminating selftest case(s) to the owning tool's existing selftest so each listed mutant makes `python3 <tool> <selftest argv from c1-mutants.json selftest_argv>` fail while pristine stays green. Tests only: do not change guard/production logic. Name each new case after the guard it pins. Then commit in the clone and run the frozen ruler on YOUR commit: `python3 {L}/.ufo/evidence/round-21/c1-survivors.py --repo <clone> --rev <clone-commit> --only {ids} --json > {W}/c1/<YourName>.json` (also record stderr + exit). Also show the full owning selftest passes on pristine bytes of your commit. If a mutant is genuinely equivalent (no observable behaviour in any reachable environment), do not fake a kill: argue it with evidence and leave it SURVIVED.
# Acceptance
{W}/patches/<YourName>.patch (diff from {BASE}), ruler receipt with killed/survived per id, new case names and the exact failing SELFTEST lines each mutant produced.
""", ["operability", "calibration"]))

ex("E01BwEnvScrub", "MB03", "Tool tools/bash-witness-study.py (`selftest` subcommand). MB03 narrows the inherited-GIT_* scrub to GIT_DIR/GIT_WORK_TREE; a kill needs an inherited GIT_* variable other than those two (e.g. GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_NAMESPACE) to visibly break or redirect the witness fixture.")
ex("E02BwConfigPins", "MB04,MB05,MB06,MB07", "Tool tools/bash-witness-study.py. These remove/alter the GIT_CONFIG_GLOBAL=/dev/null and GIT_CONFIG_NOSYSTEM=1 pins of the child env; a kill needs a hostile global config (via HOME/.gitconfig, XDG_CONFIG_HOME, or a repo-root .gitconfig for MB05) and a hostile system config (via GIT_CONFIG_SYSTEM) whose effect the selftest observes. Fixtures only under private temp dirs.")
ex("E03BwHooksPins", "MB08,MB09,MB10", "Tool tools/bash-witness-study.py. These drop `-c core.hooksPath=/dev/null` from the fixture's git init/add/commit argv. Global/system config is already pinned, so consider argv-level pinning (capture the command vectors the fixture builder issues) and template-dir hooks (GIT_TEMPLATE_DIR / init.templateDir) — a kill must be behavioural or a stated command-pin contract; say which.")
ex("E04BwPrivateRoot", "MB11,MB12", "Tool tools/bash-witness-study.py. MB11 creates the selftest child tree in private_root.parent instead of private_root; MB12 makes cleanup remove a wrong child. A kill needs the selftest to assert containment of its temp tree and complete cleanup.")
ex("E05DispBranch", "D02,D12", "Tool tools/evidence-disposition.py (`--selftest`). D02 hardcodes the attached branch to master; D12 hardcodes the configured lane.branch ref to refs/heads/master. Both survived because every fixture uses master: add non-master attached-branch and non-master configured lane.branch fixtures (route recorded in .ufo/waves/round-18/w2/MutateDisposition18.md:82-110). jj fixtures need jj on PATH (~/.local/bin).")
ex("E06DispModes", "D11", "Tool tools/evidence-disposition.py. D11 refuses historical regular blobs with mode 100755 (TREE_MODES narrowed to 100644): add a historical 100755 regular-blob acceptance fixture (.ufo/waves/round-18/w2/MutateDisposition18.md:82-110).")
ex("E07RegTimeoutZero", "R02", "Tool tools/registry-check.py (`--selftest`). R02 accepts timeout_s == 0 (guard `0 < ts <= MAX_TIMEOUT_S`; re-anchored, see c1-mutants.json). Add the zero-timeout refusal case next to timeout-nan/-infinity/-overflow (~:1501).")
ex("E08RegChildScope", "R05,R07", "Tool tools/registry-check.py. R05 removes the baseline-child exclusion (pre-existing/unrelated children must be preserved, not killed); R07 removes the post-pidfd in_row_scope() ancestry re-check. Route and expected detectors: .ufo/waves/round-18/w2/MutateRegistryCheck18.md:116-170,262-296. Process-tree fixtures must be bounded and reap everything they start.")
ex("E09TraceInputs", "T04,T12", "Tool tools/trace-inputs.py (`--selftest`). T04 anchors the pycache prefix in the shared tempdir instead of the private workdir; T12 hashes the pathname instead of the file bytes. Route: .ufo/waves/round-18/w2/MutateTraceInputs18.md:135-193.")

items.append(item("E10EnvDiffTool", "executor", f"""
# Target
C2 capability writer: new tool tools/env-diff.py in your private clone (context: Writers), Python 3 stdlib only, implementing the F5 profile protocol in context EXACTLY and producing a receipt that the frozen counter accepts.
# Change
1. `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out .ufo/evidence/round-21/f5/receipt.json` runs every contract surface under all seven profiles (bounded concurrency <=3, per-run timeout 600 s, bwrap sandbox, GIT_* scrubbed) and writes schema tameshi-env-diff-receipt-v1: {{"schema", "contract_sha256", "host": {{uname, python, node, bash versions}}, "surfaces": [{{"surface", "pin": {{repo, rev, path, blob_sha256}}, "argv", "normalization": "none", "profiles": {{name: {{exit, stdout_sha256, stderr_sha256, seconds, stdout_tail, stderr_tail}}}}, "classification", "sensitive_to"}}]}}. It verifies each blob sha256 against the contract before running (mismatch -> refuse that surface, never classify). The runner surface has no frozen blob_sha256: record the actual one.
2. `python3 tools/env-diff.py --selftest` — hermetic fixture targets (tiny bash scripts) that are invariant, TZ-sensitive, locale-sensitive, HOME-sensitive, COLUMNS-sensitive and nondeterministic must classify exactly; plus pin-mismatch refusal and a missing-bwrap/timeout path. Final line `ENVDIFF_SELFTEST: N/N pass`, exit 0 only if all pass. Also a `--help`/usage exit 64.
3. Commit in the clone, generate the real receipt there, commit it, then run the frozen counter on your commit: `python3 {L}/.ufo/evidence/round-21/c2-count.py --repo <clone> --rev <commit> --json` (it will report f5_entry false — the entry is not yours; classified and tool_selftest must pass).
# Acceptance
{W}/patches/E10EnvDiffTool.patch (tool + receipt), counter output saved to {W}/c2/E10-count.json with exit code, per-surface classification table in the report with each sensitivity's evidence (stdout_tail diff).
""", ["coverage", "operability"]))

for i, s in enumerate(["tameshi-runner", "js-kimi-census", "bash-surface-census", "bash-tsukuroi-census", "bash-mado-verify", "bash-checklist-run", "js-claims-check", "js-round-gate", "js-sources-check"], 11):
    items.append(item(f"E{i:02d}Probe{''.join(p.title() for p in s.split('-'))}", "executor", f"""
# Target
Independent F5 probe of surface `{s}` (pin in {L}/.ufo/evidence/round-21/c2-contract.json), run by hand from the context's F5 profile protocol — independent of the env-diff tool being written concurrently (do not read or wait for it).
# Change
Materialise the pinned blob (verify sha256 first; mismatch = stop and report), run the selftest under all seven profiles in fresh sandboxes, write {W}/f5-probes/{s}.json with the same per-profile tuple shape as the receipt schema (exit, stdout_sha256, stderr_sha256, seconds) plus classification and sensitive_to. For every differing profile, diagnose the cause: the exact differing output lines and the gate source line(s) that read the variable or depend on it (cite <repo>@<rev>:<path>:<line>). Before running, pre-register your predicted classification in the report from reading the source; then report whether it held.
# Acceptance
The JSON file, the pre-registered prediction vs observed, and diagnosed causes. No writes outside {W} and your /tmp scratch.
""", ["coverage", "freshness"]))

items.append(item("E20ColdreadKit", "executor", f"""
# Target
No-harm kit for the input-keyed calibration monitor. Editing C1/C2 files uncredits SKILL.md sections (L1 simulation per single-file append at {BASE}: bash-witness 54/61, evidence-disposition 54, registry-check 58, trace-inputs 46, SOURCES 54, README 57, PROVINCE 56, QUALITY 59, registry.json 55; LOG/SCORECARD 61). Round 20 repaired the same harm with traced source re-anchors (.ufo/evidence/round-20/coldread/{{refresh-specs.json,refresh-receipts.json,traces/L1/}}, LOG.md round-20 entry, .ufo/waves/round-20/residual/).
# Change
In your private clone build {L}-relative `.ufo/evidence/round-21/coldread/`: (1) measure.py — the round-20 selector with ONLY its default ledger path/prefix changed to round 21 (same frozen algorithm, same override refusal); (2) ledger.json carrying all 199 round-20 entries byte-equal as data; (3) refresh.py with subcommands `plan --rev REV` (lists uncredited sections and, for each, the path set of its last credited entry, as refresh specs), `trace --rev REV --section START --seat NAME --out FILE` (runs tools/trace-inputs.py around the round-20 dump recipe on a private clone at REV, never the live lane), and `append --specs --traces DIR --verdicts DIR` (appends entries only for traced sections whose seat verdict file says accurate, labelled with seat provenance; original entries untouched; prefix-preserved check). Selftest it (`refresh.py --selftest`) on a synthetic repo. Commit in clone, deliver {W}/patches/E20ColdreadKit.patch and a demonstration: plan + trace + append on a clone commit where you appended one byte to tools/trace-inputs.py, showing credited 46 -> 61 or the exact residual.
# Acceptance
Patch, selftest output, demonstration receipts and the exact commands. State plainly that these are input re-anchors, not blind cold-reads.
""", ["calibration", "operability"]))

def crit(name, body):
    items.append(item(name, "critic", body, ["calibration"]))
crit("K01AttackC1Ruler", f"""
# Target
Falsify the frozen C1 ruler {L}/.ufo/evidence/round-21/c1-survivors.py + c1-mutants.json at {BASE}.
# Change
Read-only attack: can a KILLED verdict come from a setup/import crash rather than a behavioural assertion (it counts any nonzero exit)? Is the bwrap/env -i envelope representative of how the registry runs these selftests (tools/registry.json)? Is the R02 re-anchoring (round-18 `ts > 0` line rewritten by 9ee1c80) the same semantic mutant? Are the 18 exactly the round-18 named survivors (SCORECARD.md round-18 'Open next-round work'; .ufo/waves/round-18/w2/Mutate*18.md)? Run the ruler yourself at {BASE} (`--json`, all 18) and report exact counts.
# Acceptance
Concrete defects with reproductions, or a stated failure to falsify with the attempts listed.
""")
crit("K02AttackC2Counter", f"""
# Target
Falsify the frozen C2 counter {L}/.ufo/evidence/round-21/c2-count.py + c2-contract.json, and the claim that F5 can move to Core.
# Change
In a private clone, craft adversarial receipts/entries and commit them; show whether the counter accepts: a fabricated receipt with consistent but invented digests; wrong pins; missing profiles; mislabeled classifications; an entry citing a queued (not mined) S### row; header outside the first 15 lines. Check README :40-42/:68-88 and PROVINCE.md:40-42 rules for frontier->Core and whether the counter enforces them. Report which fabrications pass (a passing fabrication is a real defect: say how wave 2 should independently verify).
# Acceptance
Table fabrication -> counter verdict -> exit, with commands.
""")
crit("K03AttackNudgeHarm", f"""
# Target
Falsify the round framing in {L}/SCORECARD.md `## Round 21` section: the stagnation-nudge waiver, claim separability, and the no-harm plan.
# Change
Check AXES.md (/home/vgpnk/Projects/shokunin/AXES.md §The stagnation nudge) against SCORECARD `## Saturation` and `## Capabilities` (any capability since round 15?); whether C1 'operability, unscored' is a legitimate axis move; whether C1 and C2 are causally separable (shared files? registry.json, README); and whether the input-keyed calibration monitor (61/61 at {BASE}) will be harmed and how that must be repaired without overstating cold-read credit.
# Acceptance
Each framing point: holds / fails with evidence lines.
""")

def sen(name, body):
    items.append(item(name, "sentinel", body, ["operability"]))
sen("S01HostileFixtureSafety", f"""
# Target
Security review of the C1 test design space: tests adding hostile git config / hook / GIT_* env fixtures to tools/bash-witness-study.py, evidence-disposition.py, registry-check.py, trace-inputs.py at {BASE}.
# Change
Read-only. Enumerate the ways such fixtures could escape (writing ~/.gitconfig, running a hook in the live lane, inheriting into the live repo, leaving processes, following symlinks out of temp). Inspect how each tool's selftest currently creates its temp roots and child env. Produce a must-hold checklist the L1 will apply to every C1 patch, and check the current code against it.
# Acceptance
Checklist with code citations (path:line at {BASE}) and any current violations.
""")
sen("S02EnvDiffSandbox", f"""
# Target
Security review of the F5 profile protocol in context (running sibling gates' selftests under bwrap with seven env profiles).
# Change
Read-only plus harmless experiments in /tmp: verify the bwrap envelope really denies writes outside /tmp/w and network; whether `host` profile leaks secrets/tokens into receipts (stdout_tail fields!); whether a gate could reach the live lane or ~/.omp. Recommend redactions (e.g. no env dumps in receipts).
# Acceptance
Findings with reproductions; must-hold list for tools/env-diff.py.
""")

def mt(name, body):
    items.append(item(name, "mutation-tester", body, ["calibration", "operability"]))
mt("MT1C1Ruler", f"""
# Target
Mutation-test the frozen C1 ruler {L}/.ufo/evidence/round-21/c1-survivors.py (copy it to /tmp scratch; never edit the lane copy).
# Change
Single-point mutants of its guards (anchor-count check, pristine-control gate, timeout -> INCONCLUSIVE, KILLED/SURVIVED mapping, exit code). For each, run the copied ruler with --only on 2-3 ids against the lane at {BASE} and record whether its output would differ from the frozen baseline (killed 0 survived 18). Name guards no observation exercises.
# Acceptance
Mutant table with observed outputs; surviving guards named.
""")
mt("MT2C2Counter", f"""
# Target
Mutation-test the frozen C2 counter {L}/.ufo/evidence/round-21/c2-count.py (scratch copy only).
# Change
Single-point mutants of each rule (pin checks, profile presence, classification rules, tool selftest gate, mined-source check, exit mapping); build a small synthetic fixture repo (private clone with committed synthetic receipt/entry/SOURCES) to observe which mutants change the verdict. Report which counter guards are untested by any fixture.
# Acceptance
Mutant table, fixture commands, survivors.
""")
mt("MT3RouteMix", f"""
# Target
Mutation-test {L}/tools/wave-route-mix.py (scratch copy): its --selftest (8 cases) and the real refusal on {L}/.ufo/waves/round-20/spec1.json (exit 1, openai-codex 35/72).
# Change
10-12 single-point mutants (parser, alias resolution, share comparison, unrouted handling, exit mapping); run --selftest and the r20 refusal per mutant; record kills; propose missing cases.
# Acceptance
Kill table and proposed cases with exact expected outputs.
""")

def sc(name, body, axes=["coverage", "freshness"]):
    items.append(item(name, "scout", body, axes))
SRC = f"Follow /home/vgpnk/Projects/shokunin/CORPUS.md section 'SOURCES.md — where a shokunin learns' and the row shape in {L}/corpus/SOURCES.md (columns id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by). Open the source live today (2026-10-21), record URL, access time, version/footer, and a located quote of <=25 words that is present verbatim. Draft (do not write SOURCES.md) a proposed row with status mined or rejected (+reason), plus whether the URL duplicates an existing row (grep SOURCES.md). Write the draft row and the quote evidence in your report."
sc("SC01SrcReproLocale", f"# Target\nSource for F5: Reproducible Builds documentation on timezones/locales and SOURCE_DATE_EPOCH (reproducible-builds.org/docs/...).\n# Change\n{SRC}\n# Acceptance\nOne or two draft rows with located quotes relevant to TZ/LANG/LC_ALL normalisation of tool output.")
sc("SC02SrcPosixLocale", f"# Target\nSource for F5: POSIX.1-2024 XBD Chapter 8 Environment Variables (pubs.opengroup.org) — LC_ALL > LC_* > LANG precedence and TZ.\n# Change\n{SRC}\n# Acceptance\nDraft row(s) with located quotes.")
sc("SC03SrcCoreutilsEnv", f"# Target\nSource for F5: GNU coreutils manual `env` invocation (-i / --ignore-environment, -u) and bwrap(1) man page (--unshare-net, --tmpfs, --bind, --die-with-parent).\n# Change\n{SRC}\n# Acceptance\nDraft rows with located quotes.")
sc("SC04SrcGitConfigEnv", f"# Target\nSource for C1: git-config(1) ENVIRONMENT (GIT_CONFIG_GLOBAL, GIT_CONFIG_SYSTEM, GIT_CONFIG_NOSYSTEM) and git(1) ENVIRONMENT VARIABLES (GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_DIR...) at git-scm.com/docs.\n# Change\n{SRC} Also state, from the docs, which inherited variables would redirect a fixture repo (input for MB03-MB07 kills).\n# Acceptance\nDraft rows + the variable list with quotes.", ["coverage", "operability"])
sc("SC05SrcGitHooks", f"# Target\nSource for C1: githooks(5) (core.hooksPath) and git-init(1) TEMPLATE DIRECTORY (init.templateDir / GIT_TEMPLATE_DIR) at git-scm.com/docs.\n# Change\n{SRC} State whether a hook can fire during `git init`, `git add`, `git commit` (which hooks), relevant to MB08-MB10.\n# Acceptance\nDraft rows + hook-per-command table with quotes.", ["coverage", "operability"])
sc("SC06SrcNodeTz", f"# Target\nSource for F5: Node.js documentation on process.env.TZ / time zone handling and Intl default locale (nodejs.org/api).\n# Change\n{SRC}\n# Acceptance\nDraft row(s) with located quotes.")
sc("SC07SrcPythonTime", f"# Target\nSource for F5: Python 3 docs time.tzset()/TZ and locale module (LC_ALL) at docs.python.org.\n# Change\n{SRC}\n# Acceptance\nDraft row(s) with located quotes.")
sc("SC08ReopenF5Rows", f"# Target\nFreshness: reopen existing rows S015 (Cram), S016 (testscript), S028 (Bazel test encyclopedia) in {L}/corpus/SOURCES.md.\n# Change\nOpen each URL live; check the row's anchor/teaches quote is still present; report exact current wording, version, and any drift. Propose recheck/used-by old->new strings for a C2 citation (do not edit).\n# Acceptance\nPer row: holds/drifted with located quote.")
sc("SC09GateEnvKumitate", f"# Target\nPredict F5 sensitivity of the four kumitate surfaces (js-kimi-census, js-claims-check, js-round-gate, js-sources-check) from source at their pinned revs (c2-contract.json).\n# Change\nRead-only `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show <rev>:<path>`; list every env read (process.env, os.homedir, Date, Intl, toLocale*, localeCompare, sort, tmpdir, columns) with line numbers and the predicted profile effect. Pre-registration only: do not run them.\n# Acceptance\nPer-surface prediction table with line citations.")
sc("SC10GateEnvBash", f"# Target\nPredict F5 sensitivity of bash-surface-census, bash-checklist-run (kagi), bash-tsukuroi-census, bash-mado-verify and the tameshi runner (tools/mutate-and-run.sh at 08175c6) from source at their pins.\n# Change\nRead-only git show; list every env dependency ($HOME, $TMPDIR, LANG/LC_* via sort/grep/[[ ]] collation, date, TZ, COLUMNS, tput) with line numbers and predicted effect. Do not run them.\n# Acceptance\nPer-surface prediction table with line citations.")
sc("SC11ReconRegistry", f"# Target\nRecon for E07/E08: tools/registry-check.py at {BASE} — semantics of the timeout guard (~:239-250), baseline_children (~:480) and in_row_scope() (~:500-520); existing selftest cases and helpers a new case should reuse.\n# Change\nRead-only. Write the exact fixture recipe that would discriminate R02, R05, R07, with expected failing output.\n# Acceptance\nRecipes with line citations.", ["operability"])
sc("SC12ReconDispTrace", f"# Target\nRecon for E05/E06/E09: tools/evidence-disposition.py (branch resolution ~:460-480, TREE_MODES ~:549/645) and tools/trace-inputs.py (pycache ~:514, sha256 ~:656) at {BASE}; existing fixture builders.\n# Change\nRead-only. Exact fixture recipe per mutant D02, D11, D12, T04, T12 with expected failing output.\n# Acceptance\nRecipes with line citations.", ["operability"])

def rv(name, body, axes=["calibration"]):
    items.append(item(name, "reviewer", body, axes))
rv("RV01RerunC1Before", f"# Target\nIndependently rerun the C1 counting command at 08175c62d661fddf052ed10abc91313dec8eb77d and at {BASE}.\n# Change\n`python3 {L}/.ufo/evidence/round-21/c1-survivors.py --repo {L} --rev <rev> --json` (it clones privately). Compare with {L}/.ufo/evidence/round-21/c1-before.json (killed 0 survived 18).\n# Acceptance\nExact outputs/exits; agree/disagree.")
rv("RV02RerunC2Before", f"# Target\nIndependently rerun the C2 counting command at {BASE}.\n# Change\n`python3 {L}/.ufo/evidence/round-21/c2-count.py --repo {L} --rev {BASE} --json`; compare with c2-before.json (0/9, no tool, no entry). Also check every frozen pin in c2-contract.json resolves to its blob sha256 in the sibling repo (read-only git cat-file).\n# Acceptance\nOutputs, exits, pin table.", ["coverage"])
rv("RV03MonitorImpact", f"# Target\nCalibration no-harm baseline and impact map.\n# Change\nIn a private clone at {BASE} run `python3 .ufo/evidence/round-20/coldread/measure.py --repo <clone> --rev {BASE} --explain` (expect 61/61, restraint 8). Then map, per SKILL.md section, which input files its currently-crediting ledger entry depends on, and list sections that would lose credit if each of these changes: tools/bash-witness-study.py, tools/evidence-disposition.py, tools/registry-check.py, tools/trace-inputs.py, corpus/SOURCES.md, corpus/README.md, PROVINCE.md, corpus/QUALITY.md, tools/registry.json, plus new files only. Write the union list to {W}/monitor-impact.json.\n# Acceptance\nThe JSON + summary counts; whether new files (tools/env-diff.py, corpus/knowledge/new.md) affect credit.")
rv("RV04RegistryRows", f"# Target\n{L}/tools/registry.json rows that C1/C2 will touch.\n# Change\nRead-only: which rows run the four C1 tools' selftests and assert exact counts/strings that added cases would change; what a new env-diff selftest row and a wave-route-mix selftest row should look like (copy the existing row shape exactly). How the full battery is run on a branch-aligned scratch mirror (see .ufo/evidence/round-20/final/registry-final.* and SCORECARD round-20).\n# Acceptance\nExact proposed JSON rows and the exact battery command.", ["operability"])
rv("RV05RouteMixReview", f"# Target\n{L}/tools/wave-route-mix.py and its demonstration .ufo/evidence/round-21/routemix-r20-spec1.* .\n# Change\nReview correctness against the live ~/.omp/agent/config.yml (read-only): YAML shapes the regex parser could misread, fallback chains ignored by design (primary-only), threshold 0.40 rationale vs round-20 deaths (35 Codex + 13 Haiku, .ufo/evidence/round-20/... original-outcomes.json under .ufo/waves/round-20/). Is 'shown able to fail' satisfied?\n# Acceptance\nDefects or holds, with reproductions.", ["calibration", "operability"])
rv("RV06MistakeSweep", f"# Target\nMistake mining input for corpus/lessons/round-21.md `## Mistakes`.\n# Change\nSweep {L}/corpus/lessons/round-20.md, round-19-verifier-spotcheck.md, the round-20 report /home/vgpnk/Projects/shokunin/.ufo/reports/round-20/tameshi.md and any round-20 closure/verifier text in /home/vgpnk/Projects/shokunin (read-only grep for 'tameshi' + 'round-20'/'r20' in .ufo/reports and MANIFEST.json) for routed defects not yet turned into a QUALITY criterion or fix. Classify each: class, evidence pointer, captured-by, proposed fix that can be shown to fail.\n# Acceptance\nTable; say 'none found' with the sweep commands if none.")
rv("RV07ProvinceRules", f"# Target\nAdmission checklist for moving F5 to Core.\n# Change\nRead {L}/PROVINCE.md:40-42, corpus/README.md frontier sections (:68-122, round-12..20 appends), corpus/QUALITY.md admission criteria, AXES.md Capabilities. Produce the exact checklist an F5 knowledge entry + README/PROVINCE append + capability row must satisfy (header format as in corpus/knowledge/guard-kill-closure.md:1-4).\n# Acceptance\nNumbered checklist with line citations.", ["coverage", "calibration"])
rv("RV08SourcesContract", f"# Target\nSOURCES contract checklist for the new rows.\n# Change\nRead /home/vgpnk/Projects/shokunin/CORPUS.md SOURCES section, {L}/corpus/SOURCES.md (Registry, Paths, Search log, Leads, Id allocation), and /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (read-only). Next free id, required search-log entry shape, what triggers W04 duplicate warnings or errors, and how used-by/status changes must be logged in the lesson's ## Gate.\n# Acceptance\nChecklist + next id + a template search-log entry.", ["coverage"])
rv("RV09BatteryBaseline", f"# Target\nOperability no-harm baseline: full registered battery at {BASE}.\n# Change\nIn a branch-aligned scratch mirror (`git clone --no-hardlinks --branch master {L} /tmp/tameshi-r21-RV09BatteryBaseline-x/fleet/tameshi-shokunin` + read-only sibling symlinks), run `python3 tools/registry-check.py --root <mirror> --rev {BASE} --json`. Save JSON to {W}/battery-baseline.json.\n# Acceptance\nheld/total, failing rows with excerpts, exact command and exit.", ["operability"])
rv("RV10DepthBaseline", f"# Target\nDepth no-harm baseline at {BASE}.\n# Change\nCommand D from {L}/SCORECARD.md:73 (expect recorded_cases=8), and `bash tools/mutate-and-run.sh --regression` in a scratch clone (expect cases=8 passed=8). Save outputs under {W}/depth/.\n# Acceptance\nOutputs, exits, durations.", ["depth"])
rv("RV11CensusSources", f"# Target\nSource census and row-shape baseline.\n# Change\nRun `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and the row-count command from /home/vgpnk/Projects/shokunin/.ufo/reports/round-20/tameshi.md:84-86 on REV={BASE}; compare with {L}/.ufo/evidence/round-21/census-start.*.\n# Acceptance\nOutputs/exits; agree/disagree.", ["coverage"])
rv("RV12F5Definition", f"# Target\nCheck the frozen C2 contract against the F5 frontier definition.\n# Change\nCompare {L}/.ufo/evidence/round-21/c2-contract.json with corpus/README.md:82 (F5 row: 'runner selftest host vs env -i LANG=C TZ=UTC: identical (H3, round 1) -> the six gate selftests measured the same way') and .ufo/evidence/kaika-round-1/capability-demo/README.md H3. Is 9 surfaces x 7 profiles a faithful (not inflated or weakened) operationalisation? What would an honest Core statement say and not say?\n# Acceptance\nHolds/fails with lines; recommended bounds wording.", ["coverage", "calibration"])
rv("RV13PriorKills", f"# Target\nCheck whether any of the 18 C1 survivors were already addressed after round 18.\n# Change\n`git -C {L} log --format='%h %ad %s' --date=iso 58e5d53..{BASE} -- tools/bash-witness-study.py tools/evidence-disposition.py tools/registry-check.py tools/trace-inputs.py` and the round-19/20 lessons/SCORECARD: any partial kill, routed equivalence argument, or explicit decision to leave one open?\n# Acceptance\nPer-id status with evidence.", ["operability", "calibration"])

items.append(item("RG1IntentWitnessPins", "revenger", f"# Target\nOriginal intent of the bash-witness child-env and fixture pins (tools/bash-witness-study.py ~:330-340 GIT_* scrub/config pins; ~:1246-1270 hooksPath pins; ~:1681 cleanup) at {BASE}.\n# Change\nRead-only: git log -S / blame, the routed defect (R17-GIT-ENV in round-17/18 lessons and corpus/knowledge/guard-kill-closure.md), and say which threat each pin defends and therefore what behavioural kill would be faithful.\n# Acceptance\nPer pin: intent, evidence, faithful kill.", ["operability"]))
items.append(item("RG2IntentRegistryGuards", "revenger", f"# Target\nOriginal intent of registry-check's timeout guard, baseline_children exclusion and post-pidfd in_row_scope check at {BASE}.\n# Change\nRead-only history (git log -S, round-18 C2 R17-TIMEOUT, defect-probes.py, MutateRegistryCheck18.md) — what each defends; what a faithful kill observes.\n# Acceptance\nPer guard: intent, evidence, faithful kill.", ["operability"]))

def sb(name, body):
    items.append(item(name, "scribe", body, ["calibration", "coverage"]))
sb("SB01LessonDraft", f"# Target\nDraft {W}/drafts/lesson-round-21.md in the shape of {L}/corpus/lessons/round-20.md (## Claim, ## Gate, ## Mistakes, bounds).\n# Change\nMistakes to draft (class · evidence pointer · captured-by · fix): (1) provider concentration — round-20 wave lost 35/72 Codex + 13 Haiku seats; captured-by none; fix tools/wave-route-mix.py refusing .ufo/waves/round-20/spec1.json (evidence .ufo/evidence/round-21/routemix-r20-spec1.*), shown able to fail. (2) stale frozen anchor — R02's round-18 @old no longer present (rewritten by 9ee1c80); caught by the ruler's anchor-count guard; re-anchored before freeze. (3) L1's first pre-freeze ruler run used PATH=/usr/bin:/bin (no jj -> 3 jj fixtures failed) and `--selftest` for bash-witness (needs `selftest`), and those first diagnostic outputs were overwritten rather than retained. Mark where results are pending.\n# Acceptance\nDraft file; no lane edits outside {W}.")
sb("SB02QualityDrafts", f"# Target\nDraft QUALITY criteria 43-44 in {W}/drafts/quality-43-44.md, following {L}/corpus/QUALITY.md:388-419 style.\n# Change\n43: a wave spec is refused before dispatch when one primary provider would host >40% of seats (tools/wave-route-mix.py; falsifier: the round-20 spec). 44: a frozen mutant population is re-anchored and anchor-counted at the freeze revision before dispatch; a stale anchor is recorded, never silently dropped (R02).\n# Acceptance\nDraft text with falsifiers.")
sb("SB03EntrySkeleton", f"# Target\nDraft {W}/drafts/hermetic-env-differential.md knowledge entry structure (header lines source:/verified-at:/recheck:/ground: as {L}/corpus/knowledge/guard-kill-closure.md:1-4).\n# Change\nMethod (7 profiles, sandbox, tuple, classification rules from .ufo/evidence/round-21/c2-contract.json), what a classification can and cannot claim (invariance within these profiles only; not full hermeticity; repeat control is F3 ground), existing sources S015/S016/S028 summaries from corpus/SOURCES.md. Leave result tables as clearly marked sections for the L1 to fill from the receipt.\n# Acceptance\nDraft file.")
sb("SB04ReadmeProvince", f"# Target\nDraft appends in {W}/drafts/readme-province.md: corpus/README.md `## Round 21` (F5 status open -> held, entry row, capability) and PROVINCE.md `## Core — round 21 append` (F5 ground).\n# Change\nMatch the append-only style of README :283-322 and PROVINCE :73-83. Use 'pending L1 fill' markers only where results are not yet known.\n# Acceptance\nDraft file.")
sb("SB05LogDraft", f"# Target\nDraft the LOG.md round-21 entry skeleton in {W}/drafts/log-round-21.md (style: tail of {L}/LOG.md round-20 entry).\n# Change\nClaims, frozen commit {BASE}, baselines (C1 0/18 at 08175c6, C2 0/9), route-mix mistake fix, monitors; result slots marked.\n# Acceptance\nDraft file.")
sb("SB06SearchLog", f"# Target\nDraft the SOURCES.md round-21 Search log entry in {W}/drafts/search-log-21.md.\n# Change\nFollow the Search log section shape in {L}/corpus/SOURCES.md (identified/screened/included/excluded counts, stop rationale). Candidate sources: reproducible-builds locale/timezone docs, POSIX XBD ch.8, GNU env, bwrap(1), git-config/git(1) env, githooks/git-init templates, Node TZ, Python time.tzset; reopen S015/S016/S028.\n# Acceptance\nDraft entry with fields for L1 to fill counts.")
sb("SB07CapabilityRow", f"# Target\nDraft capability row + SCORECARD round-21 outcome table skeleton in {W}/drafts/scorecard-21.md.\n# Change\nCapability 'hermetic env-differential probe' (tools/env-diff.py) in the row shape of {L}/SCORECARD.md:238-247; outcome table shape as SCORECARD round 18 :673-678.\n# Acceptance\nDraft file.")
sb("SB08GuardKillAddendum", f"# Target\nDraft an append-only round-21 addendum for {L}/corpus/knowledge/guard-kill-closure.md in {W}/drafts/guard-kill-addendum.md.\n# Change\nHow each of the 18 survivors is to be recorded (killed by case X / equivalent with reason), referencing c1-mutants.json; slots for results.\n# Acceptance\nDraft file.")
sb("SB09ReportSkeleton", f"# Target\nDraft the fleet report skeleton {W}/drafts/report-tameshi-21.md with the required sections in order: Work performed, Landed changes, Before -> after measurements, Sources & frontier, Trend verdicts, SHONEN (per /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-21.md §4 and §6.6), modelled on /home/vgpnk/Projects/shokunin/.ufo/reports/round-20/tameshi.md.\n# Acceptance\nDraft file with slots.")
sb("SB10ErrataNotes", f"# Target\nDraft the round-21 'Source transitions' section (status/recheck/used-by old->new log) for the lesson in {W}/drafts/source-transitions.md, in the shape of corpus/lessons/round-20.md '## Source transitions and bounded search'.\n# Acceptance\nDraft file with slots.")
sb("SB11SourcesFrontierDraft", f"# Target\nDraft the report's Sources & frontier section in {W}/drafts/sources-frontier.md using the census start output {L}/.ufo/evidence/round-21/census-start.stdout (exit 0) and the row-count command from the round-20 report.\n# Acceptance\nDraft with before values filled, after slots.")

def sm(name, body):
    items.append(item(name, "simplifier", body, ["operability"]))
sm("SM1RouteMixLean", f"# Target\nYAGNI review of {L}/tools/wave-route-mix.py (proposal only; no lane edits).\n# Change\nDead code, redundant cases, simpler parse that keeps the 8 selftest cases and the round-20 refusal. Deliver a patch file at {W}/patches/SM1RouteMixLean.patch only if strictly smaller and behaviour-identical (show selftest + r20 refusal outputs on your scratch copy).\n# Acceptance\nPatch or 'no deletion warranted' with reasons.")
sm("SM2MeasureHelpers", f"# Target\nNamed debt 'duplicated measurement helpers' (SCORECARD round-18 open work): {L}/.ufo/evidence/round-1*/measure.py, round-20/coldread/measure.py, tools/receipt-measure.py, round-21 c1/c2 rulers.\n# Change\nRead-only inventory of duplicated helpers (clone/sha/env-scrub/bwrap), and a deletion-first consolidation proposal that never alters frozen historical rulers.\n# Acceptance\nInventory table + proposal.")
sm("SM3SelftestHelpers", f"# Target\nRead-only: existing selftest helper functions in tools/bash-witness-study.py, evidence-disposition.py, registry-check.py, trace-inputs.py at {BASE} that new C1 cases should reuse instead of duplicating.\n# Change\nList helper names, signatures, line numbers, and one-line usage for each mutant group (MB03-12, D02/D11/D12, R02/R05/R07, T04/T12).\n# Acceptance\nTable; the L1 uses it to reject duplicated scaffolding.")
sm("SM4RegistryRows", f"# Target\nRead-only YAGNI review of {L}/tools/registry.json: superseded rows still carried, duplicate argv rows.\n# Change\nProposal only; never remove historical rows that receipts cite.\n# Acceptance\nList with citations.")

items.append(item("CN1SiblingOverlap", "connector", f"# Target\nSibling-overlap scan for round 21's two claims.\n# Change\nRead-only across /home/vgpnk/Projects/shokunin/*-shokunin: does any sibling lane own env-hermeticity / locale / TZ normalisation (kumitate round-gate's env -i recipe, kama endpoint health, tsukuroi host updates)? Two-lane rule (PROVINCE.md:15-16): find env-normalisation evidence in two independent lanes. Any sibling already tracking provider-concentration of waves (fleet scripts/hyaku are fleet scope: report, never absorb).\n# Acceptance\nOverlap table with paths; contested scope named.", ["adjacency", "coverage"]))

spec = {"wave": "tameshi-r21-w1", "reportDir": ".ufo/waves/round-21/w1", "maxLanes": 100, "context": CONTEXT, "items": items}
Path(f"{L}/.ufo/waves/round-21/spec1.json").write_text(json.dumps(spec, indent=1) + "\n")
from collections import Counter
print(len(items), Counter(i["role"] for i in items))
