# Round-25 C1 item R1 — multi-token stdout fixture in the ruler.
# Target: tools/command-binding.py. Suite: c1-suite.py multitoken "$MUTANT".
# Each defect is one weakening a ruler with only single-token fixtures cannot see.
@defect M1 | any-of tokens instead of all-of (round-23 closure mutant)
@old if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):
@new if all(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):

@defect M2 | first token only
@old for token in required['expect'].get('stdout_contains', [])):
@new for token in required['expect'].get('stdout_contains', [])[:1]):

@defect M3 | last token only
@old for token in required['expect'].get('stdout_contains', [])):
@new for token in required['expect'].get('stdout_contains', [])[-1:]):

@defect M4 | first sorted requirement only
@old for name in sorted(set(receipts) & set(requirements)):
@new for name in sorted(set(receipts) & set(requirements))[:1]:

@defect M5 | over-strict: tokens must appear contiguous and in declared order
@old if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):
@new if ' '.join(required['expect'].get('stdout_contains', [])) not in receipt['stdout']:

@defect M6 | last-wins: findings reset for every requirement row
@old         receipt, required = receipts[name], requirements[name]
@new         findings = set(); receipt, required = receipts[name], requirements[name]
