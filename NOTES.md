# Notes: data log and decisions (→ Methods section)

## Data
- 2026-11-11: Votes 1957–2023 from the Spijkervet release. 1956 has no vote data, and 2020 was cancelled.
- 2026-11-11: Votes 2024–2026 from EurovisionAPI/dataset (commit e564111, 26 Oct 2026), converted by scripts/convert_eurovisionapi.py.
  Validated: the 2023 final is identical in both sources (962/962 votes, total/tele/jury).
  Winners reconstruct for 2024 (CH 591) and 2025 (AT 436).
- 2026-11-16: 2026 final checked against the Eurovisionworld results table
  (https://eurovisionworld.com/esc/bulgaria-wins-the-eurovision-song-contest-2026, article 17 May 2026).
  All 25 entries match data/edges.csv on total, televote and jury points (0 mismatches). Top 10:
  BG 516 (312/204), IL 343, RO 296, AU 287, IT 281, FI 279, DK 243, MD 226, UA 221, GR 220.
  The official eurovision.tv results page returned HTTP 403 to automated fetch, so it was not used.
  Caveat: Eurovisionworld is likely the upstream of both Spijkervet (scraped from it) and EurovisionAPI,
  so this check validates our conversion, not the source data itself.
  2026-11-25: also checked against the official EBU scoreboard (eurovision.com Grand Final page, saved in raw/checks/,
  parsed by check_data.py): 25 of 25 entries identical on total, televote ("Audience") and jury. This is the
  independent check the caveat above asked for; eurovision.tv still returns HTTP 403.
- 2026-11-11: Borders from geodatasource/country-borders (CC BY-SA 4.0). Land borders only. yu/cs/wld = NaN.
- 2026-11-16: Diaspora from UN DESA International Migrant Stock 2024 (destination x origin, CC BY 3.0 IGO),
  downloaded by hand in a browser (automated fetch got HTTP 403). Built by scripts/build_diaspora.py.
  Sheet "Table 1", both sexes only, years 1990, 1995, ..., 2020, 2024 (5-year steps + 2024).
  from = destination (where migrants live, the voter), to = origin (country of birth, the receiver).
  share_of_migrants = migrants / the destination's total migrant stock (origin "World", M49 900).
  M49 -> ISO3 via pycountry (ISO 3166-1 numeric = M49 for countries). Unmatched: yu, cs, wld (no current ISO code).
  Counts are by country of BIRTH: children of migrants born in the destination are not included.
  Pairs the UN does not list are left out of diaspora.csv (not written as 0).
  2024 check: DE<-TR 1,504,743; ES<-RO 522,578; GB<-PL 902,193; CY<-GR 25,031; RU<-AM 340,512.
  DECIDED 2026-11-16 (group): pairs missing from UN DESA count as 0 in the main analysis; robustness check reruns on
  observed pairs only. Diaspora analysis covers 1997+ (televote era); each vote year uses the nearest UN year.
  TODO (group): add a second check, e.g. compare 2-3 pairs against a national statistics office figure.
- 2026-11-16: Language layer from Unicode CLDR 49 (official languages) + Glottolog 5.4 (classification tree), built by
  scripts/build_language.py -> data/language.csv (all ordered pairs, symmetric) and data/language_groups.csv (per country).
  shared_official = the two countries share a language with CLDR officialStatus "official".
  DECIDED 2026-11-16 (group): de_facto_official and official_regional do NOT count for shared_official.
  This changed 10 pairs from 1 to 0: AU–GB, AU–IE, AU–MT (en is de facto in AU), BE–MA, CH–MA, FR–MA, LU–MA, MA–MC
  (fr is de facto in MA), BY–UA, RU–UA (ru is de facto in UA). shared_official: 44 -> 34 of 1225 pairs.
  Primary language = the official or de facto official language with the largest CLDR populationPercent (de facto is
  kept here because AU has no "official" language). Script variants merged (sr_Latn -> sr). BY primary = ru, LU = fr.
  same_family / same_branch / same_subbranch compare primary languages on the Glottolog classification path
  (values.csv, parameter "classification"). family = root of the path.
  DECIDED 2026-11-16 (group): branch and sub-branch come from a named list of Glottolog nodes, data/glottolog_nodes.csv
  (glottocodes looked up in Glottolog 5.4 languages.csv; cite glottolog54). A country's branch / sub-branch = the listed
  node on its primary language's path. Branches: Germanic, Romance, Slavic, Baltic, Celtic, Hellenic, Albanian, Armenian,
  Indo-Iranian, Uralic, Turkic, Semitic, Kartvelian. Sub-branches: West/North Germanic, Italo-Western/Eastern Romance,
  South/East/West Slavic, Finnic, Hungaric, Oghuz, Northwest Semitic, Arabian, Modern Greek, Georgian-Zan.
  Glottolog has no "Baltic" node: "Baltic" = Eastern Baltic (east2280), which holds lt and lv.
  Where no sub-branch is listed (Albanian, Armenian, Baltic) the sub-branch = the branch.
  Uralic, Turkic, Kartvelian are families in Glottolog and also used as branches (so e.g. HU–FI same_branch = 1).
  Celtic and Indo-Iranian are listed but no primary language falls in them.
  (Replaces the earlier sample-split rule, which separated TR/AZ and not South/East/West Slavic.)
  ISO 639-1 -> 639-3 via pycountry. Glottolog lacks macrolanguage codes (ara, aze, est): mapped via CLDR macrolanguage
  aliases to arb, azj, ekk. sr/hr/bs are different ISO codes, so RS–HR shared_official = 0.
  yu, cs, wld: no CLDR territory -> NaN.
- 2026-11-16: Shuffle null for community structure, scripts/null_model.py (see its docstring).
  Networks: one per era on vote_type "total"; 2016+ split into jury and televote (6 main networks).
  Undirected pair A–B pools all A->B and B->A votes in the era. wld is not a node (it only votes).
  DECIDED 2026-11-16 (group): main edge weight = mean excess over the pair's votes, pairs with < 5 votes dropped
  ("mean5"). The earlier weight, summed excess ("sum", no minimum), is kept side by side. Only weights > 0 are edges.
  mean5 drops countries without any pair of >= 5 votes (e.g. 1957–74: 18 of 21 nodes).
  (Bug in the first version, fixed: see Fixes.)
  All rounds (finals and semi-finals) count.
  DECIDED 2026-11-16 (group): the 2023–2025 semi-finals were televote-only and exist only as "total" in our data; they
  are left out of the 2016+ jury and televote networks. Robustness network "2016+ televote incl. 2023–25 semis"
  relabels the total of every 2016+ round without a televote split as televote.
  The 2023 semi-finals (also televote-only, total only) were added 2026-11-16, see Fixes; they are in the robustness
  network too ("2016+ televote incl. 2023–25 semis").
  Null: within each (year, round, vote_type), each voter's points are permuted over the entries it rated; excess is
  recomputed. 1,000 shuffles, numpy seed 2805, same shuffles for both weightings. Check in the script: recomputed
  excess equals build_edges.py excess.
  Louvain (networkx 3.7, resolution 1): best modularity of 5 seeded runs, same for observed and every null network.
  Stability check: observed Q over 20 single runs, min–max in data/null_results.csv (q_obs_min20, q_obs_max20).
- 2026-11-16: Lyrics from EurovisionAPI (same commit e564111): contestant.json for all entries 1956–2026, every
  original lyrics file (o_*.txt) and the English translation (t_english.txt); other translations not copied.
  scripts/build_lyrics.py -> data/lyrics.csv: one English text per entry = t_english.txt if present, else the original
  if it is English only. 1830 entries: 1073 translation, 738 original English,
  19 without English text (mixed-language originals without translation, imaginary language,
  Montenegrin, ...; listed by the script) and left out.
  Cleaning: 7 English texts contain scraped ad HTML (google-auto-placed div/ins/iframe), removed with
  contents; other tags (<i>, <span>, <b>) removed, text kept; HTML entities decoded. Raw files unchanged.
  scripts/lyrics_similarity.py: model sentence-transformers/paraphrase-multilingual-mpnet-base-v2, revision
  4328cf26 (apache-2.0), CPU. The model reads <= 128 tokens: lines longer than 60 words are cut into 60-word pieces
  (some files have no line breaks), consecutive lines are packed into chunks <= 128 tokens, each chunk embedded,
  song vector = normalised mean of chunk vectors. Truncated chunks after this: 0.
  Excluded years: 1956 (two songs per country, no vote data) and 2020 (cancelled). 1757 songs embedded.
  similarity(A, B, year) = cosine of the two songs in that year; per era = mean over the years both had a song
  (n_years in data/lyrics_similarity.csv). A voter's own song is used even if it did not reach the final.
  Validation: data/lyrics_extremes.csv (5 most / 5 least similar same-year pairs); data/lyrics_rating_sheet.csv has
  20 pairs, 4 drawn at random from each similarity quintile so the sheet covers the full range (seed 2805), without the
  model score; the score is in data/lyrics_rating_key.csv.
  TODO (group): agree a rating scale before rating (suggestion: 1–5, "how similar are the two lyrics in topic and
  mood?"), rate independently, then report inter-rater agreement and Spearman rho between mean rating and model score.
- 2026-11-16: Taste-profile similarity, scripts/taste_similarity.py -> data/taste_similarity_year.csv, data/taste_similarity.csv.
  DECIDED 2026-11-16 (group): main lyric measure = taste_sim(A, B, t) = cosine(A's taste profile, B's song in year t).
  Taste profile = sum over every song A voted on in all years except t, leaving out all songs from B, of
  share(A -> song) x song vector. Share (points / voter's points in that round) instead of raw points so that eras with
  different point scales weigh the same; votes from vote_type "total", all rounds (semi + final both count).
  The profile uses later years too ("all other years"). The old measure (A's own song vs B's song in t) is kept as own_sim.
  Check: three profiles recomputed by brute force (loop over votes) match the vectorised result to 6 decimals.
  taste_sim vs own_sim: Pearson 0.589 / Spearman 0.563 per vote (n = 44,809);
  Pearson 0.605 / Spearman 0.593 per pair x era (n = 7,547).
- 2026-11-16: Hand-rating agreement: scripts/rating_agreement.py (Spearman rater1–rater2, each rater–model, mean–model).
  Run 2026-11-26: rater 1 = Brynja (data/ratings_rater1.csv), rater 2 = Kristófer (data/ratings_rater2.csv), merged into
  data/lyrics_rating_sheet.csv by scripts/merge_ratings.py. Numbers in RESULTS.md / key_numbers "rating_agreement".
- 2026-11-16: DECIDED (group): year-centred embeddings for every lyric cosine. lyrics_similarity.py stores raw (emb) and
  centred (emb_c) vectors: centred = song vector minus the mean vector of all embedded songs of that year, re-normalised.
  own_sim and taste_sim use centred vectors; *_raw columns keep the uncentred values for comparison.
  Same-year song pairs: raw 0.5294 ± 0.1142 -> centred -0.0341 ± 0.1367
  (Pearson raw vs centred 0.615). Per vote: taste_sim raw 0.7194 ± 0.0919 -> centred
  0.0033 ± 0.1497. taste vs own correlation: raw Pearson 0.589 -> centred 0.063 per vote;
  raw 0.605 -> centred 0.067 per pair x era.
  The rating sheet is no longer rewritten by lyrics_similarity.py (it holds the ratings); its 20 pairs were drawn on the
  raw similarity; the key now has both raw and centred scores.
- 2026-11-16: DECIDED (group): taste robustness profiles. (a) taste_sim_no_top5: also leaves out all songs of A's 5
  strongest excess partners in the era of t (highest mean signed excess A->p, vote_type total, >= 5 votes; B itself is
  always left out). (b) taste_sim_past: profile from years before t only (still without B); NaN in A's first year.
  Check: main, (a) and (b) recomputed by brute force for 4 votes (incl. wld) match to 6 decimals.
- 2026-11-16: Pair table for step 6, scripts/build_pairs.py -> data/pairs.csv. One row per directed pair A->B per sample;
  outcome and every predictor are averaged over the same votes. Samples: 2016+ jury, 2016+ televote, 2016+ televote incl.
  the 2023–25 televote-only semis (robustness), 1997–2008 (vote_type total). Pairs with >= 5 votes (as mean5 in the null
  model). wld, yu, cs dropped. Diaspora per vote: UN year nearest to the vote year (ties, e.g. 2022, go to the earlier
  UN year); diaspora_log = log(1 + migrants), missing pair = 0; diaspora_observed = share of votes where the UN lists the
  pair. taste_sim per vote comes from the matching profile (jury / televote 2016+, total for 1997–2008).
- 2026-11-16: Collinearity, scripts/collinearity.py -> data/predictor_correlations.csv, data/predictor_vif.csv.
- 2026-11-16: Regression, scripts/regression.py -> data/regression_coefs.csv, data/regression_fit.csv. OLS of
  excess_mean on border, diaspora_log, shared_official, same_family, same_branch, same_subbranch, taste_sim; outcome and
  predictors z-scored within each fit (standardised betas); 95% CIs from SEs clustered two-way by voter and receiver
  (statsmodels 0.15, cov_type "cluster" with two group columns). The intercept's two-way clustered variance can come out
  negative (not positive definite); it is not reported, the script asserts every reported SE is finite.
  Robustness specs: diaspora_observed_only (pairs with diaspora_observed = 1), drop_top5_pairs (5 unordered pairs with the
  highest mean excess over both directions), taste_no_top5, taste_past, own_sim instead of taste_sim, with_semis (televote).
  TODO (group): cite a reference for two-way clustered SEs if the paper names the method (open the source first).
- 2026-11-16: CONFIRMED (group): regression decisions 1 (>= 5 votes per pair) and 2 (diaspora_log = log(1 + migrants),
  nearest UN year, ties to the earlier year).
- 2026-11-16: DECIDED (group): language enters the regression as one categorical variable, the deepest Glottolog level
  the two primary languages share: diff_family (reference) / same_family_only / same_branch_only / same_subbranch
  (pairs.csv column lang_cat; dummies built in regression.py and collinearity.py). shared_official stays separate.
- 2026-11-16: DECIDED (group): 2016+ taste profiles per vote type: jury profile from jury votes only, televote profile
  from televotes only (both 2016+ only); 1997–2008 keeps the total-vote profile. taste_similarity.py now scores any
  (year, A, B) target, so semi-final-only songs (incl. the 2023–25 televote-only semis) get a televote profile value.
  Top-5 partners for the no-top-5 variant come from all votes of that vote type (also votes on songs without lyrics).
  Checks: the total profile reproduces the previous version to 1e-15; jury and televote profiles recomputed by brute
  force for 4 votes (2 semi-final-only) match to 6 decimals. Jury vs televote taste_sim for the same vote: Pearson
  0.309. taste vs own (centred, per vote): jury 0.002, televote 0.027.
- 2026-11-16: Figures, scripts/make_figures.py -> figures/fig1_modularity.pdf, fig2_coefficients.pdf, fig3_communities.pdf
  (+ PNG previews), captions in figures/captions.md. Fig 1–2: 3.42 in (PNAS single column, 8.7 cm); Fig 3: 7.0 in
  (two columns, 17.8 cm), country labels 6 pt; Arial; PDF fonttype 42.
  Colours: validated categorical palette (blue #2a78d6, orange #eb6834, aqua #1baf7a, yellow #eda100, magenta #e87ba4);
  validator: CVD and normal-vision checks pass, contrast warning for 3 colours on white, so every colour has its own
  marker shape and a legend or label. Fig 1 uses the mean5 weighting; grey bar = 2.5–97.5 percentile of the null.
  Fig 3: shared spring layout (networkx, seed 2805) on the union of the 2016+ jury and televote mean5 graphs; televote
  communities matched to jury communities by Jaccard overlap (scipy linear_sum_assignment); only within-community edges drawn.
- 2026-11-16: DECIDED (group): Fig 3 at two-column width (17.8 cm), labels >= 6 pt; the null-model histogram is a
  diagnostic (figures/diagnostics/null_modularity.pdf), not a paper figure.
- 2026-11-16: Leave-one-country-out check of same_family_only, scripts/leave_one_out.py -> data/leave_one_out_family.csv,
  data/diff_family_top_pairs.csv. regression.py was refactored (load_pairs, fit, main) so the check uses the same model
  code; its output is byte-identical after the refactor. In the 2016+ jury model, leaving out il or pt makes the two-way
  clustered variance of same_family_only negative (not positive definite); those two CIs are recorded as missing.
- 2026-11-16: Data checks scripted, scripts/check_data.py -> key_numbers "checks" (2023 sources, 2026 scoreboard, 2024/2025
  winners, 2023 semis, shares, excess sums). The 2026 scoreboard is a TRANSCRIPTION of the Eurovisionworld table read on
  2026-11-16, stored as raw/checks/eurovisionworld_2026_final.csv with a MANIFEST entry saying so.
  build_edges.py and build_borders.py now record their counts; taste_similarity.py records a brute-force check of 20
  random votes per profile; collinearity.py records max VIF and maxima over all samples; null_model.py records the
  largest spread of observed Q over 20 single Louvain runs (rerun: results equal to 2e-14, same partitions).
- 2026-11-16: Methods draft: paper/methods_template.md -> scripts/write_methods.py -> paper/methods.md. Every result number
  is a placeholder filled from data/key_numbers.json; the script stops on a missing key and lists the literal numbers
  left in the template (dates, versions, parameters). Edit the template, never methods.md.
- 2026-11-16: SUPERSEDED (see the eigenvalue-fix entry above): if the two-way clustered covariance of the reported coefficients is not positive
  semi-definite (a negative eigenvalue), the fit falls back to one-way clustering by voter (column "cluster" in
  data/regression_coefs.csv). Result: all six 2016+ jury fits use voter clustering; all televote and 1997–2008 fits stay
  two-way; 41 of 43 jury leave-one-out refits fall back. The check uses the reported coefficients only (the intercept,
  ~0 after z-scoring and not reported, is excluded). Reference: cameron2011multiway (verified via Crossref).
- 2026-11-16: DECIDED (group): Methods trimmed to about one PNAS page (paper/methods_template.md, ~650 words). The longer
  draft is kept in paper/methods_template_long.md (not used by scripts). Cut: per-source licences and counts, extra data
  checks (winners, 2023 semis, shares/excess sums, upstream caveat), network sizes, seeds and versions, diaspora/language
  details, chunking details, all captures/misses sentences (still in RESULTS.md), the robustness list (now
  paper/table_robustness.tex) and the software paragraph.
- 2026-11-16: Overleaf setup. paper/main.tex follows pnas-new.cls v1.44 (2018/05/06; structure checked against the copy in
  rstudio/rticles): \matmethods{\input{methods}} + \showmatmethods{}, \acknow + \showacknow{}, TODO for title, authors,
  significance, abstract, introduction, results, discussion, acknowledgements. scripts/write_paper.py (was
  write_methods.py) writes paper/methods.md, methods.tex and figure_floats.tex (captions from figures/captions.md);
  scripts/make_table_robustness.py writes paper/table_robustness.tex/.md; scripts/pack_overleaf.py copies everything into
  paper/overleaf/ (git-ignored) for upload. Test compile of the generated LaTeX in a plain article wrapper: 0 errors,
  0 undefined references or citations (the PNAS class itself could not be compiled locally: BasicTeX lacks lettrine.sty).
  references.bib: removed a file path with underscores from the undesa note (broke BibTeX/LaTeX).
- 2026-11-16: DECIDED (group): replaces the one-way fallback. All regression fits use two-way clustered SEs with the
  Cameron–Gelbach–Miller (2011) eigenvalue fix: V = U diag(lambda) U', negative eigenvalues set to zero (full covariance
  incl. intercept), CIs with the normal critical value (as statsmodels). The fix changed 6 of 19 two-way fits (all 2016+
  jury; 1–2 eigenvalues each); televote and 1997–2008 fits are unchanged. New robustness run cluster_voter: one-way
  clustering by voter. Leave-one-out refits use the same estimator. 2016+ jury same_family_only CI: [−0.102, −0.054]
  (raw two-way [−0.093, −0.063], voter-only [−0.117, −0.038]).
- 2026-11-16: DECIDED (group): captures/misses sentences back as paper/table_measures.tex (+ .md), one line each, drawn
  from RESULTS.md; hand-written (no numbers); \input in main.tex next to Methods.
- 2026-11-26: Course PNAS template (zip from the teacher, downloaded from Overleaf as Social_Graphs_Report/) has
  pnas-new.cls v1.47 (2025/11/01), pnas-new.bst, pnasresearcharticle.sty v1.3, jabbrv.sty + two .ldf, PNAS_Logo.pdf.
  These are kept unchanged in paper/pnas_template/; pack_overleaf.py copies them next to our files and writes
  paper/overleaf.zip. Checked: v1.47 defines \matmethods, \showmatmethods, \acknow, \showacknow, so main.tex is
  unchanged apart from its header comment. The downloaded folder matched the pack output except methods.tex (older,
  before the rating results). Not compiled locally (no LaTeX installed).
- 2026-11-26: The 2025 class sets page 1 as one wide text column plus a narrow column (Significance box, author
  details). main.tex now follows the official 2025 PNAS Overleaf template (Research_report.tex): \Firstpage after the
  abstract, \Endparasplit where page 1 ends (\Parasplit mid-paragraph), \dataavail for the availability statement.
  Without these the right column of page 1 ran off the page. Watermark off via \setboolean{displaywatermark}{false}
  in main.tex (class file unchanged). Overleaf compile 2026-11-26: 4 pages, no overflow.

## Decisions
- Excess = vote share minus the leave-one-out mean share the entry got from the other voters in the same round and vote type (see build_edges.py).
- Eras: 1957–74, 1975–96, 1997–2008 televote, 2009–15 50/50, 2016+ split jury/tele.
- Voting-rule changes to keep in mind: semi-finals were televote-only in 2023–2025, juries returned to semis in 2026; Rest of the World (wld) televote from 2023; NL disqualified from the 2024 final.
- TODO: decide how to treat yu / cs (drop? map to successors?).
- 2026-11-16 (group): the paper answers one question: is excess voting explained by friendship (borders, diaspora,
  language) or taste (song similarity), and do juries and televoters differ? Everything built must serve it.
- 2026-11-16 (group): diaspora missing pairs = 0 (robustness: observed pairs only); diaspora analysis 1997+, nearest UN year.
- 2026-11-16 (group): language layer = shared official language (0/1) + same language family (0/1), simplest defensible source.
- 2026-11-16 (group): add same_branch and same_subbranch from the Glottolog tree; shared_official uses CLDR "official" only.
- 2026-11-16 (group): branch / sub-branch from a named list of Glottolog nodes (data/glottolog_nodes.csv).
- 2026-11-16 (group): null model edge weight = mean excess, min 5 votes per pair; sum kept side by side.
- 2026-11-16 (group): 2024–25 televote-only semis out of the 2016+ networks; robustness run includes them in televote.
- 2026-11-16 (group): step 6 regression uses the full signed excess (not only positive).
- 2026-11-16 (group): year-centred lyric embeddings for all cosine similarities; taste robustness: no top-5 partners, past only.
- 2026-11-25 (Kristófer, course methods weeks 3–4): NMI (sklearn, arithmetic mean) of communities vs
  communities / language branch / sub-branch against 1,000 label permutations; attribute assortativity (networkx,
  unweighted) of the mean5 positive-excess networks by language branch and by UN M49 sub-region against 1,000 vote
  shuffles (null_model.py procedure); disparity-filter backbone of 2016+ jury / televote at alpha = 0.05, edge kept if
  significant from at least one end, degree-1 ends not tested. Fig 3 now draws backbone edges, not all within-community edges.
- 2026-11-25: region label = UN M49 sub-region from CLDR 49 territoryContainment (raw/cldr, already in MANIFEST); yu, cs
  get Southern Europe from CLDR's deprecated entries. null_model.py made importable (main block guarded); outputs unchanged.

## Fixes (bugs and data problems found, and what was done)
- 2026-11-16, 2023 semi-finals missing: Spijkervet has only the 2023 final, and build_edges.py took EurovisionAPI rows
  only for years Spijkervet lacked entirely. Now it takes every (year, round) Spijkervet lacks; convert_eurovisionapi.py
  is run for 2023–2026. edges.csv: 82,952 -> 83,526 rows (+574, the two 2023 semis, vote_type total only, 19 and 20
  voters incl. wld). Check: every 2023 semi voter gives exactly 58 points to 10 entries. No existing row's excess changed
  (excess is computed within a round). Effect on the null model: the six main networks are unchanged (televote-only
  semis are not in them); robustness network mean5 Q 0.439 -> 0.430, z 22.2 -> 22.1;
  sum Q 0.449 -> 0.448, z 24.8 -> 25.1. borders, diaspora, language: unchanged.
- 2026-11-16, null-model bug: the first null_model.py built undirected weights by looping over directed pairs and
  skipping A > B alphabetically, so a pair with votes only in the B->A direction was dropped. Found when switching to
  pooled pairs. E.g. 1997–2008 (sum weighting): 372 edges -> 381; Q 0.453 -> 0.450. The numbers in commit 4d4dffa are
  superseded; all current numbers come from the fixed version (pairs pooled over both directions).
- 2026-11-16, ad HTML in lyrics: 7 of the 1811 English lyrics texts contain scraped web-ad
  HTML (<div class="google-auto-placed"> with <ins>/<iframe>); before cleaning, 8 lines of 1,800–2,100 tokens.
  build_lyrics.py removes these blocks with their contents and strips other formatting tags (<i>, <span>, <b>; 63
  entries had some tag) keeping their text. Raw files are unchanged. Check: the script asserts no tag is left.

## Pending layers
- Diaspora: done 2026-11-16, see Data above.
- Language: done 2026-11-16, see Data above.
- Lyrics: done 2026-11-16, see Data above.

## Literature
<!-- One line per paper: key — what it found — how we use it. The "how we use it" part is
     ours to write; Claude only fills in what is on the page. -->
- burgoyne2023eurovision: the Spijkervet dataset paper. Source of our 1957–2023 votes.
- gatherer2006eurovision: TODO what it found / how we use it
- fenn2006europe: TODO
- spierdijk2009bias: TODO
- ginsburgh2008eurovision: TODO
- reimers2020multilingual: how the multilingual sentence-transformers models are made (knowledge distillation; sbert.net says it describes our model). Cited with reimers2019sentencebert for the lyric embeddings. TODO what it found (read it).
- blondel2008louvain: Louvain community detection. TODO how we use it
- newman2006modularity: modularity. TODO how we use it
- cameron2011multiway: two-way (multiway) cluster-robust standard errors. Used for the regression CIs. TODO what it found (read it).
- serrano2009backbone: the disparity filter for weighted networks. Used for the Fig 3 backbone (scripts/backbone.py). TODO what it found (read it).
- newman2003mixing: assortative mixing by node attributes. Used for the attribute assortativity (scripts/assortativity.py). TODO what it found (read it).
- danon2005comparing: normalised mutual information for comparing community partitions. Used for scripts/nmi.py. TODO what it found (read it).
