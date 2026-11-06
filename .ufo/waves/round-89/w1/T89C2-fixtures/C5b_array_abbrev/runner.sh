PIN_A=b83a5e5209e46aafbec6bc1796b601b9d4e4c6d1b7a9d66311286c01b7bb016e
REV_A=6dbc9421c0265f9d7a8d50870144853762cda24b
TABLE_A='A1:KILLED,A2:SURVIVED'
PIN_B=256931e5627bfa46347df35ae1c25649073ce5630975d0cdf9d301d32836a118
REV_B=54b2ed70d118610448988809bf44a98aa0156558
TABLE_B='B1:SURVIVED'
regression_specs() {
  local d=$1
  cat >"$d/leg-a.spec" <<'EOT'
@defect A1 | a1
@old exit 0
@new exit 1

@defect A2 | a2
@old echo a
@new echo A
EOT
  cat >"$d/leg-b.spec" <<'EOT'
@defect B1 | b
@old echo b
@new echo B
EOT
}
run_regression() {
  regression_case_git leg-a \
    'repoa/a.sh' "$PIN_A" "$REV_A" \
    "$specs/leg-a.spec" 'bash "$MUTANT" --selftest' "$TABLE_A" \
    "$root/leg-a"
  regression_case_git leg-b \
    'repob/b.sh' "$PIN_B" "$REV_B" \
    "$specs/leg-b.spec" 'bash "$MUTANT" --selftest' "$TABLE_B" \
    "$root/leg-b"
}
