# ReviewEntryOverclaim — Entry scope

## Finding

**Absent.** No sentence in `corpus/knowledge/r8-golden-update-flag.md` says the lane gates have zero unflagged writes.

The file contains the opposite — an explicit non-claim:

- `corpus/knowledge/r8-golden-update-flag.md:18`:
  > "The note describes a documented flag. It is not a run of TensorFlow Federated's test runner, and it does not say the lane's gates are free of unflagged writes."
- `corpus/knowledge/r8-golden-update-flag.md:14`:
  > "This entry does not claim that measurement; the counter receipt does."

## Verification

- Read: `corpus/knowledge/r8-golden-update-flag.md` (full file, 20 lines).
- Grep: `unflagged|zero|gate` on the same path — only the two lines above match; no affirmative zero-unflagged-writes sentence exists.

Live lane checkout was not edited.
