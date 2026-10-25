seat: ExecRows20

# C1 row re-verification — S102, S103, S104 (author ledger entries)

Item: C1 row re-verification for rows S102, S103, S104. All three fetched live from the row's own URL, verdict `holds`, all three `--check` runs print `verified ok`. Raw snapshots kept at `/tmp/tameshi-r45-ExecRows20/{S102,S103,S104}.raw` for L1 integration (snapshot field names `.ufo/evidence/round-45/freshness/sources/S###.raw.gz`).

No tooling installed/updated (curl + python3 already present; no installs needed). No session/credential material read.

## S102 — POSIX.1-2024 Shell Command Language §2.3 Token Recognition

- URL: `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html`
- `curl -fsSL -A 'Mozilla/5.0' --max-time 90`: exit 0
- Bytes: 357,953 | sha256: `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` (identical to the round-35 committed snapshot hash in the row's anchor)
- CHECK: `CHECK S102 verified ok` (exit 0)
- Note: POSIX 2.3 `#` sentence still states that `#` at the current character discards it and all subsequent characters up to (excluding) the next newline as a comment — grounds the teaches claim (`a '#' at the point a token begins discards that character and all up to (excluding) the next newline as a comment`).
- Quote: 23 tokens, located afresh in `--extract` output; shares content words "character" / "newline" / "excluding" / "subsequent" with scope/anchor/teaches.

```json
{"id":"S102","url":"https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd","quote":"If the current character is a '#' , it and all subsequent characters up to, but excluding, the next <newline> shall be discarded","snapshot":".ufo/evidence/round-45/freshness/sources/S102.raw.gz","author":"ExecRows20","note":"The POSIX 2.3 # sentence still states that a '#' at the current character discards it and all subsequent characters up to (excluding) the next newline as a comment, exactly grounding the teaches claim."}
```

## S103 — git-hash-object (Git reference manual)

- URL: `https://git-scm.com/docs/git-hash-object`
- `curl -fsSL -A 'Mozilla/5.0' --max-time 90`: exit 0
- Bytes: 29,933 | sha256: `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100` (identical to the round-36 committed snapshot hash in the row's anchor)
- CHECK: `CHECK S103 verified ok` (exit 0)
- Note: DESCRIPTION first sentence still opens with "Computes the object ID value for an object with specified type with the contents of the named file" — grounds the content-addressed-identity teaches (`a blob's object ID is computed from the contents of the named file`).
- Quote: 18 tokens, located afresh in `--extract` output; shares content words "object" / "contents" / "named" / "file" with scope/anchor/teaches.

```json
{"id":"S103","url":"https://git-scm.com/docs/git-hash-object","opened":"2026-10-25","verdict":"holds","raw_sha256":"dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100","quote":"Computes the object ID value for an object with specified type with the contents of the named file","snapshot":".ufo/evidence/round-45/freshness/sources/S103.raw.gz","author":"ExecRows20","note":"The DESCRIPTION first sentence still opens with 'Computes the object ID value ... with the contents of the named file', grounding the content-addressed-identity teaches."}
```

## S104 — GNU Bash Reference Manual 5.3 source (doc/bashref.texi)

- URL (byte-exact, incl. fragment): `https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303#L494-L495`
- `curl -fsSL -A 'Mozilla/5.0' --max-time 90` (fragment not sent to server): exit 0
- Bytes: 415,804 | sha256: `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`
- CHECK: `CHECK S104 verified ok` (exit 0)
- Note: `@node ANSI-C Quoting` still describes `$'...'` sequences as a special kind of single quotes with backslash escapes decoded per ANSI C — grounds the teaches claim (`Treat $'...' as a single-quoted region while honoring backslash escapes`).
- Quote: 15 tokens, located afresh in `--extract` output; shares content words "single" / "quotes" with scope/anchor/teaches.

```json
{"id":"S104","url":"https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303#L494-L495","opened":"2026-10-25","verdict":"holds","raw_sha256":"f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5","quote":"Character sequences of the form @code{$'@var{string}'} are treated as a special kind of single quotes.","snapshot":".ufo/evidence/round-45/freshness/sources/S104.raw.gz","author":"ExecRows20","note":"The ANSI-C Quoting node still describes $'...' sequences as a special kind of single quotes (with backslash escapes decoded per ANSI C), grounding the teaches claim."}
```

## Summary

| row | curl exit | bytes | sha256 | CHECK |
|-----|-----------|-------|--------|-------|
| S102 | 0 | 357,953 | `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` | `CHECK S102 verified ok` |
| S103 | 0 | 29,933 | `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100` | `CHECK S103 verified ok` |
| S104 | 0 | 415,804 | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` | `CHECK S104 verified ok` |

All three fragments validated via:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check /tmp/tameshi-r45-ExecRows20/S###.json --snapdir /tmp/tameshi-r45-ExecRows20`

Risks/blockers: none. Fragments authored (ExecRows20); non-author falsify-wave agree pending. Raw files retained in `/tmp/tameshi-r45-ExecRows20/` for L1 integration.
