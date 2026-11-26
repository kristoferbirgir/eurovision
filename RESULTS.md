# Results log (facts only, no interpretation)

Every number here is also in `data/key_numbers.json`, written by the script named next to it.
Rerun the script, then update this file if a number changed. Interpretation is the group's job.

## Data checks (`scripts/check_data.py`; key_numbers: `checks`)
- 2023 final, Spijkervet vs EurovisionAPI: 962 of 962 matched votes identical (total, televote, jury); Spijkervet has 988 rows incl. self-votes.
- 2026 final vs Eurovisionworld (transcribed table, raw/checks/): 25 of 25 entries identical; winner BG 516.
- 2026 final vs the official EBU scoreboard (eurovision.com page saved in raw/checks/, parsed by the script): 25 of 25 entries
  identical on total, televote and jury; same 25 entries as Eurovisionworld.
- Winners: 2024 CH 591, 2025 AT 436.
- 2023 semi-finals: 39 of 39 voters give 58 points to 10 entries.
- Shares sum to 1 per voter and round (max deviation 2.22e-16); excess sums to 0 per entry and round (max 5.69e-16).

## Vote network (`scripts/build_edges.py` → `data/edges.csv`, `data/edges_agg.csv`; key_numbers: `edges`)
- 83,526 rows (votes) from 69 contests, 1957–2026 (2020 cancelled), 109 rounds, 53 country codes.
- Rows by vote type: total 54,388; jury 14,503; televote 14,635.

## Borders (`scripts/build_borders.py` → `data/borders.csv`; key_numbers: `borders`)
- 2,756 ordered country pairs; 91 land borders. No data: cs, wld, yu.
- Captures: a shared land border. Misses: sea neighbours and distance.

## Diaspora (`scripts/build_diaspora.py` → `data/diaspora.csv`, key_numbers: `diaspora`)
- 12,048 rows, 1,506 ordered country pairs, UN years 1990–2024. Unmatched: yu, cs, wld.
- 2024 sanity pairs (from ← to = lives in ← born in): DE←TR 1,504,743; ES←RO 522,578; GB←PL 902,193;
  CY←GR 25,031; RU←AM 340,512.
- Captures: the number of people born in country B who live in country A (UN mid-year estimate).
- Misses: people of B descent born in A (second generation), and anyone not counted by the destination's census/registers;
  values are only every 5 years (1990–2020) plus 2024.

## Language (`scripts/build_language.py` → `data/language.csv`, `data/language_groups.csv`; node list `data/glottolog_nodes.csv`; key_numbers: `language`)
- 1,225 unordered pairs with data (50 countries; yu, cs, wld missing).
- Pairs = 1: shared_official 34 (2.8%), same_family 827 (67.5%),
  same_branch 198 (16.2%), same_subbranch 95 (7.8%).
- shared_official uses CLDR "official" only; 10 pairs changed 1 → 0 when de facto official was dropped:
  AU–GB, AU–IE, AU–MT, BE–MA, CH–MA, FR–MA, LU–MA, MA–MC, BY–UA, RU–UA.
- Spot checks (shared_official / family / branch / sub-branch): RS–HR 0/1/1/1, SE–NO 0/1/1/1, ES–PT 0/1/1/1,
  UA–RU 0/1/1/1, CZ–SK 0/1/1/1, PL–RU 0/1/1/0, TR–AZ 0/1/1/1, HU–FI 0/1/1/0, LT–PL 0/1/0/0, IT–RO 0/1/1/0, IL–MT 0/1/1/0.
- shared_official captures: whether two countries share a language CLDR lists as official.
- shared_official misses: mutual intelligibility (sr/hr/bs, sv/no/da are different codes), de facto, regional and second
  languages people actually speak (e.g. Russian in Ukraine).
- same_family captures: whether the primary languages are in the same top-level Glottolog family.
- same_family misses: closeness within a family; Indo-European covers most of Europe.
- same_branch / same_subbranch capture: whether the primary languages fall under the same named Glottolog branch
  (e.g. Slavic) / sub-branch (e.g. South Slavic).
- same_branch / same_subbranch miss: closeness below the sub-branch (Serbian–Slovenian = Serbian–Croatian), the choice of
  nodes is ours, and only each country's primary language is used.

## Null model (`scripts/null_model.py` → `data/null_results.csv`, `data/null_samples.csv`, `data/communities_obs.csv`, `figures/diagnostics/null_modularity.pdf`; key_numbers: `null_model`)
1,000 within-(year, round, vote_type) shuffles per network, the same shuffles for both weightings; Louvain best of 5 seeds.
Main weighting: mean5 = mean excess per pair (both directions pooled), pairs with ≥ 5 votes. sum = summed excess.
The last row is the robustness network (2023–25 televote-only semis added to televote).

| Network | mean5 Q obs | mean5 null mean ± SD | mean5 z | sum Q obs | sum null mean ± SD | sum z |
|---|---|---|---|---|---|---|
| 1957–1974 | 0.433 | 0.285 ± 0.031 | 4.7 | 0.415 | 0.283 ± 0.029 | 4.5 |
| 1975–1996 | 0.370 | 0.268 ± 0.021 | 4.8 | 0.346 | 0.234 ± 0.016 | 6.8 |
| 1997–2008 televote | 0.445 | 0.218 ± 0.012 | 19.5 | 0.450 | 0.198 ± 0.010 | 25.0 |
| 2009–2015 50/50 | 0.413 | 0.207 ± 0.011 | 19.5 | 0.411 | 0.194 ± 0.010 | 21.9 |
| 2016+ jury | 0.309 | 0.204 ± 0.011 | 9.8 | 0.317 | 0.196 ± 0.010 | 12.6 |
| 2016+ televote | 0.436 | 0.203 ± 0.010 | 23.3 | 0.447 | 0.195 ± 0.010 | 25.3 |
| 2016+ televote incl. 2023–25 semis | 0.430 | 0.201 ± 0.010 | 22.1 | 0.448 | 0.194 ± 0.010 | 25.1 |

| Weighting | Network | Nodes | Edges | Communities | Q obs, 20 single runs | p |
|---|---|---|---|---|---|---|
| mean5 | 1957–1974 | 18 | 62 | 4 | 0.426–0.433 | 0.0010 |
| mean5 | 1975–1996 | 28 | 142 | 4 | 0.370–0.370 | 0.0010 |
| mean5 | 1997–2008 televote | 44 | 313 | 5 | 0.428–0.445 | 0.0010 |
| mean5 | 2009–2015 50/50 | 45 | 356 | 4 | 0.402–0.413 | 0.0010 |
| mean5 | 2016+ jury | 44 | 404 | 4 | 0.275–0.309 | 0.0010 |
| mean5 | 2016+ televote | 44 | 333 | 4 | 0.419–0.436 | 0.0010 |
| mean5 | 2016+ televote incl. 2023–25 semis | 44 | 331 | 4 | 0.417–0.438 | 0.0010 |
| sum | 1957–1974 | 21 | 83 | 4 | 0.398–0.415 | 0.0010 |
| sum | 1975–1996 | 35 | 224 | 4 | 0.342–0.346 | 0.0010 |
| sum | 1997–2008 televote | 48 | 381 | 5 | 0.436–0.450 | 0.0010 |
| sum | 2009–2015 50/50 | 47 | 415 | 5 | 0.407–0.411 | 0.0010 |
| sum | 2016+ jury | 45 | 424 | 4 | 0.314–0.319 | 0.0010 |
| sum | 2016+ televote | 45 | 352 | 4 | 0.428–0.447 | 0.0010 |
| sum | 2016+ televote incl. 2023–25 semis | 45 | 347 | 3 | 0.432–0.448 | 0.0010 |

- p = (1 + number of shuffles with Q ≥ observed) / 1,001; 0.0010 means no shuffle reached the observed Q (smallest possible p).
- Observed communities per weighting and network: `data/communities_obs.csv`. Figure: mean5, six main networks.
- Captures: whether the excess-vote network splits into groups of countries that give each other more excess than
  random re-assignment of each voter's own points would produce.
- Misses: why the groups form (friendship, taste or something else); direction (A→B and B→A are pooled); negative
  mean excess (pairs dropped as edges); pairs with < 5 votes (mean5). Louvain finds a good, not necessarily the best,
  partition.

## Lyrics (`scripts/build_lyrics.py` → `data/lyrics.csv`; `scripts/lyrics_similarity.py` → `data/lyrics_similarity*.csv`, `data/lyrics_extremes.csv`, rating key; key_numbers: `lyrics`, `lyrics_similarity`)
- 1830 entries 1956–2026; 1811 with English text (1073 translations, 738 original English); 19 without.
- 1757 songs embedded (1956 and 2020 excluded), 3.05 chunks per song on average (max 9), 0 truncated.
- Vectors are year-centred (song minus the year's mean song vector). 24,902 same-year song pairs:
  centred cosine -0.0341 ± 0.1367 (SD); raw 0.5294 ± 0.1142; Pearson raw vs centred 0.615.
- Most / least similar same-year pairs (centred):
  - most: 1985 AT “Kinder dieser Welt” – LU “Children, Kinder, Enfants”: 0.604 (raw 0.796)
  - most: 2001 NL “Out On My Own” – NO “On My Own”: 0.604 (raw 0.788)
  - most: 2007 NO “Ven A Bailar Conmigo” – PT “Dança Comigo (Vem Ser Feliz)”: 0.565 (raw 0.833)
  - most: 2009 AM “Jan Jan” – MD “Hora din Moldova”: 0.544 (raw 0.737)
  - most: 2009 AM “Jan Jan” – HU “Dance With Me”: 0.541 (raw 0.796)
  - least: 2011 LT “C'est ma vie” – RU “Get You”: -0.492 (raw 0.424)
  - least: 2007 AL “Hear My Plea” – DE “Frauen regier'n die Welt”: -0.484 (raw 0.216)
  - least: 2012 GB “Love Will Set You Free” – RU “Party For Everybody”: -0.474 (raw 0.337)
  - least: 2000 BE “Envie de vivre” – NO “My Heart Goes Boom”: -0.452 (raw 0.314)
  - least: 1964 GB “I Love the Little Things” – YU “Život je sklopio krug”: -0.447 (raw 0.359)
- Captures: how close two songs' English lyrics are in meaning, relative to that year's average song.
- Misses: music, melody, genre, staging and performance; anything lost in translation; the original language itself.

## Taste-profile similarity (`scripts/taste_similarity.py` → `data/taste_similarity_year.csv`, `data/taste_similarity.csv`; key_numbers: `taste_similarity`)
Profiles from one vote type: total (all eras; used for 1997–2008), jury (2016+ jury votes), tele (2016+ televotes).
Per vote (A, B, year):

| Profile | Measure | mean | SD | n |
|---|---|---|---|---|
| total | own_sim | -0.0352 | 0.1367 | 44,827 |
| total | own_sim_raw | 0.5278 | 0.1148 | 44,827 |
| total | taste_sim | 0.0033 | 0.1497 | 45,506 |
| total | taste_sim_no_top5 | 0.0039 | 0.1452 | 45,506 |
| total | taste_sim_past | 0.0018 | 0.1411 | 44,343 |
| total | taste_sim_raw | 0.7194 | 0.0919 | 45,506 |
| jury | own_sim | -0.0265 | 0.1309 | 12,001 |
| jury | own_sim_raw | 0.5386 | 0.1014 | 12,001 |
| jury | taste_sim | 0.0001 | 0.1446 | 12,183 |
| jury | taste_sim_no_top5 | 0.0002 | 0.1399 | 12,183 |
| jury | taste_sim_past | -0.0012 | 0.1374 | 10,736 |
| jury | taste_sim_raw | 0.7255 | 0.0806 | 12,183 |
| tele | own_sim | -0.0265 | 0.1309 | 12,001 |
| tele | own_sim_raw | 0.5386 | 0.1014 | 12,001 |
| tele | taste_sim | -0.0021 | 0.1311 | 12,326 |
| tele | taste_sim_no_top5 | -0.0021 | 0.1278 | 12,326 |
| tele | taste_sim_past | -0.0025 | 0.1272 | 10,843 |
| tele | taste_sim_raw | 0.7256 | 0.0793 | 12,326 |

Pearson correlations (taste vs own: per vote unless marked; main vs variants: per pair × era):

| Profile | taste vs own, raw | taste vs own, centred | taste vs own, centred, pair × era | main vs raw | main vs no top-5 | main vs past only |
|---|---|---|---|---|---|---|
| total | 0.589 | 0.063 | 0.067 | 0.456 | 0.862 | 0.715 |
| jury | 0.573 | 0.002 | -0.022 | 0.336 | 0.807 | 0.718 |
| tele | 0.572 | 0.027 | 0.025 | 0.351 | 0.715 | 0.739 |

- Jury-profile vs televote-profile taste_sim for the same 2016+ vote: Pearson 0.309, Spearman 0.287 (n = 12,183).
- Checks: total, jury and televote profiles (incl. semi-final-only songs, robustness variants) recomputed by brute force
  for several votes match to 6 decimals.
- Captures: how close B's lyrics are to the lyrics A gave points to (with this vote type) in other years, with B's own
  songs left out, relative to each year's average song.
- Misses: music, genre and staging; A's past points also carry A's friendship bias towards countries other than B
  (the no-top-5 variant removes the 5 strongest); the main profile uses later years too (the past-only variant does not);
  jury and televote profiles only have 2016+ votes to learn from.

## Collinearity (`scripts/collinearity.py` → `data/predictor_correlations.csv`, `data/predictor_vif.csv`; key_numbers: `collinearity`)
Pearson correlation of taste_sim with each friendship predictor, pair level (samples as in the regression; taste from
the matching profile). Language as category dummies (reference diff_family).

| Sample | border | diaspora_log | shared_official | same_family_only | same_branch_only | same_subbranch | max VIF (all predictors) |
|---|---|---|---|---|---|---|---|
| jury_2016 | 0.033 | -0.012 | 0.053 | 0.046 | -0.019 | 0.04 | 1.35 |
| tele_1997 | -0.014 | -0.063 | -0.017 | 0.058 | 0.03 | 0.014 | 1.39 |
| tele_2016 | 0.058 | -0.029 | -0.018 | 0.026 | 0.007 | -0.018 | 1.35 |
| tele_2016_semis | 0.054 | -0.021 | -0.026 | 0.026 | 0.011 | -0.02 | 1.35 |

- Largest absolute correlation between any two predictors: jury_2016 border–shared_official 0.370; tele_1997 shared_official–same_subbranch 0.375; tele_2016 border–shared_official 0.370; tele_2016_semis border–shared_official 0.375.

## Hand-rating agreement (`scripts/rating_agreement.py`; key_numbers: `rating_agreement`)
Run 2026-11-26. Rater 1 = Brynja, rater 2 = Kristófer; scale 1–5 (`data/ratings_sheet.md`), rated independently, merged by
`scripts/merge_ratings.py` (40 of 40 whole numbers 1–5). Spearman ρ, n = 20 pairs (no CI or p-value computed):

| | model, year-centred (main) | model, raw |
|---|---|---|
| rater 1 | 0.434 | 0.398 |
| rater 2 | 0.035 | 0.048 |
| mean rating | 0.271 | 0.236 |

- Rater 1 vs rater 2: 0.427.
- Captures: whether two people's sense of lyric similarity ranks pairs like the model. Misses: only 20 pairs, two raters,
  English text (translations for most songs); the pairs were drawn on raw similarity.

## Main model (`scripts/build_pairs.py` → `data/pairs.csv`; `scripts/regression.py` → `data/regression_coefs.csv`, `data/regression_fit.csv`; key_numbers: `pairs`, `regression`)
OLS, one row per directed pair A → B with ≥ 5 votes; outcome = mean signed excess. Language = category of the deepest
Glottolog level the primary languages share (dummies vs reference diff_family). Taste from the matching profile
(jury / televote for 2016+, total for 1997–2008). Outcome and predictors (dummies too) z-scored within each fit
(standardised beta). 95% CIs from SEs clustered two-way by voter and receiver (Cameron, Gelbach & Miller 2011).
Same estimator in all fits: negative eigenvalues of the two-way covariance are set to 0 (Cameron–Gelbach–Miller fix);
FLAG: this changed the covariance in all six two-way 2016+ jury fits (see "SE clustering" rows). The cluster_voter
run uses one-way clustering by voter.

| term | 2016+ jury | 2016+ televote | 1997–2008 televote |
|---|---|---|---|
| border | +0.132 [+0.050, +0.215] | +0.210 [+0.125, +0.295] | +0.193 [+0.104, +0.281] |
| diaspora_log | +0.060 [+0.004, +0.116] | +0.236 [+0.162, +0.310] | +0.270 [+0.191, +0.349] |
| shared_official | +0.059 [-0.042, +0.159] | +0.038 [-0.047, +0.124] | +0.001 [-0.097, +0.098] |
| same_family_only | -0.078 [-0.102, -0.054] | -0.098 [-0.142, -0.053] | -0.101 [-0.164, -0.037] |
| same_branch_only | +0.040 [-0.027, +0.108] | +0.029 [-0.034, +0.093] | -0.010 [-0.070, +0.051] |
| same_subbranch | +0.104 [+0.050, +0.157] | +0.200 [+0.083, +0.317] | +0.257 [+0.122, +0.393] |
| taste_sim | +0.061 [+0.020, +0.102] | +0.095 [+0.036, +0.155] | +0.064 [+0.002, +0.125] |
| n pairs (countries) | 1537 (43) | 1537 (43) | 1257 (39) |
| R² | 0.081 | 0.258 | 0.310 |
| SE clustering | two-way, 2 eigenvalues set to 0 | two-way, 0 eigenvalues set to 0 | two-way, 0 eigenvalues set to 0 |

Robustness (each column changes one thing from main):

**2016+ jury** (beta; * = 95% CI excludes 0)

| term | main | diaspora_observed_only | drop_top5_pairs | taste_no_top5 | taste_past | own_sim | cluster_voter |
|---|---|---|---|---|---|---|---|
| border | +0.132* | +0.144* | +0.116* | +0.134* | +0.132* | +0.133* | +0.132* |
| diaspora_log | +0.060* | +0.034 | +0.057 | +0.059* | +0.058* | +0.058* | +0.060* |
| shared_official | +0.059 | +0.092 | -0.011 | +0.060 | +0.058 | +0.062 | +0.059 |
| same_family_only | -0.078* | -0.091* | -0.075* | -0.076* | -0.073* | -0.073* | -0.078* |
| same_branch_only | +0.040 | -0.024 | +0.046 | +0.042 | +0.041 | +0.041 | +0.040 |
| same_subbranch | +0.104* | +0.104* | +0.097* | +0.106* | +0.108* | +0.107* | +0.104* |
| taste_sim | +0.061* | +0.088* | +0.046* | +0.038* | +0.041 |  | +0.061* |
| own_sim |  |  |  |  |  | +0.013 |  |
| n | 1537 | 1015 | 1529 | 1537 | 1537 | 1537 | 1537 |
| R² | 0.081 | 0.103 | 0.053 | 0.079 | 0.079 | 0.078 | 0.081 |
| SE clustering | two-way (2 eig. → 0) | two-way (1 eig. → 0) | two-way (2 eig. → 0) | two-way (2 eig. → 0) | two-way (1 eig. → 0) | two-way (1 eig. → 0) | voter |

**2016+ televote** (beta; * = 95% CI excludes 0)

| term | main | diaspora_observed_only | drop_top5_pairs | taste_no_top5 | taste_past | own_sim | with_semis | cluster_voter |
|---|---|---|---|---|---|---|---|---|
| border | +0.210* | +0.203* | +0.198* | +0.216* | +0.214* | +0.218* | +0.220* | +0.210* |
| diaspora_log | +0.236* | +0.251* | +0.243* | +0.234* | +0.232* | +0.231* | +0.231* | +0.236* |
| shared_official | +0.038 | +0.025 | +0.000 | +0.036 | +0.038 | +0.036 | +0.049 | +0.038 |
| same_family_only | -0.098* | -0.122* | -0.100* | -0.097* | -0.101* | -0.094* | -0.101* | -0.098* |
| same_branch_only | +0.029 | +0.004 | +0.033 | +0.032 | +0.027 | +0.030 | +0.026 | +0.029 |
| same_subbranch | +0.200* | +0.218* | +0.187* | +0.200* | +0.194* | +0.199* | +0.198* | +0.200* |
| taste_sim | +0.095* | +0.103* | +0.089* | +0.046 | +0.061 |  | +0.090* | +0.095* |
| own_sim |  |  |  |  |  | +0.047* |  |  |
| n | 1537 | 1015 | 1529 | 1537 | 1537 | 1537 | 1574 | 1537 |
| R² | 0.258 | 0.301 | 0.227 | 0.252 | 0.253 | 0.252 | 0.268 | 0.258 |
| SE clustering | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | voter |

**1997–2008 televote** (beta; * = 95% CI excludes 0)

| term | main | diaspora_observed_only | drop_top5_pairs | taste_no_top5 | taste_past | own_sim | cluster_voter |
|---|---|---|---|---|---|---|---|
| border | +0.193* | +0.182* | +0.180* | +0.193* | +0.194* | +0.193* | +0.193* |
| diaspora_log | +0.270* | +0.284* | +0.288* | +0.269* | +0.267* | +0.265* | +0.270* |
| shared_official | +0.001 | -0.011 | -0.030 | +0.001 | +0.001 | -0.000 | +0.001 |
| same_family_only | -0.101* | -0.101* | -0.113* | -0.097* | -0.104* | -0.094* | -0.101* |
| same_branch_only | -0.010 | -0.032 | -0.012 | -0.006 | -0.012 | -0.006 | -0.010 |
| same_subbranch | +0.257* | +0.286* | +0.225* | +0.260* | +0.254* | +0.262* | +0.257* |
| taste_sim | +0.064* | +0.056 | +0.067* | +0.045 | +0.069* |  | +0.064* |
| own_sim |  |  |  |  |  | -0.001 |  |
| n | 1257 | 846 | 1248 | 1257 | 1257 | 1257 | 1257 |
| R² | 0.310 | 0.356 | 0.280 | 0.308 | 0.311 | 0.306 | 0.310 |
| SE clustering | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | two-way (0 eig. → 0) | voter |

- Captures: how mean excess A → B changes with each pair property, holding the others fixed, within one era and vote type.
- Misses: causal direction; anything not in the model (running order, staging, music, politics); pairs with < 5 votes;
  the 2009–2015 era and pre-1997 eras (no diaspora data before 1990); pair dependence beyond the two-way clustering.

## Leave-one-country-out: same_family_only (`scripts/leave_one_out.py` → `data/leave_one_out_family.csv`, `data/diff_family_top_pairs.csv`; key_numbers: `leave_one_out`)
All models: β from -0.123 to -0.066 over 125 refits; 95% CI includes 0 in 0.

**1997–2008 televote**: full-sample β -0.101; leaving out one of 39 countries gives β from -0.123 to -0.082; 95% CI includes 0 in 0 fits; eigenvalue fix changed 0 fits.

| left out | β | 95% CI | change vs full | eigenvalues set to 0 |
|---|---|---|---|---|
| AM | -0.123 | [-0.183, -0.062] | -0.022 | 0 |
| MT | -0.082 | [-0.144, -0.019] | +0.019 | 0 |
| DK | -0.084 | [-0.146, -0.022] | +0.017 | 0 |
| HU | -0.114 | [-0.179, -0.050] | -0.014 | 0 |
| FR | -0.087 | [-0.151, -0.024] | +0.013 | 0 |

Top 10 diff_family pairs by mean excess:

| from → to | mean excess | votes |
|---|---|---|
| LV → EE | 0.1207 | 8 |
| DE → TR | 0.1206 | 14 |
| SE → FI | 0.1176 | 9 |
| FR → TR | 0.1053 | 15 |
| EE → LV | 0.1042 | 11 |
| FR → IL | 0.1029 | 11 |
| AL → TR | 0.0977 | 8 |
| NL → TR | 0.0913 | 13 |
| EE → RU | 0.0878 | 12 |
| TR → BA | 0.0859 | 12 |

**2016+ jury**: full-sample β -0.078; leaving out one of 43 countries gives β from -0.087 to -0.066; 95% CI includes 0 in 0 fits; eigenvalue fix changed 43 fits.

| left out | β | 95% CI | change vs full | eigenvalues set to 0 |
|---|---|---|---|---|
| RU | -0.066 | [-0.093, -0.039] | +0.012 | 2 |
| IT | -0.068 | [-0.098, -0.039] | +0.009 | 1 |
| AM | -0.087 | [-0.112, -0.062] | -0.009 | 1 |
| PT | -0.087 | [-0.108, -0.066] | -0.009 | 2 |
| SE | -0.069 | [-0.091, -0.046] | +0.009 | 1 |

Top 10 diff_family pairs by mean excess:

| from → to | mean excess | votes |
|---|---|---|
| AZ → RU | 0.1323 | 6 |
| HR → HU | 0.0883 | 5 |
| AZ → AL | 0.0879 | 10 |
| BG → MT | 0.0867 | 5 |
| RU → AZ | 0.0850 | 6 |
| HU → DK | 0.0813 | 5 |
| GR → AZ | 0.0744 | 8 |
| MT → IT | 0.0736 | 10 |
| FI → SE | 0.0699 | 13 |
| AZ → UA | 0.0645 | 11 |

**2016+ televote**: full-sample β -0.098; leaving out one of 43 countries gives β from -0.114 to -0.090; 95% CI includes 0 in 0 fits; eigenvalue fix changed 0 fits.

| left out | β | 95% CI | change vs full | eigenvalues set to 0 |
|---|---|---|---|---|
| AL | -0.114 | [-0.156, -0.071] | -0.016 | 0 |
| AM | -0.111 | [-0.156, -0.066] | -0.014 | 0 |
| PL | -0.107 | [-0.152, -0.063] | -0.010 | 0 |
| DK | -0.090 | [-0.136, -0.044] | +0.008 | 0 |
| GR | -0.105 | [-0.148, -0.061] | -0.007 | 0 |

Top 10 diff_family pairs by mean excess:

| from → to | mean excess | votes |
|---|---|---|
| GE → AM | 0.1622 | 7 |
| RS → HU | 0.1462 | 6 |
| LV → EE | 0.1318 | 7 |
| MT → IT | 0.1085 | 10 |
| SE → FI | 0.1025 | 11 |
| LT → EE | 0.1004 | 9 |
| MD → AZ | 0.0914 | 8 |
| RU → AZ | 0.0898 | 6 |
| GE → AZ | 0.0880 | 7 |
| AZ → IL | 0.0843 | 12 |

## Region (`scripts/build_region.py` → `data/region.csv`; key_numbers: `region`)
- 52 countries, 7 UN M49 sub-regions from CLDR 49 territoryContainment; missing: wld.
- Countries per region: Australia and New Zealand 1; Eastern Europe 10; Northern Africa 1; Northern Europe 10; Southern Europe 16; Western Asia 6; Western Europe 8. yu, cs: Southern Europe (CLDR deprecated entries).
- Captures: the UN statistical sub-region of each country.
- Misses: borders inside a region and closeness across region lines (e.g. CY is Western Asia, not with GR); one-country regions (AU, MA).

## NMI (`scripts/nmi.py` → `data/nmi.csv`; key_numbers: `nmi`)
sklearn normalized_mutual_info_score (arithmetic mean); null: second labelling permuted over the same countries, 1,000 times. Communities: mean5, from data/communities_obs.csv.

| Partition A | Partition B | Countries | Groups A / B | NMI obs | null mean ± SD | z | p |
|---|---|---|---|---|---|---|---|
| 2016+ jury communities | 2016+ televote communities | 44 | 4 / 4 | 0.360 | 0.092 ± 0.040 | 6.8 | 0.0010 |
| 1957–1974 communities | language branch | 17 | 4 / 3 | 0.346 | 0.194 ± 0.088 | 1.7 | 0.0689 |
| 1957–1974 communities | language subbranch | 17 | 4 / 4 | 0.595 | 0.255 ± 0.082 | 4.2 | 0.0020 |
| 1975–1996 communities | language branch | 27 | 4 / 7 | 0.467 | 0.248 ± 0.054 | 4.0 | 0.0020 |
| 1975–1996 communities | language subbranch | 27 | 4 / 10 | 0.484 | 0.311 ± 0.053 | 3.3 | 0.0020 |
| 1997–2008 televote communities | language branch | 43 | 5 / 11 | 0.510 | 0.262 ± 0.036 | 6.9 | 0.0010 |
| 1997–2008 televote communities | language subbranch | 43 | 5 / 17 | 0.609 | 0.352 ± 0.033 | 7.7 | 0.0010 |
| 2009–2015 50/50 communities | language branch | 45 | 4 / 11 | 0.436 | 0.221 ± 0.034 | 6.4 | 0.0010 |
| 2009–2015 50/50 communities | language subbranch | 45 | 4 / 17 | 0.565 | 0.295 ± 0.034 | 7.9 | 0.0010 |
| 2016+ jury communities | language branch | 44 | 4 / 11 | 0.417 | 0.222 ± 0.036 | 5.3 | 0.0010 |
| 2016+ jury communities | language subbranch | 44 | 4 / 17 | 0.524 | 0.300 ± 0.033 | 6.8 | 0.0010 |
| 2016+ televote communities | language branch | 44 | 4 / 11 | 0.395 | 0.217 ± 0.036 | 5.0 | 0.0010 |
| 2016+ televote communities | language subbranch | 44 | 4 / 17 | 0.500 | 0.294 ± 0.033 | 6.2 | 0.0010 |

- p = (1 + shuffles with NMI ≥ observed) / 1,001.
- Captures: how much knowing a country's community in one partition tells about its group in another (0 = nothing, 1 = same partition).
- Misses: which groups match; NMI rises with the number of groups (the shuffle null keeps group sizes, so z is the fairer comparison); one Louvain partition per network.

## Attribute assortativity (`scripts/assortativity.py` → `data/assortativity.csv`; key_numbers: `assortativity`)
networkx attribute_assortativity_coefficient on the unweighted mean5 positive-excess networks; null: 1,000 vote shuffles per network (null_model.py procedure, own draws). Language: yu, cs left out.

| Network | Attribute | Nodes | Edges | r obs | null mean ± SD | z | p |
|---|---|---|---|---|---|---|---|
| 1957–1974 | language_branch | 17 | 54 | 0.123 | -0.064 ± 0.075 | 2.5 | 0.0110 |
| 1957–1974 | region | 18 | 62 | 0.185 | -0.066 ± 0.062 | 4.0 | 0.0010 |
| 1975–1996 | language_branch | 27 | 134 | 0.099 | -0.027 ± 0.030 | 4.2 | 0.0010 |
| 1975–1996 | region | 28 | 142 | 0.087 | -0.029 ± 0.033 | 3.5 | 0.0010 |
| 1997–2008 televote | language_branch | 43 | 297 | 0.080 | -0.016 ± 0.015 | 6.3 | 0.0010 |
| 1997–2008 televote | region | 44 | 313 | 0.151 | -0.021 ± 0.018 | 9.5 | 0.0010 |
| 2009–2015 50/50 | language_branch | 45 | 356 | 0.089 | -0.025 ± 0.015 | 7.8 | 0.0010 |
| 2009–2015 50/50 | region | 45 | 356 | 0.123 | -0.031 ± 0.017 | 8.9 | 0.0010 |
| 2016+ jury | language_branch | 44 | 404 | 0.060 | -0.027 ± 0.014 | 6.1 | 0.0010 |
| 2016+ jury | region | 44 | 404 | 0.098 | -0.023 ± 0.017 | 7.3 | 0.0010 |
| 2016+ televote | language_branch | 44 | 333 | 0.107 | -0.027 ± 0.015 | 9.0 | 0.0010 |
| 2016+ televote | region | 44 | 333 | 0.148 | -0.023 ± 0.017 | 10.1 | 0.0010 |

- Captures: whether positive-excess edges join countries with the same language branch / region more often than the edge ends' label mix would give.
- Misses: edge weights (the networkx function ignores them); direction; negative excess; closeness between labels (Slavic–Baltic counts as different as Slavic–Semitic).

## Disparity-filter backbone (`scripts/backbone.py` → `data/backbone_edges.csv`; key_numbers: `backbone`)
Serrano et al. 2009, implemented in backbone.py; mean5 networks; edge kept if alpha < 0.05 from at least one end (degree-1 ends not tested). Check: toy graph asserted; other alphas below.

| Network | Nodes | Edges | Backbone edges (α 0.05) | Kept | Nodes with a backbone edge | α 0.01 | α 0.10 | Within community: all / backbone |
|---|---|---|---|---|---|---|---|---|
| 2016+ jury | 44 | 404 | 23 | 5.7% | 33 | 8 | 52 | 42.8% / 78.3% |
| 2016+ televote | 44 | 333 | 29 | 8.7% | 38 | 6 | 60 | 50.4% / 93.1% |

- Captures: for each country, the partners that get a larger share of its positive excess than an even split over its partners would give.
- Misses: negative excess; direction (pooled pairs); the threshold α is a choice; edges of degree-1 countries are only tested from the other end.

## Figures (`scripts/make_figures.py` → `figures/fig1_modularity.pdf`, `figures/fig2_coefficients.pdf`, `figures/fig3_communities.pdf`; captions `figures/captions.md`)
- Fig 1: observed modularity vs the shuffle null (mean5), six networks; numbers as in the Null model table.
- Fig 2: main-model betas with 95% CIs for 2016+ jury, 2016+ televote, 1997–2008 televote; numbers as in the Main model table.
- Robustness table: `paper/table_robustness.tex` / `.md` (`scripts/make_table_robustness.py`).
- Fig 3 (two-column): 2016+ jury and televote Louvain communities (mean5), 44 countries and 4 communities each, shared layout;
  edges = disparity-filter backbone (α = 0.05): 23 of 404 jury edges, 29 of 333 televote edges (see Disparity-filter backbone).
