# Results outline (facts only — the sentences and interpretation are ours to write)

How to use: one subsection per paragraph of the Results in `paper/main.tex`. Each lists what the paragraph
reports, the numbers it can quote (all from `RESULTS.md` / `data/key_numbers.json`; check against those before
submitting), and where the figure/table is. "Our reading" is left for us. Numbers here were copied from RESULTS.md
on 2026-11-26; if a script is rerun, recheck them.

Space: the PDF is 4 pages with all text sections as TODO; the limit is 6 incl. references. That leaves roughly
2 pages (~1,600–1,800 words) for abstract, significance, introduction, results and discussion together. A rough
split: Results ~600–700 words, Introduction ~400, Discussion ~400–500.

Suggested order follows the question: (1) is there excess-vote structure at all? (2) what goes with it —
friendship or taste? (3) do juries and televoters differ? (4) how robust is it?

---

## R1. Countries form voting blocs beyond chance (Fig. 1; Table 1A)

Reports: observed modularity Q vs the shuffle null, per era.

| Network | Q obs | null mean ± SD | z |
|---|---|---|---|
| 1957–1974 | 0.433 | 0.285 ± 0.031 | 4.7 |
| 1975–1996 | 0.370 | 0.268 ± 0.021 | 4.8 |
| 1997–2008 televote | 0.445 | 0.218 ± 0.012 | 19.5 |
| 2009–2015 50/50 | 0.413 | 0.207 ± 0.011 | 19.5 |
| 2016+ jury | 0.309 | 0.204 ± 0.011 | 9.8 |
| 2016+ televote | 0.436 | 0.203 ± 0.010 | 23.3 |

- No shuffle reached the observed Q in any network (p = 0.001, the smallest possible with 1,000 shuffles).
- 4–5 communities per network; 18–45 countries per network.
- Summed-excess weighting gives the same picture (Table 1A, z 4.5–25.3).
- Our reading: TODO (e.g. how the eras compare; jury vs televote Q).

## R2. The blocs line up with language and region (NMI, assortativity; Fig. 3)

Reports: how well communities match language groups, and whether positive-excess edges join similar countries.

- NMI, communities vs language sub-branch: 0.500 (2016+ televote, z 6.2) to 0.609 (1997–2008, z 7.7);
  1957–1974: 0.595 (z 4.2, only 17 countries). vs language branch: 0.346 (1957–74, z 1.7, p 0.069 — not
  significant) to 0.510 (1997–2008, z 6.9).
- Attribute assortativity (unweighted), language branch: r 0.060 (2016+ jury) to 0.123 (1957–74);
  region: r 0.087 (1975–96) to 0.185 (1957–74). All above the shuffle null (p ≤ 0.011).
  2016+ jury vs televote: language 0.060 vs 0.107; region 0.098 vs 0.148.
- Backbone (Fig. 3, α = 0.05): 23 of 404 jury edges and 29 of 333 televote edges kept; within-community share
  of edges 42.8% (all) → 78.3% (backbone) for jury, 50.4% → 93.1% for televote.
- Our reading: TODO (which blocs are visible in Fig. 3; do not over-read single edges).

## R3. What predicts excess between a pair: friendship vs taste (Fig. 2; main model)

Reports: standardised betas (95% CI), one model per sample; n = 1,537 / 1,537 / 1,257 directed pairs.

| term | 2016+ jury | 2016+ televote | 1997–2008 televote |
|---|---|---|---|
| border | +0.132 [+0.050, +0.215] | +0.210 [+0.125, +0.295] | +0.193 [+0.104, +0.281] |
| diaspora_log | +0.060 [+0.004, +0.116] | +0.236 [+0.162, +0.310] | +0.270 [+0.191, +0.349] |
| shared_official | +0.059 [-0.042, +0.159] | +0.038 [-0.047, +0.124] | +0.001 [-0.097, +0.098] |
| same_family_only | -0.078 [-0.102, -0.054] | -0.098 [-0.142, -0.053] | -0.101 [-0.164, -0.037] |
| same_branch_only | +0.040 [-0.027, +0.108] | +0.029 [-0.034, +0.093] | -0.010 [-0.070, +0.051] |
| same_subbranch | +0.104 [+0.050, +0.157] | +0.200 [+0.083, +0.317] | +0.257 [+0.122, +0.393] |
| taste_sim | +0.061 [+0.020, +0.102] | +0.095 [+0.036, +0.155] | +0.064 [+0.002, +0.125] |
| R² | 0.081 | 0.258 | 0.310 |

- Reference category for language: different families. Betas are comparable within a model (all z-scored).
- Predictors are weakly correlated (max |r| 0.375, max VIF 1.39) — worth one clause.
- same_family_only is negative in all three models (see R5 for the check).
- Our reading: TODO (friendship terms vs taste term; what the negative family-only term could mean —
  note RESULTS.md lists the top different-family pairs, e.g. LV→EE, DE→TR, SE→FI).

## R4. Juries vs televoters

Reports: the jury/televote contrast, drawn from R1–R3 (no new analysis).

- Q: jury 0.309 (z 9.8) vs televote 0.436 (z 23.3).
- R²: jury 0.081 vs televote 0.258.
- Diaspora beta: jury +0.060 vs televote +0.236; same_subbranch +0.104 vs +0.200; border +0.132 vs +0.210.
- Taste beta: jury +0.061 vs televote +0.095 (CIs overlap).
- NMI jury vs televote communities: 0.360 (z 6.8; null 0.092 ± 0.040).
- Our reading: TODO. Careful: overlapping CIs are not a formal test of difference.

## R5. Robustness (Table 1B; leave-one-out; hand ratings)

- Table 1B: one choice changed per row (diaspora observed pairs only, drop 5 strongest pairs, taste without
  top-5 partners, taste from earlier years only, own-song similarity, televote incl. semis, voter-only
  clustering). Pick out which terms keep their sign/CI across rows (read it off Table 1B yourselves).
  Notable rows to look at: taste_sim loses its * in some runs (e.g. jury "taste from earlier years" +0.04;
  televote "taste without top-5 partners" +0.05); own-song similarity is ~0 in jury (+0.01) and 1997–2008 (−0.00).
- Leave one country out: same_family_only stays between −0.123 and −0.066 over 125 refits; CI never includes 0.
- Hand ratings (lyric measure check): raters agree ρ = 0.427; mean rating vs model ρ = 0.271
  (rater 1 0.434, rater 2 0.035); n = 20 pairs, no CI. Already in Methods → only mention here if we use it.
- Our reading: TODO (what holds up, what doesn't).

---

## Not for Results (other sections)

- Introduction: the question (CLAUDE.md), prior work in NOTES.md "Literature" — those "what it found / how we
  use it" lines still need to be filled in from the papers.
- Discussion: limitations are already listed per measure in Table 2 (captures / misses) — refer to it rather than
  repeating.
- Abstract ≤ 250 words, significance ≤ 120 words (PNAS asks 50–120).
