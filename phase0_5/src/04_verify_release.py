"""Fail-closed verification for the exclusion-primary two-arm release."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pypdf import PdfReader


HERE = Path(__file__).resolve().parents[1]
PARENT = HERE.parent
RESULTS = HERE / "results"
MANUSCRIPT = PARENT / "manuscript"
NUMBERS = PARENT / "NUMBERS.md"
PRIMARY = "exclude_annotation_coincident"
INCLUSIVE = "include_annotation_coincident"
LEGACY = "legacy_158"
sys.path.insert(0, str(PARENT / "tools"))
from release_policy import release_source_files  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return bool(np.isclose(float(left), float(right), atol=tolerance, rtol=0))


def true_count(series: pd.Series) -> int:
    if pd.api.types.is_bool_dtype(series):
        return int(series.sum())
    return int(series.astype(str).str.lower().eq("true").sum())


def site_keys(data: pd.DataFrame) -> set[tuple[str, int]]:
    return set(zip(data.acc.astype(str), data.pos.astype(int)))


def parse_frozen_hashes(text: str) -> dict[str, str]:
    return dict(
        re.findall(r"^- `([^`]+)` — `([0-9a-f]{64})`$", text, re.MULTILINE)
    )


def clean_cell(value: str) -> str:
    return value.replace("**", "").strip()


def parse_arm_numbers(text: str, row_prefix: str) -> dict[str, float | int]:
    row = next(
        line for line in text.splitlines()
        if line.startswith(f"| {row_prefix}")
    )
    cells = [clean_cell(cell) for cell in row.strip().strip("|").split("|")]
    interval = re.search(
        r"([0-9.]+)–([0-9.]+) → ([0-9.]+) \[([0-9.]+), ([0-9.]+)\]",
        cells[5],
    )
    if interval is None:
        raise ValueError(f"could not parse canonical interval from: {row}")
    return {
        "n_sites": int(cells[1]),
        "n_proteins": int(cells[2]),
        "n_positive": int(cells[3]),
        "auc": float(cells[4]),
        "ci_low": float(interval.group(1)),
        "ci_high": float(interval.group(2)),
        "rounded_auc": float(interval.group(3)),
        "rounded_ci_low": float(interval.group(4)),
        "rounded_ci_high": float(interval.group(5)),
    }


def table_arm_matches(
    table: pd.DataFrame,
    cohort: str,
    expected: dict[str, float | int],
    estimate_column: str,
) -> bool:
    rows = table.loc[table.cohort == cohort]
    if len(rows) != 1:
        return False
    row = rows.iloc[0]
    return (
        int(row.n_sites) == expected["n_sites"]
        and int(row.n_proteins) == expected["n_proteins"]
        and int(row.n_positive) == expected["n_positive"]
        and close(row[estimate_column], expected["auc"], 5e-7)
        and close(row.ci_low, expected["ci_low"], 5e-7)
        and close(row.ci_high, expected["ci_high"], 5e-7)
    )


def main() -> None:
    numbers_text = NUMBERS.read_text()
    frozen_hashes = parse_frozen_hashes(numbers_text)
    required_frozen = {
        "results/statistics.json",
        "results/analysis_final.csv",
        "phase0_5/results/phase0_5_statistics.json",
    }
    freeze_checks = {
        relative: (
            relative in frozen_hashes
            and (PARENT / relative).is_file()
            and sha256(PARENT / relative) == frozen_hashes[relative]
        )
        for relative in required_frozen
    }
    if not all(freeze_checks.values()):
        report = {
            "status": "FAIL",
            "reason": "NUMBERS.md freeze hash mismatch; numerical outputs were not used",
            "freeze_hash_checks": freeze_checks,
        }
        (RESULTS / "verification_report.json").write_text(
            json.dumps(report, indent=2) + "\n"
        )
        failed = [name for name, passed in freeze_checks.items() if not passed]
        raise SystemExit(f"freeze verification failed: {', '.join(failed)}")

    canonical = {
        PRIMARY: parse_arm_numbers(numbers_text, "**Primary:"),
        INCLUSIVE: parse_arm_numbers(numbers_text, "**Sensitivity:"),
    }
    draw_match = re.search(
        r"Both protein-cluster intervals use \*\*([0-9,]+) draws\*\* and seed \*\*([0-9]+)\*\*",
        numbers_text,
    )
    if draw_match is None:
        raise SystemExit("could not parse canonical bootstrap contract from NUMBERS.md")
    canonical_draws = int(draw_match.group(1).replace(",", ""))
    canonical_seed = int(draw_match.group(2))

    phase0 = json.loads((PARENT / "results" / "statistics.json").read_text())
    phase05 = json.loads((RESULTS / "phase0_5_statistics.json").read_text())
    parent_data = {
        PRIMARY: pd.read_csv(PARENT / "results" / "analysis_final.csv"),
        INCLUSIVE: pd.read_csv(PARENT / "results" / "analysis_inclusive_sensitivity.csv"),
    }
    child_data = {
        PRIMARY: pd.read_csv(RESULTS / "phase0_5_primary_analysis.csv"),
        INCLUSIVE: pd.read_csv(RESULTS / "phase0_5_inclusive_sensitivity_analysis.csv"),
    }
    disposition = pd.read_csv(PARENT / "results" / "cohort_disposition.csv")
    pae_manifest = pd.read_csv(RESULTS / "alphafold_pae_manifest.csv")
    parent_arm_estimates = pd.read_csv(PARENT / "results" / "cohort_arm_primary_estimates.csv")
    child_arm_estimates = pd.read_csv(RESULTS / "cohort_arm_primary_estimates.csv")
    parent_cutoffs = pd.read_csv(PARENT / "results" / "cohort_arm_cutoffs.csv")
    child_cutoffs = pd.read_csv(RESULTS / "cohort_arm_cutoffs.csv")
    parent_logistic = pd.read_csv(PARENT / "results" / "cohort_arm_logistic.csv")
    child_logistic = pd.read_csv(RESULTS / "regression_models.csv")
    parent_descriptives = pd.read_csv(PARENT / "results" / "cohort_arm_descriptives.csv")
    child_descriptives = pd.read_csv(RESULTS / "cohort_arm_descriptives.csv")
    confidence = pd.read_csv(RESULTS / "confidence_strata.csv")
    cohort_sensitivity = pd.read_csv(RESULTS / "cohort_sensitivity.csv")
    pae_at10 = pd.read_csv(RESULTS / "pae_column_sensitivity_at_10A.csv")
    pae_grid = pd.read_csv(RESULTS / "pae_filter_grid_72x3.csv")
    sift_sensitivity = pd.read_csv(RESULTS / "sift_comparator_sensitivity.csv")
    feature_definitions = pd.read_csv(RESULTS / "feature_definition_sensitivity.csv")

    expected_strata = {
        "all",
        "site_plddt_ge_50",
        "site_plddt_ge_70",
        "site_and_target_plddt_ge_70",
        "site_plddt_ge_90",
        "site_and_target_plddt_ge_90",
        "pair_pae_max_le_5",
        "pair_pae_max_le_10",
        "pair_pae_max_le_15",
        "high_confidence_joint",
        "very_high_confidence_joint",
    }
    expected_pae_columns = {
        "pae_pair_max",
        "pae_site_to_target",
        "pae_pair_mean",
        "pae_target_to_site",
    }
    expected_grid_cohorts = {PRIMARY, INCLUSIVE, LEGACY}

    checks: dict[str, bool] = {
        "numbers_freeze_hashes_verified_before_use": all(freeze_checks.values()),
        "named_cohort_contract_in_parent_json": (
            phase0["primary_cohort"] == PRIMARY
            and phase0["inclusive_sensitivity_cohort"] == INCLUSIVE
        ),
        "named_cohort_contract_in_phase0_5_json": (
            phase05["primary_cohort"] == PRIMARY
            and phase05["inclusive_sensitivity_cohort"] == INCLUSIVE
        ),
        "named_switch_present_in_parent_analysis": all(
            token in (PARENT / "src" / "03_analysis.py").read_text()
            for token in (
                'PRIMARY_COHORT = "exclude_annotation_coincident"',
                'INCLUSIVE_COHORT = "include_annotation_coincident"',
            )
        ),
        "named_switch_consumed_by_phase0_5": all(
            token in (HERE / "src" / "02_phase0_5_analysis.py").read_text()
            for token in (PRIMARY, INCLUSIVE)
        ),
    }

    for cohort, expected in canonical.items():
        parent = parent_data[cohort]
        child = child_data[cohort]
        parent_stats = phase0["cohorts"][cohort]
        child_cluster = (
            phase05["primary_auc"]["protein_cluster_bootstrap"]
            if cohort == PRIMARY
            else phase05["inclusive_sensitivity_auc"]["protein_cluster_bootstrap"]
        )
        checks.update({
            f"{cohort}_parent_counts_match_numbers": (
                len(parent) == expected["n_sites"]
                and parent.acc.nunique() == expected["n_proteins"]
                and true_count(parent.has_pheno) == expected["n_positive"]
            ),
            f"{cohort}_phase0_5_counts_match_numbers": (
                len(child) == expected["n_sites"]
                and child.acc.nunique() == expected["n_proteins"]
                and true_count(child.has_pheno) == expected["n_positive"]
            ),
            f"{cohort}_parent_and_phase0_5_sites_identical": (
                site_keys(parent) == site_keys(child)
            ),
            f"{cohort}_json_counts_match_numbers": (
                parent_stats["n_sites"] == expected["n_sites"]
                and parent_stats["n_proteins"] == expected["n_proteins"]
                and parent_stats["n_positive"] == expected["n_positive"]
                and phase05["cohort_counts"][cohort]["n_sites"] == expected["n_sites"]
                and phase05["cohort_counts"][cohort]["n_proteins"] == expected["n_proteins"]
                and phase05["cohort_counts"][cohort]["n_positive"] == expected["n_positive"]
            ),
            f"{cohort}_auc_matches_numbers": (
                close(parent_stats["auc_distance"]["auc"], expected["auc"], 5e-7)
                and close(parent_stats["auc_distance"]["ci_low"], expected["ci_low"], 5e-7)
                and close(parent_stats["auc_distance"]["ci_high"], expected["ci_high"], 5e-7)
                and close(child_cluster["estimate"], expected["auc"], 5e-7)
                and close(child_cluster["ci_low"], expected["ci_low"], 5e-7)
                and close(child_cluster["ci_high"], expected["ci_high"], 5e-7)
            ),
            f"{cohort}_bootstrap_contract": (
                parent_stats["auc_distance"]["draws"] == canonical_draws
                and parent_stats["auc_distance"]["seed"] == canonical_seed
                and child_cluster["draws"] == canonical_draws
            ),
            f"{cohort}_unique_site_keys": (
                not parent.duplicated(["acc", "pos"]).any()
                and not child.duplicated(["acc", "pos"]).any()
            ),
            f"{cohort}_enriched_qc_complete": (
                child.dist_core_A.notna().all()
                and child.pae_pair_max.notna().all()
                and child.sscore_rms.notna().all()
                and int(child.phenotype_count_reconstruction_mismatch.sum()) == 0
                and float(child.core_distance_recompute_delta_A.abs().max()) < 1e-4
                and sorted(child.alphafold_version.astype(int).unique().tolist()) == [6]
                and true_count(child.wgs_additional_mutation_flag) == 0
                and true_count(child.scar_control_correlation_flag) == 0
            ),
            f"{cohort}_parent_arm_table_matches_numbers": table_arm_matches(
                parent_arm_estimates, cohort, expected, "auc"
            ),
            f"{cohort}_phase0_5_arm_table_matches_numbers": table_arm_matches(
                child_arm_estimates, cohort, expected, "estimate"
            ),
        })

    checks.update({
        "primary_excludes_all_annotation_coincident_rows": (
            true_count(parent_data[PRIMARY].is_itself_annot) == 0
            and true_count(child_data[PRIMARY].is_itself_annot) == 0
        ),
        "inclusive_retains_three_annotation_coincident_rows": (
            true_count(parent_data[INCLUSIVE].is_itself_annot) == 3
            and true_count(child_data[INCLUSIVE].is_itself_annot) == 3
        ),
        "primary_is_exact_inclusive_minus_coincident_rows": (
            site_keys(parent_data[PRIMARY])
            == site_keys(
                parent_data[INCLUSIVE].loc[
                    ~parent_data[INCLUSIVE].is_itself_annot.astype(bool)
                ]
            )
        ),
        "all_point_mutants_dispositioned": len(disposition) == 497,
        "raw_screen_profile_count_reconciles_source": (
            int(disposition.raw_profile_available.sum()) == 474
        ),
        "sequence_qc_eligible_count": int(disposition.eligible_raw_cohort.sum()) == 427,
        "pae_manifest_covers_inclusive_proteins": (
            len(pae_manifest) == canonical[INCLUSIVE]["n_proteins"]
            and set(pae_manifest.acc) == set(child_data[INCLUSIVE].acc)
        ),
        "parent_complete_arm_outputs": (
            len(parent_arm_estimates) == 2
            and len(parent_cutoffs) == 8
            and len(parent_logistic) == 6
            and len(parent_descriptives) == 2
            and set(parent_cutoffs.cohort) == {PRIMARY, INCLUSIVE}
            and set(parent_logistic.cohort) == {PRIMARY, INCLUSIVE}
            and set(parent_descriptives.cohort) == {PRIMARY, INCLUSIVE}
        ),
        "phase0_5_complete_arm_outputs": (
            len(child_arm_estimates) == 2
            and len(child_cutoffs) == 8
            and len(child_logistic) == 10
            and len(child_descriptives) == 2
            and set(child_cutoffs.cohort) == {PRIMARY, INCLUSIVE}
            and set(child_logistic.cohort) == {PRIMARY, INCLUSIVE}
            and set(child_descriptives.cohort) == {PRIMARY, INCLUSIVE}
        ),
        "confidence_table_has_all_eleven_strata_for_both_arms": (
            len(confidence) == 22
            and set(confidence.cohort) == {PRIMARY, INCLUSIVE}
            and all(
                set(confidence.loc[confidence.cohort == cohort, "stratum"]) == expected_strata
                for cohort in (PRIMARY, INCLUSIVE)
            )
        ),
        "confidence_all_rows_reuse_frozen_arm_intervals": all(
            (
                len(rows := confidence.loc[
                    (confidence.cohort == cohort) & (confidence.stratum == "all")
                ]) == 1
                and close(rows.iloc[0].estimate, phase0["cohorts"][cohort]["auc_distance"]["auc"])
                and close(rows.iloc[0].ci_low, phase0["cohorts"][cohort]["auc_distance"]["ci_low"])
                and close(rows.iloc[0].ci_high, phase0["cohorts"][cohort]["auc_distance"]["ci_high"])
                and int(rows.iloc[0].draws) == canonical_draws
            )
            for cohort in (PRIMARY, INCLUSIVE)
        ),
        "confidence_post_result_rows_use_declared_sensitivity_budget": (
            confidence.loc[confidence.stratum != "all", "draws"].astype(int).between(
                int(phase05["n_sensitivity_bootstrap"] * 0.95),
                phase05["n_sensitivity_bootstrap"],
            ).all()
        ),
        "cohort_sensitivity_table_complete": len(cohort_sensitivity) == 7,
        "pae_at10_table_complete_for_three_cohorts": (
            len(pae_at10) == 12
            and set(pae_at10.cohort) == expected_grid_cohorts
            and set(pae_at10.pae_column) == expected_pae_columns
            and all(len(pae_at10.loc[pae_at10.cohort == cohort]) == 4 for cohort in expected_grid_cohorts)
        ),
        "pae_grid_has_72_cells_for_each_of_three_cohorts": (
            len(pae_grid) == 216
            and set(pae_grid.cohort) == expected_grid_cohorts
            and set(pae_grid.pae_column) == expected_pae_columns
            and all(len(pae_grid.loc[pae_grid.cohort == cohort]) == 72 for cohort in expected_grid_cohorts)
        ),
        "declared_pair_max_joint_cell_is_grid_minimum_in_all_cohorts": all(
            (
                len(cell := pae_grid.loc[
                    (pae_grid.cohort == cohort)
                    & (pae_grid.pae_column == "pae_pair_max")
                    & (pae_grid.pae_threshold_A == 10)
                    & (pae_grid.site_plddt_floor == 70)
                ]) == 1
                and float(cell.iloc[0].auc_rank_low_to_high_within_cohort) == 1
                and close(cell.iloc[0].auc, pae_grid.loc[pae_grid.cohort == cohort, "auc"].min())
            )
            for cohort in expected_grid_cohorts
        ),
        "obsolete_72x2_grid_absent": not (RESULTS / "pae_filter_grid_72x2.csv").exists(),
        "sift_table_complete_for_three_cohorts": (
            len(sift_sensitivity) == 3
            and set(sift_sensitivity.cohort) == expected_grid_cohorts
        ),
        "sift_points_inside_corresponding_distance_intervals": all(
            (
                phase0["cohorts"][cohort]["auc_distance"]["ci_low"]
                <= sift_sensitivity.loc[
                    sift_sensitivity.cohort == cohort, "sift_auc"
                ].iloc[0]
                <= phase0["cohorts"][cohort]["auc_distance"]["ci_high"]
            )
            for cohort in (PRIMARY, INCLUSIVE)
        ),
        "feature_table_primary_row_reuses_primary_interval": (
            len(primary_feature := feature_definitions.loc[
                feature_definitions.distance_definition == "dist_core_A"
            ]) == 1
            and close(primary_feature.iloc[0].estimate, phase0["cohorts"][PRIMARY]["auc_distance"]["auc"])
            and close(primary_feature.iloc[0].ci_low, phase0["cohorts"][PRIMARY]["auc_distance"]["ci_low"])
            and close(primary_feature.iloc[0].ci_high, phase0["cohorts"][PRIMARY]["auc_distance"]["ci_high"])
            and int(primary_feature.iloc[0].draws) == canonical_draws
        ),
        "residue_table_complete": len(pd.read_csv(RESULTS / "residue_class_sensitivity.csv")) == 3,
        "feature_definition_table_complete": len(feature_definitions) == 5,
        "continuous_table_complete": len(pd.read_csv(RESULTS / "continuous_outcomes.csv")) == 5,
        "benchmark_table_complete": len(pd.read_csv(RESULTS / "predictor_benchmark.csv")) == 5,
        "within_protein_table_complete": (
            len(pd.read_csv(RESULTS / "within_protein_auc.csv"))
            == phase05["within_protein_discrimination"]["informative_proteins"]
        ),
        "supplement_workbook_exists": (
            (RESULTS / "phase0_5_supplement.xlsx").is_file()
            and (RESULTS / "phase0_5_supplement.xlsx").stat().st_size > 10000
        ),
    })

    narrative_paths = [
        PARENT / "RESULTS.md",
        HERE / "RESULTS.md",
        HERE / "ANALYSIS_PROVENANCE.md",
        MANUSCRIPT / "preprint_draft_v1.md",
    ]
    narrative_text = {path: path.read_text() for path in narrative_paths}
    primary_interval = (
        f"{canonical[PRIMARY]['rounded_ci_low']:.3f}–"
        f"{canonical[PRIMARY]['rounded_ci_high']:.3f}"
    )
    inclusive_interval = (
        f"{canonical[INCLUSIVE]['rounded_ci_low']:.3f}–"
        f"{canonical[INCLUSIVE]['rounded_ci_high']:.3f}"
    )
    primary_bracket_interval = (
        f"{canonical[PRIMARY]['rounded_ci_low']:.3f}, "
        f"{canonical[PRIMARY]['rounded_ci_high']:.3f}"
    )
    inclusive_bracket_interval = (
        f"{canonical[INCLUSIVE]['rounded_ci_low']:.3f}, "
        f"{canonical[INCLUSIVE]['rounded_ci_high']:.3f}"
    )
    manuscript_text = narrative_text[MANUSCRIPT / "preprint_draft_v1.md"]
    abstract_text = manuscript_text.split("## Introduction", 1)[0]
    stale_interval = re.compile(r"0\.435\s*[/,–-]\s*0\.650")
    checks.update({
        "canonical_primary_interval_in_all_narratives": all(
            primary_interval in text or primary_bracket_interval in text
            for text in narrative_text.values()
        ),
        "canonical_inclusive_interval_in_all_narratives": all(
            inclusive_interval in text or inclusive_bracket_interval in text
            for text in narrative_text.values()
        ),
        "abstract_names_primary_and_inclusive_arms": all(
            token in abstract_text
            for token in (
                "primary cohort excluded",
                f"{canonical[PRIMARY]['n_sites']} substitutions",
                f"{canonical[PRIMARY]['rounded_auc']:.3f}",
                primary_interval,
                "named inclusive sensitivity",
                f"{canonical[INCLUSIVE]['n_sites']} substitutions",
                f"{canonical[INCLUSIVE]['rounded_auc']:.3f}",
                inclusive_interval,
            )
        ),
        "stale_interval_absent_from_narratives": all(
            stale_interval.search(text) is None for text in narrative_text.values()
        ),
        "pae_pair_max_disclosed_in_phase0_5_narratives": all(
            "pae_pair_max" in narrative_text[path]
            for path in (
                HERE / "RESULTS.md",
                HERE / "ANALYSIS_PROVENANCE.md",
                MANUSCRIPT / "preprint_draft_v1.md",
            )
        ),
        "range_restriction_caveat_absent_from_results_and_manuscript": all(
            re.search(r"range[- ]restrict", narrative_text[path], re.IGNORECASE) is None
            for path in (
                PARENT / "RESULTS.md",
                HERE / "RESULTS.md",
                MANUSCRIPT / "preprint_draft_v1.md",
            )
        ),
    })

    pdf_path = MANUSCRIPT / "preprint_draft_v1.pdf"
    pdf_reader = PdfReader(str(pdf_path))
    pdf_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
    render_manifest_path = MANUSCRIPT / "rendered" / "render_manifest.json"
    render_manifest = json.loads(render_manifest_path.read_text())
    expected_page_files = [
        f"page-{page:02d}.png" for page in range(1, len(pdf_reader.pages) + 1)
    ]
    actual_page_files = sorted(
        path.name for path in (MANUSCRIPT / "rendered").glob("page-*.png")
    )
    rendered_rows = render_manifest["pages"]
    rendered_hashes_match = all(
        (MANUSCRIPT / "rendered" / row["file"]).is_file()
        and sha256(MANUSCRIPT / "rendered" / row["file"]) == row["sha256"]
        and (MANUSCRIPT / "rendered" / row["file"]).stat().st_size == row["bytes"]
        for row in rendered_rows
    )
    contact = render_manifest["contact_sheet"]
    contact_path = MANUSCRIPT / "rendered" / contact["file"]
    page_match = re.search(
        r"rebuilt review PDF contains \*\*([0-9]+) pages\*\*",
        numbers_text,
    )
    if page_match is None:
        raise SystemExit("could not parse canonical PDF page count from NUMBERS.md")
    canonical_pdf_pages = int(page_match.group(1))
    roc_band_match = re.search(
        r"Figure 1B ROC envelope.*?\*\*([0-9,]+)\*\* protein-cluster draws"
        r".*?seed \*\*([0-9]+)\*\*",
        numbers_text,
        re.DOTALL,
    )
    checks.update({
        "rebuilt_pdf_page_count_matches_numbers": len(pdf_reader.pages) == canonical_pdf_pages,
        "canonical_intervals_present_in_pdf_text": (
            primary_interval in pdf_text and inclusive_interval in pdf_text
        ),
        "stale_interval_absent_from_pdf_text": stale_interval.search(pdf_text) is None,
        "pdf_contains_primary_and_named_inclusive_language": (
            "primary cohort excluded" in pdf_text
            and "named inclusive sensitivity" in pdf_text
        ),
        "render_manifest_bound_to_current_pdf": (
            render_manifest["pdf_sha256"] == sha256(pdf_path)
            and render_manifest["page_count"] == len(pdf_reader.pages)
            and render_manifest["render_dpi"] >= 144
        ),
        "rendered_page_set_exactly_matches_pdf": (
            actual_page_files == expected_page_files
            and [row["file"] for row in rendered_rows] == expected_page_files
            and [row["page"] for row in rendered_rows]
            == list(range(1, len(pdf_reader.pages) + 1))
        ),
        "rendered_page_hashes_match_manifest": rendered_hashes_match,
        "rendered_contact_sheet_matches_manifest": (
            contact_path.is_file()
            and sha256(contact_path) == contact["sha256"]
            and contact_path.stat().st_size == contact["bytes"]
        ),
        "render_manifest_row_count_matches_pdf": len(rendered_rows) == len(pdf_reader.pages),
        # The panel-composed figures are what the editable manuscript and the Word build
        # embed. Before this check they were the only reader-facing artifacts bound by
        # nothing: not the freeze gate, not the render manifest, not the clean room.
        # Hashes are declared in NUMBERS.md section 17 and parsed by parse_frozen_hashes.
        "panel_figures_match_numbers": all(
            relative in frozen_hashes
            and (PARENT / relative).is_file()
            and sha256(PARENT / relative) == frozen_hashes[relative]
            for relative in (
                "manuscript/figure1.png",
                "manuscript/figure2.png",
                "manuscript/figure1.pdf",
                "manuscript/figure2.pdf",
            )
        ),
        "panel_figure_provenance_declared": (
            "## 17. Figure Provenance" in numbers_text
            and "manuscript/panels/compose.py" in numbers_text
            and roc_band_match is not None
        ),
        "panel_roc_band_contract_matches_source": (
            roc_band_match is not None
            and re.search(
                r"^N_BAND, SEED = numbers_roc_band\(\)",
                (PARENT / "manuscript" / "panels" / "src" / "p1b_roc.py").read_text(),
                re.MULTILINE,
            )
            is not None
        ),
    })

    checks = {name: bool(passed) for name, passed in checks.items()}
    failed = [name for name, passed in checks.items() if not passed]
    report = {
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "failed": failed,
        "numbers_authority": {
            "path": str(NUMBERS.relative_to(PARENT)),
            "frozen_hashes": frozen_hashes,
            "freeze_hash_checks": freeze_checks,
        },
        "cohort_contract": {
            "primary": PRIMARY,
            "inclusive_sensitivity": INCLUSIVE,
        },
        "pdf": {
            "path": str(pdf_path.relative_to(PARENT)),
            "sha256": sha256(pdf_path),
            "pages": len(pdf_reader.pages),
            "render_manifest": str(render_manifest_path.relative_to(PARENT)),
        },
        "max_core_distance_delta_A": {
            cohort: float(child_data[cohort].core_distance_recompute_delta_A.abs().max())
            for cohort in (PRIMARY, INCLUSIVE)
        },
    }
    (RESULTS / "verification_report.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

    release_files = set(release_source_files(PARENT))
    release_files.discard(RESULTS / "release_manifest.csv")
    manifest_rows = [
        {
            "path": str(path.relative_to(PARENT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(release_files)
    ]
    pd.DataFrame(manifest_rows).to_csv(RESULTS / "release_manifest.csv", index=False)

    if failed:
        raise SystemExit(f"verification failed: {', '.join(failed)}")
    print(f"PASS: {len(checks)} checks; manifest contains {len(manifest_rows)} files")


if __name__ == "__main__":
    main()
