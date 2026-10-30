# Proposed header patch for `.ufo/evidence/round-58/controls.sh`

Apply to the round-58 staged instrument before commit; do not apply in place from this seat.

Replace the current generation explanation with an explicit pre-registration immediately after the usage comment:

```diff
-# ONE GENERATION. Controls are RECOMPUTED, never READ (round-56 lesson, Attempt 4, first
+# PRE-REGISTERED GENERATION ORDER (round-56 lesson, Attempt 4, first Mistakes row; R56.5):
+#   generation 1 is bootstrap only; generation 2 is the scored generation. Both are
+#   recomputed from BASE/REV inputs; neither generation reads a receipt produced by this
+#   round. A generation is never inferred from previously committed round receipts.
+# Controls are RECOMPUTED, never READ (round-56 lesson, Attempt 4, first
 # Mistakes row; R56.5): round 56's C2 arm 5 read the round's committed controls-a/b.stdout, so
```

Add the own-receipts discriminator after the paragraph that disallows reading same-round receipts:

```diff
+# OWN-RECEIPTS DISCRIMINATOR: any arm that evaluates receipts produced by this run must
+# establish producer provenance (the receipt's producer identity and generation) before
+# treating it as a control result; a receipt merely present in the clone is not evidence
+# that this invocation produced it. The do-nothing arm is not satisfied by ambient receipts.
```

The current staged header already says recomputed/never read, but it calls the process ONE GENERATION and has no producer-provenance discriminator. Replace that contradiction rather than appending a second incompatible generation description. The deciding-run header may retain its independent fresh-clone / receipt-gate design; the discriminator governs any own-receipts arm in controls.
