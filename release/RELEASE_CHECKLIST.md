# Release Checklist

Statuses are evidence-based. “Prepared” means the local artifact exists; “complete” requires the named
test or human signature.

| Gate | Status | Evidence required |
|---|---|---|
| Frozen scientific results | Complete locally | `NUMBERS.md` hashes and scientific verifier pass |
| Adversarial internal review | Complete locally | Four labeled reports and response log |
| Standalone release root | Complete locally | Built archive omits source workbooks and includes every invoked file |
| Fresh-environment reproduction | Complete locally | Passing `release/clean_room_report.json` names the exact archive and matching frozen hashes |
| Source-study redistribution | Resolved locally | Workbooks omitted; authoritative fetch and inner-file checksums pass |
| UniProt/AlphaFold rights and notices | Complete locally | `THIRD_PARTY_NOTICES.md` plus file-level manifest |
| Dependency and interpreter record | Complete locally | `requirements-lock.txt` plus clean-room environment report |
| Supplement regeneration and visual QA | Complete locally | Generated workbook, error scan, all-sheet visual pass |
| PDF regeneration and visual QA | Complete locally | Hash-bound page renders and all-page visual pass |
| Author identity and declarations | **Blocked on Kyle** | Signed `AUTHOR_SIGNOFF.md` |
| Independent human methods review | **Blocked on reviewer** | Completed `EXTERNAL_METHODS_REVIEW.md` and response log |
| Public repository | Not created | Exact reviewed release candidate pushed after sign-offs |
| Immutable archive and DOI | Not created | Matching archive deposited after sign-offs |
| Public preprint | Not submitted | Same manuscript/archive version submitted after all gates |

## Public-account sequence

1. Complete author and external-review signatures.
2. Rebuild and re-verify the exact release candidate.
3. Create the public repository and push only that candidate.
4. Reserve and then publish the immutable archive DOI for the same commit/archive hash.
5. Replace provisional repository/DOI text in the manuscript and citation metadata.
6. Rebuild once more, verify hash agreement, and submit the same version to the preprint server.
