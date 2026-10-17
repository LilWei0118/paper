# Paper source

This repository contains the LaTeX source for a collaborative research paper. GitHub `main` is the personal working copy; the original collaborative Overleaf project is a read-only upstream for this clone.

## Compile

- **Main document:** `sample-sigconf.tex`
- **Compiler:** pdfLaTeX
- **Bibliography:** BibTeX, using `sample-base.bib` and `ACM-Reference-Format.bst`
- **Overleaf:** Import this GitHub repository into a personal project, set `sample-sigconf.tex` as the Main document, select pdfLaTeX, then Recompile. The source uses relative figure paths, so no path changes are needed.

The root contains the ACM class and style files used by the manuscript. `figures/` contains PDF and PNG figures referenced from the LaTeX source; newly redrawn previews are organized in `figures/hcw_figures/`. `software.bib` and `07-rebuttal.tex` are retained as project material even though the current main document does not include them.

## Manuscript structure

| File | Content |
| --- | --- |
| `00-abstract.tex` | Abstract |
| `01-introduction.tex` | Introduction |
| `02-background.tex` | Background and motivation |
| `03-design.tex` | Method and design |
| `04-evaluation.tex` | Implementation and evaluation |
| `05-related_work.tex` | Related work |
| `08-discussion.tex` | Discussion |
| `06-conclusion.tex` | Conclusion |
| `07-rebuttal.tex` | Separate rebuttal material |

The chapter files are included by `sample-sigconf.tex`; it also selects the bibliography style and database. Existing `README.txt` contains the upstream ACM template documentation.

## Repository workflow

Edit locally, then commit and push to GitHub `main`. In the personal Overleaf project, pull the GitHub changes and recompile. The original collaborative Overleaf remote is named `upstream-overleaf` and must only be fetched. Review differences and possible conflicts with the collaborators' version before merging upstream changes; never push to that remote.
