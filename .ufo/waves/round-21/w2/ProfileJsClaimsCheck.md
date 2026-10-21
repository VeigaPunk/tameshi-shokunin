done

# js-claims-check F5 independent observation

## Findings

No falsification found for `js-claims-check`. The producer's `invariant` classification and clean exit 0 are independently reproduced from the pinned blob, including an actual `CLAIMS_SELFTEST: 39/39 pass` and `VERDICT: PASS` result (not a uniform usage/setup response).

## Pin and method

- Contract: `.ufo/evidence/round-21/c2-contract.json:31` pins `kumitate-shokunin`, revision `175de6ba2e9e904010411b19cab27e0af9aad3d4`, `scripts/claims-check.mjs`, SHA-256 `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`, interpreter `node`. The contract's seven required profiles and classification rules are at lines 9–22.
- Independently materialized the pinned Git blob with `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin cat-file blob 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs`; its observed SHA-256 was `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` (matches the contract). `git rev-parse 175de6ba2e9e904010411b19cab27e0af9aad3d4` returned that exact revision.
- Used the scratch-only independent observer `/tmp/tameshi-r21-ProfileJsClaimsCheck-lt2jRs/independent_f5_js_claims_check.py`; it does not import, invoke, or reuse `tools/env-diff.py` or its helpers. It fetched and hash-checked the blob itself, ran seven subprocesses concurrently in distinct fresh scratch directories, removed inherited `GIT_*` variables, used the required per-profile environments, and compared exact raw `(exit, stdout SHA-256, stderr SHA-256)` tuples without normalization.
- The command `python3 /tmp/tameshi-r21-ProfileJsClaimsCheck-lt2jRs/independent_f5_js_claims_check.py` completed successfully (exit 0). Runtime versions observed: bubblewrap 0.13.1, Node.js v24.21.0, Python 3.14.8. Each run used `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w node /tmp/w/target.mjs --selftest`; clean used `HOME=/tmp/w/home TMPDIR=/tmp/w/tmp LANG=C LC_ALL=C TZ=UTC` and inherited PATH. `clean_repeat` used a separate scratch directory. The other overlays were `TZ=Pacific/Chatham`, `LANG=LC_ALL=en_US.UTF-8`, `HOME=/nonexistent`, and `COLUMNS=20 LINES=5 TERM=dumb`.

## Results and producer comparison

| Profile | Exit | Stdout SHA-256 | Stderr SHA-256 | Suite output |
|---|---:|---|---|---|
| host | 0 | `fad7141588972f711c1961316414a6e6a6a2a573889f968cc6086cf6e44c318a` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 39/39 pass; PASS |
| clean | 0 | same | same | 39/39 pass; PASS |
| clean_repeat | 0 | same | same | 39/39 pass; PASS |
| tz | 0 | same | same | 39/39 pass; PASS |
| locale | 0 | same | same | 39/39 pass; PASS |
| home | 0 | same | same | 39/39 pass; PASS |
| columns | 0 | same | same | 39/39 pass; PASS |

All runs emitted exactly 42 stdout bytes (`CLAIMS_SELFTEST: 39/39 pass\nVERDICT: PASS\n`) and 0 stderr bytes. The tuple is identical across all seven profiles; `clean` and `clean_repeat` both exit 0. Therefore the independent classification is `invariant`, `sensitive_to: []`, agreeing with `.ufo/evidence/round-21/f5/receipt-final-production.json` for `js-claims-check` (which reports the same classification, exits, hashes and pass count).

There is no raw random-path variation in the valid observations. The pinned selftest creates a temporary directory via `mkdtempSync(join(tmpdir(), 'kumitate-claims-selftest-'))` at `scripts/claims-check.mjs:599–601` and removes it in `finally` at lines 853–855. On a successful run it emits the pass count and verdict at lines 861–862; the random path is not written to stdout/stderr.

Preserved harness note: an initial local attempt mistakenly set clean-profile `HOME`/`TMPDIR` to the *outer host* scratch path rather than `/tmp/w/home` and `/tmp/w/tmp` inside bubblewrap. That attempt failed with `ENOENT` in `mkdtemp`; its clean and repeat stderr included their different outer scratch paths. I corrected the observer to the contract's in-sandbox paths and excluded that setup-error run from the independent seven-profile result above. It was an observer setup defect, not producer nondeterminism.

## Residual risk and verification gaps

This is scoped only to `js-claims-check`; the other eight frozen surfaces, the whole F5 gate, and C2 admission were not re-executed here. No source behavior beyond this pinned selftest surface is established by this result.

## Evidence

Independent result: `.ufo/waves/round-21/w2/surfaces/js-claims-check.json` (SHA-256 `7817fd023ba2e82c073c09de417fb61e7b8e02642bd9c7770593faac9918c3a3`).
