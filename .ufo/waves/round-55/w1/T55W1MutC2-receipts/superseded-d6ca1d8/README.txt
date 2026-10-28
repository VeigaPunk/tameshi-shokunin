These are the FIRST-PASS receipts of this seat, kept for the record and NOT scored.

While this item ran, the lane re-froze the C2 counter twice (e2979f2 amendments 1-7;
133b2ce amendment 8, which added the ninth allocating mode registry-check --rev and
changed three denominators). The first pass measured the pre-amendment bytes
sha256 d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a with a
hand-built fixed tree; both were abandoned mid-item.

Because an integrator's `git add -A` swept this seat's in-progress directory into
commit 133b2ce, those first-pass files now live as tracked siblings one level up
and are left untouched there:
  ../P-base.meta, ../P-base.stdout            (base, pre-amendment bytes: total=18)
  ../counter-bytes.txt                        (pre-amendment hashes)
  ../fixed-tree-line-*.txt                    (hand-built fixed tree, one line each)
  ../mutants/mN.diff                          (pre-amendment single-edit diffs)

The scored set is ../mutants-133b2ce/, ../verdicts/, ../verdict-lines.txt and
../counter-under-test.sha256 (0458f632... at rev 133b2ce).
