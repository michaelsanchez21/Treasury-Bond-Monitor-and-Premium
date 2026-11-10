# Term Premium Monitor

A one-page site that plots a 10-year Treasury's modified duration and the 10-year term premium since 1990, then measures what the April 2025 term-premium jump did to the U.S. dollar.

## Put it online (GitHub Pages)

1. Create a new public repository on GitHub and upload everything in this folder, including the hidden `.github` folder.
2. Get the data. Either:
   - on GitHub: Actions tab → "Update FRED data" → Run workflow (it commits `data/fred.csv`), or
   - on your computer: `python fetch_data.py`, then commit `data/fred.csv` and `data/meta.json`.
3. Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`. The URL appears there after a minute.

The workflow re-downloads the data every Tuesday, so the page stays current.

## Preview locally

`python -m http.server` in this folder, then open http://localhost:8000. Opening `index.html` directly from disk will not load the data.

## Files

- `index.html`: the page. Window dates, baseline length and your name are in the `CFG` block at the top of the script.
- `fetch_data.py`: downloads THREEFYTP10, DGS10 and DTWEXBGS from FRED into `data/fred.csv`.
- `.github/workflows/update-data.yml`: runs the script weekly and on demand.
