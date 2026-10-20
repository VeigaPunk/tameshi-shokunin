# `sources-check.mjs` strace summary

- Target: kumitate `scripts/sources-check.mjs` at `0acb7752d19058b953ebbeba253b1e35f6548de5`, SHA-256 `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f`.
- Invocation: `strace -f -e trace=%file,%network -o <private-TMPDIR>/sources-check.strace.log env -i PATH=<dispatch PATH> HOME=<private> TMPDIR=<private> LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=<scratch> node sources-check.mjs --selftest`.
- Result: strace exit 0; target stdout ends `SOURCES_SELFTEST: 46/46 pass` / `VERDICT: PASS`; stderr 0 bytes. Trace retained as `strace.log` (4,814 lines, 497,006 bytes, SHA-256 `dbad6312c795ee5d3fa07db9b07572de7d1b443a93fd001e96cc922fdf156514`).

## Findings

- **Reads under `~/Projects`:** zero trace lines referenced `/home/vgpnk/Projects`.
- **Network-class syscalls:** 1,108 total: `socketpair=129`, `setsockopt=516`, `shutdown=43`, `getsockname=210`, `getsockopt=210`. The observed socket family was `AF_UNIX` (339 family-bearing lines); no `AF_INET`/`AF_INET6`, `connect`, `bind`, `send*`, or `recv*` calls. These are local Unix-domain IPC/socketpair operations, not observed external network access.
- **File writes/mutations:** 315 successful filesystem operations resolved within the private `TMPDIR` (fixture create/read-write/cleanup). The only successful write-capable open outside it was `openat(..., "/dev/null", O_WRONLY|O_CREAT|O_TRUNC, ...)` for a shell redirection; this is a special-device sink, not a persistent regular-file write. One `O_RDWR` open of `/dev/tty` failed with `ENXIO`. No successful regular-file or directory mutation outside `TMPDIR` was observed. Relative `unlinkat` paths were resolved through the traced directory descriptors and fell within `TMPDIR`.

**Scope limit:** the requested `%file,%network` trace does not include `write(2)`/`writev(2)` data syscalls. The report therefore classifies path-level writes from successful write-capable opens and filesystem mutation syscalls; stdout/stderr were captured by the parent process, and the trace includes the `/dev/null` sink open described above.
