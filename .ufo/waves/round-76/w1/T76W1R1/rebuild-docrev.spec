# T76W1R1 rebuild of the base doc-rev-ignored survivor: the exact single edit
# the committed mut-base-docrev.py carries vs base ss bytes (if a.doc_rev: -> if False:).
@defect doc-rev-ignored | the selfstate CLI ignores --doc-rev (r75 settlement errata; T76W1R1 rebuild on base)
@old         if a.doc_rev:
@new         if False:
