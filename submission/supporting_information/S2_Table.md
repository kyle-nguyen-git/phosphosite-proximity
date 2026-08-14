# S2 Table. The 72-cell confidence-by-predicted-aligned-error grids

Every cell is an AUC for distance under one combination of predicted-aligned-error column, PAE
threshold and site pLDDT floor, computed with the same estimator as the primary. The grid is a post hoc
family and is part of the 255-estimate yeast count of §2.2. No cell is a declared result.

## Four summaries at 10 Å

| Cohort | PAE column | Definition | Sites | Proteins | Affected | AUC |
|---|---|---|---:|---:|---:|---:|
| Primary (163 sites) | `pae_pair_max` | maximum of both directed entries | 44 | 21 | 25 | 0.435789 |
| Primary (163 sites) | `pae_site_to_target` | site to target | 48 | 22 | 27 | 0.458554 |
| Primary (163 sites) | `pae_pair_mean` | mean of both directed entries | 51 | 22 | 28 | 0.489130 |
| Primary (163 sites) | `pae_target_to_site` | target to site | 57 | 26 | 30 | 0.520988 |
| Inclusive (166 sites) | `pae_pair_max` | maximum of both directed entries | 47 | 23 | 28 | 0.496241 |
| Inclusive (166 sites) | `pae_site_to_target` | site to target | 51 | 24 | 30 | 0.512698 |
| Inclusive (166 sites) | `pae_pair_mean` | mean of both directed entries | 54 | 24 | 31 | 0.538569 |
| Inclusive (166 sites) | `pae_target_to_site` | target to site | 60 | 28 | 33 | 0.564534 |
| Legacy (158 sites) | `pae_pair_max` | maximum of both directed entries | 42 | 21 | 23 | 0.423341 |
| Legacy (158 sites) | `pae_site_to_target` | site to target | 46 | 22 | 25 | 0.445714 |
| Legacy (158 sites) | `pae_pair_mean` | mean of both directed entries | 49 | 22 | 26 | 0.476589 |
| Legacy (158 sites) | `pae_target_to_site` | target to site | 54 | 25 | 27 | 0.504801 |

## Primary (163 sites) — 72 cells

Range 0.416268 to 0.569444; median 0.489018. Support runs from 35 to 163 sites.

| PAE column | Threshold (Å) | pLDDT floor | Sites | Proteins | Affected | AUC |
|---|---:|---:|---:|---:|---:|---:|
| `pae_pair_max` | 5 | 0 | 37 | 20 | 20 | 0.488235 |
| `pae_pair_max` | 5 | 50 | 37 | 20 | 20 | 0.488235 |
| `pae_pair_max` | 5 | 70 | 35 | 20 | 18 | 0.483660 |
| `pae_pair_max` | 10 | 0 | 44 | 21 | 25 | 0.435789 |
| `pae_pair_max` | 10 | 50 | 43 | 20 | 24 | 0.425439 |
| `pae_pair_max` | 10 | 70 | 41 | 20 | 22 | 0.416268 |
| `pae_pair_max` | 15 | 0 | 55 | 23 | 30 | 0.520000 |
| `pae_pair_max` | 15 | 50 | 53 | 21 | 28 | 0.510000 |
| `pae_pair_max` | 15 | 70 | 49 | 21 | 25 | 0.486667 |
| `pae_pair_max` | 20 | 0 | 67 | 29 | 37 | 0.506306 |
| `pae_pair_max` | 20 | 50 | 62 | 25 | 34 | 0.471639 |
| `pae_pair_max` | 20 | 70 | 54 | 23 | 28 | 0.461538 |
| `pae_pair_max` | 25 | 0 | 81 | 31 | 44 | 0.505528 |
| `pae_pair_max` | 25 | 50 | 66 | 25 | 37 | 0.492078 |
| `pae_pair_max` | 25 | 70 | 56 | 23 | 29 | 0.468710 |
| `pae_pair_max` | 30 | 0 | 151 | 45 | 76 | 0.509649 |
| `pae_pair_max` | 30 | 50 | 79 | 31 | 43 | 0.489018 |
| `pae_pair_max` | 30 | 70 | 60 | 24 | 31 | 0.459399 |
| `pae_pair_mean` | 5 | 0 | 39 | 20 | 20 | 0.492105 |
| `pae_pair_mean` | 5 | 50 | 39 | 20 | 20 | 0.492105 |
| `pae_pair_mean` | 5 | 70 | 37 | 20 | 18 | 0.488304 |
| `pae_pair_mean` | 10 | 0 | 51 | 22 | 28 | 0.489130 |
| `pae_pair_mean` | 10 | 50 | 50 | 21 | 27 | 0.479871 |
| `pae_pair_mean` | 10 | 70 | 48 | 21 | 25 | 0.469565 |
| `pae_pair_mean` | 15 | 0 | 63 | 27 | 34 | 0.529412 |
| `pae_pair_mean` | 15 | 50 | 59 | 23 | 32 | 0.501157 |
| `pae_pair_mean` | 15 | 70 | 53 | 22 | 27 | 0.484330 |
| `pae_pair_mean` | 20 | 0 | 79 | 33 | 41 | 0.524390 |
| `pae_pair_mean` | 20 | 50 | 68 | 27 | 37 | 0.502180 |
| `pae_pair_mean` | 20 | 70 | 56 | 23 | 29 | 0.468710 |
| `pae_pair_mean` | 25 | 0 | 99 | 36 | 52 | 0.533961 |
| `pae_pair_mean` | 25 | 50 | 70 | 28 | 38 | 0.507401 |
| `pae_pair_mean` | 25 | 70 | 57 | 24 | 29 | 0.470443 |
| `pae_pair_mean` | 30 | 0 | 163 | 48 | 79 | 0.526823 |
| `pae_pair_mean` | 30 | 50 | 79 | 31 | 43 | 0.489018 |
| `pae_pair_mean` | 30 | 70 | 60 | 24 | 31 | 0.459399 |
| `pae_site_to_target` | 5 | 0 | 40 | 21 | 22 | 0.494949 |
| `pae_site_to_target` | 5 | 50 | 40 | 21 | 22 | 0.494949 |
| `pae_site_to_target` | 5 | 70 | 38 | 21 | 20 | 0.488889 |
| `pae_site_to_target` | 10 | 0 | 48 | 22 | 27 | 0.458554 |
| `pae_site_to_target` | 10 | 50 | 47 | 21 | 26 | 0.448718 |
| `pae_site_to_target` | 10 | 70 | 45 | 21 | 24 | 0.438492 |
| `pae_site_to_target` | 15 | 0 | 58 | 24 | 33 | 0.472727 |
| `pae_site_to_target` | 15 | 50 | 56 | 22 | 31 | 0.460645 |
| `pae_site_to_target` | 15 | 70 | 52 | 22 | 28 | 0.434524 |
| `pae_site_to_target` | 20 | 0 | 68 | 30 | 37 | 0.500436 |
| `pae_site_to_target` | 20 | 50 | 62 | 25 | 34 | 0.471639 |
| `pae_site_to_target` | 20 | 70 | 54 | 23 | 28 | 0.461538 |
| `pae_site_to_target` | 25 | 0 | 82 | 32 | 45 | 0.494294 |
| `pae_site_to_target` | 25 | 50 | 66 | 25 | 37 | 0.492078 |
| `pae_site_to_target` | 25 | 70 | 56 | 23 | 29 | 0.468710 |
| `pae_site_to_target` | 30 | 0 | 151 | 45 | 76 | 0.509649 |
| `pae_site_to_target` | 30 | 50 | 79 | 31 | 43 | 0.489018 |
| `pae_site_to_target` | 30 | 70 | 60 | 24 | 31 | 0.459399 |
| `pae_target_to_site` | 5 | 0 | 45 | 22 | 23 | 0.501976 |
| `pae_target_to_site` | 5 | 50 | 45 | 22 | 23 | 0.501976 |
| `pae_target_to_site` | 5 | 70 | 42 | 21 | 20 | 0.511364 |
| `pae_target_to_site` | 10 | 0 | 57 | 26 | 30 | 0.520988 |
| `pae_target_to_site` | 10 | 50 | 54 | 23 | 28 | 0.506868 |
| `pae_target_to_site` | 10 | 70 | 49 | 21 | 25 | 0.478333 |
| `pae_target_to_site` | 15 | 0 | 74 | 31 | 38 | 0.569444 |
| `pae_target_to_site` | 15 | 50 | 64 | 26 | 33 | 0.561095 |
| `pae_target_to_site` | 15 | 70 | 53 | 22 | 26 | 0.521368 |
| `pae_target_to_site` | 20 | 0 | 90 | 33 | 50 | 0.517000 |
| `pae_target_to_site` | 20 | 50 | 69 | 27 | 38 | 0.505942 |
| `pae_target_to_site` | 20 | 70 | 56 | 23 | 29 | 0.468710 |
| `pae_target_to_site` | 25 | 0 | 102 | 37 | 52 | 0.551154 |
| `pae_target_to_site` | 25 | 50 | 70 | 28 | 38 | 0.507401 |
| `pae_target_to_site` | 25 | 70 | 57 | 24 | 29 | 0.470443 |
| `pae_target_to_site` | 30 | 0 | 163 | 48 | 79 | 0.526823 |
| `pae_target_to_site` | 30 | 50 | 79 | 31 | 43 | 0.489018 |
| `pae_target_to_site` | 30 | 70 | 60 | 24 | 31 | 0.459399 |

## Inclusive (166 sites) — 72 cells

Range 0.486316 to 0.600949; median 0.536494. Support runs from 38 to 166 sites.

| PAE column | Threshold (Å) | pLDDT floor | Sites | Proteins | Affected | AUC |
|---|---:|---:|---:|---:|---:|---:|
| `pae_pair_max` | 5 | 0 | 40 | 22 | 23 | 0.554987 |
| `pae_pair_max` | 5 | 50 | 40 | 22 | 23 | 0.554987 |
| `pae_pair_max` | 5 | 70 | 38 | 22 | 21 | 0.557423 |
| `pae_pair_max` | 10 | 0 | 47 | 23 | 28 | 0.496241 |
| `pae_pair_max` | 10 | 50 | 46 | 22 | 27 | 0.489279 |
| `pae_pair_max` | 10 | 70 | 44 | 22 | 25 | 0.486316 |
| `pae_pair_max` | 15 | 0 | 58 | 25 | 33 | 0.563636 |
| `pae_pair_max` | 15 | 50 | 56 | 23 | 31 | 0.557419 |
| `pae_pair_max` | 15 | 70 | 52 | 23 | 28 | 0.541667 |
| `pae_pair_max` | 20 | 0 | 70 | 31 | 40 | 0.543333 |
| `pae_pair_max` | 20 | 50 | 65 | 27 | 37 | 0.514479 |
| `pae_pair_max` | 20 | 70 | 57 | 25 | 31 | 0.513648 |
| `pae_pair_max` | 25 | 0 | 84 | 33 | 47 | 0.537090 |
| `pae_pair_max` | 25 | 50 | 69 | 27 | 40 | 0.530172 |
| `pae_pair_max` | 25 | 70 | 59 | 25 | 32 | 0.518519 |
| `pae_pair_max` | 30 | 0 | 154 | 47 | 79 | 0.528270 |
| `pae_pair_max` | 30 | 50 | 82 | 33 | 46 | 0.522343 |
| `pae_pair_max` | 30 | 70 | 63 | 26 | 34 | 0.507099 |
| `pae_pair_mean` | 5 | 0 | 42 | 22 | 23 | 0.558352 |
| `pae_pair_mean` | 5 | 50 | 42 | 22 | 23 | 0.558352 |
| `pae_pair_mean` | 5 | 70 | 40 | 22 | 21 | 0.561404 |
| `pae_pair_mean` | 10 | 0 | 54 | 24 | 31 | 0.538569 |
| `pae_pair_mean` | 10 | 50 | 53 | 23 | 30 | 0.531884 |
| `pae_pair_mean` | 10 | 70 | 51 | 23 | 28 | 0.526398 |
| `pae_pair_mean` | 15 | 0 | 66 | 29 | 37 | 0.567568 |
| `pae_pair_mean` | 15 | 50 | 62 | 25 | 35 | 0.543915 |
| `pae_pair_mean` | 15 | 70 | 56 | 24 | 30 | 0.535897 |
| `pae_pair_mean` | 20 | 0 | 82 | 35 | 44 | 0.556818 |
| `pae_pair_mean` | 20 | 50 | 71 | 29 | 40 | 0.539516 |
| `pae_pair_mean` | 20 | 70 | 59 | 25 | 32 | 0.518519 |
| `pae_pair_mean` | 25 | 0 | 102 | 38 | 55 | 0.559381 |
| `pae_pair_mean` | 25 | 50 | 73 | 30 | 41 | 0.543445 |
| `pae_pair_mean` | 25 | 70 | 60 | 26 | 32 | 0.520089 |
| `pae_pair_mean` | 30 | 0 | 166 | 50 | 82 | 0.544135 |
| `pae_pair_mean` | 30 | 50 | 82 | 33 | 46 | 0.522343 |
| `pae_pair_mean` | 30 | 70 | 63 | 26 | 34 | 0.507099 |
| `pae_site_to_target` | 5 | 0 | 43 | 23 | 25 | 0.555556 |
| `pae_site_to_target` | 5 | 50 | 43 | 23 | 25 | 0.555556 |
| `pae_site_to_target` | 5 | 70 | 41 | 23 | 23 | 0.555556 |
| `pae_site_to_target` | 10 | 0 | 51 | 24 | 30 | 0.512698 |
| `pae_site_to_target` | 10 | 50 | 50 | 23 | 29 | 0.505747 |
| `pae_site_to_target` | 10 | 70 | 48 | 23 | 27 | 0.500882 |
| `pae_site_to_target` | 15 | 0 | 61 | 26 | 36 | 0.516667 |
| `pae_site_to_target` | 15 | 50 | 59 | 24 | 34 | 0.508235 |
| `pae_site_to_target` | 15 | 70 | 55 | 24 | 31 | 0.489247 |
| `pae_site_to_target` | 20 | 0 | 71 | 32 | 40 | 0.537903 |
| `pae_site_to_target` | 20 | 50 | 65 | 27 | 37 | 0.514479 |
| `pae_site_to_target` | 20 | 70 | 57 | 25 | 31 | 0.513648 |
| `pae_site_to_target` | 25 | 0 | 85 | 34 | 48 | 0.525901 |
| `pae_site_to_target` | 25 | 50 | 69 | 27 | 40 | 0.530172 |
| `pae_site_to_target` | 25 | 70 | 59 | 25 | 32 | 0.518519 |
| `pae_site_to_target` | 30 | 0 | 154 | 47 | 79 | 0.528270 |
| `pae_site_to_target` | 30 | 50 | 82 | 33 | 46 | 0.522343 |
| `pae_site_to_target` | 30 | 70 | 63 | 26 | 34 | 0.507099 |
| `pae_target_to_site` | 5 | 0 | 48 | 24 | 26 | 0.559441 |
| `pae_target_to_site` | 5 | 50 | 48 | 24 | 26 | 0.559441 |
| `pae_target_to_site` | 5 | 70 | 45 | 23 | 23 | 0.575099 |
| `pae_target_to_site` | 10 | 0 | 60 | 28 | 33 | 0.564534 |
| `pae_target_to_site` | 10 | 50 | 57 | 25 | 31 | 0.554591 |
| `pae_target_to_site` | 10 | 70 | 52 | 23 | 28 | 0.534226 |
| `pae_target_to_site` | 15 | 0 | 77 | 33 | 41 | 0.600949 |
| `pae_target_to_site` | 15 | 50 | 67 | 28 | 36 | 0.597670 |
| `pae_target_to_site` | 15 | 70 | 56 | 24 | 29 | 0.570881 |
| `pae_target_to_site` | 20 | 0 | 93 | 35 | 53 | 0.544340 |
| `pae_target_to_site` | 20 | 50 | 72 | 29 | 41 | 0.542093 |
| `pae_target_to_site` | 20 | 70 | 59 | 25 | 32 | 0.518519 |
| `pae_target_to_site` | 25 | 0 | 105 | 39 | 55 | 0.575636 |
| `pae_target_to_site` | 25 | 50 | 73 | 30 | 41 | 0.543445 |
| `pae_target_to_site` | 25 | 70 | 60 | 26 | 32 | 0.520089 |
| `pae_target_to_site` | 30 | 0 | 166 | 50 | 82 | 0.544135 |
| `pae_target_to_site` | 30 | 50 | 82 | 33 | 46 | 0.522343 |
| `pae_target_to_site` | 30 | 70 | 63 | 26 | 34 | 0.507099 |

## Legacy (158 sites) — 72 cells

Range 0.406015 to 0.553968; median 0.479704. Support runs from 34 to 158 sites.

| PAE column | Threshold (Å) | pLDDT floor | Sites | Proteins | Affected | AUC |
|---|---:|---:|---:|---:|---:|---:|
| `pae_pair_max` | 5 | 0 | 35 | 20 | 18 | 0.477124 |
| `pae_pair_max` | 5 | 50 | 35 | 20 | 18 | 0.477124 |
| `pae_pair_max` | 5 | 70 | 34 | 19 | 17 | 0.474048 |
| `pae_pair_max` | 10 | 0 | 42 | 21 | 23 | 0.423341 |
| `pae_pair_max` | 10 | 50 | 41 | 20 | 22 | 0.411483 |
| `pae_pair_max` | 10 | 70 | 40 | 19 | 21 | 0.406015 |
| `pae_pair_max` | 15 | 0 | 52 | 22 | 27 | 0.506667 |
| `pae_pair_max` | 15 | 50 | 51 | 21 | 26 | 0.496923 |
| `pae_pair_max` | 15 | 70 | 48 | 20 | 24 | 0.477431 |
| `pae_pair_max` | 20 | 0 | 64 | 29 | 34 | 0.489216 |
| `pae_pair_max` | 20 | 50 | 60 | 25 | 32 | 0.456473 |
| `pae_pair_max` | 20 | 70 | 53 | 22 | 27 | 0.451567 |
| `pae_pair_max` | 25 | 0 | 78 | 31 | 41 | 0.489782 |
| `pae_pair_max` | 25 | 50 | 64 | 25 | 35 | 0.478818 |
| `pae_pair_max` | 25 | 70 | 55 | 22 | 28 | 0.458995 |
| `pae_pair_max` | 30 | 0 | 146 | 45 | 71 | 0.504789 |
| `pae_pair_max` | 30 | 50 | 76 | 31 | 40 | 0.486806 |
| `pae_pair_max` | 30 | 70 | 59 | 23 | 30 | 0.449425 |
| `pae_pair_mean` | 5 | 0 | 37 | 20 | 18 | 0.482456 |
| `pae_pair_mean` | 5 | 50 | 37 | 20 | 18 | 0.482456 |
| `pae_pair_mean` | 5 | 70 | 36 | 19 | 17 | 0.479876 |
| `pae_pair_mean` | 10 | 0 | 49 | 22 | 26 | 0.476589 |
| `pae_pair_mean` | 10 | 50 | 48 | 21 | 25 | 0.466087 |
| `pae_pair_mean` | 10 | 70 | 47 | 20 | 24 | 0.460145 |
| `pae_pair_mean` | 15 | 0 | 60 | 26 | 31 | 0.513904 |
| `pae_pair_mean` | 15 | 50 | 57 | 23 | 30 | 0.487654 |
| `pae_pair_mean` | 15 | 70 | 52 | 21 | 26 | 0.474852 |
| `pae_pair_mean` | 20 | 0 | 76 | 33 | 38 | 0.508310 |
| `pae_pair_mean` | 20 | 50 | 66 | 27 | 35 | 0.488479 |
| `pae_pair_mean` | 20 | 70 | 55 | 22 | 28 | 0.458995 |
| `pae_pair_mean` | 25 | 0 | 95 | 36 | 48 | 0.526596 |
| `pae_pair_mean` | 25 | 50 | 68 | 28 | 36 | 0.493924 |
| `pae_pair_mean` | 25 | 70 | 56 | 23 | 28 | 0.460459 |
| `pae_pair_mean` | 30 | 0 | 158 | 48 | 74 | 0.522040 |
| `pae_pair_mean` | 30 | 50 | 76 | 31 | 40 | 0.486806 |
| `pae_pair_mean` | 30 | 70 | 59 | 23 | 30 | 0.449425 |
| `pae_site_to_target` | 5 | 0 | 38 | 21 | 20 | 0.483333 |
| `pae_site_to_target` | 5 | 50 | 38 | 21 | 20 | 0.483333 |
| `pae_site_to_target` | 5 | 70 | 37 | 20 | 19 | 0.479532 |
| `pae_site_to_target` | 10 | 0 | 46 | 22 | 25 | 0.445714 |
| `pae_site_to_target` | 10 | 50 | 45 | 21 | 24 | 0.434524 |
| `pae_site_to_target` | 10 | 70 | 44 | 20 | 23 | 0.428571 |
| `pae_site_to_target` | 15 | 0 | 55 | 23 | 30 | 0.456000 |
| `pae_site_to_target` | 15 | 50 | 54 | 22 | 29 | 0.445517 |
| `pae_site_to_target` | 15 | 70 | 51 | 21 | 27 | 0.424383 |
| `pae_site_to_target` | 20 | 0 | 65 | 30 | 34 | 0.483871 |
| `pae_site_to_target` | 20 | 50 | 60 | 25 | 32 | 0.456473 |
| `pae_site_to_target` | 20 | 70 | 53 | 22 | 27 | 0.451567 |
| `pae_site_to_target` | 25 | 0 | 79 | 32 | 42 | 0.478121 |
| `pae_site_to_target` | 25 | 50 | 64 | 25 | 35 | 0.478818 |
| `pae_site_to_target` | 25 | 70 | 55 | 22 | 28 | 0.458995 |
| `pae_site_to_target` | 30 | 0 | 146 | 45 | 71 | 0.504789 |
| `pae_site_to_target` | 30 | 50 | 76 | 31 | 40 | 0.486806 |
| `pae_site_to_target` | 30 | 70 | 59 | 23 | 30 | 0.449425 |
| `pae_target_to_site` | 5 | 0 | 43 | 22 | 21 | 0.489177 |
| `pae_target_to_site` | 5 | 50 | 43 | 22 | 21 | 0.489177 |
| `pae_target_to_site` | 5 | 70 | 41 | 20 | 19 | 0.502392 |
| `pae_target_to_site` | 10 | 0 | 54 | 25 | 27 | 0.504801 |
| `pae_target_to_site` | 10 | 50 | 52 | 23 | 26 | 0.492604 |
| `pae_target_to_site` | 10 | 70 | 48 | 20 | 24 | 0.468750 |
| `pae_target_to_site` | 15 | 0 | 71 | 30 | 35 | 0.553968 |
| `pae_target_to_site` | 15 | 50 | 62 | 26 | 31 | 0.549428 |
| `pae_target_to_site` | 15 | 70 | 52 | 21 | 25 | 0.512593 |
| `pae_target_to_site` | 20 | 0 | 86 | 33 | 46 | 0.509783 |
| `pae_target_to_site` | 20 | 50 | 67 | 27 | 36 | 0.492832 |
| `pae_target_to_site` | 20 | 70 | 55 | 22 | 28 | 0.458995 |
| `pae_target_to_site` | 25 | 0 | 98 | 37 | 48 | 0.544167 |
| `pae_target_to_site` | 25 | 50 | 68 | 28 | 36 | 0.493924 |
| `pae_target_to_site` | 25 | 70 | 56 | 23 | 28 | 0.460459 |
| `pae_target_to_site` | 30 | 0 | 158 | 48 | 74 | 0.522040 |
| `pae_target_to_site` | 30 | 50 | 76 | 31 | 40 | 0.486806 |
| `pae_target_to_site` | 30 | 70 | 59 | 23 | 30 | 0.449425 |

Source: `phase0_calibration/phase0_5/results/pae_filter_grid_72x3.csv` and
`pae_column_sensitivity_at_10A.csv`. Registered in `NUMBERS.md` §9.
