# Eurovision: friendship or taste? (DTU 02805 final project)

Question: is excess voting at Eurovision explained by friendship (borders, diaspora,
language) or by taste (song similarity)? Do juries and televoters differ?

## Pipeline
- `python scripts/convert_eurovisionapi.py 2023 2024 2025 2026` → raw/votes_eurovisionapi.csv
- `python scripts/build_edges.py` → data/countries.csv, data/edges.csv, data/edges_agg.csv
- `python scripts/build_borders.py` → data/borders.csv
- `python scripts/build_diaspora.py` → data/diaspora.csv
- `python scripts/build_language.py` → data/language.csv, data/language_groups.csv
- `python scripts/null_model.py` → data/null_results.csv, data/null_samples.csv, data/communities_obs.csv, figures/diagnostics/null_modularity.pdf
- `python scripts/build_lyrics.py` → data/lyrics.csv; `python scripts/lyrics_similarity.py` → data/lyrics_similarity*.csv, rating sheet
- `python scripts/taste_similarity.py` → data/taste_similarity*.csv; `make_rating_files.py` → data/ratings_rater{1,2}.csv, ratings_sheet.md; after hand ratings `merge_ratings.py`, then `rating_agreement.py`
- `python scripts/build_pairs.py` → data/pairs.csv; `collinearity.py`; `regression.py` → data/regression_*.csv
- `python scripts/build_region.py` → data/region.csv; `nmi.py` → data/nmi.csv; `assortativity.py` → data/assortativity.csv; `backbone.py` → data/backbone_edges.csv (before make_figures)
- `python scripts/make_figures.py` → figures/fig1_modularity.pdf, fig2_coefficients.pdf, fig3_communities.pdf
- `python scripts/check_data.py`, `leave_one_out.py`; `make_table_robustness.py`; `python scripts/write_paper.py` → paper/methods.md/.tex, figure_floats.tex (edit paper/methods_template.md, figures/captions.md); `pack_overleaf.py` → paper/overleaf/ + overleaf.zip (class files from paper/pnas_template/, the course template; never edit them)
- Every quoted number goes into data/key_numbers.json via scripts/key_numbers.py (never by hand); add it to RESULTS.md with captures/misses.
- Join every layer on country-pair codes from data/countries.csv (ISO2 lower case, ISO3 for external data).

## Start and end of every session
- **Start:** read STATUS.md, then NOTES.md. Tell the user what is done, what is in progress
  (and by whom), and propose the next step from "Next up". If someone else's task is listed under
  "In progress", don't touch its files.
- **When starting a task:** add a line under "In progress" (who, what, branch, date).
- **End (or after each finished step):** update STATUS.md: move the task to Done, update
  "Last updated", add a Log line (date, who, what changed, what to check), add any new open
  questions. Log data decisions in NOTES.md. Then commit, including STATUS.md.

## Rules
- Raw data lives in raw/ with an entry in raw/MANIFEST.json (source, date, commit/checksum). Never hand-edit raw data.
  Never invent a data URL. If a download fails, say so and leave the layer pending; never substitute made-up data.
- References live in references.bib. Never write a reference from memory: open the DOI or URL,
  copy the fields shown there, and mark anything missing with a TODO comment. Each paper also gets
  a line under "Literature" in NOTES.md (what it found, how we use it). Data sources need both a
  MANIFEST entry and a bib entry, including any attribution text their license requires.
- Every analysis needs a check: a shuffle null, a second method, or a hand-labeled sample, with the result reported.
- Scripts in scripts/, figures in figures/, exploratory notebooks in notebooks/.
- Log data decisions in NOTES.md (it becomes the Methods section).
- Do not write the group's findings, interpretations or reflections. Leave TODOs. Every member must be able to explain all code.
- Deadline: paper (PNAS LaTeX template, 6 pages incl. refs) + 3 slides + reflection, Fri 27 Nov 23:59. Presentations Wed 2 Dec.
