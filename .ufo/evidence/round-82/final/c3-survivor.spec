# round-82 wave survivor pins (T82W1M1 r2/r3): the two single edits that
# survived the declared 14/14 before the landing extended A8/A13.
@defect db-r2-manifest-rev-unresolved | bind_manifest drops its resolve_rev call (M1 r2 SURVIVED 14/14); A13_manifest_rev_binding must kill it
@old     resolved = resolve_rev(repo, rev)
@new     resolved = rev

@defect db-r3-manifest-rev-empty-guard-removed | main()'s empty --manifest-rev guard is deleted (M1 r3 SURVIVED 14/14); A8_refusals must kill it
@old         if args.manifest_rev is not None and not args.manifest_rev:\n            sys.stderr.write("defect-bind: --manifest-rev needs a revision\\n")\n            return 2\n
@new
