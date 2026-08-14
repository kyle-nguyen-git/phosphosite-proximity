# S1 Appendix. Annotation records, residue expansion, and a withdrawn count

Every `ACT_SITE` record covers a single residue. Expanding all 262 eligible records to one row per
covered residue gives 594 rows: 565 after removing duplicates on (accession, start, end) and 566 on
(accession, start, end, feature type). The target set itself is **560 distinct residues**, and that
count reproduces exactly. The excess over 560 arises from P12904, whose intervals are recorded once per
ligand, so the same residue appears under more than one record.

An earlier expanded row count kept in the analysis records does not reproduce under any simple rule and
is **withdrawn**. It is named here rather than deleted because it appeared in an earlier version of
this manuscript. No figure, table or claim in the present text depends on it; the numerical authority
bars citing it.
