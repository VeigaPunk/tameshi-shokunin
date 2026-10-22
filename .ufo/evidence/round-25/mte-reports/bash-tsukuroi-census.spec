@defect B1 | tsukuroi-census.sh:473
@old     if [ "$smi" != ok ]; then
@new     if [ "$smi" == ok ]; then

@defect B2 | tsukuroi-census.sh:281
@old   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
@new   if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 2 ]; then

@defect B3 | tsukuroi-census.sh:434-452
@old   # kerr == 0 is only a pass if the ring really has data; an empty ring cannot be told\n  # apart from a clean one, and must never be quoted as a fake HEALTHY.\n  if [ "$kerr" -eq 0 ]; then\n    if [ "$ring" = 'journalctl-k' ]; then\n      cap "$JOURNALCTL" -k -b -o json --no-pager\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (journalctl -k -b lists no kernel entries)'\n        return\n      fi\n    else\n      cap "$DMESG"\n      if [ "$CAP_RC" -ne 0 ] || [ "$(nlines "$CAP_OUT")" -eq 0 ]; then\n        DRV_V=BLOCKED\n        DRV_NOTE='kernel ring empty/unreadable (dmesg lists no records)'\n        return\n      fi\n    fi\n  fi\n
@new 

@defect B4 | tsukuroi-census.sh:578
@old       /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
@new       /"_TRANSPORT":"kernel"/ { k++; next }

@defect B5 | tsukuroi-census.sh:615
@old       drift=$((drift + 1))
@new       drift=$((drift + 2))

@defect B6 | tsukuroi-census.sh:210
@old   if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
@new   if [ "$(rank "$2")" -lt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi

@defect B7 | tsukuroi-census.sh:160
@old SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}
@new SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}

@defect B8 | tsukuroi-census.sh:935
@old       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 2 ;;
@new       *) printf 'tsukuroi-census: unknown argument: %s\\n' "$1" >&2; usage >&2; exit 1 ;;

@defect B9 | tsukuroi-census.sh:967
@old     "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V"
@new     "$roll" "$SYS_V" "$PKG_V" "$DRV_V" "$JRN_V"

@defect B10 | tsukuroi-census.sh:487-493
@old   else\n    if [ "$smi" = ok ] && [ "$mods" -gt 0 ]; then\n      nv='present(pci inventory unreadable)'\n    else\n      DRV_V=BLOCKED\n      modnote='PCI inventory unreadable and no positive nvidia evidence — cannot assess read-only'\n    fi\n
@new   else\n    nv='absent(pci_10de=0)'\n
