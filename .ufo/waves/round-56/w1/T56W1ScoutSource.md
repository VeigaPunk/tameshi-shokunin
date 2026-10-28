# T56W1ScoutSource — one external source for C2

Opened 2026-10-28T18:42:42Z. No tool was installed (curl 8.23.0 already on the host). Nothing in `corpus/`, `SKILL.md`, `tools/`, or the frozen round-56 instruments was edited. The row below is a proposal; this seat did not append it.

## Admitted

| | |
|---|---|
| URL | https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md |
| Raw | https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md |
| Access | 2026-10-28T18:42:42Z, curl 8.23.0, HTTP/2 200, `text/plain; charset=utf-8` |
| Pin | tag `v1.2.0`, commit `df02077bf97218a8860a5c534eff1f1381f56984` |
| Same bytes | `main` `50bf01716982189898823e90586075f37cd9bb7d` (2026-10-21) and the file's last change `06eafe3635bf8a425ad52cc82c6c90861e94a471` (2024-05-06, "Clarify that digests don't have to be cryptographic ones.") |
| sha256 | `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` |
| Size | 2492 bytes, 73 lines |
| Snapshot | `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md` (the HTTP body; the sha256 is of this file) |

The three raw URLs (last-touch commit, `v1.2.0`, `main`) hashed equal. Receipt: `.ufo/waves/round-56/w1/T56W1ScoutSource-receipts/fetch.txt` and `sha256sum.txt`. The GitHub etag `913aa95e…cdbb08` is not this sha256.

**Quote (11 words).** Heading `## Fields`, field `subject`, the paragraph that begins `IMPORTANT`, snapshot lines 54-55. The snapshot breaks the sentence after "regardless of". Drop the leading `> ` and fold the newline:

> Subject artifacts are matched purely by digest, regardless of content type.

Line 54 is `> IMPORTANT: Subject artifacts are matched purely by digest, regardless of`. Line 55 begins `> content type.`

Same field, lines 36-37, folded the same way: "Set of software artifacts that the attestation applies to. Each element represents a single software artifact. Each element MUST have `digest` set." Lines 3-4: the Statement binds the attestation "to a particular subject".

**Inference, not the spec's words.** A statement whose subject digest is not the artifact being evaluated is not evidence for that artifact. The spec states who the statement applies to and that the match is the digest. It does not say "evidence", and "regardless of content type" is not "regardless of name" (lines 42-45 let a consumer use `name` in policy).

**Tier.** A, for the scope "what an in-toto Statement v1 applies to". `CORPUS.md` gives A to a spec that is primary for that scope. Kind `spec`. It is not A for the lane's `rev=` encoding, and not A for DSSE verification.

**Proposed row (do not treat as appended).** Next unused id at base `981c5e8b` is S281 (SOURCES.md footer). Status stays `queued` until `corpus/knowledge/receipt-revision-binding.md` cites it; the C2 counter's docs arm counts that entry only when the cited row's status is `mined` and `used-by` names the entry. Recheck `365d`: re-fetch the raw URL at `v1.2.0` and at `main` and compare to the snapshot sha256. `on-release` would miss a `main`-only edit between tags.

```
| S281 | Statement layer specification (in-toto Attestation Framework v1) — https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md | spec | A | what an in-toto Statement v1 applies to: the artifacts its subject identifies by digest | ## Fields, subject, IMPORTANT paragraph, lines 54-55 @ v1.2.0 (commit df02077bf97218a8860a5c534eff1f1381f56984; fetched 2026-10-28; sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea; snapshot .ufo/evidence/round-56/assimilation/in-toto-statement-v1.md) | subject artifacts are matched purely by digest, and each subject element must have digest set | queued | 2026-10-28 | 365d | — |
```

## Duplicate check

`corpus/SOURCES.md` at the work tree (footer matches base `981c5e8b`). Every fragment exited 1 with no output. Receipt: `.ufo/waves/round-56/w1/T56W1ScoutSource-receipts/duplicate-sweep.txt`.

```
grep -n -F -- 'in-toto/attestation' corpus/SOURCES.md          exit=1
grep -n -F -- 'github.com/in-toto' corpus/SOURCES.md           exit=1
grep -n -F -- 'in-toto.io/Statement' corpus/SOURCES.md         exit=1
grep -n -F -- 'spec/v1/statement.md' corpus/SOURCES.md         exit=1
grep -n -F -- 'secure-systems-lab/dsse' corpus/SOURCES.md      exit=1
grep -n -F -- 'in-toto' corpus/SOURCES.md                      exit=1
grep -n -F -r --include='*.md' -- 'in-toto/attestation' corpus exit=1
```

Not a within-scope duplicate. Appending S281 does not trip census E04 on this URL.

## Rejected

DSSE Protocol, https://github.com/secure-systems-lab/dsse/blob/master/protocol.md — version 1.0.2 as printed in the file (May 10, 2024). Fetched the same minute. `master` `b531b787bb3e5f0c3e1c19cee84da1c5d569b061` (2026-10-09) is byte-identical to the file's last change `1d14ad6f941e31670a9ee42d64afd8ce1572bc37`. sha256 `6c0d965475162230f9f461acf634b4d4b409eab1a1839d31a9c24c76b3676253`. Snapshot: `.ufo/waves/round-56/w1/T56W1ScoutSource-receipts/dsse-protocol.md` (a receipt, not an assimilation source).

**Quote (6 words).** `## Signature Definition`, parameters, line 27: "SERIALIZED_BODY: Arbitrary byte sequence to be signed."

**Reason.** The protocol signs an arbitrary byte string plus a payload type. It never names a subject and never requires a digest. Verification (lines 91-101) stops at signature, payload type, and parse. A signed statement about another revision still verifies, so this page cannot ground "a statement about another subject is not evidence."

**Why it looks related.** Line 36 uses `application/vnd.in-toto+json` as a payload-type example. That is the envelope a statement travels in.

**Flip.** Admit it for this scope only if the protocol required the verifier to reject a payload whose subject digest is not the artifact being evaluated. It does not. Do not append a row.

## Search log

Question: which primary spec says an attestation applies only to the subject it identifies by digest? Date 2026-10-28. Identified 2, screened 2, included 1 (statement spec), excluded 1 (DSSE). Stop: the included page is the spec of the statement shape the claim names.

`resource_descriptor.md` is only a link from statement.md line 68. It was not opened as a source and is not quoted.
