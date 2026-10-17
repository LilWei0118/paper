# Codex workflow for this paper

- Treat `upstream-overleaf` as fetch-only. Never push to it or modify the original collaborative Overleaf project. Its configured push URL intentionally rejects pushes.
- Use GitHub `origin` and the local `main` branch for the personal working copy.
- Do not discard local edits, overwrite collaborator changes, or change paper text/layout/figures unless the user requests it.
- When the user asks to **sync the paper**, inspect and summarize local changes, commit the intended changes, push to `origin main`, report the commit SHA, and remind the user to pull GitHub changes into the personal Overleaf project and recompile.
- If the user asks for collaborator updates, fetch `upstream-overleaf` first. Compare it with local `main`, explain differences and possible conflicts, and wait for the user's confirmation before merging.
- Keep LaTeX build products out of commits; keep source `.tex`, `.bib`, style files, and required figures.
- Put newly redrawn figure previews in `figures/hcw_figures/`, and update `\includegraphics` paths only when the user selects a figure for the paper.
