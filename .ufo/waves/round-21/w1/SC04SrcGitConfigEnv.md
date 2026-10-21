done

# SC04 — Git environment source findings

## Opened-source record

- **Accessed:** 2026-10-21, fetch batch started `2026-10-21T12:08:15Z` (UTC). Both canonical pages returned HTTP 200. The static page reads also rendered their requested environment sections successfully.
- **Git manuals:** `https://git-scm.com/docs/git-config` and `https://git-scm.com/docs/git`.
- **Version/footer:** both pages show “last updated in 2.56.0”; the version list's current 2.56.0 entry is dated 2026-09-28. The host reports `git version 2.56.0` (separate from the documentation version assertion).
- **Saved fetched HTML:** `/tmp/tameshi-r21-SC04/fetch/git-config.html` SHA-256 `d8b55eb7227ea4bc30d38c274193fe1bd69a2fa866f21def34f28afad93ca1a3`; `/tmp/tameshi-r21-SC04/fetch/git.html` SHA-256 `abd98088a0dc6f92c7dc11ee9f34b71ec2b55bfbb879c71394dd6e8ff9eae28e`.

## Proposed SOURCES rows — draft only

Current registry says next unused ID is S079. Both rows are proposed as `mined` because the official manuals directly define the scoped behavior. `used-by` is a **proposed** citation destination, not a claim that the current knowledge file already cites these new IDs; per the SOURCES contract, the status must not be landed as mined until the knowledge/lesson citation is added.

```markdown
| S079 | git-config(1): Environment variables (Git 2.56.0 docs) — https://git-scm.com/docs/git-config | docs | A | Git's selected global/system configuration sources and bypass, for subprocess fixture hygiene | §ENVIRONMENT: GIT_CONFIG_GLOBAL, GIT_CONFIG_SYSTEM, GIT_CONFIG_NOSYSTEM @ Git 2.56.0 docs, fetched 2026-10-21 | GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM select alternate config files instead of defaults; GIT_CONFIG_NOSYSTEM skips system config, so inherited Git config is a separate fixture input from repository-location variables | mined | 2026-10-21 | on-release | corpus/knowledge/guard-kill-closure.md (proposed citation; pending) |
| S080 | git(1): Repository-related environment variables (Git 2.56.0 docs) — https://git-scm.com/docs/git | docs | A | Git's repository/worktree/index/object-database redirection and repository discovery | §ENVIRONMENT VARIABLES, The Git Repository: GIT_INDEX_FILE through GIT_COMMON_DIR @ Git 2.56.0 docs, fetched 2026-10-21 | GIT_DIR, GIT_WORK_TREE and GIT_COMMON_DIR redirect repository metadata or worktree; GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY and GIT_ALTERNATE_OBJECT_DIRECTORIES redirect index or object access; namespace and discovery variables change ref or discovery context | mined | 2026-10-21 | on-release | corpus/knowledge/guard-kill-closure.md (proposed citation; pending) |
```

**Duplicate check:** `git-config` URL is not present in the registry. `git` URL is an exact duplicate of S063 (`https://git-scm.com/docs/git`); S063's scope/anchor is repository discovery (`GIT_CEILING_DIRECTORIES`, `GIT_DIR`), not the full repository-variable list or git-config environment. S080 is complementary coverage on the same primary manual, not a correction to S063. Registry search found related but different URLs S062 (`git-rev-parse`) and S074 (`git-symbolic-ref`).

## Located quote evidence (all quotations verbatim and ≤25 words)

1. `git-config(1)`, §ENVIRONMENT, entries `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM`: “Take the configuration from the given files instead from global or system-level configuration.” (13 words.)
2. `git-config(1)`, §ENVIRONMENT, `GIT_CONFIG_NOSYSTEM`: “Whether to skip reading settings from the system-wide $(prefix)/etc/gitconfig file.” (11 words.)
3. `git(1)`, §ENVIRONMENT VARIABLES → The Git Repository, `GIT_DIR`: “If the GIT_DIR environment variable is set then it specifies a path to use instead of the default .git for the base of the repository.” (25 words.)
4. Same section, `GIT_INDEX_FILE`: “This environment variable specifies an alternate index file.” (8 words.)
5. Same section, `GIT_OBJECT_DIRECTORY`: “If the object storage directory is specified via this environment variable then the sha1 directories are created underneath” (17 words.)
6. Same section, `GIT_ALTERNATE_OBJECT_DIRECTORIES`: “This variable specifies a ":" separated (on Windows ";" separated) list of Git object directories which can be used to search for Git objects.” (24 words.)
7. Same section, `GIT_WORK_TREE`: “Set the path to the root of the working tree.” (10 words.)
8. Same section, `GIT_COMMON_DIR`: “If this variable is set to a path, non-worktree files that are normally in $GIT_DIR will be taken from this path instead.” (20 words.)
9. Same section, `GIT_NAMESPACE`: “Set the Git namespace; see gitnamespaces[7] for details.” (8 words.)
10. Same section, `GIT_CEILING_DIRECTORIES`: “it is a list of directories that Git should not chdir up into while looking for a repository directory” (18 words.)
11. Same section, `GIT_DISCOVERY_ACROSS_FILESYSTEM`: “This Boolean environment variable can be set to true to tell Git not to stop at filesystem boundaries.” (17 words.)
12. `git(1)`, §ENVIRONMENT VARIABLES → Other, config injection: “These environment variables will override values in configuration files, but will be overridden by any explicit options passed via `git` `-c`.” (21 words.)
13. `git-config(1)`, `core.worktree`: “Set the path to the root of the working tree.” (10 words.) This establishes the config key's path effect; it does not say every environment-config selector sets that key.

## Inherited variables relevant to a redirected fixture repo

The Git 2.56.0 manual separates direct path redirection from variables that change lookup context or configuration. For MB03–MB07, an inherited Git environment is not neutralized by unsetting only `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`:

- **Repository/worktree roots and metadata:** `GIT_DIR` substitutes a path for the default `.git` repository base; `GIT_WORK_TREE` sets the working-tree root; `GIT_COMMON_DIR` routes non-worktree files normally in `$GIT_DIR` to another path (worktree-specific `HEAD` and index remain in `$GIT_DIR`). These are direct repository/worktree context overrides.
- **Index/object state:** `GIT_INDEX_FILE` selects an alternate index. `GIT_OBJECT_DIRECTORY` selects the object storage directory instead of `$GIT_DIR/objects`. `GIT_ALTERNATE_OBJECT_DIRECTORIES` adds object directories used for object lookup; Git does not write new objects to those alternate directories. These can make reads/writes use state outside the fixture even when the selected working tree looks correct.
- **Repository view/discovery (not direct path settings):** `GIT_NAMESPACE` selects a refs namespace. `GIT_CEILING_DIRECTORIES` bounds the upward repository-discovery walk, but its documentation explicitly says it does not exclude an explicit `GIT_DIR`. `GIT_DISCOVERY_ACROSS_FILESYSTEM` changes whether discovery crosses filesystem boundaries and likewise does not affect an explicit `GIT_DIR`.
- **Configuration plane:** `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` select config files instead of the ordinary global/system files; `GIT_CONFIG_NOSYSTEM` suppresses system config. They do not themselves name a repository path, but the selected config can set `core.worktree` (which the git-config page defines as the working-tree root). `GIT_CONFIG_COUNT` with `GIT_CONFIG_KEY_<n>` / `GIT_CONFIG_VALUE_<n>` adds runtime config pairs that override file values; those are also relevant to config-driven location settings. The docs distinguish these from the direct path variables.
- **Conclusion [INFERENCE]:** for fixture isolation, scrub inherited `GIT_*` before Git invocations rather than maintaining only a three-variable list. At minimum the direct path/state set above must be neutralized. Keep config-file selectors and runtime config injection in the same scrub; disabling only `GIT_CONFIG_NOSYSTEM` does not neutralize global config or runtime pairs.

## Commands and evidence

- `mkdir -p /tmp/tameshi-r21-SC04/fetch && date -u '+%Y-%m-%dT%H:%M:%SZ' && curl -sSL --max-time 60 -o /tmp/tameshi-r21-SC04/fetch/git-config.html -w 'git-config HTTP %{http_code} %{size_download}B\n' https://git-scm.com/docs/git-config && curl -sSL --max-time 60 -o /tmp/tameshi-r21-SC04/fetch/git.html -w 'git HTTP %{http_code} %{size_download}B\n' https://git-scm.com/docs/git && sha256sum /tmp/tameshi-r21-SC04/fetch/git-config.html /tmp/tameshi-r21-SC04/fetch/git.html` — exit 0; HTTP 200, 830605 B and 244227 B respectively; hashes above; batch timestamp `2026-10-21T12:08:15Z`.
- `git --version` — exit 0; `git version 2.56.0`.
- Registry exact-URL search with `functions.grep`, path `corpus/SOURCES.md`, pattern `git-scm\.com/docs/(git-config|git)\b` — returned S063 exact `git` URL; no exact `git-config` URL. Related different URLs S062 and S074 are present.
- Read-only web reads: `https://git-scm.com/docs/git-config#_environment` and `https://git-scm.com/docs/git#_environment_variables`; successful section reads and quote checks above.
- No source registry edit, knowledge edit, tests, builds, or tools installed.
