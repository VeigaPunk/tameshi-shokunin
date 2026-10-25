seat: T46CritEntryCluster
item: attacked `corpus/knowledge/r6-flaky-failures-cluster.md` for overreach — unlabelled inference, unsnapshot-supported numbers and causal claims, scope creep, PROVINCE and QUALITY exposure, and the honesty of "F3 stays open"

# T46CritEntryCluster — overreach attack on the round-46 F3 cluster entry

## Binding

Every line quoted below is the byte at the content revision, not the working tree.

```
$ L=/home/vgpnk/Projects/shokunin/tameshi-shokunin; REV=6f2168e028ce7ff6e82ac92093ac05dd1f147c32
$ git -C "$L" show $REV:corpus/knowledge/r6-flaky-failures-cluster.md | sha256sum
a1651a6966be38439a9ea5a6fbe393f16f02b091208ca77e769f3cf11b393356  -
$ sha256sum "$L/corpus/knowledge/r6-flaky-failures-cluster.md"
a1651a6966be38439a9ea5a6fbe393f16f02b091208ca77e769f3cf11b393356  corpus/knowledge/r6-flaky-failures-cluster.md
$ git -C "$L" diff --stat $REV -- corpus/knowledge/r6-flaky-failures-cluster.md corpus/README.md
(empty)
```

I am not an author of this entry (wave-1 author: `.ufo/waves/round-46/w1/ScribeEntryCluster.md`). Scratch confined to `/tmp/tameshi-r46-T46CritEntryCluster/`. No counter was run as a verdict; the deciding runs are the L1's. No lane write, no git/jj write, no pacman, no installs.

## Verdict

The entry's mechanical C3 conjuncts hold (15 located quotes, 14 fresh against the package copy, all token labels measured). **The overreach is real and the frozen counter cannot see it**: `entry_ok()` in `.ufo/evidence/round-46/coverage/measure.py:124-152` checks the provenance trio, the cited row, `used-by`, and located/fresh quotes only — it never checks whether a lane-facing sentence is labelled `Inference:`. Four HIGH defects follow, all in §2 and §3, and they falsify `corpus/README.md:573`'s claim that "the entry's fixture-craft reading … is labelled inference".

No BLOCKING finding: nothing here falsifies `C3_R46_PASS` (the contract's C3 statement is about rows, entries, indexing and located quotes, all of which I measured and found satisfied). If the L1 treats `corpus/QUALITY.md:6` (admission-bar item 3) as an admission condition for the round's entries, then F1 and F4 are BLOCKING for the entry's standing; I state that reading explicitly rather than silently upgrading the severity.

| ID | Severity | Attacked line | Defect | Criterion |
|---|---|---|---|---|
| F1 | HIGH | L28 sentence 2 | scope transfer to the lane's controls presented as snapshot content, unlabelled | `QUALITY.md:6` (item 3); `PROVINCE.md` round-46 append |
| F2 | HIGH | L28 sentence 1 + final clause | F3's control population misdescribed: the paper's unit (distinct co-failing tests) does not exist in an F3 sweep (one exact argv repeated) | `QUALITY.md:6`; `PROVINCE.md` (craft owns the rule) |
| F3 | HIGH | L28 second `Inference:` | premise contradicted by the entry's own L22 quote; "cannot detect clustering at all" is a universal negative the snapshot does not state | `QUALITY.md:1` (falsifiable), `:6` |
| F4 | HIGH | L32 sentence 3 | unlabelled inference ("therefore reads the cause"), in a section claiming "stated from the quoted sentences only", doing the transfer L38 disclaims | `QUALITY.md:6`; `PROVINCE.md` round-46 append |
| F5 | LOW | L28 sentence 1 | states only the count branch of F3's rule; drops "or a named mismatch" (correctly quoted at L4) | `QUALITY.md:1` |
| F6 | LOW | L28 parenthetical; `README.md:573` | "mean 13.5 members over the authors' 810 flaky tests" — denominator not stated by the abstract, and arithmetically inconsistent | `QUALITY.md:2` |
| F7 | LOW | L32 sentence 1 | F8 row paraphrased as something it does not say | `QUALITY.md:2` |
| F8 | LOW | L6 (H1) | the thesis ("a set of green reruns is not a set of independent observations") carries no label; the snapshot states nothing about reruns | `QUALITY.md:6` |
| F9 | INFO | whole entry | no sibling lane gate is named, so no claim can be false against one; PROVINCE exposure is F1/F2/F4 only, no absorption of flaky-test engineering | — |
| F10 | INFO | `README.md:577` | "F3 stays `open`" is honest for what this entry delivers, with one caveat at L28 | — |

## F1 — HIGH — the lane's control population is imported from the snapshot without a label

Attacked: `corpus/knowledge/r6-flaky-failures-cluster.md:28`, text before the first `Inference:` label:

```
$ git -C "$L" show $REV:corpus/knowledge/r6-flaky-failures-cluster.md | sed -n '28p' | awk -F'Inference:' '{print $1}'
The F3 rule counts byte-identical controls. The snapshot says the failures such controls probe are not scattered: most of them sit in clusters that share a root cause, and the clusters are large (mean 13.5 members over the authors' 810 flaky tests).
```

Why it is overreach. The snapshot's population is stated by the entry itself at L18: `"We used an established dataset of 10,000 test suite runs from 24 Java projects on GitHub…"` / `"It contains 810 flaky tests…"`. The sentence at L28 says the snapshot states something about **"the failures such controls probe"** — the lane's repeated-control targets. The snapshot contains no lane gate, no control, and no mutation survivor; L43 of the same entry says so ("no gate of this lane is in it"). The sentence is therefore an inference presented as observation, and it is the exact reading `PROVINCE.md`'s round-46 append commits the entries not to make unlabelled ("the entries' readings for survivor lists and rerun evidence are labelled inference").

It also falsifies the round's own index claim:

```
$ grep -c 'is labelled inference' "$L/corpus/README.md"
1
$ sed -n '573p' "$L/corpus/README.md"
| `knowledge/r6-flaky-failures-cluster.md` | A published abstract states that flaky tests co-occur in clusters with shared root causes (75% of 810 flaky tests, mean cluster size 13.5); the entry's fixture-craft reading — controls or survivors drawn from one cluster are one observation — is labelled inference | S258 |
```

"controls … drawn from one cluster are one observation — is labelled inference" is false at L28. Impacted axes: coverage (the entry's standing as an admitted, source-headed reading), calibration (a record claim that disagrees with the record).

Smallest safe correction (append-only, `QUALITY.md` criterion 35): append a dated erratum that replaces L28 sentence 2 with an `Inference:`-prefixed sentence scoped to the paper's population, e.g. `Inference: if the lane's repeated-control targets behave like the authors' 810 flaky tests, most of them would sit in clusters that share a root cause (the snapshot's population, not this lane's); the snapshot states nothing about the failures these controls probe.` Do not rewrite L28 in place.

## F2 — HIGH — the paper's unit of clustering does not exist in an F3 sweep

Attacked: `r6-flaky-failures-cluster.md:28`, both the first sentence and the closing clause.

F3's rule, as the entry itself quotes it at L4 and as the frontier table states it:

```
$ sed -n '80p' "$L/corpus/README.md" | rev | cut -c1-120 | rev
 (`.ufo/evidence/kaika-round-1/capability-demo/README.md` H2) → N ≥ 3 byte-identical controls, or a named mismatch |
$ sed -n '7,9p' "$L/tools/repeat-control.py"
control run per sweep, no repeat-control option"), and one run cannot separate
a stable baseline from a flaky one. This gate runs one exact argv N >= 3 times
and decides whether the N pristine controls agreed.
```

Byte-identical controls are **one exact argv run N times**. The entry's L28 says `"N controls drawn from one cluster are one probe of one cause repeated N times"` and closes with `"a sweep that draws several cases from one gate should record that they share a gate rather than scoring them as separate controls"`.

Two defects:
1. An F3 sweep holds one case repeated, not several cases; there is no co-occurrence matrix in it, so the paper's clustering result cannot be observed — or missed — by an F3 sweep. The paper's unit (distinct tests that fail together) is absent from the surface the paragraph claims to speak about.
2. The conclusion "the count of controls is an upper bound on independent evidence" is true of byte-identical controls **by construction**, and is already the lane's own standing rule (`QUALITY.md` criterion 11: a repeated-control clean verdict "never proves determinism"). Presenting it as a consequence of the snapshot is false provenance: the snapshot adds nothing to the F3 count.

The closing recommendation also addresses a practice F3's rule does not contain ("several cases from one gate"), so a reader cannot tell whether it is an F3 change or a survivor-set change — it sits under the heading `## 2. What this says about the lane's F3 control count`.

Smallest safe correction: append an erratum narrowing §2 to what the paper can bear — the paper's clusters are distinct tests; F3's controls are one argv repeated, so the snapshot bears on survivor sets and on cross-case reruns (§4's subject), not on the byte-identical control count; the count-as-upper-bound is F3's own definition plus criterion 11, not a result of S258.

## F3 — HIGH — the 10,000-run premise is contradicted ten lines above it

Attacked: `r6-flaky-failures-cluster.md:28`, second `Inference:`: `"the clustering itself needed 10,000 suite runs to become visible, so a three-control sweep cannot detect clustering at all"`.

```
$ git -C "$L" show $REV:corpus/knowledge/r6-flaky-failures-cluster.md | grep -n '10,000' | cut -c1-230
18:**The data.** "We used an established dataset of 10,000 test suite runs from 24 Java projects on GitHub, …
22:**The cheap substitute.** "Instead of requiring 10,000 test suite runs to identify systemic flakiness" (11 tokens) "we demonstrated a lightweight alternative by training machine learning models based on static test case distance measures" (17 tokens)
28:The F3 rule counts byte-identical controls. The snapshot says the failures such controls probe are not scattered: …
```

The abstract's sentence is a contrast: 10,000 runs was the cost of the dataset-based identification, and the authors **demonstrated a lightweight alternative** that does not use reruns. The entry quotes that sentence at L22 and then, at L28, asserts as a premise that clustering "needed 10,000 suite runs to become visible" and concludes a three-control sweep "cannot detect clustering at all". The paper's own quoted alternative is the counterexample: at least one demonstrated detector of systemic flakiness does not need 10,000 runs. The universal negative "at all" is stated nowhere in the snapshot and is falsified by the entry's own bytes.

Smallest safe correction: append an erratum replacing the premise and dropping "at all" — the abstract states the authors' clustering used a 10,000-run dataset and that they demonstrated a non-rerun alternative (L22); the snapshot states nothing about three-control sweeps.

## F4 — HIGH — an unlabelled inference in the section that claims to state only what is quoted

Attacked: `r6-flaky-failures-cluster.md:32`, sentence 3, under the heading `## 3. The F8 link, stated from the quoted sentences only`:

```
$ git -C "$L" show $REV:corpus/knowledge/r6-flaky-failures-cluster.md | sed -n '32p' | awk -F'Inference:' '{print $1}'
F8 asks for an expectation fixed outside the code under mutation (`corpus/README.md` F8 row). The located sentence above names what the members of a cluster have in common: "co-occurring failures that share the same root causes" (8 tokens). An expectation that reads one member of such a cluster therefore reads the cause the other members also carry.
```

Why it is overreach:
- It is a lane-facing claim about F8's expectation, with no `Inference:` label, in the one section whose heading promises quoted-only content. Every other lane-meaning step in the entry is labelled (L4, L28 ×2, L32 sentence 4, L36, L37).
- It is the very transfer §4 disclaims at L38: `"The snapshot reports flaky *test failures* in 24 Java projects; it contains no data on mutation survivors, and the application to this lane's survivor sets is an inference, not a result of the paper."` §3 makes the transfer as a deduction ("therefore") three lines before §4 says it is not a result of the paper.
- It is unsound on its own terms. The abstract's root causes are named at L24 — `"intermittent networking issues and instabilities in external dependencies"` — established by the authors' manual stack-trace inspection, not readable by an expectation. An expectation anchored on one member's observed outcome is not evidence about the cause the members share; the step needs at least "the shared cause is what makes the members co-occur", which the abstract does not state for an expectation.

Smallest safe correction: append an erratum prefixing the sentence with `Inference:` and weakening it to what the quoted sentence supports — `Inference: if the cluster's members share a root cause, an expectation anchored on one member's observed outcome is not evidence about the other members' outcomes` — and move it under §4's `(Inference)` heading.

## F5 — LOW — half of F3's rule

`r6-flaky-failures-cluster.md:28` sentence 1 says `"The F3 rule counts byte-identical controls."` The rule quoted correctly at L4 has two branches — `N ≥ 3 byte-identical controls, **or a named mismatch**` (`corpus/README.md:80`, output above). §2's argument therefore binds only the count branch, and a sweep that takes the named-mismatch branch is outside it; the entry does not say so. Correction: name both branches in the erratum F2 already requires.

## F6 — LOW — a denominator the abstract does not state

`r6-flaky-failures-cluster.md:28`: `"the clusters are large (mean 13.5 members over the authors' 810 flaky tests)"`. The snapshot states `"75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests"` (L20, 22 tokens, located) — a per-cluster mean, with no denominator. 75% of 810 is not an integer:

```
$ python3 -c 'print(0.75*810)'
607.5
```

so the 810 is not literally the denominator of the 75% figure. Same defect propagated to the round's index row (`corpus/README.md:573`, `"(75% of 810 flaky tests, mean cluster size 13.5)"`). Correction: `mean cluster size of 13.5 flaky tests (abstract; no denominator stated)` in the erratum, and the README row's parenthetical should be narrowed by an appended erratum or left standing as a derivation the L1 names.

## F7 — LOW — the F8 row paraphrased into something it does not say

`r6-flaky-failures-cluster.md:32` sentence 1: `"F8 asks for an expectation fixed outside the code under mutation (`corpus/README.md` F8 row)."`

```
$ sed -n '85p' "$L/corpus/README.md"
| F8 | oracle anchoring as a survivor class | S012 | open | 0 test-oracle lines → one survivor classified against an independently anchored expectation |
```

The row's move is a classification of one survivor against an independently anchored expectation; it does not say "fixed outside the code under mutation", and "independently anchored" is not defined there. A paraphrase carrying a definition the cited row does not state is an unanchored claim (`QUALITY.md:2`). Correction: quote the row's move or drop the paraphrase.

## F8 — LOW — the H1 thesis carries no label

`r6-flaky-failures-cluster.md:6`: `# Flaky failures come in clusters, so a set of green reruns is not a set of independent observations`. The second clause is the entry's thesis; the snapshot says nothing about reruns, and the entry itself records at L44 that `"a same-job-rerun miss rate is not stated in this snapshot"`. The lane's convention does put claims in H1 (`r5-undetected-flaky-failures.md:6`, `r8-gtest-primer-independence.md:6` do the same), and §4 labels the reading, so this is LOW — but the entry's strongest sentence is the one the label reaches last. Correction (optional, same erratum): `… so a set of green reruns is not a set of independent observations (Inference)`.

## F9 — INFO — PROVINCE and sibling gates

- **Sibling gates.** The entry names no sibling lane: `grep -nE 'kumitate|kagi|mado|tsukuroi|kaidoku|sibling'` over the entry at REV prints nothing. Per the item, I did not read sibling gates for correctness, and there is no claim here that a sibling gate could make false.
- **PROVINCE.** `PROVINCE.md`'s round-46 append says the entries' readings "are labelled inference, and flaky-test engineering as such stays adjacent (report, never absorb)". The entry does **not** absorb flaky-test engineering: it recommends nothing about repairing flaky tests and makes no claim about the Java projects' practice. §4's prescriptions (cluster membership beside a per-survivor verdict) are about this lane's own classification, i.e. in province, and are labelled. The province breach is confined to F1, F2 and F4 — unlabelled readings of the lane's controls and F8 expectations — not a domain grab.

## F10 — INFO — is "F3 stays open" honest?

`corpus/README.md:577`: "F3 stays `open` — these entries state what the literature measures, they do not measure the lane's own controls (the repeated-control capability does)."

For this entry: **yes, honest**. The entry runs no lane command, cites no lane measurement, and its own L38/L43/L44 keep the transfer an inference. Caveat: L28's unlabelled sentence *is* a statement about the lane's controls derived from the snapshot — if it were read as an observation, "F3 stays open" would be false for this entry. It is an unlabelled inference, not a measurement, so the frontier row stands; fixing F1 removes the caveat.

## Checks that found no defect (reported as run, not as absolution)

1. **Quote audit against the counter's own fold** — `python3 /tmp/tameshi-r46-T46CritEntryCluster/audit.py` (reads `git show REV:…` for the entry, the snapshot and the package copy; `QUOTE_RE`/`fold` copied from `measure.py:52,59-64`):

```
snapshot sha256 28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14
L12  tokens=14  label=14   located=1 fresh=1
L14  tokens=21  label=21   located=1 fresh=1
L16  tokens=20  label=20   located=1 fresh=1
L16  tokens=13  label=13   located=1 fresh=1
L16  tokens=18  label=18   located=1 fresh=1
L18  tokens=24  label=24   located=1 fresh=1
L18  tokens=19  label=19   located=1 fresh=1
L20  tokens=12  label=12   located=1 fresh=1
L20  tokens=22  label=22   located=1 fresh=0
L20  tokens=6   label=6    located=1 fresh=1
L22  tokens=11  label=11   located=1 fresh=1
L22  tokens=17  label=17   located=1 fresh=1
L24  tokens=16  label=16   located=1 fresh=1
L24  tokens=17  label=17   located=1 fresh=1
L32  tokens=8   label=8    located=1 fresh=1
quotes=15 located=15 fresh=14
```

Every label equals the measured whitespace-token count under the counter's fold, and every quote is in the 6–25 band — `QUALITY.md` criterion 87 is satisfied, and L8's "14 of the 15 located quotes do not occur in the committed package copy" is exact.

2. **Snapshot digest and venue facts** — `sha256sum` of the committed snapshot equals the L1 prefix `28d2954d…` and the full digest in L3. Counts in the raw snapshot: `'Submitted on 23 Apr 2025'` 1, `'Wed, 23 Apr 2025 14:51:23 UTC (79 KB)'` 1, `'Journal reference'` 0, `'Comments'` 0, `'and 3 other authors'` 0. The four authors in L8 match the four `citation_author` meta tags (Parry/Kapfhammer/Hilton/McMinn); the page's "by Owain Parry and 2 other authors" line is arXiv's own display text and is not a contradiction. L42's venue and no-peer-review-status claims hold.
3. **Recheck command re-run** (network, read-only):

```
$ curl -fsSL --max-time 40 'https://arxiv.org/abs/2504.16777' -o /tmp/tameshi-r46-T46CritEntryCluster/live-abs.html; echo "curl_exit=$?"
curl_exit=0
$ ls -l /tmp/tameshi-r46-T46CritEntryCluster/live-abs.html
-rw-r--r-- 1 vgpnk vgpnk 43376 Oct 25 19:25 /tmp/tameshi-r46-T46CritEntryCluster/live-abs.html
$ grep -c 'co-occurring failures that share the same root causes' /tmp/tameshi-r46-T46CritEntryCluster/live-abs.html
3
$ cmp -s /tmp/tameshi-r46-T46CritEntryCluster/live-abs.html "$L/.ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html" && echo IDENTICAL
IDENTICAL
```

L3's three numbers (count 3, 43,376 bytes, cmp-identical) reproduce.
4. **Package-copy provenance** — the entry dropped the package's `CC BY 4.0`, the package's `preprint`/peer-review claim, its `tier A` grade and its S140 rerun-rate sentence, and none of those reappear; the inherited overreach the package carried as observation (`a cluster's members share a cause`) survives only in the shape of F4.

## Unrun (by bounds, not skipped silently)

- The deciding runs of the three counters: not run. Bounds reserve them for the L1. I read `entry_ok()` and replicated its fold; I did not execute `coverage/measure.py` against the lane as a verdict.
- No sibling lane gate was read, per the item.
- The paper body (PDF/HTML) was not fetched: like the entry, this review rests on the committed abstract snapshot.

## Tooling

No installs, no upgrades, no pacman transaction. Scratch: `/tmp/tameshi-r46-T46CritEntryCluster/` (`audit.py`, `abs.txt`, `live-abs.html`). The lane checkout was written only at this report.
