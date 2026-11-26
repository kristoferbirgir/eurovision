# Eurovision: friendship or taste?

Course project: social graphs. Starting point: the vote network.

## Data
- `raw/votes.csv`, `raw/contestants.csv`: the [Spijkervet/eurovision-dataset](https://github.com/Spijkervet/eurovision-dataset) release, scraped from Eurovisionworld.
  - Covers 1957–2023. 2023 semi-finals and 2024–2026 come from [EurovisionAPI/dataset](https://github.com/EurovisionAPI/dataset) (`raw/eurovisionapi/`, converted by `scripts/convert_eurovisionapi.py`). 2020 was cancelled.
  - The jury/televote split runs from 2016 on. `wld` = the "Rest of the World" online televote (2023).
  - `contestants.csv` also has `lyrics` (99% of entries), `composers` and `lyricists`.
- Citations: `references.bib` (verified entries only; open TODOs are marked inside).
- `raw/borders/`: land borders from [geodatasource/country-borders](https://github.com/geodatasource/country-borders) (CC BY-SA 4.0).
- Sources, dates and checksums: `raw/MANIFEST.json`. Decisions: `NOTES.md`.

## Build
```
python scripts/convert_eurovisionapi.py 2023 2024 2025 2026
python scripts/build_edges.py
python scripts/build_borders.py
python scripts/build_diaspora.py
python scripts/build_language.py
python scripts/null_model.py      # ~2 min
python scripts/build_lyrics.py
python scripts/lyrics_similarity.py   # ~1.5 min, downloads the model once
python scripts/taste_similarity.py
python scripts/make_rating_files.py   # data/ratings_rater1/2.csv + data/ratings_sheet.md (never overwrites)
python scripts/merge_ratings.py       # after both raters are done: checks 40 values are 1-5, fills lyrics_rating_sheet.csv
python scripts/rating_agreement.py    # then: Spearman agreement between raters and with the model
python scripts/build_pairs.py
python scripts/collinearity.py
python scripts/regression.py
python scripts/check_data.py
python scripts/leave_one_out.py
python scripts/build_region.py      # data/region.csv (UN M49 sub-region from CLDR)
python scripts/nmi.py               # data/nmi.csv
python scripts/assortativity.py     # data/assortativity.csv (~15 s)
python scripts/backbone.py          # data/backbone_edges.csv (Fig 3 edges)
python scripts/make_figures.py      # figures/fig1-3 (PDF) + captions in figures/captions.md
python scripts/make_table_robustness.py   # paper/table_robustness.tex/.md
python scripts/write_paper.py       # paper/methods.md/.tex + figure_floats.tex from templates + key_numbers.json
python scripts/pack_overleaf.py     # paper/overleaf/ + paper/overleaf.zip: complete Overleaf project (incl. paper/pnas_template/)
```
This produces:
- `data/countries.csv`: country code → ISO3 and name. Use ISO3 to join UN migrant stock, borders and language data.
- `data/edges.csv`: one row per vote: year, era, round, vote_type (total/jury/tele), from, to, points, share, expected, excess.
- `data/borders.csv`: from, to, border (0/1, land borders only).
- `data/diaspora.csv`: from, to, year, migrants (born in `to`, living in `from`), share_of_migrants. UN DESA 2024.
- `data/language.csv`: from, to, shared_official, same_family, same_branch, same_subbranch (0/1), primary_from, primary_to. CLDR 49 + Glottolog 5.4.
- `data/glottolog_nodes.csv`: our named list of Glottolog branch / sub-branch nodes (glottocodes).
- `data/language_groups.csv`: per country, the primary language and its family, branch and sub-branch names.
- `data/lyrics.csv`: one English lyrics text per entry. `data/lyrics_similarity.csv`: era, from, to, similarity, n_years.
- `data/taste_similarity.csv`: era, from, to, taste_sim (A's taste profile vs B's songs), own_sim (A's own song vs B's).
- `data/pairs.csv`: one row per directed pair per sample (2016+ jury / televote, 1997–2008): mean excess + all predictors.
- `data/regression_coefs.csv`: standardised betas with 95% CIs per model and robustness spec.
- `data/key_numbers.json`: every number the paper quotes, written by the scripts. `RESULTS.md`: the same numbers with context.
- `data/edges_agg.csv`: from→to totals per era and vote_type: n_votes, excess_sum, excess_mean, points_sum.
- `data/null_results.csv`: observed modularity vs the shuffle null per weighting and network (Q, null mean/SD, z, p).
  `data/null_samples.csv`: null Q of every shuffle. `data/communities_obs.csv`: observed Louvain communities (weighting, network, community, code).
- `data/lyrics_embeddings.npz`: lyric embeddings per entry (emb raw, emb_c year-centred). `data/lyrics_similarity_year.csv`: year, from, to, similarity (centred), similarity_raw.
- `data/lyrics_extremes.csv`: the 5 most and 5 least similar song pairs (check).
- `data/taste_similarity_year.csv`: per vote: taste_sim and its robustness versions (raw, no top-5 partners, past only), own_sim.
- `data/lyrics_rating_sheet.csv`: the 20 hand-rating pairs (+ rating_rater1/2 after merging). `data/lyrics_rating_key.csv`: model scores for
  those pairs; do not open before both raters are done. `data/ratings_rater1.csv`, `data/ratings_rater2.csv`: one file per rater
  (pair_id, song_a, song_b, rating). `data/ratings_sheet.md`: the 20 pairs with both lyrics, for reading.
- `data/predictor_correlations.csv` (sample, var1, var2, pearson), `data/predictor_vif.csv` (sample, predictor, vif): collinearity check.
- `data/regression_fit.csv`: per model and spec: n, R², clustering, eigenvalue clips, n countries.
- `data/leave_one_out_family.csv`: same_family_only beta with one country left out; `data/diff_family_top_pairs.csv`: top different-family pairs.
- `data/region.csv`: code, m49, region (UN M49 sub-region from CLDR). `data/nmi.csv`: NMI between partitions vs label shuffles.
  `data/assortativity.csv`: attribute assortativity per network vs the vote-shuffle null. `data/backbone_edges.csv`: every 2016+ edge
  with its disparity-filter alpha, backbone flag and whether it lies inside a community.

**excess** = the share of the voter's points that went to B, minus the average share B got from all *other* voters that night. A positive value means A over-rated B compared with the rest of Europe, so song quality is removed. Running order and staging are not removed.

## Checks done
Full list with numbers: RESULTS.md ("Data checks" and the check under each analysis); `scripts/check_data.py`.
- Each voter's shares sum to 1 per round; excess sums to 0 per entry and round.
- 2023 final: the two vote sources agree 962/962.
- 2026 final: 25/25 entries match both Eurovisionworld and the official EBU scoreboard (total, televote, jury).
- Every analysis has a shuffle null, a second method or a hand-labelled sample (see RESULTS.md).

## Next
See STATUS.md ("Next up" and "Open questions").

## Setup
```
uv venv .venv && source .venv/bin/activate && uv pip install -r requirements.txt
```
