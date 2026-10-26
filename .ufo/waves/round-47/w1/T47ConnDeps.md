# T47ConnDeps — how sibling lanes state environment prerequisites and live-state dependence, compared with round-47 C1's `deps` clause

Seat: `T47ConnDeps` (connector, wave-1 of round 47, hyaku run 7 attempt 1) ·
lane `tameshi-shokunin` @ freeze `9acfbe21435e1976636a276448dee1d5e7155915`
Scope: read-only scan of sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin`
plus the fleet `.ufo/waves/` artifacts those lanes authored; comparison against
`.ufo/evidence/round-47/calibration/measure.py` and its frozen statements list.
Nothing was written outside this report; no lane, index, or jj state was touched;
no tool was installed (nothing was needed).

## Axes named (godspeed)

1. **calibration** — does the standing row's dependence clause say what the reader
   may conclude from it (prerequisite list vs observed differential vs hermeticity
   certificate)? This is C1's axis; the lowest non-retired axis at base (6).
2. **adjacency** — which sibling patterns are worth travelling into the lane's own
   method, and which are wrong to copy (they belong to a sibling's gate, not to
   tameshi's counter).
3. **operability** — does the clause survive a cold reader plus the deciding
   receipt without re-running the six-profile sweep by hand?

The move I propose improves (1) and (3), borrows from (2), and touches no other
axis. It does not judge any sibling's gate and proposes no edit to a sibling repo.

## Sibling inventory — path:line, what the lane states, the reproducibility verdict it makes

### kumitate — gate registry rows name their prerequisites and their fault classes

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `kumitate-shokunin/SKILL.md:728` | Cap-run hermetic suite row: "needs `systemd-run --user` and unprivileged bwrap" | **Prerequisite list, attached to the standing row.** The row's own text carries the two host capabilities; a reader of the checklist knows before running it what must exist. |
| `kumitate-shokunin/SKILL.md:742-745` | "Exit 2, or no verdict line at all, is a tool/environment fault (`--src` missing, empty scan set, unparsable surface JSON, a pin that no longer resolves to its recorded revision, a ratchet whose revision is stale): fix the tool, not the claim." | **Environment fault is separated from claim failure by exit code.** A missing capability is not a false claim; it is a different outcome class with a different owner. |
| `kumitate-shokunin/SKILL.md:637` | jj-seat-demo row: "Exit 2 is an environment fault (no jj/git/coreutils), never a pass." | Same separation, at the level of one named tool (jj). |
| `kumitate-shokunin/SKILL.md:816-818` | cite-check: "`--selftest` runs the hermetic 20-case fixture suite (fixtures only — live-tree assertions moved to `--integrations`, which is where a sibling lane's doc drift shows up)" | **Hermetic scope is stated by the tool's own split**, not by a promise in prose: the selftest is scoped to fixtures, live-tree assertions have their own name. |
| `kumitate-shokunin/SKILL.md:882` | proxy-check contract: "zero deps, node ≥20, READ-ONLY, no network" | **Dependency envelope as a closed list** on the tool's own row. |

### kagi — a row that cannot be exercised is *named* and *counted* in the verdict

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `kagi-shokunin/corpus/claim-ledger.sh:122-129` | "A row is a HOST row when its note carries `[host]` or `[substrate]`. `verify` and `cells` never run a host row by default; they print `HOST-SKIP <id>` and count `host_skipped=N`. Only the explicit flag `--allow-host-rows` runs them (no environment variable is honoured, so a parent shell cannot leak consent)." | **Non-exercise is a first-class, per-row, non-inheritable fact.** The skip carries a row id and a reason; consent is an explicit argv flag, so a parent shell cannot silently authorise a host read. |
| `kagi-shokunin/corpus/claim-ledger.sh:574-577` | the skip itself: `HOST-SKIP %s reason=host-row-not-authorized` and `C_HOST=$((C_HOST + 1))` | The reason string is machine-greppable; the count is a separate counter, not folded into the pass/fail tally. |
| `kagi-shokunin/corpus/claim-ledger.sh:1222-1232`, `:1256-1261` | every summary line carries `host_skipped=%d` — `CLAIM_LEDGER: CLEAN (… host_skipped=12)`, `CELL_AUDIT: CLEAN (… host_skipped=0)` | **"CLEAN" is never ambiguous about coverage**: the count of unrun rows travels inside the verdict line itself, so a reader cannot mistake a partially exercised ledger for a fully exercised one. |
| `kagi-shokunin/SKILL.md:750` | registry row: "`--allow-host-rows` is the only consent to run `[host]`/`[substrate]` rows" | Consent is spelled out where the gate is registered, not discovered in a script. |
| `kagi-shokunin/SKILL.md:756-760` | "Whole `verify` and `cells` are now safe-by-default entry points: a host row prints `HOST-SKIP <id>` and counts `host_skipped=N` instead of running" | The scope of what was *not* checked is stated as a durable contract, including the residual bound (a new wrapper script is not recognised by name). |

### chousa — name the executable, and say what is NOT claimed

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `chousa-shokunin/SKILL.md:73-74` | "The gate ran against a named, absolute grep binary, not the caller's `PATH` (round 35)." An override `RESEARCH_GATE_GREP` "must be an absolute path whose `--version` names GNU grep; anything else exits 2 with `research-gate: GREP_PROVENANCE refused:` **before a record is read**." | **Identity of the executed program, pinned by absolute path and self-reported version, with fail-closed refusal before any work.** The host's `PATH` is explicitly not trusted. |
| `chousa-shokunin/SKILL.md:642-651` | `grep_pin_init` resolves one absolute binary, verifies its own `--version` names GNU grep, refuses an unverifiable pin with exit 2, calls the absolute path directly — "never through `command`, which a caller can shadow with a `BASH_ENV` function" | Same, at implementation level: the shadowing vector is named, not just avoided. |
| `chousa-shokunin/SKILL.md:733-736` | "**What is NOT claimed.** C1 is PATH-independence, not tamper-proof hashing … C2 covers `BASH_ENV` only — the gate process itself already sourced the caller's startup file, and `ENV`/`SHELLOPTS`/`TMPDIR` are named debt." | **The negative space is stated next to the positive claim.** This is the single most transferable sentence I found in the fleet for a deps-style clause. |

### kotodama — graded fallbacks and a closed disposition vocabulary

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `kotodama-shokunin/reports/round-39/calib/Ca01-protocol.md:111` | Tier A — canonical: mount-namespace containment over a shared-object clone | **Tiered reproduction**, with the canonical tier named first. |
| `…/Ca01-protocol.md:189` | Tier B — "fallback without bwrap: real worktree + chdir shim (--check only)"; "Publish mode is forbidden in Tier B" | A fallback is not silently equal to the canonical path: each tier carries its own limits. |
| `…/Ca01-protocol.md:218` | Tier C — "last resort: rewrite-on-copy (altered-source replay) … It changes the executed bytes, so it does **not** satisfy 'reproduced under protocol' for an unmodified-bytes disposition" | **The tier caps the strength of the conclusion.** |
| `…/Ca01-protocol.md:240-253` | §9 disposition vocabulary: `reproduced-under-protocol` / `dispositioned-mismatch` (with named causes `clock`, `later-tree`, `later-fleet-state`, `named-input-drift`) / `confirmed-could-not-reproduce` ("only after Tier A and Tier B both fail with recorded diagnostics") | **Named cause classes instead of a smoothed scalar.** |

### kaidoku — typed refusals: absent-vs-wrong is a type, not a code

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `kaidoku-shokunin/SKILL.md:72-73` | "`provider_unavailable`, retryable:true | provider engine absent (`REA_PWNTOOLS_PYTHON`, `REA_IDA_MCP_CONFIG`) | operator-owned env key; retryable after provisioning" vs "`capability_unavailable`/`unsupported_provider`, retryable:false | tool absent (…`REA_BINWALK_COMMAND` 3.1.x, `REA_UNBLOB_COMMAND` 26.6.x…) | both kinds exit **1** — check `retryable`, not RC" | **Same exit code, different type.** The refusal says who owns the missing thing and whether retrying can help — information a bare exit code destroys. |

### souji — a missing prerequisite is its own exit class; a skip is never a pass

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `souji-shokunin/SKILL.md:189, :190, :196, :198` | verdict maps read "0 clean; 1 failed …; **2 could-not-evaluate missing prerequisite**" | **Third outcome class**, distinct from both clean and failed. |
| `souji-shokunin/SKILL.md:194` | "jj absent → the optional real-jj J9 arm SKIPs … SKIP is never PASS" | A skip is never laundered into a pass. |

### mado — environment gate with a named fallback branch

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `mado-shokunin/SKILL.md:300-303` | "**Environment gate** — all must pass; any fail → live layer UNKNOWN → file-byte branch" with the concrete checks (`command -v hyprctl` → `/usr/bin/hyprctl`, version line, `hyprctl configerrors` empty, instance count, signature shape check) | **Preconditions are enumerated as commands, and a failed precondition routes to a declared weaker evidence class (UNKNOWN → file-byte), not to a pass.** |
| `mado-shokunin/SKILL.md:781-784` | `bash tools/mado-verify.sh --no-live` "file plane only; verdict names the skipped live layer"; `--selftest` "hermetic fixture assertions (no substrate reads)" | The verdict names the scope it skipped, in the verdict line. |

### revenger — what a green replay is and is not

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `revenger-shokunin/SKILL.md:615-618` | "no current-host truth (the freshness rows are byte survival, frozen in `claims.md`). A green census or counter is a saved-input replay result against a committed tree; it is evidence of consistency, not of provenance." | **A replay verdict is scoped to the saved input.** |

### kama / kotoba / tsukuroi / kengaku — inherited prerequisites, declared prerequisites, override honesty

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `kama-shokunin/SKILL.md:870-871` | "Git>=2.45 remains an inherited prerequisite, not restored older-Git support or operator approval" | An inherited version floor is stated as a bound on what is claimed. |
| `kotoba-shokunin/SKILL.md:231-237` | "Every prerequisite — any binary, file, env var, or sibling artifact a body **procedure** assumes — has a **fail-closed** path stated … or is declared in `metadata.requires`. Carve-out: a tool named inside an evidence *recipe* … is a suggested reproduction path, not a runtime prerequisite" | **Declared prerequisites live in a separate field from recipe tools**, and each has a fail-closed path. |
| `kotoba-shokunin/SKILL.md:330-333` | "Every external command *and file path* named in the body resolves: binary on PATH (`command -v`), absolute path declared, file path resolvable … or a prerequisite check stated" | PATH resolution is a gate, not an assumption. |
| `tsukuroi-shokunin/SKILL.md:307-310` | "The `TSUKUROI_*` env overrides exist to make the selftest hermetic …; a live verdict produced with overrides would not be a measurement of the host — fixture runs only." | **A measure that alters the environment is labelled as a different kind of run.** |
| `kengaku-shokunin/SKILL.md:499` | "a hermetic gate must never read `/proc` — pin committed bytes instead" | Hermeticity is enforced by construction, not asserted. |

### mori / chousa (fleet wave artifacts, authored by those lanes)

| path:line | what it states | verdict about reproducibility |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/shokunin12h-20261014-p4-mori-r1/members/ThreatModel.md:171` | "`check()` uses `env -i`. `check_cli` does not, and only passes `--help` / `--bogus`, which exit before probes." | The lane records **where its env scrub does and does not apply** — an asymmetry stated, not hidden. |
| `…/p4-mori-r1/members/CensusIdempotence.md:71, :98` | fixture invocations under `env -i PATH="$FX/bin:/usr/bin:/bin" HOME=/tmp LC_ALL=C …` | Env scrubbing is in the invocation, reproducible by copy-paste. |
| `…/p5-chousa-r1/members/GateFixtureDesign.md:181-215` | an "Env | Role" table (fixture mode, pointer root, …) and `env -i PATH="/usr/bin:/bin" HOME="$WORK/home" … bash "$GATE" verify` | **Each env var has a stated role**; the empty HOME is part of the design, not an accident. |

### The lane's own prior art is finer than any sibling's

| path:line | what it states | verdict |
|---|---|---|
| `tameshi-shokunin/tools/env-diff.py:29` | `PROFILES = ("host", "clean", "clean_repeat", "tz", "locale", "home", "columns")` — seven profiles, one delta each | **One variable per profile**, so a difference is attributed to a named variable. |
| `tameshi-shokunin/tools/env-diff.py:40-54`, `:98-107` | per-profile env dicts; `classify()` returns `unavailable` / `nondeterministic` / `invariant` / `env-sensitive` | **Four-way classification**, including `unavailable` (missing process, timeout, red control) as its own class. |
| `tameshi-shokunin/corpus/knowledge/hermetic-env-differential.md:46-54` | decision table: "clean raw tuple differs from clean_repeat → nondeterministic → do not attribute profile differences to one environment variable"; "repeat-identical clean; one or more other profiles differ → env-sensitive → **Name exactly the differing profiles**" | The lane already knows how to say "which variable", and already knows that a difference without a repeat control proves nothing. |
| `tameshi-shokunin/corpus/knowledge/hermetic-env-differential.md:41-42` | "PATH remains a declared host dependency, not a pinned executable identity." | The lane's own stance: PATH is a dependency, not an identity. |

## Comparison with this round's C1 `deps` clause

What the clause is (`calibration/measure.py`):

* `DEP_NAMES = ('bwrap','env','fleet-root','jj','node')` (`:53`); `DEPS_RE = re.compile(r'deps `([a-z,-]+)`')` (`:56`);
  `CLAIM_CAP` (`:54`) requires, in one cell, `` → `value`, exit N, tool sha256 `hash`, deps `names` ``.
* The observed set is derived, not declared (`:302-307`): `env` when P0 (live host) differs from
  P1 (clean full profile); `bwrap`/`jj`/`node` when P2/P3/P4 (P1 minus that tool) differ from P1;
  `fleet-root` when P5 (P1 inside a bwrap-bound decoy fleet root) differs from P1.
* `comparable()` (`:234-240`): cap rows compare **(line, exit)**; axis rows compare **(line)** only.
* Profile construction: P0 = inherited env minus `GIT_*` plus `REV` (`:62-65`, `:177-179`);
  P1–P4 = fixed env whose `PATH` is a shim directory of `/usr/bin` symlinks plus `node`/`jj`/`jq`
  symlinked from `shutil.which` (`:156-189`); P5 = P1's env under `/usr/bin/bwrap --bind <decoy> <FLEET>`.

### Measured evidence (sanctioned `--only` probes, scratch only, exit never a verdict)

`--only depth,calibration` at the freeze rev → all three axis rows identical across P0..P5
(`depth_score=9`, `calibration_restraint_score=6`, `freshness score=9`), `observed_deps=none`,
and each axis row `UNPARSED` because at the freeze revision the rows do not yet carry a deps
clause (the lane's own control `control/controls-at-freeze.stdout` CTL_I: `unparsed=22`).

`--only "hermetic env-differential probe,mutation report interop,effective expectation reconciliation"`:

```
hermetic env-differential probe   P0=ENVDIFF_SELFTEST: 9/9 pass   P1=2/9 pass  P2=2/9  P3=2/9  P4=1/9  P5=2/9   → env,node
mutation report interop           P0=17/17 pass  P1..P3=17/17  P4=UNOBSERVABLE|exit=2  P5=17/17                 → node
effective expectation reconciliation P0=66/66  P1=P2=66/66  P3=UNOBSERVABLE|exit=1  P4=P5=66/66                → jj
```

`--only "six-leg regression ledger,retained invocation-context gate"`:

```
six-leg regression ledger   P0..P3=REGRESSION: PASS (cases=9 passed=9)  P4=SETUP (cases=9 passed=4)  P5=SETUP (cases=9 passed=0) → fleet-root,node
retained invocation-context gate  P0..P4=SELFTEST: PASS (49/49) exit 0   P5=SELFTEST: PASS (49/49) exit 1                     → fleet-root
```

These reproduce the lane's own control CTL_J exactly (`dep_mismatch=5`, same five statements, same
dep sets) at a different revision (CTL_J ran at `21463350…`, my probes at the freeze `9acfbe21…`),
and CTL_K already shows the format is achievable: with per-row correct deps the counter prints
`dep_mismatch=0 total=0 C1_R47_PASS=true` (`rev=de46947f…`).

### What the comparison shows — five contradictions, stated not smoothed

1. **The deps clause is an observed differential, but reads like a prerequisite list.**
   Of the five non-empty dep sets the lane has observed, the *effect* of each axis differs:
   * **absence** (the statement could not be observed at all): `jj` for `effective expectation
     reconciliation` (P3 `UNOBSERVABLE|exit=1`), `node` for `mutation report interop`
     (P4 `UNOBSERVABLE|exit=2`);
   * **substitution** (a different value printed): `env` for `hermetic env-differential probe`
     (9/9 → 2/9), `node` for the same row (2/9 → 1/9), `fleet-root` + `node` for `six-leg regression
     ledger` (PASS → SETUP 0/9 / 4/9);
   * **exit-only** (identical printed line, different exit): `fleet-root` for `retained
     invocation-context gate` (49/49 exit 0 → 49/49 exit 1).
   A cold reader of `deps \`jj\`` cannot tell which of the three it is, and the three lead to
   different readings: "the tool must exist", "the value depends on the tool's version or
   behaviour", "only the exit status is sensitive".
2. **The contract names one comparison tuple; the counter uses two.**
   `contract.json` C1.statement says the deps clause equals the set observed "by comparing its
   **(line, exit)**" under the six profiles. `measure.py:234-240` compares (line, exit) for the 19
   cap rows but **(line) only** for the 3 axis rows (`depth`, `calibration`, `freshness`), and
   `observe()` (`:220-224`) never records an exit code for an axis row. Harmless at the freeze
   (measured: all three axis rows byte-identical across P0..P5), but it is a latent divergence in
   a frozen instrument between the contract's stated method and the instrument's method.
3. **`fleet-root` is confounded with bwrap confinement.** P5 is P1 *plus* the bwrap wrapper
   (`:212-213`: `/usr/bin/bwrap --die-with-parent --bind / / --dev-bind /dev /dev --bind <decoy> <FLEET>`),
   whereas the `bwrap` axis (P2) is bwrap removed from `PATH`. A P5 difference therefore cannot be
   attributed to the decoy root alone from the receipt.
4. **The "clean" profile is not host-independent.** `build_shim` (`:156-173`) symlinks `/usr/bin`
   and then adds `node`/`jj`/`jq` from `shutil.which` on the *deciding shell's* `PATH`. Measured
   on this host: `node` → `/run/user/1000/fnm_multishells/13812_1792946939276/bin/node` (an fnm
   session path), `jj` → `/home/vgpnk/.local/bin/jj`. So P1–P4 inherit the deciding session's node
   location; the `node` axis means "node absent", while node's identity is ambient.
5. **`env` is one coarse bucket.** P0-vs-P1 changes `PATH`, `HOME`, `TMPDIR`, `LANG`/`LC_ALL`,
   `TZ` and every other inherited variable at once, so `deps \`env\`` cannot name which variable
   moved. The lane's own `tools/env-diff.py` (7 one-delta profiles, 4-way classification) already
   does this properly.

### Which sibling pattern is better than the deps clause, and why

* **Better on "what may I conclude" — kumitate's exit map (`SKILL.md:742-745`, `:637`) and
  kaidoku's typed refusals (`SKILL.md:72-73`).** Both separate *the capability was absent* from
  *the claim is wrong*, using a field (exit code / `retryable` type) rather than prose. The
  deps clause has no such field: `jj` and `env` are the same token kind even though one means
  "the row could not be observed" and the other "the row printed something else".
* **Better on "what was not checked" — kagi's `HOST-SKIP <id> reason=…` + `host_skipped=N`
  (`claim-ledger.sh:122-129`, `:574-577`, `:1222-1261`).** The count of unrun rows travels inside
  the verdict line, so `CLEAN` is never ambiguous about coverage. C1's deps clause carries the
  opposite property: it names the axes but says nothing about *how* each axis behaved, and the
  deciding receipt's `PROFILES` lines are where that behaviour actually lives.
* **Better on negative space — chousa `SKILL.md:733-736`** ("What is NOT claimed … PATH-independence,
  not tamper-proof hashing … `ENV`/`SHELLOPTS`/`TMPDIR` are named debt") and revenger
  `SKILL.md:615-618` ("evidence of consistency, not of provenance"). Both bound the claim next to
  the claim.
* **Better on named causes — kotodama `Ca01-protocol.md:240-253`**: a closed vocabulary of causes
  instead of one scalar.
* **Better overall than any sibling: the lane's own `tools/env-diff.py` / `hermetic-env-differential.md`
  (one delta per profile, `unavailable` as its own class, "Name exactly the differing profiles").**
  It is in-lane, already committed, and already sourced; the round-47 `deps` axis set is a coarser
  instance of the same idea.

### Which sibling pattern would be wrong to copy into tameshi's method

* **souji's `SKIP` for an absent tool (`SKILL.md:194`)** — wrong here: C1's population is a frozen
  22-statement list pinned by sha256; a skip would shrink the denominator silently, and the deps
  clause's whole purpose is to name the missing axis instead of dropping the row.
* **kotodama's Tier B/C fallback (`Ca01-protocol.md:189`, `:218`)** — wrong as a reproduction
  strategy for the deciding run: Tier B/C changes the worktree, the executed bytes, or the
  confinement, so the observation would no longer be the observation C1 states. (The *vocabulary*
  half — named causes, capped conclusion strength — is borrowable; the execution half is not.)
* **chousa's absolute-binary pinning (`SKILL.md:73-74`, `:642-651`)** — wrong as a mechanism for
  C1: C1's tool sha256 is a digest of the tool *file*, and pinning the interpreter would change
  what the standing row states about the command. (Its *negative-space* half is borrowable.)
* **kotoba's `metadata.requires` declaration (`SKILL.md:231-237`)** — wrong as a semantics change:
  a declared prerequisite list is what the author believed; C1's clause is what the measurement
  observed. Substituting "declared" for "observed" would be a downgrade, and the control
  `CTL_J` (every row says `deps none` → `dep_mismatch=5`) is exactly the failure mode a declared
  list produces.
* **kumitate's blanket "fix the tool, not the claim" (`SKILL.md:742-745`)** — wrong to apply
  wholesale to a drift-detecting monitor: a dependency-induced difference and a genuine drift must
  stay distinguishable, otherwise a real drift would be filed as an environment fault.
* **mado's "environment gate → file-byte fallback" (`SKILL.md:300-303`)** — wrong to import: it is
  a routing rule for a live-substrate gate, and C1 has no weaker evidence class to fall back to;
  C1's own classes are already correct (`UNOBSERVABLE` is counted separately from `MISMATCH`).

## The one bounded move (connector proposal — travels in this report; no sibling edit)

**Give the standing row a *basis* clause next to the machine-checked `deps` clause, so the deps
set cannot be over-read as a prerequisite list — and derive the basis from the deciding receipt
rather than from a new claim.**

Concretely, in the round-47 SCORECARD block (append-only, after the last existing row):

1. Keep every row's existing machine clause byte-for-byte in the shape the frozen counter parses:
   `` → `value`, exit N, tool sha256 `sha`, deps `names` ``. This part is verified by C1 and must
   not change. (Parse tolerance was checked directly against `claim_of()`: text appended *after*
   the parsed clause does not alter the parsed `(value, exit, sha)` triple or the dep set; the
   token `deps \`` must not be reused inside the appended text, so use a different key.)
2. Add one **static, method-level** sentence per row — or one shared paragraph for the whole
   round-47 block, which is cheaper and less drift-prone — that states the basis of the clause:
   * the comparison tuple actually used per row kind: (line, exit) for capability rows,
     (line) for axis rows (contradiction 2, stated rather than smoothed);
   * what each axis means: `env` = P0 (live host, inherited env minus `GIT_*`) versus P1 (fixed
     env: shimmed `PATH`, scratch `HOME`, `LANG`/`LC_ALL=C`, `TZ=UTC`); `bwrap`/`jj`/`node` =
     P1 minus that tool from the shimmed `PATH`; `fleet-root` = P1 under `bwrap` with a decoy
     root bound over the fleet root — i.e. **also** under bwrap confinement, so the axis is
     confounded (contradiction 3);
   * that the clause is an **observed differential over six profiles on this host**, not a
     prerequisite list and not a hermeticity certificate, and that a named axis means "the
     comparison moved", which may be absence (`UNOBSERVABLE`), substitution, or exit-only change
     (contradiction 1);
   * the residual live-state debt in the lane's own words (chousa's pattern): the `node` identity
     in P1–P4 is the deciding shell's `shutil.which` result — an fnm session path on this host —
     so PATH is a declared host dependency, not a pinned executable identity
     (contradiction 4), and `env` is one coarse bucket that does not name which variable moved
     (contradiction 5; the finer per-variable method is `tools/env-diff.py`, not adopted here
     because changing the frozen counter's profile set would be an amendment).

Why this and not more: it improves calibration (the standing row's claim is no longer stronger
than the instrument), improves operability (a cold reader learns the clause's meaning from the
row, not from re-running six profiles), and costs one paragraph — it does **not** touch the frozen
counter, the frozen statements list (sha256 `924102df…`), the append-only prefix rule, or any
sibling repo. It borrows three sibling patterns (chousa's negative space, kagi's
"what was not checked is visible", kotodama's named causes) and refuses four (souji's skip,
kotodama's fallback execution, chousa's binary pinning, kotoba's declared list).

**Circularity risk and how it is avoided.** Per-row effect kinds ("absence" vs "substitution")
depend on the deciding run, so they must **not** be written into the SCORECARD before that run.
They belong in the committed deciding receipt, which already prints `PROFILES <id>: P0=… P5=…` and
`STATEMENT … observed=… (exit=N)` per statement (`measure.py:320-325`). The SCORECARD paragraph
carries only the **frozen method facts** (tuple per kind, profile construction, axis meaning,
negative space) — properties of the pinned counter, not of a run — so it can be written before the
deciding run and re-verified against it afterwards. This is the round-43 lesson applied
pre-emptively: the record must agree with the tree at the landing commit, so a method fact stated
in prose is safe only if it is a property of pinned bytes.

**Affected axes:** calibration (C1, +), operability (reading the row, +), adjacency (borrows from
siblings, +). Untouched: C2 (operability claim), C3 (coverage claim), the no-harm monitors.

## Verification of this report's own claims

| claim | how it was checked | result |
|---|---|---|
| the five dep sets and their effects | counter `--only` probes at the freeze rev, scratch under `/tmp/tameshi-r47-T47ConnDeps/` | reproduced CTL_J's five dep sets; effect kinds read off the printed per-profile tuples (2 absence, 3 substitution, 1 exit-only across the five) |
| axis rows are compared by line only | `measure.py:220-224`, `:234-240` read; axis rows probed across P0..P5 | all three identical across six profiles; `observed_deps=none` |
| appended text after the parsed clause does not change the parse | direct call into the frozen `claim_of()` with three evidence strings (plain / tagged / duplicate-deps) | all three returned the same `(value, exit, sha)` triple and the same dep set |
| P0/P1–P5 profile construction | `measure.py:62-65`, `:156-189`, `:212-213` read | as described; `node` resolved to an fnm session path, `jj` to `~/.local/bin/jj` on this host |
| sibling quotations | every path:line above read or grepped in place under `/home/vgpnk/Projects/shokunin/` | quoted text matches the cited lines; no citation is from memory |
| no lane mutation | only this file was written; no `git`/`jj` write command run in any lane; no sibling edited | clean |

Tool installs / updates: **none** (no tooling was needed; the probes used the lane's own python3
and the host's `bwrap`/`jj`/`node` as found). No pacman transaction; the host-wide pacman pause
was honoured.

Report: `.ufo/waves/round-47/w1/T47ConnDeps.md`
