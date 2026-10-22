# T8-2 mutation spec — kumitate scripts/claims-check.mjs @ e9a21b44… (git blob fae4bbc… @ 175de6b)
# Sites < 470 (chain) sit under the first @defect's group headers; each @old asserted count==1 by t8_2_check.py.

@defect D1 | verdict token: MATCH -> OK on the CLAIMS verdict line (row A)
@old `CLAIMS: MATCH (rows=${totals.rows}
@new `CLAIMS: OK (rows=${totals.rows}

@defect D2 | exit map: DRIFT path returns 0
@old return verdict === 'MATCH' ? 0 : 1;
@new return 0;

@defect D3 | predicate: warnings are always drift (the --strict promotion dropped)
@old drift: errors > 0 || (Boolean(strict) && warnings > 0)
@new drift: errors > 0 || warnings > 0

@defect D4 | boundary: NOTE_AMBIGUOUS threshold 2 hits -> 3
@old else if (hits.length > 1 &&
@new else if (hits.length > 2 &&

@defect D5 | inverted condition: a live anchor now requires blank endpoints
@old && lines[a - 1].trim() !== '' && lines[b - 1].trim() !== '');
@new && lines[a - 1].trim() === '' && lines[b - 1].trim() === '');

@defect D6 | reported field: JSON schema id swapped
@old schema: CONTRACT, contract: CONTRACT,
@new schema: 'claims-check-v0', contract: CONTRACT,

@defect D7 | cap unreached: DRIFT finding cap 6 -> 5
@old shown.slice(0, 6)
@new shown.slice(0, 5)

@defect D8 | threshold unasserted: symbol floor 3 -> 2 chars
@old && t.length >= 3);
@new && t.length >= 2);

@defect D9 | unreached arm: a covered cell with only prose parts no longer errors
@old && claimed.length + explicit.length + unresolved.length === 0) {
@new && claimed.length + explicit.length === 0) {

@defect D10 | candidate order swapped (case name claims it, assert cannot see it)
@old join(homedir(), 'Projects', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),
@new join(homedir(), 'Projects', 'origin-work', 'ufo-fsd-alpha'),\n  join(homedir(), 'Projects', 'ufo-fsd-alpha'),
