"""Collect everything Overleaf needs into one flat folder: paper/overleaf/ (not tracked by git).

Copies paper/main.tex, paper/methods.tex, paper/figure_floats.tex, paper/table_robustness.tex,
paper/table_measures.tex, references.bib, the three figure PDFs and the PNAS class files from
paper/pnas_template/ (the course template, pnas-new.cls v1.47). The folder is a complete project:
paper/overleaf.zip (also written) can be uploaded to Overleaf as a new project (New Project > Upload Project),
or upload the folder's files to the existing one.
Run write_paper.py and make_table_robustness.py first.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper/overleaf"
FILES = ["paper/main.tex", "paper/methods.tex", "paper/figure_floats.tex", "paper/table_robustness.tex",
         "paper/table_measures.tex",
         "references.bib", "figures/fig1_modularity.pdf", "figures/fig2_coefficients.pdf",
         "figures/fig3_communities.pdf"]
TEMPLATE = sorted((ROOT / "paper/pnas_template").iterdir())  # class, style, bst, logo: copied unchanged

shutil.rmtree(OUT, ignore_errors=True)  # the folder only ever holds copies made by this script
OUT.mkdir(parents=True)
for f in FILES:
    shutil.copy2(ROOT / f, OUT / Path(f).name)
for f in TEMPLATE:
    shutil.copy2(f, OUT / f.name)
print(f"{OUT.relative_to(ROOT)}/: " + ", ".join(Path(f).name for f in FILES))
print("  + template: " + ", ".join(f.name for f in TEMPLATE))
shutil.make_archive(str(OUT), "zip", OUT)  # paper/overleaf.zip, flat (files at the zip root)
print(f"{OUT.relative_to(ROOT)}.zip")
