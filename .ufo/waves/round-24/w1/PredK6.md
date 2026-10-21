# PredK6 — falsification of frozen predicate K6 (`source-read-red-substitution`)

**Verdict: K6 is sound on the delivered revision — it cannot pass vacuously, it passes for
exactly the intended reason (the frozen `bundle_sha256` literal pin in the registry row), and
the base receipt in `before.json` is honest and byte-reproducible. Three calibration
defects remain, none of which falsifies the round-24 claim: (F1, latent) the frozen ruler
credits K6 whenever the row stops being held, without asserting that the substituted pair
is still a *self-consistent red* bundle — a concrete counterexample exists; (F2, moderate)
K6 has **zero** discrimination power over tool-side code, so it is blind to a plausible
weakening (removal of the `SNAPSHOT_TAMPERED` verification), which is caught only by the
separate selftest row; (F3, low) the ruler's `any(...)` semantics would not notice an
unpinned active row coexisting with the pinned one.**

Reviewed revision: `c8c5b88c8e961a929cdc351b95a7074c76958909` (`git rev-parse HEAD`).
Base under attack: `6a1821a8897eea6e7d9669292160ec9593669409`.
Lane: leaf reviewer — no subagent dispatch, no labrat probe spawned.
Lane bounds honoured: no production file edited; **no** registry battery, gate or selftest
executed inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; all execution happened in
`/tmp/k6/**` trees extracted with read-only `git archive`; git use was read-only
(`log`/`show`/`diff`/`archive`, `GIT_OPTIONAL_LOCKS=0`).

---

## Axes (godspeed)

| Axis | Question for K6 | Answer |
|---|---|---|
| **Vacuity** | Can K6 be green without the red row ever running or without the pin existing? | No. Control requires `held is True` from a real row execution; any parse/shape error degrades to `None` and the predicate is *not* credited. |
| **Wrong reason** | Can the row fail after substitution for a reason other than the digest pin? | Not on the delivered ruler: the only failing expectation is the pinned literal (`stdout_missing` = exactly one entry). A latent path exists (F1). |
| **Discrimination** | Does K6 discriminate a plausible weaker implementation? | Yes for the routed defect (the missing pin) and for a regenerated bundle+expected pair. No for tool-side weakenings that leave digest computation intact (F2). |
| **Base honesty** | Is `before.json` (1/11) reproducible with the frozen ruler? | Yes — reproduced exactly (1/11, K6 control True / substituted True) with the byte-identical ruler. |

---

## What the frozen predicate actually is

`.ufo/evidence/round-24/measure.py:38-43` freezes the K6 pin pair:

```python
PINS = [
    ('K5', 'frozen-clean-substitution', '.ufo/evidence/round-23/replay/bundle.json',
     '.ufo/evidence/round-23/replay/expected.json'),
    ('K6', 'source-read-red-substitution', '.ufo/evidence/round-23/source-read-bundle.json',
     '.ufo/evidence/round-23/source-read-expected.json'),
]
```

The K6 code path (`measure.py:92-137`):

* `registry_rows_for(root, path)` (`:92-95`) — active registry rows whose `argv` element equals the bundle path.
* `held(root, name)` (`:97-104`) — runs `tools/registry-check.py --root R --only NAME --json` and returns
  `rows[0]['held'] is True`; on any parse/shape error it returns `None` (never a silent pass).
* `substitute(root, 'K6', bundle, expected)` (`:107-117`) — appends `'\n'` to `receipts[0]['stdout']`,
  re-serialises `json.dumps(value, sort_keys=True, indent=2) + '\n'`, writes the bundle, and **rewrites the
  expected file with the new digest** (so the pair stays self-consistent).
* credit rule (`:133-135`): `all(control held is True) and any(after held is False)`.

Production surface exercised: `tools/registry.json:980-988` (active row
`command-binding-source-read-red-pinned`, `expect.exit = 1`,
`expect.stdout_contains = ['"finding_ids": ["ARGV_MISMATCH"]',
'"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf"']`),
its superseded predecessor `tools/registry.json:949-958`, and `tools/command-binding.py:115-130`
(`check()`: recompute digest over raw bundle bytes, `SNAPSHOT_TAMPERED` on mismatch) plus
`tools/command-binding.py:209-213` (report fields `exit`, `finding_ids`, `bundle_sha256`).
Row-level `held` semantics: `tools/registry-check.py:718-720`
(`held = got == expected_exit and not missing and cleanup_ok`, `missing` = stdout tokens absent).

The routed defect this predicate closes is verbatim at
`.ufo/waves/round-23/fresh-adjudication.json:61-67`: *"The command-binding-frozen-clean and
source-read-red registry rows do not pin bundle_sha256 literals, so a regenerated bundle and
expected pair would still hold."* (S085, quoted in `corpus/lessons/round-24.md:40-41`).

---

## Method (read-only inspection + private `/tmp` clones)

1. Extracted both revisions read-only: `git archive c8c5b88 | tar -x -C /tmp/k6/delivered`,
   `git archive 6a1821a | tar -x -C /tmp/k6/base`.
2. Replayed the **frozen** K6 path verbatim by importing the delivered `measure.py` and calling its own
   `registry_rows_for` / `held` / `substitute` (no re-implementation, no transcription risk).
3. Ran the frozen ruler end-to-end against the base tree and against the delivered tree.
4. Ran targeted mutations in `/tmp` copies only.

---

## Evidence

### E1 — K6 discriminates on the delivered revision, and for the intended reason

```
$ python3 /tmp/k6/k6probe.py /tmp/k6/d1        # frozen measure.py helpers, delivered tree
active rows naming bundle: ['command-binding-source-read-red-pinned']
control: {'command-binding-source-read-red-pinned': (True, 0)}
after  : {'command-binding-source-read-red-pinned': (False, 1)}
K6 discriminated = True
```

Registry-level detail (same tree, before/after the substitution), from
`tools/registry-check.py --only command-binding-source-read-red-pinned --json`:

```
control : exit 0 | {"expect":1,"got":1,"held":true,"elapsed_s":0.307}
          stdout_tail: {"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf",
                         "exit": 1, "finding_ids": ["ARGV_MISMATCH"], "schema": "command-binding-report-v1"}
after   : exit 1 | {"expect":1,"got":1,"held":false,
                    "stdout_missing": ["\"bundle_sha256\": \"db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf\""]}
```

Read that carefully — it is the whole answer to "wrong reason?": after substitution the row still
**executed** (`got == expect == 1`), the red finding is **unchanged**
(`finding_ids == ["ARGV_MISMATCH"]`), and the *single* failing expectation is the pinned digest
literal. The pin is the discriminator; nothing else moved.

### E2 — the substituted bundle really is "another self-consistent red bundle"

The re-serialisation is byte-exact, so K6's mutation is a single appended `'\n'` inside
`receipts[0].stdout` and nothing else:

```
orig sha    db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf
recanon sha db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf   identical bytes: True
```

And the substituted pair is self-consistent (the tool's own tamper check does **not** fire):

```
bundle substituted, expected NOT updated -> exit 2 {"finding_ids": ["SNAPSHOT_TAMPERED"], ...}
bundle + expected both substituted      -> exit 1 {"finding_ids": ["ARGV_MISMATCH"], "bundle_sha256": "de5c3bf0..."}
```

So the adversary input is exactly the adversarial shape K6 claims to cover: a *different but
self-consistent* red bundle whose regenerated expected file agrees with it.

### E3 — the routed defect's own wording ("a regenerated bundle and expected pair") is caught

Re-serialising the **same semantic bundle** with `indent=4` and regenerating the expected file
(a true regeneration, not a byte tweak):

```
regenerated-pair tool exit 1 {"bundle_sha256": "7bdd8f56ccb8c2ce92c5dd208d1cf982933f7dd9ee1e9547405be45ebafd0dea",
                               "exit": 1, "finding_ids": ["ARGV_MISMATCH"], ...}
registry-check exit 1 held=False stdout_missing=['"bundle_sha256": "db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf"']
```

### E4 — the pin cannot be faked by echoed bundle content

`grep -c db620668… source-read-bundle.json` → `0` (the literal occurs nowhere in the bundle), and
the tool's report carries four scalar fields only (`tools/command-binding.py:210-211`). The
substring check in `tools/registry-check.py:718` therefore cannot be satisfied by bundle payload.

### E5 — base receipt honesty (1/11 reproduced exactly; K6 correctly not credited at base)

The frozen ruler is immutable and matches the receipt's recorded instrument hash:

```
$ sha256sum .ufo/evidence/round-24/measure.py
0a7f6daa7ddaa0ef0b4140c20f5e3eef91b781f2d3119e1819c83191e57daa64   == before.json instrument_sha256
same sha at e338f1b, d2eaecd, bd38c02, c8c5b88  (git log -- .ufo/evidence/round-24/measure.py → one commit only)
```

Re-running the frozen ruler against an extracted base tree:

```
$ python3 /tmp/k6/delivered/.ufo/evidence/round-24/measure.py --repo /tmp/k6/base
discriminated 1 of 11
K1 disc=False  K2 disc=False  K3 disc=False  K4 disc=True
K5 rows=['command-binding-frozen-clean'] control={'…': True} subst={'…': True}  disc=False
K6 rows=['command-binding-source-read-red'] control={'…': True} subst={'…': True}  disc=False
K7..K11 disc=False reason=tool-absent
```

This matches `before.json` (`"discriminated": 1, "total": 11`) exactly, and the K6 row is
non-discriminated **for the right reason**: the base row
(`tools/registry.json:949-958`, `command-binding-source-read-red`) pins no digest literal, so the
substituted bundle still holds it. No convenience number: K4 is the only discriminator because it
was already killed by the round-23 `all-of-tokens` case.

### E6 — delivered number reproduced independently

```
$ python3 /tmp/k6/delivered/.ufo/evidence/round-24/measure.py --repo /tmp/k6/full-d
discriminated 11 of 11   (K6: control {'command-binding-source-read-red-pinned': True}
                                   subst {'command-binding-source-read-red-pinned': False})
```

This matches the shipped receipt `.ufo/evidence/round-24/after.json` (11/11, exit 0, same
instrument sha, revision `c8c5b88`). The no-harm registry sweep
(`.ufo/evidence/round-24/noharm-c8c5b88.json`) shows `held 47/47`, with
`command-binding-source-read-red-pinned` active and held, and the predecessor row `superseded`
with `superseded_by` set (append-only preserved).

---

## Findings

### F1 (latent, low) — the ruler credits K6 without checking that the substitute stayed a self-consistent red bundle

`measure.py:133-135` credits discrimination when the row stops being held, whatever caused it.
Counterexample (executed): substitute the bundle but leave the **stale** expected file in place,
so the pair is *inconsistent* and the tool's own tamper detection fires instead of the pin:

```
$ (bundle substituted, expected NOT updated)
registry-check exit 1 held=False got=2 expect=1
stdout_missing=['"finding_ids": ["ARGV_MISMATCH"]', '"bundle_sha256": "db620668…"']
```

Under the frozen formula this is `control True` + `after False` → K6 would be credited, although
the substituted bundle is **not** "another self-consistent red bundle" and the failure came from
`SNAPSHOT_TAMPERED`, not from the pin. The delivered `substitute()` (`:107-117`) does rewrite the
expected file consistently, so **this path is not taken today** — E2 proves the delivered run is
credited for the right reason — but the ruler contains no assertion that forbids it, and the K6
row output records only `control`/`substituted` booleans, not `got`/`stdout_missing`, so a future
reviewer cannot tell the two situations apart from the receipt.

*Smallest safe correction:* in `pin_rows`, after substitution, also record the row's `got` and
`stdout_missing` in the K6 row, and require that the substituted pair is still red and
self-consistent (e.g. `got == expect.exit` and the missing needles are exactly the pinned digest
literal) before crediting discrimination. No production file changes; the ruler is a frozen
artefact, so this belongs to the next round's ruler, not to `c8c5b88`.

### F2 (moderate, covered elsewhere) — K6 has no discrimination power over tool code

K6's signal comes entirely from two things: the registry row's literal pin (data) and the tool's
emission of the computed digest. Any weakening that leaves digest computation intact is invisible
to K6. Executed counterexample (M3): delete the tamper verification in `tools/command-binding.py`
(`check()`, `:124-126` — `if digest != expected['bundle_sha256']: return 2, ['SNAPSHOT_TAMPERED'], digest`):

```
$ python3 /tmp/k6/k6probe.py /tmp/k6/m3run
control: {…: (True, 0)}   after: {…: (False, 1)}   K6 discriminated = True     <-- blind spot
$ python3 tools/command-binding.py --selftest        # in the mutated /tmp tree
CASE tampered FAIL
COMMAND_BINDING_SELFTEST: 43/44 pass   (exit 1)
```

So a weaker implementation (the tool no longer verifies that the expected file pins the bundle
bytes) is *not* discriminated by K6 — the substituted pair is self-consistent by construction, so
the pin is the only surviving signal. M3 is caught, however, by the separate public selftest case
`tampered` (`tools/command-binding.py:176-177`) and therefore by the active registry row
`command-binding-selftest-r24` (`tools/registry.json`, expects `COMMAND_BINDING_SELFTEST: 44/44 pass`).
The wave as a whole is not blind; the *predicate* is.

This matches the contract's own scope (`contract.json` bounds: *"K5-K6 count digest pins against
self-consistent substituted bundles"*) and the knowledge entry's bound (*"A bundle digest pin means
a later commit that changes both the row and the bundle selects a new contract. Neither the pin nor
the gate authenticates the producer."*, `corpus/knowledge/replay-projection-hardening.md:44-46`), so
it is a calibration limit, not a false claim — but it should be stated explicitly: **K6 certifies
the pin, not the tool's tamper check.**

*Smallest safe correction:* either add one frozen predicate of the shape "bundle substituted with
the expected file left stale ⇒ `SNAPSHOT_TAMPERED` / exit 2" (the machinery already exists —
`substitute()` without the expected rewrite), or record in `corpus/lessons/round-24.md` and
`corpus/knowledge/replay-projection-hardening.md` that K6 pins the *row*, and that tool-side digest
enforcement is covered by the selftest's `tampered` case, not by K6.

### F3 (low) — `any(...)` semantics would tolerate an unpinned active row beside the pinned one

`measure.py:133-135` credits K6 when *any* active row naming the bundle stops being held. If a
future registry left the unpinned predecessor `command-binding-source-read-red` **active** alongside
the pinned successor, K6 would still be credited while the unpinned row keeps holding the
substituted bundle. Today's registry is clean (predecessor is `superseded`, `noharm-c8c5b88.json`
confirms `superseded_by`), so this is latent.

*Smallest safe correction:* require *all* active rows naming the bundle to fail, or require the
pinned row to be among the failing rows.

### Non-findings (checked, no defect)

* **Vacuity.** `held()` returns `None` on any parse/shape failure (`measure.py:97-104`), and the
  credit rule requires `is True` for the control and `is False` for at least one row afterwards; a
  missing/unparseable row therefore yields *not discriminated*, never a pass. With no active row
  naming the bundle the ruler records `reason: no-active-row` (`:126-129`) — also not a pass.
* **Wrong reason (delivered).** E1: `got == expect == 1`, `finding_ids` unchanged, the only
  `stdout_missing` entry is the pinned literal.
* **Same-identity rerouting.** K6 exercises the production row's own `argv` and the same bundle
  path it names; no substituted path, no shadow copy of the registry.
* **Substitution strength.** The mutation is byte-minimal (E2) and the stronger "regenerated
  bundle + regenerated expected" form is caught too (E3).
* **Pin satisfiability.** The literal occurs nowhere in the bundle payload (E4); the report prints
  four scalar fields only.
* **Base honesty.** E5: byte-identical ruler, exact 1/11 reproduction, K6 non-discriminated at base
  for the substantive reason (no pin in the base row).
* **Docs.** `corpus/knowledge/replay-projection-hardening.md:16` and `corpus/lessons/round-24.md:53`
  describe K5/K6 accurately (pin required; base 1/11), and both carry the correct bounds.

---

## Base result in `before.json` — honest?

**Yes.** The ruler bytes are identical to the recorded `instrument_sha256` and were never touched
after the freeze commit; re-running that ruler against an extracted `6a1821a` tree reproduces
`discriminated 1 / total 11` exactly, with K6 recorded as `control True / substituted True`
(i.e. the base genuinely fails to discriminate because the base row pins no digest literal), and
K7–K11 as `tool-absent` because `tools/registry-replay.py` did not exist at base. The note in
`before.json` ("K4 already discriminated at base … so before is 1/11") matches the reproduction.

## Smallest safe correction (none required for the round-24 claim)

No change to `c8c5b88` is needed: the delivered K6 credit is earned for the intended reason and the
base receipt is reproducible. The corrections above (F1 assertion + recording `got`/`stdout_missing`
in the K6 row; F2 an explicit note that K6 certifies the row pin while the tool's tamper check is
covered by the selftest's `tampered` case; F3 `all` instead of `any`) belong to the next round's
ruler/lesson and change no production behaviour.

---

**Not claimed here:** producer authentication, promotion, historical R17-CMD-BIND closure, numeric
score uplift, or general mutation adequacy. **Tooling:** no package was installed or upgraded for
this lane (CPython 3.14.8 and coreutils sufficed); the tooling directive therefore records no
install/update.
