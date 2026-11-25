# Proposals

Changes to the shared registries proposed by entry branches, one file per entry, `<snapshot>-<topic>.json`. The format is in [`../CONTRIBUTING.md`](../CONTRIBUTING.md). `tools/check_claims.py` reads them as if folded in; `tools/fold_proposals.py` folds them into `data/` in the merge pass and deletes them.
