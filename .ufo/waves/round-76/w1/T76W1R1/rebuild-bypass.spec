# T76W1R1 rebuild of the base bypass survivor from plans/round-76.plan.md R76-C1
# (same old/new as the r76 spec seventh block) applied to pristine base bytes.
@defect adv-seatreports-require-printed-bypass | require_printed is dropped in the seat_reports branch only (r75 carry T75W1R1; T76W1R1 rebuild on base)
@old     if kind == 'seat_reports':\n        printed = _record_claim(row, readers, require_printed=True)
@new     if kind == 'seat_reports':\n        printed = _record_claim(row, readers)
