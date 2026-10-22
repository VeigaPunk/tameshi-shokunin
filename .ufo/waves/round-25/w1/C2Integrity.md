# C2Integrity — vendored MTE vendor tarballs vs npm registry and GitHub master schema

Lane: TameshiR25 / round 25, wave 1. Target revision: c9ff09fb41fb8aac5fc335faf10858ff606bd5df.
Scope: `tameshi-shokunin/tools/vendor/*.tgz` verified against the npm registry, the `PACKAGES` table in `tools/mte-interop.py`, the sha512 of the files, and the GitHub master schema member. Read-only; wrote only this report (plus `/tmp/c2integ` scratch).

## Verdict

PASS on every named check. The two vendored tarballs are byte-identical to the official `registry.npmjs.org` artifacts, match their npm registry `dist.integrity`, match the `sha512` pins in the `PACKAGES` table, and the schema member the tool reads (`package/src/mutation-testing-report-schema.json`) is byte-identical to the GitHub master file. No correction needed; nothing differs.

## Findings (all PASS, evidence under each)

### 1. Vendored files ↔ `PACKAGES` pins (sha512) — match

`tools/mte-interop.py:50-56` pins two entries; `:158-163` (`verified_tarball`) recomputes `sha512-<base64>` from the tarball bytes and raises on mismatch.

Pin (base64) decoded to hex vs `sha512sum` of the vendored files:

| file | PACKAGES pin (b64→hex) | file sha512sum | match |
|---|---|---|---|
| `mutation-testing-report-schema-3.9.0.tgz` | `dbc0a86e…f15225` | `dbc0a86eb70b7509b7e73c927a668b30aad4a5571c2cc0350de9141ad7decce4a69c8d17abca098ac8b16273b4050608c0a0a428befe004ef5fee5aafef15225` | exact |
| `mutation-testing-metrics-3.9.0.tgz` | `1368bef1…c8e71` | `1368bef1b5e81124fc288c89ca673e3a33b7796f90da0040c08fa1874b6f119c627fd9d94276b0021ffeda12d683e699456b06e6cdc8e710c01997c42f10bb87` | exact |

Command: node script decoding the pin from base64 to hex and hashing the file bytes (independent of the tool's own code path); output `match_pin=true` for both.

### 2. Pins ↔ npm registry `dist.integrity` — match

`npm view mutation-testing-report-schema@3.9.0 dist.integrity` →
`sha512-28CobrcLdQm35zySemaLMKrUpVccLMA1DekUGtfezOSmnI0Xq8oJisixYnO0BQYIwKCkKL7+AE71/uWq/vFSJQ==`
`npm view mutation-testing-metrics@3.9.0 dist.integrity` →
`sha512-E2i+8bXoEST8KIyJymc+OjO3eW+Q2gBAwI+hh0tvEZxif9nZQnawAh/+2hLWg+aZRWsG5s3I5xDAGZfELxC7hw==`

Both strings are character-for-character equal to the `PACKAGES` entries at `tools/mte-interop.py:52-55`. Registry also confirms `name`/`version` as pinned.

### 3. Vendored bytes ↔ freshly packed official artifacts — byte-identical

Two independent retrievals on 2026-10-22, both compared with `cmp` against the vendored files:

- `cd /tmp/c2integ && npm pack mutation-testing-report-schema@3.9.0 mutation-testing-metrics@3.9.0 --pack-destination /tmp/c2integ` → sha512 of both equals the vendored hashes above.
- Direct `curl https://registry.npmjs.org/<name>/-/<name>-3.9.0.tgz` for both → `cmp` clean both ways; `DIRECT_DOWNLOAD_IDENTICAL`.

Provenance on the registry packages: maintainers `nicojs`, `strykermutator-npa` (the official Stryker Mutator npm org), license `Apache-2.0`, `main = dist/src/index.js` — consistent with the stryker-mutator/mutation-testing-elements monorepo packages of the same names.

### 4. Tool-read schema member ↔ GitHub master — byte-identical

The tool reads `SCHEMA_MEMBER = 'package/src/mutation-testing-report-schema.json'` (`tools/mte-interop.py:57`, loaded in `load_schema()` at `:167-171` directly from the tarball, no extraction to disk).

- GitHub master `https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/master/packages/report-schema/src/mutation-testing-report-schema.json` → 12799 bytes, sha512 `a8568aeb…1d3999a`.
- `tar -xzf` of the vendored tgz then `cmp package/src/mutation-testing-report-schema.json master-schema.json` → `SRC_MEMBER_IDENTICAL_TO_MASTER` (exit 0). **What differs: nothing.**

Side note (not a defect): the tgz also carries `package/dist/src/mutation-testing-report-schema.json` (16445 bytes), which differs from master only in whitespace (`cmp` differs at line 2 char 5 — prettier-rendered). It is semantically identical to the src member (`JSON.stringify(src) === JSON.stringify(dist)` → true), and the tool does not read it.

### 5. Member is a valid draft-07 schema and the tool's usage compiles

`uv run --no-project --with jsonschema==4.25.1 python3` compiling the vendored member with `jsonschema.Draft7Validator` succeeds; it validates a minimal `{"schemaVersion":"1","thresholds":{"high":80,"low":60},"files":{}}` document and rejects one missing `files`. This matches the tool's call pattern (`Draft7Validator(load_schema())`, `:237`-ish in `check()`).

### 6. Version currency — no drift

`npm view <pkg> dist-tags.latest` → `3.9.0` for both packages; the version lists end at `3.9.0` (history `3.8.0`, `3.8.4`, `3.9.0`). The pins reference the current release of both packages, so the vendored set is not stale.

## Tarball hygiene (checked in passing)

Member listing (`tar -tzvf`) shows only `package/{LICENSE,README.md,package.json,tsconfig,src,dist,…}` files; no install scripts, no executables outside `dist/`. The tool's own extraction guard (`official_metrics`, `:182-193`) rejects members outside `package/` and `..` components and writes only under a mkdtemp — consistent with what the tarballs contain. The metrics tarball contains no schema files; the schema lives only in the report-schema tarball, and grep over `tools/` finds `mutation-testing-report-schema.json` referenced only in `mte-interop.py` — single source of truth.

## Residual risk / verification gaps

- Trust anchors: the registry integrity came from `npm view` over TLS to `registry.npmjs.org`, and the master schema from raw.githubusercontent over TLS; a CA/TLS compromise at fetch time would be needed to fool both, but npm provenance attestations were not verified, nor was the Stryker git release tag cross-checked. Cheap hardening if ever needed: `npm audit signatures` or publishing the observed registry hashes as the permanent pin (which the `PACKAGES` table already effectively is, per finding 2).
- The `PACKAGES` pin and the code that enforces it live in the same file (`mte-interop.py`), so the pin is only as trustworthy as the lane revision itself; this check pins the artifacts to the registry, which is the stronger anchor, so residual risk here is negligible for the artifacts.
- The metrics package is verified only against the registry, not against a GitHub-built artifact (Stryker publishes no identical build output in the repo; the repo sources compile `src/*.ts` to `dist/*.js` via tsup with output not committed). Registry integrity + official maintainers is the strongest reachable anchor for it; the tgz contains both compiled `dist/` and original `src/` for review (the tool runs `dist/src/…` via `main`).

## Tooling record

No tools installed or upgraded (operator 2026-10-19 directive): used preinstalled `node` v24.21.0 / `npm` 11.19.0 / `curl`, plus `uv run --with jsonschema==4.25.1` (no global install). All work in `/tmp/c2integ` scratch; no production files touched, no git/jj writes in the lane.
