# round-82 C3 before-state: the single test-text mutant on the BASE tool bytes
# (the round-81 mutation-tester's named gap — this instrument carries no
# selftest-text pin). Expectation: SURVIVED at 11/11.
@defect db-a1-assertion-weakened | arm A1's summary conjunct is deleted, retaining the arm name and its fixture execution; the base suite must still report 11/11
@old             and "DEFECT_BIND: rows=1 closed=1 open=0 unexpected=0" in text,
@new             and True,
