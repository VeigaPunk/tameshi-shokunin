seat: RevJudge01

C1 falsify re-judgment of wave-1 ledger entries S064, S070, S103. Inputs read at commit ad5942c6e9858af19d00000b58439b321ddfa62b (`.ufo/evidence/round-45/freshness/ledger.json`, `.ufo/evidence/round-45/freshness/sources/S{064,070,103}.raw.gz`); live fetches done 2026-10-25 by me (non-author). Scratch under `/tmp/tameshi-r45-RevJudge01/`. No tools installed or upgraded (existing curl 8.x, python3, sha256sum, git only; none needed).

## Verdicts

- S064 agree — reviewer RevJudge01 — sha equal across my live fetch / ledger raw_sha256 / gunzipped committed snapshot (70e9d811ce19161107f482f2734f0c1f06af499aec1ff4f13cccd6343be3f00d), and the 20-token quote sits verbatim in the §Identifying non-hermeticity list body (not copied from the row's cells, 3 shared content words: absolute, binaries, paths), supporting the teaches claim's "host binaries, absolute paths ... named inputs outside the key".
- S070 agree — reviewer RevJudge01 — sha equal across my live fetch / ledger raw_sha256 / gunzipped committed snapshot (19fc78ffa39058c17ed038f2270855dcbb7055fe70c129f9a33b9c94a5566d95), and the 23-token quote opens the Repository Locations subsection body named by the anchor (not row-copied, 4 shared content words: folder, location, tree, walks), supporting "GIT_DIR names the .git folder and, when unset, git walks up parent directories".
- S103 agree — reviewer RevJudge01 — sha equal across my live fetch / ledger raw_sha256 / gunzipped committed snapshot (dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100), and the 18-token quote is the §DESCRIPTION first sentence named by the anchor (not row-copied, 4 shared content words: contents, file, named, object), supporting "a blob's object ID is computed from the contents of the named file".

## Provenance (sha256 comparisons)

Commands: `curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-RevJudge01/<id>.live '<entry.url>'`, `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show ad5942c6e9858af19d00000b58439b321ddfa62b:<entry.snapshot> | gunzip -c > <id>.snap`, then `sha256sum`.

```
70e9d811ce19161107f482f2734f0c1f06af499aec1ff4f13cccd6343be3f00d  S064.live
70e9d811ce19161107f482f2734f0c1f06af499aec1ff4f13cccd6343be3f00d  S064.snap   (ledger raw_sha256: same)
19fc78ffa39058c17ed038f2270855dcbb7055fe70c129f9a33b9c94a5566d95  S070.live
19fc78ffa39058c17ed038f2270855dcbb7055fe70c129f9a33b9c94a5566d95  S070.snap   (ledger raw_sha256: same)
dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100  S103.live
dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100  S103.snap   (ledger raw_sha256: same)
```

All three byte-equal → provenance confirmed; each quote is therefore also present in today's live text (identical bytes). S103's snapshot additionally matches the sha256 the row's own anchor recorded at round-36 (dd826dae...), so the page is unchanged since the row was mined.

## Located context (frozen counter normalization, ±~110 chars)

`python3 .ufo/evidence/round-45/freshness/measure.py --extract <id>.snap`:

- S064 (§Identifying non-hermeticity list item; 20 tokens): `... usually involving build IDs or timestamps System binaries that differ across hosts (such as /usr/bin binaries, absolute paths, system C++ compilers for native C++ rules autoconfiguration) Writing to the source tree during the build ...`
- S070 (Repository Locations subsection body; 23 tokens): `... Git uses several environment variables to determine how it interfaces with the current repository. GIT_DIR is the location of the .git folder. If this isn't specified, Git walks up the directory tree until it gets to ~ or / , looking for a .git directory at every step ...`
- S103 (§DESCRIPTION first sentence; 18 tokens): `... [--] <file>... DESCRIPTION Computes the object ID value for an object with specified type with the contents of the named file (which can be outside of the work tree), and optionally writes the resulting object into the object database ...`

None is nav/title/footer/cookie chrome; each is body content in the anchored section and says the claim.

## Mechanical cross-check with the frozen counter (seat helper, not a measurement)

`measure.py --check frag_<id>.json --snapdir /tmp/tameshi-r45-RevJudge01 --rev 3310e7be803516ca5934b4e949d91bcec824b179` (fragments = the ad5942c6 ledger entries):

```
CHECK S064 verified ok
CHECK S070 verified ok
CHECK S103 verified ok
```

This independently confirms quote length 6–25, quote-not-copied-from-row, and ≥2 shared content words. Residual risk: none observed for these three rows; verdicts rest on byte-identical live/snapshot/ledger evidence.
