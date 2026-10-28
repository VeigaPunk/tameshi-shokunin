# T54W1ScoutS278 — S278 re-opened

Axis: coverage. Milestone: source S278 re-opened independently.
No tools installed. Lane production files were not edited.

## What was opened

- Row: `corpus/SOURCES.md` line 153 (teaches cell is the note judged below). Anchor text: `` `_candidate_tempdir_list` :163-165 @ v3.12.7 (sha256 fb44155f...) ``.
- Related note that cites the same span: `corpus/knowledge/scratch-root-contract.md` lines 14 and 17–20.
- Source: `https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py`, fetched twice. Function body executed from that file (`_candidate_tempdir_list` and `_get_default_tempdir`). Interpreter: Python 3.14.8. The file under test is the 3.12.7 blob, not the host stdlib copy.

## Commands and output

First fetch (the command the item names), scratch copy later deleted:

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS278
curl -fsSL --max-time 60 -o /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS278/tempfile.py \
  https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py
sha256sum /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS278/tempfile.py
```

```
fb44155f430fac1923d3d7b6af1a0210edcfb580291d664e66f338491d68b62b  .../tempfile.py
```

32236 bytes, 952 LF lines, no CR.

Second fetch, same URL, written beside the proof (HTTP 200, 32236 bytes) and executed:

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ScoutS278-receipts/prove.py
```

Stdout: `.ufo/waves/round-54/w1/T54W1ScoutS278-receipts/prove.out`.
Fetched blob: `.ufo/waves/round-54/w1/T54W1ScoutS278-receipts/tempfile-v3.12.7.py`.
`NOTE_JOIN_MATCH True`. Both fetches share sha256 `fb44155f430fac1923d3d7b6af1a0210edcfb580291d664e66f338491d68b62b`. The row's `fb44155f...` is that prefix, not a different digest.

## Lines the row cites (:163-165)

The function starts at line 156. The cited span is only the environment loop, and those three lines are:

```
163|    for envname in 'TMPDIR', 'TEMP', 'TMP':
164|        dirname = _os.getenv(envname)
165|        if dirname: dirlist.append(dirname)
```

The teaches quote is those three lines with the body indentation removed and a `; ` between the assignment and the `if`. Token-for-token it matches. It does not add or drop a call.

## Does `if dirname:` skip an empty value?

Yes. `_os.getenv` returns `None` when the name is absent and `""` when it is set to empty. Both are falsy, so neither is appended.

Executed from the fetched function, with `TEMP` and `TMP` removed:

| `TMPDIR` | `getenv` | skipped | `dirlist` head |
|---|---|---|---|
| absent | `None` | yes | `['/tmp', '/var/tmp', '/usr/tmp', <cwd>]` |
| `""` | `''` | yes | same four entries; `""` not in the list |
| `""` and `TEMP=""` and `TMP=""` | all `''` | yes | same four entries |
| `" "` (one space) | `' '` | no | `[' ', '/tmp', ...]` |

A space is not an empty value. The note says "empty", so the space case bounds the claim; it does not falsify it. `bool("")` is `False`. `bool(None)` is `False`.

Empty and unset produce the same candidate list and, with no usable `TEMP`/`TMP`, the same winner: `_get_default_tempdir()` returned `/tmp` for both. "Empty behaves as unset" does not outrun this function.

## Does the note's sentence outrun the source?

Teaches sentence, byte-exact from `corpus/SOURCES.md` line 153:

> `for envname in 'TMPDIR', 'TEMP', 'TMP': dirname = _os.getenv(envname); if dirname: dirlist.append(dirname)` — an empty value is skipped, so empty behaves as unset and the next candidate wins

Split verdict.

- "an empty value is skipped" does not outrun. Line 165 is that test, and the run above shows `""` never enters `dirlist`.
- "empty behaves as unset" does not outrun inside `_candidate_tempdir_list` / `_get_default_tempdir`. Same list, same winner, for absent vs `""`.
- "and the next candidate wins" does outrun `:163-165`, and it is not always true of the rest of the file.

Those three lines only append a truthy environment value. They do not choose a directory. The chooser is `_get_default_tempdir` at lines 195–211: the first entry in which it can create, write, and unlink a file. Two runs with `TMPDIR=""`:

- `TEMP` set to a real writable directory: that directory is appended and it wins.
- `TEMP` set to a path that does not exist: `if dirname:` is still true, so the missing path is appended, and it does not win. The winner was `/tmp`.

So the next name wins only when it is usable. The cited lines do not say that, and they do not perform the selection. When `TEMP` and `TMP` are empty too, there is no next environment candidate in the cited loop; `/tmp` is appended later at line 173 and wins only because it is usable. Line 167's comment says "Failing that", but the `extend` is unconditional — the OS locations are always queued behind whatever the loop kept.

A sentence that would not outrun the file:

> an empty value is not appended, the same as an unset name; `_get_default_tempdir` later returns the first entry where it can create a file, which may be a later environment value or an OS location.

## Contract sentences that cite S278

`corpus/knowledge/scratch-root-contract.md` line 14:

> **unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278) and the platform default applies

"skips an empty candidate" holds. "the next candidate wins" has the same overreach as the row. "the platform default applies" holds in the tested case where `TEMP` and `TMP` are absent (`winner /tmp`, same as fully unset). It does not hold when `TEMP` is a usable directory: that directory won, not `/tmp`. Read as "whatever `gettempdir()` returns", the phrase is the resolver itself, and the unconditional "wins" is still the part that outruns.

Lines 18–20, "an empty `TMPDIR` never becomes a candidate directory", match the run (`empty_in_dirlist False`). That clause does not outrun. The next sentence ("A tool that treated `""` as a path would try to allocate under the working directory") is a counterfactual about code that lacks the `if`. It is consistent with this file's later `os.path.abspath` step (`abspath("") == getcwd()` was true in the same run; `os.path.join("", "probe")` is `probe`) but it is not what lines 163–165 do.

## Scratch

`/fast/scratch/hyaku/tameshi-r54/T54W1ScoutS278/` was removed after the receipt blob was confirmed identical to the curl download. Nothing left under that tree.
