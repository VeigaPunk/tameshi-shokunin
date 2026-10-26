# T50ScribePkgIeice receipts — F6 IEICE technical-report triage (2026-10-26)

## R1 fetch (Wayback capture of the lab PDF URL, as S197 cites)
$ curl -fsS -m 90 -o ieice.pdf https://web.archive.org/web/20260416233249/https://sdl.ist.osaka-u.ac.jp/pman/pman3.cgi?DOWNLOAD=749; sha256sum ieice.pdf; file ieice.pdf
344a5ae6cb83df12a9bf9841e5cd11c0ebefd1341eb878c5e2a8eba96e8f4b3c  ieice.pdf
ieice.pdf: PDF document, version 1.5 (zip deflate encoded)
676980 bytes

## R2 byte-identity with the campaign persisted copy (/home/vgpnk/Projects/shokuknow/lanes/tameshi/round7/evidence/)
$ sha256sum lanes/tameshi/round7/evidence/ieice-techrep-125-376.pdf; diff -q lanes/.../ieice-techrep-125-376.txt ieice.txt
344a5ae6cb83df12a9bf9841e5cd11c0ebefd1341eb878c5e2a8eba96e8f4b3c  /home/vgpnk/Projects/shokuknow/lanes/tameshi/round7/evidence/ieice-techrep-125-376.pdf
extracted text IDENTICAL

## R3 the entry recheck command, run verbatim
$ curl -fsSL '<wayback url>' | pdftotext -layout - - | grep -c '提案手法によるミュータント生成・統合は手動で行った'
1

## R4 page placement (pdftotext -f N -l N)
page 1: 表1=0 あらまし=1 without-peer-review=1
page 5: 表1=2 あらまし=0 without-peer-review=0
page 6: 表1=0 あらまし=0 without-peer-review=0

## R5 volume-line absence (the entry says the footers carry only page markers)
$ grep -cE '125|376|025|030' ieice.txt
0
page markers:
127:                                                                                             —2—
187:                                                                                —3—
251:                                                                                 —4—
309:                                                                               —5—
388:                                                                                                                  —6—
