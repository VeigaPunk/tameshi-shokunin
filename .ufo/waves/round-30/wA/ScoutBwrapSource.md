# ScoutBwrapSource — bwrap 0.13.1 flag meanings

Seat: TameshiR30A2.ScoutBwrapSource-7. Axis: freshness. No tools installed. No lane file except this report was written. No gate was run. `c1-measure-v4.py` and `corpus/SOURCES.md` were not edited.

## Verdict

`--unshare-all` in bwrap 0.13.1 is not "share nothing." The manual defines it as six flags, and two of those six are try-else-skip. Mount setup, environment, procfs, tmpfs, parent death, and the terminal session are separate sentences. v4's sandbox is whatever that argv actually passes (`c1-measure-v4.py:321-326` and the extra `--bind` / `--chdir` at `:335`), which is the rule the upstream README states.

Local rendered `man bwrap` (package bubblewrap 0.13.1-1) and upstream `bwrap.xml` at tag v0.13.1 say the same things for every flag below. Opened 2026-10-23.

## Evidence

### What was opened

- `bwrap --version` printed `bubblewrap 0.13.1`. `type bwrap` resolved `/usr/bin/bwrap`.
- `pacman -Qi bubblewrap`: Name bubblewrap, Version `0.13.1-1`, URL `https://github.com/containers/bubblewrap`, Install Date Tue 20 Oct 2026 09:16:29 AM -03.
- `man -w bwrap` printed `/usr/share/man/man1/bwrap.1.gz` (649 groff lines). `man bwrap` was read in full.
- Upstream file: `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/bwrap.xml` HTTP 200, 33289 bytes, 681 lines, sha256 `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da`. The same bytes at commit `362936aea0d5c6e70f7af75d2d44b5a914cb4ba2` (same size, same sha256).
- Upstream README: `https://raw.githubusercontent.com/containers/bubblewrap/v0.13.1/README.md` HTTP 200, 10687 bytes, 246 newlines, sha256 `0c1dc12c6d94017c45e220fc0e5b679f24c0f09494bdd4bc7157d8abcd75c001`.
- GitHub tag object `46ec5c413a3c1da265624ddac3a715b4d1bc487d` (annotated tag `v0.13.1`, tagger Alexander Larsson, `2026-10-14T12:16:41Z`, message "Released: 2026-10-14") points at commit `362936aea0d5c6e70f7af75d2d44b5a914cb4ba2`.

A scan of that `bwrap.xml` for a line containing both "time" and "namespace" hit only line 173, because "sometimes" contains the letters "time" next to the phrase "user namespaces." There is no time-namespace option in the file.

### Where v4 passes the flags

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v4.py:321-326`:

```
bwrap --unshare-all --die-with-parent --new-session --clearenv
  --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib
  --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc
  --proc /proc --dev /dev --tmpfs /tmp
  --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp
```

The selftest call (`:335-336`) appends `--bind <work> /w --chdir /w bash <runner> --selftest` and sets Python `start_new_session=True`. That Python flag is not `--new-session`.

## Quotes (25 words or fewer)

Rendered `man bwrap` matches each sentence. Locators below are `bwrap.xml` at the commit above, unless noted. Groff line numbers are `/usr/share/man/man1/bwrap.1.gz`.

### `--unshare-all`

"Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try" (13 words). `bwrap.xml:159`. Groff `:137-145`.

The two try flags, same file:

- "Create a new user namespace if possible else skip it" (10). `:131`. Groff `:104`.
- "Create a new cgroup namespace if possible else skip it" (10). `:155`. Groff `:134`.

### `--clearenv`

"Unset all environment variables, except for PWD and any that are subsequently set by --setenv" (15). `:233-235`. Groff `:226-231`.

### `--proc`

"Mount procfs on DEST" (4). `:403`. Groff `:423-426`.

### `--tmpfs`

"Mount new tmpfs on DEST. If the previous option was --perms, it sets the mode of the tmpfs. Otherwise, the tmpfs has mode 0755." (24). `:412-414`. Groff `:435-439`.

"If the previous option was --size, it sets the size in bytes of the tmpfs. Otherwise, the tmpfs has the default size." (22). `:415-416`. Groff `:439-440`.

The manual never states a byte count for that default.

### `--die-with-parent`

"Ensures child process (COMMAND) dies when bwrap's parent dies." (9). `:589`.

"Kills (SIGKILL) all bwrap sandbox processes in sequence from parent to child including COMMAND process when bwrap or bwrap's parent dies." (21). `:589-591`. Same paragraph: "See prctl, PR_SET_PDEATHSIG." (`:592`). Groff `:589` joins both sentences.

### `--new-session`

"Create a new terminal session for the sandbox (calls setsid())." (10). `:575`.

"This disconnects the sandbox from the controlling terminal which means the sandbox can't for instance inject input into the terminal." (20). `:575-577`.

"if you don't use --new-session, it is recommended to use seccomp to disallow the TIOCSTI ioctl" (16). `:579-580`. The note names CVE-2017-5226 (`:583`).

README `:162-163`: "If you are not filtering out TIOCSTI commands using seccomp filters, argument --new-session is needed" (15).

## Documented caveats (what is not sealed by the word "all")

1. User and cgroup are optional. The equivalence uses `--unshare-user-try` and `--unshare-cgroup-try`, not `--unshare-user` and `--unshare-cgroup`. Either namespace stays the caller's if the try skips. Separately, the description says "the user namespace is required if bwrap is not run as root" (12 words, `:57-58`, groff `:44`). The manual does not say which exit status follows a skipped user namespace. That runtime result was not measured here.

2. The mount namespace is not one of the six flags. "By default, bwrap creates a new mount namespace for the sandbox." (11, `:56`). README `:133`: "bubblewrap always creates a new mount namespace" (7). The empty root is that default, not an `--unshare-all` effect: "creating a new, completely empty, filesystem namespace where the root is on a tmpfs that is invisible from the host" (20, `:49-50`). [INFERENCE] the "filesystem namespace" sentence and the "mount namespace" sentence are the same default, because they are consecutive and only the mount namespace is named as the default. Later mounts put host paths back into it.

3. A later `--share-net` puts the network namespace back. "Retain the network namespace, overriding an earlier --unshare-all or --unshare-net" (10, `:163`). "When options are used multiple times, the last option wins, unless otherwise specified." (13, `:73`). v4's argv has no `--share-net`.

4. `--unshare-all` does not block further user namespaces. `--disable-userns` does: "Prevent the process in the sandbox from creating further user namespaces, so that it cannot rearrange the filesystem namespace" (19, `:178-179`). "This option requires --unshare-user." (4, `:185`). It does not say `--unshare-user-try` or `--unshare-all` is enough. v4 passes neither `--disable-userns` nor `--unshare-user`. The same page says "sometimes bubblewrap itself creates nested user namespaces (to work around some kernel issues)" (13, `:173`), so one successful user setup is not documented as exactly one namespace.

5. No time namespace is named. README `:137-152` lists CLONE_NEWUSER, CLONE_NEWIPC, CLONE_NEWPID, CLONE_NEWNET, CLONE_NEWUTS, and seccomp. It does not list cgroup or time. The manual's equivalence does list cgroup (as try). The option entry, not the shorter README list, is the meaning of `--unshare-all`. Absence of a time-namespace option is a property of this text, not a kernel measurement.

6. `--clearenv` keeps `PWD`. The word "subsequently" is the manual's order rule: a `--setenv` placed before `--clearenv` is outside the exception. v4 puts the four `--setenv` options after `--clearenv` (`:321` then `:325`), so PATH, HOME, LANG, and TMPDIR are inside the exception, and `PWD` still survives. This was not tested by swapping the order.

7. `--proc` only mounts procfs. "The sandbox will not see any processes outside the sandbox." (10) is README `:145`, under PID namespaces, not under `--proc`. `--unshare-pid` is in the six-flag list and is not a try flag. v4 therefore asks for a new pid namespace and, separately, mounts procfs at `/proc`.

8. v4's `--tmpfs /tmp` is preceded by `--dev /dev` (`:324`), not by `--perms` or `--size`. Documented result: mode 0755, and whatever "the default size" means. No byte cap is stated.

9. `--die-with-parent` is a death signal, not a namespace. The same paragraph first names the parent's death, then says the kill also happens when bwrap itself dies, and that the kill is SIGKILL of all sandbox processes from parent to child. It cites `PR_SET_PDEATHSIG`. It does not describe a race if the parent is already dead.

10. `--new-session` is `setsid` and a disconnected controlling terminal. It is the documented alternative to a seccomp filter for TIOCSTI (CVE-2017-5226). It does not unshare anything. v4 passes `--new-session` and passes no `--seccomp` or `--add-seccomp-fd`.

11. The finished sandbox is the argv, not the tool. README `:45-46`: "bubblewrap is not a complete, ready-made sandbox with a specific security policy" (12). README `:52-54`: "the level of protection between the sandboxed processes and the host system is entirely determined by the arguments passed to bubblewrap" (21). README `:167-168`: "Everything mounted into the sandbox can potentially be used to escalate privileges." (12). v4 ro-binds host `/usr` and `/etc`.

12. Two defaults sit outside `--unshare-all`. "By default no caps are left in the sandboxed process." (10, `:615`). README `:37`: "bubblewrap uses PR_SET_NO_NEW_PRIVS to turn off setuid binaries" (8).

### What remains shared, on this text alone

Shared or still reachable unless some other flag says otherwise:

- the user namespace, if `--unshare-user-try` skips
- the cgroup namespace, if `--unshare-cgroup-try` skips
- the network namespace, if a later `--share-net` is present (not in v4)
- `PWD` after `--clearenv`
- host content at every path the argv mounts (`/usr` and `/etc` in v4)
- the ability to create further user namespaces (`--disable-userns` is absent, and it requires `--unshare-user`)
- the controlling terminal, unless `--new-session` or a TIOCSTI seccomp filter is also present
- seccomp, which none of these flags loads

Not claimed: that a time namespace stays shared. The opened 0.13.1 manual and README never name one. Not claimed: an observed `bwrap` exit code. This seat did not run `bwrap`.

## Smallest safe correction

When a counter claim says v4 isolation "is `--unshare-all`," replace that with the argv's own flags:

- mount namespace: always new, empty tmpfs root, then the binds
- ipc, pid, net, uts: requested by the equivalence, not as try flags
- user and cgroup: requested only as try-else-skip
- environment: cleared except `PWD` and the four later `--setenv` values
- `/proc`: a procfs mount; hiding other processes is the pid-namespace sentence
- `/tmp`: a new tmpfs, mode 0755, size unnamed
- `/dev`: a new devtmpfs (`:407`), which this report was not asked to define beyond that
- parent death: SIGKILL via `PR_SET_PDEATHSIG` when bwrap or its parent dies
- terminal: `setsid`, the documented TIOCSTI mitigation, with no seccomp program in the argv
- host `/usr` and `/etc` remain visible
- nested user namespaces are not disabled

Do not treat Python `start_new_session=True` (`:336`) as `--new-session`.

## Draft row S093

Not appended. `corpus/SOURCES.md` as read this round ends at S092 (`:101`). Contract: `CORPUS.md` "SOURCES.md — where a shokunin learns" (v1, 11 cells, no `|` inside a cell). Status `queued` because nothing cites it yet. Recheck `on-release` because the manual says "Currently equivalent."

| S093 | bwrap(1), bubblewrap 0.13.1 — https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml | docs | A | documented meaning of --unshare-all, --clearenv, --proc, --tmpfs, --die-with-parent, and --new-session in bwrap 0.13.1; not a measured security boundary for any argv | tag v0.13.1, annotated tag 46ec5c413a3c1da265624ddac3a715b4d1bc487d, commit 362936aea0d5c6e70f7af75d2d44b5a914cb4ba2, released 2026-10-14; bwrap.xml:159, :233-235, :403, :412-416, :575-577, :589-592; README.md:52-54 and :133; xml sha256 2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da (33289 bytes); local man bubblewrap 0.13.1-1, /usr/share/man/man1/bwrap.1.gz:137-145, opened 2026-10-23 | score --unshare-all as its six-flag expansion, with user and cgroup try-else-skip, and score every other flag on its own sentence; the word all is not a sealed isolation claim | queued | 2026-10-23 | on-release | — |

### Gate quote (rule 1)

URL: `https://github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml` (raw bytes also fetched from commit `362936aea0d5c6e70f7af75d2d44b5a914cb4ba2`). Access date: 2026-10-23. Quote, 13 words, `bwrap.xml:159`: "Unshare all possible namespaces. Currently equivalent with: --unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try."

## Unresolved

- No `bwrap` process was started, so a skipped `--unshare-user-try` has no observed exit status.
- No probe of kernel time namespaces. The gap is only that this manual does not name one.
- Groff and `bwrap.xml` were compared sentence by sentence for these flags, not as a byte-identical man build.
- Another seat may take id S093 before this draft is appended. This report does not append it.
