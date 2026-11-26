# Status: read this first, update it last

Two of us work on this project. Every Claude Code session starts by reading this file and
ends by updating it, so whoever opens the repo next knows where things stand.

_Last updated: 2026-11-26, main.tex fixed for the 2025 PNAS first-page layout; compiles in Overleaf._

## Done
- [x] Vote network 1957–2026 with excess scores: `data/edges.csv`, `data/edges_agg.csv`
- [x] 2024–2026 added from EurovisionAPI; 2023 final cross-checked (962/962)
- [x] 2026 final verified against Eurovisionworld (25/25 entries match)
- [x] Border layer: `data/borders.csv` (land borders only)
- [x] Diaspora layer: `data/diaspora.csv` from UN DESA Migrant Stock 2024 (1990–2024, 1,506 pairs)
- [x] Language layer: `data/language.csv` (CLDR 49 official languages + Glottolog 5.4 family/branch/sub-branch)
- [x] Null model: `data/null_results.csv`, `figures/null_modularity.pdf` (6 networks × 1,000 shuffles)
- [x] Lyrics: `data/lyrics.csv`, embeddings, `data/lyrics_similarity.csv` per era; rating sheet ready
- [x] 2023 semi-finals added from EurovisionAPI (edges.csv +574 rows)
- [x] Taste-profile similarity: `data/taste_similarity.csv` (taste_sim + own_sim)
- [x] Hand ratings merged (`data/lyrics_rating_sheet.csv`) and rating agreement run: RESULTS.md, Methods validation sentence
- [x] Year-centred lyric embeddings; taste robustness profiles (no top-5 partners, past only)
- [x] Collinearity check: `data/predictor_correlations.csv`, `data/predictor_vif.csv`
- [x] Step 6 main model: `data/regression_coefs.csv` (3 models × 6–7 specs)
- [x] Step 7 figures: `figures/fig1_modularity.pdf`, `fig2_coefficients.pdf`, `fig3_communities.pdf` + `figures/captions.md`
- [x] Leave-one-country-out check of same_family_only: `data/leave_one_out_family.csv`, `data/diff_family_top_pairs.csv`
- [x] Data checks scripted: `scripts/check_data.py`
- [x] Step 8 Methods draft: `paper/methods.md` / `methods.tex` (generated from `paper/methods_template.md`, ~1 page)
- [x] Robustness table: `paper/table_robustness.tex` / `.md`
- [x] Measures table (captures / misses): `paper/table_measures.tex` / `.md`
- [x] Overleaf: `paper/main.tex` + `python scripts/pack_overleaf.py` → `paper/overleaf/` + `paper/overleaf.zip` (complete project with the course template from `paper/pnas_template/`, pnas-new.cls v1.47)
- [x] Report files: `RESULTS.md` (facts per step) and `data/key_numbers.json` (written by scripts via `scripts/key_numbers.py`)
- [x] Course methods (weeks 3–4), branch feat/course-measures: NMI `data/nmi.csv`, attribute assortativity `data/assortativity.csv` (language branch, UN M49 region `data/region.csv`), disparity backbone `data/backbone_edges.csv`; Fig 3 redrawn with backbone edges
- [x] 2026 final checked against the official EBU scoreboard too (25/25, scripted in check_data.py)
- [x] Citation tracking: `references.bib` with 6 data + 6 papers, all verified against their pages

## In progress
<!-- One line per active task: who, what, branch, started. Delete the line when done. -->
- (none)

## Next up (in order)
1. Group writing (outline for Results: paper/results_outline.md): TODO sections in paper/main.tex (abstract, significance, introduction, results, discussion), 3 slides, reflection (deadline Fri 27 Nov 23:59)

## Decisions
- Diaspora: missing UN pairs = 0 (robustness: observed pairs only); diaspora analysis 1997+, each vote year matched to nearest UN year.
- Language: shared_official uses CLDR "official" only; branch / sub-branch from named Glottolog nodes (`data/glottolog_nodes.csv`).
- Null model: edge weight = mean excess, min 5 votes per pair (sum kept side by side). 2024–25 televote-only semis out of 2016+ networks; robustness run includes them.
- Step 6: regression on the full signed excess; >= 5 votes per pair; diaspora_log = log(1 + migrants) at nearest UN year.
- Language in the regression: one category (diff_family ref / same_family_only / same_branch_only / same_subbranch) + shared_official.
- Fig 3 at two-column width (17.8 cm), labels >= 6 pt; Fig 1–2 single column.
- The null-model histogram is a diagnostic in figures/diagnostics/, not a paper figure.
- Clustering: two-way by voter and receiver with the Cameron–Gelbach–Miller eigenvalue fix in all fits; one-way by voter as a robustness run.
- Methods trimmed to ~1 page; robustness runs in one table.
- Taste profiles per vote type for 2016+ (jury from jury votes, televote from televotes); 1997–2008 total.
- Lyrics: all cosines on year-centred vectors.
- Lyrics: main measure = taste_sim (A's taste profile from other years, B's songs excluded) vs B's song; own_sim kept for comparison.
- edges.csv: EurovisionAPI fills every (year, round) Spijkervet lacks (2023 semis added).

## Open questions (for the humans)
- Read Serrano 2009, Newman 2003, Danon 2005 (NOTES Literature TODOs).
- Length: a stand-in two-column 9pt build (no PNAS class locally) is ~4–5 pages (5 after the 2026-11-25 bib additions) with Methods, 3 figures, 2 tables and refs, but no abstract / intro / results / discussion yet. Check in Overleaf.
- Merge feat/course-measures into main (not pushed yet).
- EurovisionAPI has no stated license (GitHub API: none): ask the maintainers or say so in the data availability statement.
- paper TODOs: repository URL / data availability statement; captures/misses now in paper/table_measures.tex.
- Overleaf: compiles (4 pages on 2026-11-26, limit 6 incl. refs). When writing, keep \Endparasplit in main.tex at the end of page 1 (\Parasplit if page 1 ends mid-paragraph).
- Abstract, Significance, Introduction, Results text, Discussion, reflection: ours to write (TODO headers in methods_template.md).
- Hand ratings: rater 2 vs model is near 0 (0.035) while rater 1 vs model is 0.434; decide how to report this (n = 20, no CI computed).
- Fill in the "what it found / how we use it" lines under Literature in NOTES.md (read the papers)
- How to treat yu / cs (drop, or map to successors)?
- Which era(s) does the paper focus on?

## Log
<!-- Newest first. One line per session: date, who, what changed, what to check. -->
- 2026-11-26, Brynja (via Claude): paper/results_outline.md — facts per Results paragraph (R1–R5) with numbers from RESULTS.md, interpretation left TODO. Check: split the paragraphs between us.
- 2026-11-26, Brynja (via Claude): main.tex for the 2025 PNAS class: \Firstpage / \Endparasplit (page 1 layout), \dataavail, no DRAFT watermark, xurl, table_measures widths. Compiled in Overleaf: 4 pages, nothing over the margins. Check: move \Endparasplit as page 1 fills.
- 2026-11-26, Brynja (via Claude): course PNAS template (pnas-new.cls v1.47) into paper/pnas_template/; pack_overleaf.py copies it and writes paper/overleaf.zip; main.tex header updated. Check: upload overleaf.zip to Overleaf and compile.
- 2026-11-26, Brynja (via Claude): rater 1 ratings, merge_ratings.py + rating_agreement.py run, RESULTS / NOTES / Methods sentence. Check: the rating table in RESULTS.md.
- 2026-11-25, Kristófer (via Claude): docs sync: README build list / data files / checks, CLAUDE.md diagnostics path, RESULTS edges + borders, MANIFEST entry for the derived raw/votes_eurovisionapi.csv. Open: data/ratings_sheet_blind.md (untracked, not ours) conflicts with rater numbering.
- 2026-11-25, Kristófer (via Claude): bib TODOs resolved (DOIs for Burgoyne, Ginsburgh, Reimers 2019; Blondel journal; Reimers 2020 added; CLDR / UN license notes); 2026 final vs EBU scoreboard scripted. Check: Methods validation sentence.
- 2026-11-25, Kristófer (rater 2): all 20 ratings in data/ratings_rater2.csv. Rater 1: fill data/ratings_rater1.csv without opening ratings_rater2.csv.
- 2026-11-25, Kristófer (via Claude): per-rater files + ratings_sheet.md (make_rating_files.py), merge_ratings.py (1–5 check). Check: agree the scale wording in ratings_sheet.md before rating.
- 2026-11-25, Kristófer (via Claude): Methods paragraph (3 sentences) for NMI, assortativity, backbone; table_measures notes (unweighted; CY in Western Asia); methods.tex regenerated, overleaf repacked. Check: page count in Overleaf.
- 2026-11-25, Kristófer (via Claude): nmi.py, assortativity.py, backbone.py, build_region.py; null_model.py importable (outputs unchanged); Fig 3 = backbone edges, caption numbers from key_numbers. Check: Fig 3 at print size; RESULTS.md NMI / assortativity / backbone tables.
- 2026-11-16, Kristófer: CGM eigenvalue fix for all fits (replaces voter fallback), cluster_voter robustness row, Fig 2/tables regenerated, table_measures.tex. Check: jury CIs in RESULTS.md.
- 2026-11-16, Kristófer: clustering fallback (jury fits), Cameron et al. 2011 in bib, Methods trimmed, robustness table, Overleaf files. Check: paper/main.tex in Overleaf.
- 2026-11-16, Kristófer: check_data.py, Methods draft (write_methods.py), counts recorded by build scripts. Check: read paper/methods.md.
- 2026-11-16, Kristófer: Fig 3 two-column, histogram to diagnostics, leave-one-out check (leave_one_out.py). Check: RESULTS.md leave-one-out section.
- 2026-11-16, Kristófer: step 7 figures (make_figures.py) + captions. Check: the three PDFs at print size.
- 2026-11-16, Kristófer: language as category, taste profiles per vote type, step 6 rerun. Check: main table in RESULTS.md.
- 2026-11-16, Kristófer: year-centred embeddings, taste robustness profiles, collinearity, step 6 regression (build_pairs.py, regression.py). Check: coefficient tables in RESULTS.md.
- 2026-11-16, Kristófer: added 2023 semis (build_edges.py), reran pipeline + null model; taste_similarity.py; rating_agreement.py; Fixes log in NOTES. Check: taste vs own correlation in RESULTS.md.
- 2026-11-16, Kristófer: step 5 lyrics (build_lyrics.py, lyrics_similarity.py, raw lyrics, model in MANIFEST/bib). Check: lyrics_extremes.csv; do the hand rating.
- 2026-11-16, Kristófer: named Glottolog nodes for branches; null model rerun with mean5 + sum weighting + robustness network; fixed a dropped-pairs bug; found 2023 semis gap. Check: RESULTS.md tables.
- 2026-11-16, Kristófer: step 4 null model (null_model.py, null_results.csv, figure). Check: the table in RESULTS.md and data/communities_obs.csv.
- 2026-11-16, Kristófer: language layer revised: same_branch/same_subbranch, shared_official official-only (10 pairs changed). Check: data/language_groups.csv.
- 2026-11-16, Kristófer: step 3 language layer (build_language.py, language.csv, CLDR + Glottolog in MANIFEST/bib), RESULTS.md, key_numbers.json. Check: spot-check pairs in RESULTS.md.
- 2026-11-16, Kristófer: diaspora layer (build_diaspora.py, diaspora.csv, MANIFEST, references.bib). Check: the 5 sanity pairs in NOTES.md.
- 2026-11-16, Kristófer (via Claude): added references.bib + citation rule in CLAUDE.md + Literature section in NOTES.md
- 2026-11-16, Kristófer: added upstream caveat to the 2026 check (NOTES.md); started diaspora layer
- 2026-11-16, Kristófer: verified 2026 final, pinned deps (requirements.txt)
- 2026-11-11, Kristófer: initial pipeline, data 1957–2026, borders layer
