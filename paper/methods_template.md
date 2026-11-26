<!-- Methods (about one PNAS page). Edit THIS file; run `python scripts/write_paper.py` to produce
     paper/methods.md (Markdown) and paper/methods.tex (LaTeX for Overleaf).
     Double-brace placeholders are filled from data/key_numbers.json. Literal numbers must be parameters,
     dates or versions, never results. [@key] = citation key in references.bib. $...$ = LaTeX math.
     The longer earlier draft is in paper/methods_template_long.md. -->

**Data.** Votes for 1957–2023 come from the Eurovision dataset of Burgoyne et al. [@burgoyne2023eurovision];
the 2023 semi-finals and 2024–2026 from EurovisionAPI [@eurovisionapi2026] (commit e564111). The table has
{{edges.n_rows|,}} votes (voter, receiver, round, vote type) from {{edges.n_contest_years}} contests ({{edges.years.0}}–{{edges.years.1}}; 2020 cancelled);
separate jury and televote points exist from 2016. Land borders come from GeoDataSource
[@geodatasource_borders]; diaspora from the UN DESA International Migrant Stock 2024 [@undesa2024migrantstock];
official languages from Unicode CLDR 49 [@cldr49]; language classification from Glottolog 5.4
[@glottolog54]; lyrics and English translations from EurovisionAPI ({{lyrics.n_with_english|,}} of {{lyrics.n_entries|,}} entries have
English text). Sources, retrieval dates, checksums and licences are listed in the repository.

**Excess votes.** Each voter's points in a round were converted to shares of its points in that round.
The expected share of an entry is the mean share it received from all other voters in the same round
and vote type; excess is the observed minus the expected share. Excess removes how much everyone
liked a song that night, but not running order or staging. Eras follow the voting rules: 1957–1974,
1975–1996, 1997–2008 (televote), 2009–2015 (50/50) and 2016–2026 (jury and televote reported separately).

**Community structure.** For each era, and for 2016–2026 jury and televote separately, countries were
linked by their mean excess over all votes between them in both directions (pairs with at least
{{null_model.min_votes_mean5}} votes; positive weights only). Communities were found with the Louvain method
[@blondel2008louvain], keeping the highest modularity $Q$ [@newman2006modularity] of {{null_model.louvain_seeds}} seeded runs.
In the null model each voter's set of points in a year, round and vote type was randomly re-assigned
among the entries it rated and excess recomputed ({{null_model.n_shuffles|,}} shuffles per network). We report
$z = (Q_\mathrm{obs} - \overline{Q}_\mathrm{null}) / \mathrm{SD}(Q_\mathrm{null})$.

**Partition comparison, assortativity and backbone.** We compared partitions with normalised mutual
information (NMI) [@danon2005comparing], 2016–2026 jury against televote communities and each network's
communities against the Glottolog branch and sub-branch of the main language, each against {{nmi.n_shuffles|,}}
random permutations of the second labelling. Attribute assortativity [@newman2003mixing] of each
positive-excess network (edges unweighted) by language branch and by UN M49 sub-region (from CLDR) was
compared with {{assortativity.n_shuffles|,}} networks from the vote shuffle above. Fig. \ref{fig:fig3} shows the
disparity-filter backbone [@serrano2009backbone] of the 2016–2026 networks ($\alpha$ = {{backbone.alpha}}; an edge is
kept if significant from either end), which keeps {{backbone.networks.2016+ jury.n_backbone_edges}} of {{backbone.networks.2016+ jury.n_edges}} jury and {{backbone.networks.2016+ televote.n_backbone_edges}} of {{backbone.networks.2016+ televote.n_edges}} televote edges.

**Pair predictors.** *Border*: shared land border. *Diaspora*: $\log(1 + m)$, with $m$ the number of people
born in the receiving country living in the voting country in the UN year nearest the vote; pairs the
UN does not list count as zero. *Language*: shared official language (CLDR status "official"), and the
deepest Glottolog level shared by the two countries' main languages: different families (reference),
same family only, same branch only (e.g. Slavic) or same sub-branch (e.g. South Slavic).

**Taste profile.** English lyrics were embedded with paraphrase-multilingual-mpnet-base-v2
[@reimers2019sentencebert; @reimers2020multilingual], in chunks of at most {{lyrics_similarity.max_seq_length}} tokens averaged per song, and each song vector
was centred on the mean of its year. A voter's taste profile for a vote on country $B$ in year $t$ is
the share-weighted sum of the vectors of all songs it gave points to in other years, leaving out every
song from $B$; for 2016–2026 profiles are built from jury votes and televotes separately. Taste
similarity is the cosine between the profile and $B$'s song in year $t$.

**Regression.** For each directed pair with at least {{pairs.min_votes}} votes, signed excess and all predictors were
averaged over the same votes, in three samples: 2016–2026 jury and televote ({{pairs.samples.jury_2016.n_pairs|,}} pairs each)
and 1997–2008 ({{pairs.samples.tele_1997.n_pairs|,}} pairs). We fitted ordinary least squares with outcome and predictors
z-scored within each sample. Confidence intervals (95%) use standard errors clustered two-way by voting
and receiving country [@cameron2011multiway]; in every fit, negative eigenvalues of the two-way covariance
matrix were set to zero, as proposed there (this changed {{regression._n_fits_eig_clipped}} of {{regression._n_fits_two_way}} fits, all 2016–2026 jury).
All robustness runs are in Table \ref{tab:robustness}; Table \ref{tab:measures} lists what each measurement captures and misses.

**Validation.** For the 2023 final the two vote sources agree on {{checks.final_2023_sources.n_identical}} of {{checks.final_2023_sources.n_matched}} votes, and the
reconstructed 2026 final matches the official EBU scoreboard [@ebu2026grandfinal] for {{checks.final_2026_vs_ebu.n_identical}} of {{checks.final_2026_vs_ebu.n_entries}} entries. Taste profiles
recomputed by a direct loop over votes agree with the vectorised computation (largest difference
{{taste_similarity.brute_force_check.total.max_abs_diff}}). Predictors are weakly correlated (largest $|r|$ = {{collinearity.all_samples.max_abs_corr}}; largest variance inflation factor
{{collinearity.all_samples.max_vif}}). Leaving out one country at a time, the same-family-only coefficient stays between
{{leave_one_out.all_models.beta_min|.3f}} and {{leave_one_out.all_models.beta_max|.3f}} in all three models (the 95% CI includes 0 in {{leave_one_out.all_models.n_ci_includes_0}} of {{leave_one_out.all_models.n_refits}} refits). Two of us rated
{{rating_agreement.n_pairs}} song pairs (four from each quintile of model similarity) from 1 to 5 for similarity in topic and mood, each
without seeing the other's ratings or the model score; Spearman's $\rho$ between the raters is {{rating_agreement.spearman_rater1_vs_rater2}}, and between the
mean rating and the year-centred model similarity {{rating_agreement.spearman_mean_vs_model_centred}}.
