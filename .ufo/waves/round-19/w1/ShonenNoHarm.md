# ShonenNoHarm — tameshi round 19 attempt 1, w1 (advisory scout)

- Seat: `TameshiR19-2.ShonenNoHarm` (scout, read-only). Date: 2026-10-21, observed
  02:44–03:04 -03:00.
- Target: compare the current `SHONEN.md` four marks and evidence links with the protocol.
  No promotion is claimed.
- Status: advisory findings only, not closure or admission. I made no production edit, no
  Git/JJ write, and no tool install, and I sent no peer messages. I ran no lane-owned
  gate, selftest, measure, or monitor. All Git reads used `GIT_OPTIONAL_LOCKS=0`.
- Moving target: L1 landed five commits while this seat ran. The last one I checked was
  `refs/heads/master` = `refs/remotes/origin/master` =
  `cecaefe73482504a814064dd7b2242c8c0b8ad50` at 03:04:36. At that time the worktree
  `SHONEN.md` matched `cecaefe`.

## Verdict (advisory)

| Axis | Result |
|---|---|
| A1 canonical form | **PASS** at every revision checked. |
| A2 marks / no promotion | **PASS**: four `[~]`, zero `[x]`, zero `[ ]`, and nothing promoted. |
| A3 evidence links resolve at the same revision | **PASS** at every revision checked. |
| A4 box-3 evidence covers the page at that revision | **Harmed at four intermediate landings, then restored at `cecaefe`** (necessary conditions only). The final receipt is still owed (F4). |
| A5 metadata accuracy of the box-3 repair | **OPEN**: the text says "eleven" buckets; the ledger has 13 (F2). |

## Sources opened (pinned)

- Canonical protocol, read in the `~/Projects/kimi-shokunin` checkout (`SHOKUNIN_PLUGIN`
  is unset). HEAD is `e737d2ea97f6b0198503e077676c3f2ea07974a9` (2026-10-19), the
  worktree is clean against HEAD, and `PROTOCOL.md` sha256 is `622b29a0…1739fd0`.
  - `PROTOCOL.md:446`: "the seed block (indented lines below) must diff byte-identical
    modulo `<name>` = the repo's directory name"
  - `PROTOCOL.md:446`: "marks are confined to the box character plus one indented
    evidence line per box"
  - `PROTOCOL.md:66–67`: "The lane's own assessment is `[~]` asserted (with its evidence
    pointer); only a non-author `<id>` may write `[x]`"
  - `PROTOCOL.md:71–72`: "box 3 requires `SKILL.md`/`corpus/` instructions executable
    without oral context, self-contained, and with resolvable pointers"
  - Seed block: `PROTOCOL.md:453–465`. It is byte-identical at `bc7d690` (2026-10-13) and
    `e737d2e` (`diff` was empty), so the protocol requires no regeneration.
  - `PROTOCOL-APPENDIX.md:30` "Canonical form" row: kagi had bare `[x]`, kotoba had
    per-box prose, kengaku had a stale 3-box file. tameshi shows none of these.
- The round-18 spot-check (`corpus/lessons/round-18-verifier-spotcheck.md` §1, §5, §7) was
  used as the prior pass baseline.
- Lane files were read as Git blobs at the revisions below, plus the worktree. These
  include `SHONEN.md`, `reports/round-1-calibration.md`, the round-18 and round-19
  `coldread/ledger.json`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-19.md`
  and fleet `MANIFEST.json`.
- I read `.ufo/evidence/round-18/measure.py` (lines 1–60, 121–136, 209–276, 549–700) and
  the round-19 `coldread/measure.py` wrapper (24 lines). I did not execute either.

Revisions checked:

| Label | Revision |
|---|---|
| r18 delivered | `4b7c6823a462f5ea2eafcb262275300a545f3ed7` |
| frozen baseline | `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190` |
| round-19 freeze | `78b99ddcbf46f06246b978c8f5d4b6720dc5f59e` |
| round-19 landing 1 | `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9` |
| round-19 landing 2 | `7af123b0e068cd5e6b651aab31a813cc170d70a2` |
| round-19 landing 3 | `c5730cc5d39ac45ad147c9cac29573ea04745ab5` |
| round-19 landing 4 | `88c8073a79e94d9fcc47deba0b04aa087fdabb4c` |
| round-19 landing 5 | `cecaefe73482504a814064dd7b2242c8c0b8ad50` |
| worktree | read at 03:04 |

Every round-19 commit is authored `tameshi-shokunin <tameshi@shokunin.local>`.
`7243e7f` is an ancestor of master (exit 0).

## A1–A3: canonical form, marks and links (observed; `compare.py`)

`SHONEN.md` blobs:

- `de1b1d98…` at `4b7c682`, `7243e7f`, `78b99dd` and `21e7932`.
- `f9b7c896…` at `7af123b`, `c5730cc`, `88c8073`, `cecaefe` and the worktree.

The only change is line 10, the box-3 evidence line:

- Before:
  `  [lane assertion, no independent promotion verifier](.ufo/evidence/round-18/coldread/ledger.json)`
- After:
  `  [lane assertion, input-keyed monitor only; no independent promotion verifier](.ufo/evidence/round-19/coldread/ledger.json)`

At every revision and in the worktree:

- **Seed.** The seed lines match exactly once `<name>` is substituted
  (`tameshi-shokunin`) and the box characters are normalized. There are 4 boxes and a
  single trailing newline.
- **Marks.** The census is `{'~': 4}`: no `[x]`, no `[ ]`.
- **Evidence lines.** Each box has exactly one 2-space-indented evidence line, and each is
  a single markdown link.
- **Boxes 1, 2 and 4.** They link to `reports/round-1-calibration.md#box-1/2/4`. The
  target blob `fc46d59d…` is unchanged since `cd31c6b` (2026-10-15). Each anchor matches
  exactly one heading (`## box-1`, `## box-2`, `## box-4`).
- **Box 3.** The linked ledger exists in the same revision's tree and parses as JSON:
  - Through `21e7932` it is the round-18 ledger, `d654f3d2…`.
  - From `7af123b` it is the round-19 ledger. It landed in the same commit as the
    `SHONEN.md` edit. Its blob changes on every landing: `4b79c671` → `7336fbd8` →
    `c5a31879` → `2d6377dd`.
- **Prose (advisory only).** Strictly, the link-label wording could be read against
  "no other prose". However, the round-18 non-author check (§1, `SHONEN canonical form`)
  passed the same convention. The words added in round 19 narrow the claim rather than
  promote anything.

## A2: no promotion (observed)

- `MANIFEST.json` `roster` has 13 rows and none is tameshi; its mint note says the roster
  row is withheld. No `rounds[].promotions` entry names tameshi.
- `.ufo/evidence/round-19/contract.json:13` (at `21e7932` and `cecaefe`) lists the
  invariant `"no promotion"`.
- `SCORECARD.md:697` (at `21e7932` and `cecaefe`) says independent promotion is not
  claimed.
- `corpus/lessons/round-19.md:70–71` (at `21e7932` and `cecaefe`) says the four `[~]`
  "remain assertions, not independent promotion checks".
- All six round-19 commits, `78b99dd` through `cecaefe`, have author and committer
  `tameshi-shokunin <tameshi@shokunin.local>`.
- There are zero `[x]` marks anywhere in `SHONEN.md` history from `4b7c682` to `cecaefe`.

## A4: box-3 evidence against the page at each revision (`box3_cover.py`)

`box3_cover.py` is my own reimplementation of the round-18 sectionizer and input gate,
written from reading the code, not by importing it. It checks only necessary conditions.
"Inputs equal" is an upper bound: the trace, veto and class gates are not reproduced.

| Revision | Box-3 ledger (entries) | `SKILL.md` | Sections | sha-matched | Inputs equal |
|---|---|---|---|---|---|
| `4b7c682` | r18 `d654f3d2` (159) | `1334c512` | 60 | 60 | 60 |
| `7243e7f` | r18 `d654f3d2` (159) | `1334c512` | 60 | 60 | 60 |
| `21e7932` | r18 `d654f3d2` (159) | `4d0190fd` | 60 | **59** (1925 has no entry) | **49** |
| `7af123b` | r19 `4b79c671` (159, all equal to r18 entries) | `b653979a` | 60 | **59** (1925) | **48** (adds 1499) |
| `c5730cc` | r19 `7336fbd8` (170) | `b653979a` | 60 | 60 | **59** (1499) |
| `88c8073` | r19 `c5a31879` (171) | `0e3d7453` | 60 | **59** (1855 has no entry) | 59 |
| `cecaefe` | r19 `2d6377dd` (172) | `0e3d7453` | 60 | 60 | 60 |

At `21e7932`, these 10 sections fail on input drift: 6, 131, 375, 1380, 1479, 1517, 1548,
1563, 1609 and 1905. The drifted inputs are `corpus/QUALITY.md`, `corpus/README.md`,
`corpus/SOURCES.md` and `corpus/knowledge/mutation-case-kumitate-sources-check.md`.

**Agreement with the lane's own receipts, derived independently.**

- `current-ledger-monitor-21e7932.json` (committed in `7af123b`) records restraint 6,
  credited 49, `box3_full_page` false.
- `current-ledger-monitor-c5730cc.json` (committed in `88c8073`) records restraint 6,
  covered 59/60, and
  `missing: [{"heading": "### Gate/probe registry", "reason": "input-drift:SHONEN.md;…", "start": 1499}]`.

Both match my counts exactly. For `7af123b` and `88c8073` there is no lane receipt. My
inference there: round-18 `measure.py:611–622` cannot credit a section that has no
matching entry, so `box3_full_page` is false and restraint is 6 at those revisions.

At `cecaefe`, 47/60 sections pass only through carried round-17/18 entries. The other
**13/60 pass only through round-19 entries whose seat is "L1 TameshiR19-2 author source
re-anchor"**: sections 6, 131, 375, 1380, 1479, 1499, 1517, 1548, 1563, 1609, 1855, 1905
and 1925.

## Findings and failing criteria

**F1. SHONEN.md is a recorded input of its own box-3 evidence.** Observed; repaired at
`88c8073`; can recur.

- Four ledger entries record `SHONEN.md` as an input: sections 17, 1155, 1436 and 1499.
- The `7af123b` pointer edit changed `SHONEN.md` from `de1b1d98` to `f9b7c896`. That
  drifted section 1499's only otherwise-passing entry (r18 seat CR36, read_rev
  `01d586dd`). Inputs-equal fell from 49 to 48, and `c5730cc` stayed at 59/60.
- `88c8073` re-anchored 1499. The new entry records `SHONEN.md` = `f9b7c896`.
- Failing criterion: any later byte change to `SHONEN.md` breaks full-page coverage at the
  delivered revision, unless 1499 is re-anchored again in the same revision. (17 and 1436
  currently also pass through entries that do not depend on `SHONEN.md`.)

**F2. The re-anchor count in the text is stale.** Observed at `cecaefe`; the worktree was
unchanged at 03:03:24.

- `SCORECARD.md:738–739` says "the eleven invalidated buckets receive provenance-labeled
  L1-author input-keyed source re-reads". `LOG.md:1190` and
  `corpus/lessons/round-19.md:92` also say eleven.
- The committed ledger has **13** such entries. The two added after that text are:
  - 1499, the `SHONEN.md` link input, re-anchored in `88c8073`;
  - 1855, re-anchored in `cecaefe` after `88c8073` migrated the recipe line at
    `SKILL.md:1890`.
- A grep of `SCORECARD`, `LOG`, the lesson, `README`, `QUALITY` and `SKILL` at `cecaefe`
  finds no mention of `1499`, `1855`, "link-input" or "recipe migration".
- This is the same defect class as R18-3 (spot-check §5c, arithmetic).
- Failing criterion: at the delivered revision, the stated count must equal the number of
  ledger entries whose seat is "L1 TameshiR19-2 author source re-anchor". That number is
  13 at `cecaefe`.

**F3. Boundary for closure to rule on** (inference; I make no ruling).

- The frozen context says "no promotion or new cold-read coverage claimed".
- At the current page, 13/60 box-3 sections are credited only by new round-19 L1-author
  entries.
- The lane labels these as neither independent/blind cold-read nor required-command
  coverage (`SCORECARD.md:739–740`). The `SHONEN.md` label says "input-keyed monitor
  only".
- Precedent: the round-18 report's box-3 line disclosed "17 sections L1-completed".
- The marks stay `[~]`, which is correct under `PROTOCOL.md:66–67`. Every ledger entry is
  lane evidence anyway.

**F4. No receipt yet backs "numeric calibration 8→8" at the revision that will be
delivered** (observed; this is the R18-5 pattern).

- The lane's own rule, `SCORECARD.md:740–741` at `cecaefe`: "The final no-harm receipt
  must name its delivered revision and reproduce restraint8".
- At `cecaefe`, current monitors exist only for `21e7932` and `c5730cc`, and both record
  restraint 6. My necessary conditions are 60/60 at `cecaefe`, so 8 is plausible but not
  established.
- Failing criterion: closure needs a committed receipt with all of:
  - `revision` equal to the delivered revision
  - `calibration_restraint_score == 8`
  - `box3_full_page == true`
  - `overrides_used == false`
  - strict trace gate
  - default ledger `.ufo/evidence/round-19/coldread/ledger.json`
- Any commit that adds only the receipt must leave `SKILL.md`, `SHONEN.md` and every
  recorded input untouched. Otherwise the measured revision and the delivered revision
  diverge again.

**F5. The box-1/2/4 evidence target carries stale protocol line cites.** Pre-existing,
advisory, outside the C1 population; no expansion is claimed.

- `reports/round-1-calibration.md:17–23, 73, 107, 134, 169, 206–212` cite `PROTOCOL.md`
  lines 413, 419–431, 425–428 and 327–346 with no protocol revision. These matched
  kimi-shokunin `bc7d690` (2026-10-13), where the seed rows were 425–428.
- At canonical `e737d2e`, the seed rows are 459–462 and those lines hold unrelated text.
  Lines 63–68 still match.
- The repository citations in that file are pinned to `284ab0f` and still resolve with
  identical bytes at `cecaefe`:
  - `LOG.md:277–298`, `PROVINCE.md:3–18` and `mutation-case-kagi-census.md:1–17` are
    sha-equal.
  - The `SKILL.md:58/466/497` headings are unchanged.
- `PROVINCE.md` (`8006da5d…`), `reports/round-1-calibration.md` and the round-18 ledger
  have no commits in `7243e7f..cecaefe`. Box 4's evidence is dated 2026-10-15, and round 19
  introduced no drift in it.

## Observed / inference / unknown

- **Observed:** every byte and hash fact above; the two lane monitor receipts; and the
  13-entry and "eleven" counts.
- **Inference:** restraint 6 at `7af123b` and `88c8073`, from reading `measure.py`
  without executing it.
- **Unknown:**
  - whether the trace, veto and class gates credit all 60 sections at `cecaefe`;
  - which revision will finally be delivered (L1 was still landing);
  - whether closure counts the 13 L1 re-anchors as "new cold-read coverage" (F3).

## Method, commands, code

Read-only Git commands, run from the lane repo:

```
rev-parse
log
show REV:path
cat-file blob
ls-tree -z
diff --stat / --numstat / -U0
merge-base --is-ancestor
```

Other plain reads: `stat`, `ls`, `cat -A SHONEN.md`, `sed -n` on `PROTOCOL.md` at
`bc7d690` and `e737d2e`, and inline Python JSON reads of `MANIFEST.json`, the ledgers and
the monitors.

Scratch is `/tmp/shonen-noharm-r19/` (disposable).

- `compare.py`: sha256 `eabfa0210cec621729906e11b6428c64afde793a77ae56a4994d01ff2a662688`,
  exit 0. Output `compare.out.json`:
  `6b70d84e8d28eb0fb8fdb13e80c909c14baabd8640e2df2a632e2a00fc2380f4`.
- `box3_cover.py`: sha256 `b1331fb4bc9a5355e135dce8d786ab300cfb25fdc044d7a2863e3b952f67b4d6`,
  exit 0. Output `box3_cover.out.json`:
  `2d10084dceb41e579fa1fb8f69b9a7851e05534f9484979b97dafc8eef3d6bf0`.

Disclosed scratch error: the first `box3_cover.py` run read `ls-tree`'s type field instead
of its mode field. Every input therefore showed `input-not-blob`. I fixed this before
drawing any finding. All counts above come from the corrected runs.

The L1-only breakdown came from this inline snippet, which imports my own module, not
lane code:

```python
import json,sys; sys.path.insert(0,'/tmp/shonen-noharm-r19'); import box3_cover as B
rev="cecaefe73482504a814064dd7b2242c8c0b8ad50"
skill=B.blob(rev,"SKILL.md"); led=json.loads(B.blob(rev,B.box3_ledger(rev))); by={}
for e in led["entries"]: by.setdefault(e.get("sha256"),[]).append(e)
cache={}; only_l1=[]
for s in B.sectionize(skill):
    p=[e for e in by.get(s["sha256"],[]) if B.inputs_ok(rev,e,cache)[0]]
    l1=[e for e in p if any("L1 TameshiR19-2" in str(x) for x in (e.get("seats") or []))]
    if l1 and len(l1)==len(p): only_l1.append(s["start"])
print(len(only_l1), only_l1)   # 13 [6,131,375,1380,1479,1499,1517,1548,1563,1609,1855,1905,1925]
```

### compare.py (verbatim)

```python
#!/usr/bin/env python3
"""Read-only SHONEN.md canonical-form + evidence-link comparison (tameshi r19 ShonenNoHarm).

Reads git blobs only (GIT_OPTIONAL_LOCKS=0); never writes the lane repo.
"""
import hashlib, json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
PROTO = "/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md"
NAME = os.path.basename(LANE)  # <name> = repo directory name
REVS = {
    "r18-delivered": "4b7c6823a462f5ea2eafcb262275300a545f3ed7",
    "r19-baseline": "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190",
    "r19-freeze": "78b99ddcbf46f06246b978c8f5d4b6720dc5f59e",
    "r19-land-1": "21e79329f8bdcf01a62be63b3e46db4a7de6b6f9",
    "r19-land-2": "7af123b0e068cd5e6b651aab31a813cc170d70a2",
    "r19-land-3": "c5730cc5d39ac45ad147c9cac29573ea04745ab5",
    "r19-land-4": "88c8073a79e94d9fcc47deba0b04aa087fdabb4c",
    "r19-land-5": "cecaefe73482504a814064dd7b2242c8c0b8ad50",
    "master-tip": "refs/heads/master",
}
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0")


def git(*args, check=True):
    p = subprocess.run(["git", "-C", LANE, *args], capture_output=True, env=ENV)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {args}: {p.stderr.decode()}")
    return p


def blob(rev, path):
    p = git("show", f"{rev}:{path}", check=False)
    return p.stdout if p.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


def seed_lines():
    lines = open(PROTO, encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("The canonical `SHONEN.md` seed"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("Marks:"))
    block = lines[start + 1:end]
    while block and block[0] == "":
        block.pop(0)
    while block and block[-1] == "":
        block.pop()
    out = []
    for l in block:
        if l == "":
            out.append("")
        else:
            assert l.startswith("    "), repr(l)
            out.append(l[4:])
    return [l.replace("<name>", NAME) for l in out], start + 1


def gh_slugs(md_text):
    slugs, counts, in_fence = [], {}, False
    for l in md_text.split("\n"):
        if l.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", l)
        if not m:
            continue
        s = m.group(2).strip().lower()
        s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE).replace(" ", "-")
        n = counts.get(s, 0)
        counts[s] = n + 1
        slugs.append(s if n == 0 else f"{s}-{n}")
    explicit = re.findall(r'<a\s+(?:id|name)="([^"]+)"', md_text)
    return slugs, counts, explicit


BOX_RE = re.compile(r"^- \[(.)\] (.*)$")
LINK_RE = re.compile(r"^  \[([^\]]*)\]\(([^)\s]+)\)$")


def analyse(label, rev, text, seed, resolve):
    res = {"label": label, "rev": rev}
    lines = text.split("\n")
    res["ends_with_newline"] = text.endswith("\n") and not text.endswith("\n\n")
    if res["ends_with_newline"]:
        lines = lines[:-1]
    normalized, boxes, extra, i = [], [], [], 0
    while i < len(lines):
        l = lines[i]
        m = BOX_RE.match(l)
        if m:
            normalized.append(f"- [ ] {m.group(2)}")
            ev = []
            j = i + 1
            while j < len(lines) and lines[j].startswith("  ") and not BOX_RE.match(lines[j]):
                ev.append(lines[j]); j += 1
            boxes.append({"mark": m.group(1), "text": m.group(2), "evidence_lines": ev})
            i = j
            continue
        normalized.append(l)
        i += 1
    res["seed_identical_modulo_name_and_marks"] = normalized == seed
    if normalized != seed:
        import difflib
        res["seed_diff"] = list(difflib.unified_diff(seed, normalized, "seed", label, lineterm=""))
    res["box_count"] = len(boxes)
    res["mark_census"] = {k: sum(1 for b in boxes if b["mark"] == k) for k in sorted({b["mark"] for b in boxes})}
    per = []
    for n, b in enumerate(boxes, 1):
        e = {"box": n, "mark": b["mark"], "n_evidence_lines": len(b["evidence_lines"])}
        if len(b["evidence_lines"]) == 1:
            lm = LINK_RE.match(b["evidence_lines"][0])
            e["evidence_line"] = b["evidence_lines"][0]
            e["is_single_md_link"] = bool(lm)
            if lm:
                label_txt, target = lm.group(1), lm.group(2)
                e["link_label"], e["link_target"] = label_txt, target
                path, _, anchor = target.partition("#")
                e["path"], e["anchor"] = path, anchor or None
                tb = resolve(path)
                e["target_exists"] = tb is not None
                e["target_sha256"] = sha(tb)
                if tb is not None and anchor:
                    slugs, counts, explicit = gh_slugs(tb.decode("utf-8", "replace"))
                    e["anchor_resolves"] = anchor in slugs or anchor in explicit
                    base = anchor
                    e["anchor_heading_count"] = counts.get(base, 0)
                if tb is not None and path.endswith(".json"):
                    try:
                        json.loads(tb)
                        e["json_parses"] = True
                    except Exception as x:
                        e["json_parses"] = f"no: {x}"
        per.append(e)
    res["boxes"] = per
    return res


def main():
    seed, seed_line = seed_lines()
    out = {"protocol": PROTO, "protocol_sha256": sha(open(PROTO, "rb").read()),
           "seed_first_line_no": seed_line, "seed": seed, "name": NAME, "results": []}
    for label, rev in REVS.items():
        full = git("rev-parse", rev).stdout.decode().strip()
        text_b = blob(full, "SHONEN.md")
        r = analyse(label, full, text_b.decode("utf-8"), seed,
                    lambda p, full=full: blob(full, p))
        r["shonen_sha256"] = sha(text_b)
        r["shonen_git_blob"] = git("rev-parse", f"{full}:SHONEN.md").stdout.decode().strip()
        out["results"].append(r)
    wt = open(os.path.join(LANE, "SHONEN.md"), "rb").read()

    def wt_resolve(p):
        fp = os.path.join(LANE, p)
        return open(fp, "rb").read() if os.path.isfile(fp) else None

    r = analyse("working-copy", "WORKTREE", wt.decode("utf-8"), seed, wt_resolve)
    r["shonen_sha256"] = sha(wt)
    out["results"].append(r)
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
```

### box3_cover.py (verbatim)

```python
#!/usr/bin/env python3
"""Independent necessary-condition reconstruction of SHONEN box-3 ledger coverage.

Re-implements (does not import or execute) the documented sectionizer of
tameshi .ufo/evidence/round-18/measure.py (HEADING_RE ^#{1,3}(\\s|$) outside ```
fences; section = heading line .. line before next heading, trailing blank lines
stripped, '\\n'-joined, no trailing newline; preamble before first heading) and
checks, per revision, (a) section sha256 matched by >=1 ledger entry and
(b) >=1 matching entry whose recorded inputs (minus SKILL.md and the r17/r18
ledger paths) are blobs at REV with equal sha256. Trace, veto and class gates
are NOT reconstructed, so (b) is an upper bound on strict credit.
Reads git blobs only with GIT_OPTIONAL_LOCKS=0; writes nothing in the lane.
"""
import hashlib, json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
LEDGERS = {".ufo/evidence/round-17/coldread/ledger.json",
           ".ufo/evidence/round-18/coldread/ledger.json",
           ".ufo/evidence/round-19/coldread/ledger.json"}
# r18 IGNORED_INPUTS plus the r19 wrapper's added ledger path
IGNORED = {"SKILL.md"} | LEDGERS
HEADING_RE = re.compile(r"^#{1,3}(?:\s|$)")
ENV = {"PATH": "/usr/bin:/bin", "GIT_OPTIONAL_LOCKS": "0", "HOME": os.environ.get("HOME", "/tmp")}
REVS = [("r18-delivered", "4b7c6823a462f5ea2eafcb262275300a545f3ed7"),
        ("r19-baseline", "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190"),
        ("r19-land-1", "21e79329f8bdcf01a62be63b3e46db4a7de6b6f9"),
        ("r19-land-2", "7af123b0e068cd5e6b651aab31a813cc170d70a2"),
        ("r19-land-3", "c5730cc5d39ac45ad147c9cac29573ea04745ab5"),
        ("r19-land-4", "88c8073a79e94d9fcc47deba0b04aa087fdabb4c"),
        ("r19-land-5", "cecaefe73482504a814064dd7b2242c8c0b8ad50")]
LINK_RE = re.compile(r"\]\(([^)\s#]+)")


def box3_ledger(rev):
    """Ledger path linked from the SHONEN box-3 block at REV (box line + indented continuation)."""
    lines = blob(rev, "SHONEN.md").decode("utf-8").split("\n")
    boxes, cur = [], None
    for l in lines:
        if re.match(r"^- \[[x~ ]\] ", l):
            cur = [l]
            boxes.append(cur)
        elif cur is not None and l[:1] in (" ", "\t") and l.strip():
            cur.append(l)
        else:
            cur = None
    m = LINK_RE.search("\n".join(boxes[2]))
    return m.group(1)


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True, env=ENV)


def blob(rev, path):
    p = git("cat-file", "blob", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def mode(rev, path):
    p = git("ls-tree", "-z", rev, "--", path)
    recs = [r for r in p.stdout.split(b"\0") if r]
    return recs[0].split(b" ")[0].decode() if len(recs) == 1 else None


def sectionize(raw):
    lines = raw.decode("utf-8", "surrogateescape").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    heads, fence = [], False
    for i, l in enumerate(lines):
        if l.strip().startswith("```"):
            fence = not fence
            continue
        if not fence and HEADING_RE.match(l):
            heads.append(i)
    pairs = ([(0, heads[0])] if heads and heads[0] > 0 else []) + list(zip(heads, heads[1:] + [len(lines)])) if heads else [(0, len(lines))]
    out = []
    for s, e in pairs:
        body = list(lines[s:e])
        while body and body[-1].strip() == "":
            body.pop()
        out.append({"start": s + 1, "end": e, "heading": lines[s] if s in heads else "",
                    "sha256": hashlib.sha256("\n".join(body).encode("utf-8", "surrogateescape")).hexdigest()})
    return out


def inputs_ok(rev, entry, cache):
    inp = entry.get("inputs")
    if not isinstance(inp, dict):
        return False, "inputs-not-dict"
    view = {k: v for k, v in inp.items() if k not in IGNORED}
    if not view:
        return False, "inputs-empty"
    for p, want in sorted(view.items()):
        key = (rev, p)
        if key not in cache:
            m = mode(rev, p)
            b = blob(rev, p) if m in ("100644", "100755") else None
            cache[key] = (m, hashlib.sha256(b).hexdigest() if b is not None else None)
        m, got = cache[key]
        if m is None:
            return False, f"input-missing:{p}"
        if m not in ("100644", "100755"):
            return False, f"input-not-blob:{p}"
        if got != want:
            return False, f"input-drift:{p}"
    return True, None


def main():
    res = []
    for label, rev in REVS:
        skill = blob(rev, "SKILL.md")
        ledger_path = box3_ledger(rev)
        ledger_raw = blob(rev, ledger_path)
        ledger = json.loads(ledger_raw)
        by_sha = {}
        for e in ledger["entries"]:
            by_sha.setdefault(e.get("sha256"), []).append(e)
        secs = sectionize(skill)
        cache, matched, inputs_pass, missing, drift = {}, 0, 0, [], []
        for s in secs:
            ms = by_sha.get(s["sha256"], [])
            if not ms:
                missing.append({"start": s["start"], "end": s["end"], "heading": s["heading"], "sha256": s["sha256"]})
                continue
            matched += 1
            oks = [inputs_ok(rev, e, cache) for e in ms]
            if any(ok for ok, _ in oks):
                inputs_pass += 1
            else:
                drift.append({"start": s["start"], "heading": s["heading"], "reasons": sorted({r for _, r in oks})})
        res.append({"label": label, "rev": rev, "box3_ledger": ledger_path,
                    "skill_sha256": hashlib.sha256(skill).hexdigest(),
                    "ledger_sha256": hashlib.sha256(ledger_raw).hexdigest(),
                    "ledger_entries": len(ledger["entries"]),
                    "ledger_expect_skill_sha": ledger.get("_meta", {}).get("expect_skill_sha"),
                    "sections_total": len(secs), "sha_matched": matched,
                    "sha_matched_and_inputs_equal": inputs_pass,
                    "unmatched_sections": missing, "input_gate_failures": drift})
    json.dump(res, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
```

Note: the docstring of `box3_cover.py` says the ignored set is "SKILL.md and the r17/r18
ledger paths". The code, via `LEDGERS`, also ignores the round-19 ledger path. That
matches the round-19 wrapper's `IGNORED_INPUTS | {LEDGER}`.
