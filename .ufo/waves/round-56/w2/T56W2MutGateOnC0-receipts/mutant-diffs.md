# Mutant diffs at C0 (one exact edit each)

### M1  drop-RECEIPT_REV_ABSENT

verdict KILLED  tally 18/19  failing ['absent-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M1)
@@ -122,7 +122,7 @@
     if regex is not None and not re.search(regex, text, re.M):
         codes.append('RECEIPT_REQUIRED_LINE_MISSING')
         detail = 'regex=%r' % regex
-    if not revs:
+    if False and not revs:
         codes.append('RECEIPT_REV_ABSENT')
         detail = detail or 'no rev= token'
         return codes, detail, None
```

### M2  drifted_paths-returns-empty

verdict KILLED  tally 18/19  failing ['content-drift-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M2)
@@ -81,7 +81,7 @@
            and git(['-C', lane, 'cat-file', '-e', '%s:%s' % (rev_b, p)]).returncode != 0:
             gone.append('<unresolvable-path:%s>' % p)
     r = git(['-C', lane, 'diff', '--name-only', rev_a, rev_b, '--'] + list(paths))
-    return [p for p in r.stdout.decode().splitlines() if p] + gone
+    return []
 
 
 def parse_receipts(args):
```

### M3  is_ancestor-always-true

verdict KILLED  tally 18/19  failing ['control-not-ancestor-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M3)
@@ -67,7 +67,7 @@
 
 
 def is_ancestor(lane, older, newer):
-    return git(['-C', lane, 'merge-base', '--is-ancestor', older, newer]).returncode == 0
+    return True
 
 
 def drifted_paths(lane, rev_a, rev_b, paths):
```

### M4  skip-digest-check

verdict KILLED  tally 18/19  failing ['digest-mismatch-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M4)
@@ -116,7 +116,7 @@
         want = sidecar.read_text('utf-8', 'surrogateescape').split()[0] if sidecar.read_text(
             'utf-8', 'surrogateescape').split() else ''
         got = hashlib.sha256(data).hexdigest()
-        if want != got:
+        if False and want != got:
             codes.append('RECEIPT_DIGEST_MISMATCH')
             detail = 'sidecar=%s got=%s' % (want[:12], got[:12])
     if regex is not None and not re.search(regex, text, re.M):
```

### M5  allow-multiple-revs-in-positive-role

verdict KILLED  tally 18/19  failing ['ambiguous-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M5)
@@ -137,7 +137,7 @@
     if codes:
         return codes, detail, revs
     if role_name in ('positive', 'verdict'):
-        if len(revs) > 1:
+        if False and len(revs) > 1:
             codes.append('RECEIPT_REV_AMBIGUOUS')
             return codes, 'revs=%s' % ','.join(revs), revs
         full = resolved[revs[0]]
```

### M6  skip-required-line-check

verdict KILLED  tally 18/19  failing ['required-line-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M6)
@@ -119,7 +119,7 @@
         if want != got:
             codes.append('RECEIPT_DIGEST_MISMATCH')
             detail = 'sidecar=%s got=%s' % (want[:12], got[:12])
-    if regex is not None and not re.search(regex, text, re.M):
+    if False and regex is not None and not re.search(regex, text, re.M):
         codes.append('RECEIPT_REQUIRED_LINE_MISSING')
         detail = 'regex=%r' % regex
     if not revs:
```

### M7  empty-file-treated-as-present

verdict KILLED  tally 18/19  failing ['empty-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M7)
@@ -104,7 +104,7 @@
     if not p.is_file():
         return ['RECEIPT_NOT_BLOB'], 'path=%s' % path, None
     data = p.read_bytes()
-    if not data.strip():
+    if False and not data.strip():
         return ['RECEIPT_EMPTY'], 'path=%s' % path, None
     # a receipt that git knows must be a blob at the certified revision's tree? No:
     # the receipt is checked where it lives (working tree or committed), so only
```

### M8  drop-RECEIPT_CONTROL_NOT_ANCESTOR

verdict KILLED  tally 18/19  failing ['control-not-ancestor-refused']

```diff
--- a/tools/receipt-revision-gate.py
+++ b/tools/receipt-revision-gate.py (mutant M8)
@@ -155,7 +155,7 @@
         return codes, detail, revs
     for r, full in resolved.items():
         if not is_ancestor(lane, full, certified):
-            codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')
+            pass  # mutant: drop RECEIPT_CONTROL_NOT_ANCESTOR
             detail = 'rev=%s' % r
     return codes, detail, revs
 
```
