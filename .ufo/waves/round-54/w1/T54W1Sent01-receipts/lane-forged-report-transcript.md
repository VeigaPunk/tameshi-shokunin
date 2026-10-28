# T54W1Sent01 — lane-side forged reader report: bytes, hash, removal

Executed once, at 2026-10-28 (seat T54W1Sent01), against the lane's own wave
directory. The file existed for one command and was removed in the same command;
the bytes are kept here so the receipt survives the deletion.

## Command (as run, single shell)

```bash
set -u; W=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1; F=$W/T54W1ReadForged.json
printf '%s\n' '{"heading": "## Standing rules", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "section_sha256": "9942353c95371f27904c3a8ea2df7aedffd15ff8f03d9b05c07933fb9ee7b339", "findings": []}' > "$F"
echo "== bytes written:"; wc -c < "$F"; sha256sum "$F"; xxd "$F" | head -8
echo "== no companion MD by construction:"; ls "$W"/T54W1ReadForged.md 2>&1 || true
rm -f -- "$F"
echo "== after delete:"; test ! -e "$F" && echo "ABSENT $F"
ls "$W" | grep -i forged || echo "no forged artefacts remain in the lane wave dir"
```

## Output (verbatim)

```
== bytes written:
187
358f05c755804a5b0c864bd1000df62037b0a5399718937e63824a9c36d1d2b9  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ReadForged.json
00000000: 7b22 6865 6164 696e 6722 3a20 2223 2320  {"heading": "## 
00000010: 5374 616e 6469 6e67 2072 756c 6573 222c  Standing rules",
00000020: 2022 6361 6e64 223a 2022 3539 6333 3831   "cand": "59c381
00000030: 3039 6266 3131 3964 3065 3964 3466 3837  09bf119d0e9d4f87
00000040: 3836 3434 6138 3262 6162 6339 3337 6263  8644a82babc937bc
00000050: 3165 222c 2022 7365 6374 696f 6e5f 7368  1e", "section_sh
00000060: 6132 3536 223a 2022 3939 3432 3335 3363  a256": "9942353c
00000070: 3935 3337 3166 3237 3930 3463 3361 3865  95371f27904c3a8e
== no companion MD by construction:
ls: cannot access '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ReadForged.md': No such file or directory
== after delete:
ABSENT /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w1/T54W1ReadForged.json
no forged artefacts remain in the lane wave dir
```

The 187 bytes are stored beside this file as
`lane-forged-report-T54W1ReadForged.json` (sha256
`358f05c755804a5b0c864bd1000df62037b0a5399718937e63824a9c36d1d2b9`).

`section_sha256` above is `sha256("T54W1Sent01 forged guess, never read the
section")` — a guess, obtained by running no reader tool.
