# T54W1ScoutS279 — S279 re-opened

Axis: coverage. Milestone: source S279 re-opened independently.

S279 was fetched again, hashed, and compared with the committed snapshot, with the `corpus/SOURCES.md` teaches cell, and with `corpus/knowledge/scratch-root-contract.md`. No lane production file was edited. Scratch `/fast/scratch/hyaku/tameshi-r54/T54W1ScoutS279` was removed after the receipt copy.

## Re-open

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS279
cd /fast/scratch/hyaku/tameshi-r54/T54W1ScoutS279
curl -fsSL --max-time 60 -o tempfile.html -D headers.txt \
  -w 'http_code=%{http_code} size=%{size_download}\n' \
  https://docs.python.org/3/library/tempfile.html
sha256sum tempfile.html
```

Output:

```
http_code=200 size=75190 content_type=text/html
6b0edccf2e7f94fd574632a7ef445c7e0852ac0a362a7bfaed3aaf6b6b8ef7ba  tempfile.html
```

Response headers (selected): `HTTP/2 200`, `content-type: text/html`, `content-length: 75190`, `last-modified: Wed, 28 Oct 2026 12:45:58 GMT`, `etag: "6ae1ee86-125b6"`.

Same sha256 and same 75190 bytes as the committed snapshot `.ufo/evidence/round-54/assimilation/S279-tempfile-docs.html` (byte-identical). The row anchor `§tempfile.gettempdir @ fetched 2026-10-28 (sha256 6b0edccf...)` matches this prefix. `corpus/lessons/round-54.md` calls the same prefix "20462 B text-extracted"; that size is not this body. An HTMLParser strip of script/style produced 21248 bytes with a different sha (`4df9a301…`). The hash on the row is the HTML document, not a text extract.

Receipts: `.ufo/waves/round-54/w1/T54W1ScoutS279-receipts/tempfile.html`, `headers.txt`, `empty-scan.txt`.

## Search-list sentence the row quotes

Row teaches cell, byte-exact:

> "The list is: The directory named by the TMPDIR environment variable" then TEMP, TMP and platform locations — the documented order a missing or empty TMPDIR falls through

Located in the rendered `tempfile.gettempdir` definition (HTML id `#tempfile.gettempdir`). `TMPDIR` is not contiguous in the HTML: tags split it (`<span class="pre">TMPDIR</span>`). The visible text is:

> Python searches a standard list of directories to find one which the calling user can create files in. The list is:
>
> 1. The directory named by the TMPDIR environment variable.
> 2. The directory named by the TEMP environment variable.
> 3. The directory named by the TMP environment variable.
> 4. A platform-specific location: on Windows, `%USERPROFILE%\AppData\Local\Temp`, `%SYSTEMROOT%\Temp`, `C:\TEMP`, `C:\TMP`, `\TEMP`, and `\TMP`; on all other platforms, `/tmp`, `/var/tmp`, and `/usr/tmp`.
> 5. As a last resort, the current working directory.

The quoted words occur in that order. The row's "then TEMP, TMP and platform locations" matches items 2–4 and stops. Item 5 (current working directory) is on the same list and is not in the row.

The rest of that definition says the search result is cached (`tempdir`) and that 3.10 always returns a `str`. It does not mention an empty value.

## Does the note attribute the empty-string rule to the docs?

The page says nothing about empty. Case-insensitive counts on the 75190-byte document: `empty` 0, `unset` 0, `not set` 0, `blank` 0, `zero-length` 0, `falls through` 0, `getenv` 0. The four `""` hits are page chrome (`href=""` and a JS `replace`), not an environment-variable rule.

**The row's teaches gloss does attribute it.** The clause "the documented order a missing or empty TMPDIR falls through" states the empty-string rule as a property of the documented order. The page does not. "Missing" is also not the page's word; the supported claim is only that `gettempdir` walks that list until it finds a directory the caller can create files in.

**`corpus/knowledge/scratch-root-contract.md` does not attribute the empty-string rule to the docs.** The empty arm is pinned to S278 (`if dirname` / an empty value is not appended). The S279 citation is only the list's first entry and the fact that the documented search continues. That citation does not say the docs define `TMPDIR=""`.

## Sentences in `scratch-root-contract.md` that S279 does not support

S279 supports only the `gettempdir` search list above (ordered walk for a directory the caller can create files in; result cached; return type since 3.10). It does not support the following sentences. Citations in parentheses are the row the contract actually names, when it names one.

Supported, and therefore not in this list: the clause "the documented list also starts at \"the directory named by the TMPDIR environment variable\" and then falls through (S279)." "Falls through" here is the ordered search, which the page does state. It is not an empty-string rule. The contract's quotation lowercases the page's "The".

Not supported by S279:

1. "Every lane tool that allocates scratch through a `strict_scratch_root()` helper shares one contract."
2. "Before round 53 the helpers were seven near-copies of the same fifteen lines and only some of their callers mapped the failure to the documented class; round 54 makes the mapping uniform and this note is the rule the seven tools and their registry rows now name." ("documented class" here is the lane exit class, not the Python docs.)
3. Unset arm: "the platform default (`tempfile.gettempdir()`) is used" when `TMPDIR` is absent. The page documents `gettempdir`'s list; it does not state a closed "absent means the platform default" rule, and the same list's last resort is the current working directory, not only a platform temp directory.
4. Empty arm: "**unset**: Python's resolver skips an empty candidate, so the next candidate wins (S278) and the platform default applies". The skip is S278. S279 never says an empty candidate is skipped.
5. Unusable arm: "the tool refuses before it allocates: the value is named, the class is printed, nothing falls back to `/tmp`" / exit **2, could-not-evaluate**. The page's search does continue to `/tmp`, `/var/tmp`, and `/usr/tmp`, then the current working directory. Refusal with no `/tmp` fallback is a lane rule and is the opposite of that list.
6. "The empty arm is not a convenience."
7. The S278 clause of the next sentence: an empty `TMPDIR` "never becomes a candidate directory" because of `if dirname`. S279 does not say that. Only the following clause (list starts at the TMPDIR entry and the search continues) is S279.
8. "A tool that treated `\"\"` as a path would try to allocate under the working directory — a silent, wrong scratch root — which is why the arm is declared rather than left to whatever `os.path.isdir(\"\")` happens to return." The page lists the cwd as the search's last resort; it does not say that `""` is the cwd, that using it is wrong, or anything about `os.path.isdir`.
9. "The standard fixes only the variable's meaning, not its empty-string handling" plus the POSIX "shall represent a pathname…" quotation (S277).
10. "The empty arm is therefore a lane declaration that follows the resolver the lane actually calls, and the registry rows say so." This correctly refuses to treat the empty arm as a documentation rule. S279 still does not support it.
11. "A set-but-unusable `TMPDIR` is an environment fact, not a failed measurement: the gate did not run, so no verdict may be printed and the exit class is could-not-evaluate (2), never 1 (a verdict of \"differs\"/\"failed\") and never a traceback."
12. "Round 53 removed the silent `/tmp` fallback in seven tools and its own closure spot-check routed the residue: four of the seven still raised an uncaught `RuntimeError` from the self-test path (rc 1 with a traceback of the message), so the class existed in three tools and not in four (routed defect R53.6)."
13. "Round 54 gives each of the four a `ScratchRootUnusable(RuntimeError)` subclass raised by the helper and caught at the entry point, printing one line that names the value and the class."
14. The measurement paragraph (`c2/measure.py`, 7/7 exit 2, 7/7 exit 0 on the empty arm, 7/7 exit 0 on a usable root with no `mkdir` under `/tmp` under `strace`, 7/7 `scratch_root` cells, and the self-test blind spot).
15. "A tool that returns 0 after printing the could-not-evaluate line (control CTL_EXIT0), or that names the class without the value, fails the counter."
16. "A tool that regains a `dir=\"/tmp\"` literal fails the round-53 monitor and the C2 `tmp_mkdirs` arm together."

## Verdict

The re-opened page is the bytes the row hashed. The search-list quotation is the first entry of `tempfile.gettempdir`'s list. The row's teaches gloss attributes an empty-string fallthrough to those docs; the page has no such rule, so that gloss fails the "must not" check. The contract note does not make that attribution: it cites S278 for the skip and S279 only for the ordered list. Every other sentence in the contract is outside what S279 supports; the unusable arm's "nothing falls back to `/tmp`" is the one that conflicts with the list S279 actually documents.
