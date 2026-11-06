# T89M1 post-hoc confirmation probes — NOT part of the pre-registered 23-defect sweep.
# Both target branches the pre-registered sweep's D19 (rev binding) / W_CONTROL arm
# left ambiguous. Same suite and runner as the primary sweep.
# Target: tools/ledger-witness.py @ 8876cca5dbb877b168aa09a86128d672f6b4ed5a (sha256 0839f587...).
@defect R01_MAT_REV_DROP | W_MAT: accept a `git show <anyrev>:PATH` exec (rev binding dropped; path suffix only)
@old and "show" in d[1] and want in d[1]
@new and "show" in d[1] and any(a.endswith(":" + path) for a in d[1])

@defect R02_CONTROL_BYTES | W_CONTROL: the pristine-copy bytes == pinned blob comparison dropped
@old if st["blob"] is not None and sha256_file(st["prist"]) != sha256_bytes(st["blob"]):
@new if False:
