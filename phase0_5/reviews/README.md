# Internal Adversarial Review Set

These reports are AI-assisted internal review aids. They are not independent peer review, a senior-author
endorsement, biological validation, or the independent human methods review required by
`release/EXTERNAL_METHODS_REVIEW.md`.

`NUMBERS.md` is the sole numerical authority. Each reviewer was instructed to verify its frozen hashes
before using a project result. Dispositions and implemented changes are tracked in `RESPONSE_LOG.md`.
After these reports were written, the clean-environment audit exposed BLAS-dependent last-bit drift in
continuous-model serialization. `NUMBERS.md` now carries the refrozen deterministic hash; hashes quoted
inside the dated reviews describe their audit snapshot and are not the current authority.

- `statistical_methods_review.md` — estimand, clustered inference, sensitivities, and claim boundaries.
- `biological_structural_review.md` — biological construct, annotation evidence, structural geometry,
  AlphaFold provenance, and endpoint interpretation.
- `manuscript_claims_review.md` — line-by-line claims, declarations, artifacts, and release gates.
- `reproducibility_release_review.md` — standalone package, source rights, dependency lock, and
  reproduction audit.

Human author review and external review remain separate recorded gates even when every internal item is
resolved technically.
