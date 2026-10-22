# ReReplay09 — Re-Attack R23 wave-2: witness-metadata-selftest (Rollen-Reviewer)

**Rolle:** Reviewer (Replay09, ursprünglich R23-Welle 2; Sitz damals gestorben, nie berichtet).
**Umfang:** Nur die Zeile `witness-metadata-selftest` aus `tools/registry.json`. Falsifikation der exakten Bindung von Frozen-argv/expect an (a) die Baseline-Quelle, (b) die neu einbehaltenen Aufruf-Metadaten und (c) die vollständigen Ausgabestreams der Replay-Artefakte der Runde 23.
**Auftrag:** Feldgenaue falsche Akzeptanz finden oder statisch exakte Bindung bestätigen; genau ein adversarielles Delta benennen. Kein Registry-Kommando ausgeführt, keine Suite gelaufen, keine Repo-Writes außer diesem Bericht. Alle Prüfungen mit `GIT_OPTIONAL_LOCKS=0` bzw. in `/tmp/re09` (eigener Sandbox-Klon der Werkzeuge, kein Schreibzugriff auf die Lane).

## 1. Geprüfte Artefakte (alle vorhanden, alle gelesen)

| Artefakt | Befund |
|---|---|
| `.ufo/evidence/round-23/requirements.json` | 43 Requirements, `source_revision` 28cae17…, `registry_sha256` ebd2e69… |
| `.ufo/evidence/round-23/replay/bundle.json` | Schema command-binding-v1, Revision 496d212…, 43/43 Receipts, cwd = Temp-Klon |
| `.ufo/evidence/round-23/replay/observations.json` | argv, cwd, Revision, Messintervalle, vollständige Streams pro Zeile, `runner_sha256` cba166… |
| `.ufo/evidence/round-23/replay.py` | Produktionsinstrument, 87 Zeilen, im Repo committed (8f66b5d) |
| `.ufo/evidence/round-23/registry-baseline.json` | Eingefrorenes Registry-Snapshot |
| `.ufo/evidence/round-23/replay/expected.json` | Caller-Commitment: `bundle_sha256` = 3d6c99b7… (sha256sum bundle.json bestätigt identisch) |
| `tools/command-binding.py` | Prüfer der Bindung (Zeile 1–220 gelesen) |
| `tools/registry-check.py` | Runner (`run_row`, `_argv_outside_fleet`, Zeile 632–716 gelesen) |

## 2. Beweisstand: tatsächlich vorhanden, nicht erschlossen

Direkt verifiziert (Kommandos mit beobachteten Ausgaben):

1. **Frozen-Registry-Digest:** `sha256sum registry-baseline.json` = `ebd2e69a…` = `requirements.json.registry_sha256` → `True`.
2. **Requirements = aktive Zeilen des Baseline-Registries:** Projection `[{'name','argv','expect'}]` der 43 aktiven Zeilen == `frozen['requirements']` → `True` (43).
3. **Bundle-Digest-Pin:** `expected.json.bundle_sha256` = `3d6c99b70b3e30b9…` == sha256sum(bundle.json) = `3d6c99b70b3e30b9…`. Identisch.
4. **Runner-Identität:** `observations.json.runner_sha256` = `cba16646…` == sha256sum(tools/registry-check.py) = `cba16646…`. Der im Replay verwendete Runner ist byte-identisch mit dem aktuellen.
5. **Vollständige Streams:** `bundle.json`-Receipt der Zeile == `observations.json`-Zeile (argv, exit 0, stdout, stderr ''-Zeichen-gleich). `stdout_tail` ≠ `stdout` → die Tail-Ebene des Läufers ist tatsächlich kürzer als der Volltext; die Replay-Artefakte enthalten den Volltext, nicht nur Tails. 39 `SELFTEST_CASE`-Zeilen, alle enden auf `OK`, letzte Zeile `SELFTEST: PASS 39/39`, stderr leer.
6. **Werkzeug-Quelle zur Baseline:** `tools/witness-metadata.py` unverändert seit round-13 (4acc607); kein Diff zwischen 496d212 und Arbeitskopie. Die im Replay ausgeführte Selbsttest-Logik (`SELFTEST_CASES`, Zeile 659; Ergebnisdruck 1207–1211) ist die aktuelle.
7. **Registry-Zeile:** 496d212 == c9ff09f == Arbeitskopie, byte-identische Zeile `witness-metadata-selftest` (argv `python3 tools/witness-metadata.py --selftest`, expect exit 0, `stdout_contains ["SELFTEST: PASS"]`, timeout 60, source `SKILL.md@98bea7d:1553`).

## 3. Die eigentliche Bindungsprüfung (statisch + dynamisch)

Ich habe die von der Zeile deklarierte Bindung im Sandbox-Klon gegen die Frozen-Artefakte ausgeführt:

```
cd /tmp/re09 && python3 command-binding.py --bundle cb-bundle.json --expected cb-expected.json --json
→ {"exit": 0, "finding_ids": [], "bundle_sha256": "3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9"}
```

Ergebnis: **exit 0, keine Findings.** Die exakte Bindung hält auf der Ebene, auf der sie deklariert ist:

- Name/argv (kein Shell-Normalisieren, exakte Token-Sequenz), kanonischer absoluter cwd, volle 40-stellige Revision, Integer-Exit, Pflicht-Tokens im stdout.
- Alle 43 Receipts decken alle 43 Requirements ab, gleiche Revision/cwd überall.
- Digest-Pin verhindert jede Byte-Veränderung des Bundles (SNAPSHOT_TAMPERED → exit 2, im Selbsttest des Prüfers selbst verankert).

## 4. Adversarielles Delta (das eine benannte Schwachstelle)

Die Bindung ist auf Bundle-Ebene exakt, **aber die Bindungstiefe der `stdout_contains`-Bedingungen ist substring-basiert**. Drei konkret ausgeführte Gegenproben gegen den Prüfer (jeweils mit konsistent neu berechnetem `expected.json`, also ein Angreifer, der den Caller-Pin kontrolliert):

| Probe | Manipulation | Ergebnis |
|---|---|---|
| 1 | `'SELFTEST: PASS 39/39'` → `'XSELFTEST: PASS 39/39 (FAKE)'` (Präfix-Fälschung) | **exit 0** — fälschlich akzeptiert |
| 2 | Alle stdout-Zeilen mit Whitespace gepolstert | **exit 0** — fälschlich akzeptiert |
| 3 | Letzte `SELFTEST_CASE`-Zeile entfernt (39→38 Fälle) | **exit 1, STDOUT_MISMATCH** — korrekt abgefangen, weil dabei der Sammel-Token `SELFTEST: PASS` mitentfiel |
| 4 | Eine Fallzeile `OK → FAIL` bei gleichem Exit | **exit 0** — fälschlich akzeptiert, solange `SELFTEST: PASS`-Token irgendwo steht |

Probe 4 zeigt das schärfste Feld: eine Fallzeile mit `observed=… FAIL` bleibt unsichtbar, weil nur der Sammel-Token `SELFTEST: PASS` gebunden ist. **Interne Konsistenz rettet die Zeile trotzdem:** im Werkzeug (witness-metadata.py:1207–1211) wird `SELFTEST: PASS n/n` nur bei `failures == 0` gedruckt und Exit 0 nur dann zurückgegeben; ein gedrucktes `FAIL` erzwingt `SELFTEST: FAIL` und Exit 1. Ein konsistenter gefälschter Stream müsste also auch den Exit fälschen — und der Exit ist Teil der exakten Bindung. Das verbleibende echte Delta ist daher nicht die Fallzeile, sondern die Token-Toleranz (Proben 1–2): Der Prüfer akzeptiert Präfix-/Whitespace-manipulierten stdout, **solange** die Bytes des Bundles unverändert sind; eine Fälschung setzt voraus, dass der Angreifer das `expected.json` (Caller-Commitment) mitschreiben kann. Das ist genau die Grenze, die das Werkzeug selbst im Docstring benennt: „The expected file is the trusted caller-owned commitment."

**Einstufung:** Kein Feld-Level-false-Acceptance in der deklarierten Bindung selbst; das Delta ist die Substring-Toleranz von `stdout_contains` als known limitation, abgedeckt durch (a) Digest-Pin des Bundles und (b) trusted-caller-Annahme des expected-Files. Für die Falsifikationsfrage „hält die exakte Bindung der Zeile?" lautet die Antwort: **ja, auf der deklarierten Ebene, mit benannter Restschwäche.**

## 5. Gilt der Befund weiterhin bei c9ff09fb…?

- `tools/witness-metadata.py`: unverändert seit round-13 (4acc607), kein Diff bis HEAD.
- `tools/registry.json`: Zeile unverändert (496d212 == c9ff09f == Arbeitskopie).
- `tools/command-binding.py`: seit 496d212 nur eine Änderung (d2eaecd): Selbsttest lädt jetzt zusätzlich `.ufo/evidence/round-24/extra-cases.json`. `evaluate()`/`check()` — die für die Zeile relevante Bindungslogik — ist unverändert; das adversarielle Delta (Substring-Toleranz) gilt unverändert.
- `tools/registry-check.py`: byte-identisch (sha256 gleich, s. o.). Der Runner, der `run_row` mit `retain_streams` nutzt, ist der gleiche.
- Die Zeile ist **nicht** ersetzt: Status weiterhin `active`, keine `superseded_by`-Verkettung auf die Zeile.

**Fazit:** Der R23-Befund trägt unverändert fort; die Replay-Artefakte sind authentisch und vollständig, die exakte Bindung hält, das benannte adversarielle Delta (Token-Substring-Toleranz + trusted-caller) bleibt die einzige Schwachstelle und ist im Werkzeug selbst dokumentiert.

## 6. Produzenten-Authentifizierung / historische Metadaten

Ich erhebe **keinen** Anspruch auf Produzenten-Authentifizierung: Die Artefakte belegen Konsistenz (Digest-Pins, byte-identische Quellen, vollständige Streams), nicht wer sie erzeugt hat. Keine rückwirkende Auffüllung historischer Metadaten (die `observations.json` trägt neue Ausführungs-Metadaten nur für die Replay-Ausführung selbst; die historischen R12/R13-Beobachtungen bleiben unangetastet — das entspricht dem Docstring des Instruments: „it never fills those fields into historical observations").

---
R23-REATTACK Replay09: AGREE
