"""Download the three FRED series the page uses and merge them into data/fred.csv.

Run from the repository root:   python fetch_data.py
No third-party packages needed. The GitHub Action in .github/workflows runs the
same script on a schedule so the page stays current.

Series
  THREEFYTP10  Kim-Wright term premium on a 10-year zero-coupon bond (Federal Reserve Board), percent, daily
  DGS10        10-year Treasury constant-maturity yield (Federal Reserve H.15), percent, daily
  DTWEXBGS     Nominal broad U.S. dollar index, goods and services (Federal Reserve H.10), Jan 2006 = 100, daily
"""
import csv
import io
import json
import os
import urllib.request
from datetime import datetime, timezone

SERIES = ["THREEFYTP10", "DGS10", "DTWEXBGS"]
START = "1990-01-01"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start}"


def fetch(sid):
    req = urllib.request.Request(URL.format(sid=sid, start=START),
                                 headers={"User-Agent": "Mozilla/5.0 (course project data refresh)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8")
    rows = csv.reader(io.StringIO(text))
    header = next(rows)
    # FRED's first column is "observation_date" (older files used "DATE").
    out = {}
    for r in rows:
        if len(r) < 2:
            continue
        date, val = r[0].strip(), r[1].strip()
        if val in ("", "."):
            continue
        try:
            out[date] = float(val)
        except ValueError:
            continue
    if not out:
        raise RuntimeError(f"No observations parsed for {sid}; header was {header}")
    return out


def main():
    data = {sid: fetch(sid) for sid in SERIES}
    dates = sorted(set().union(*[d.keys() for d in data.values()]))
    os.makedirs("data", exist_ok=True)
    with open("data/fred.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date"] + SERIES)
        for d in dates:
            w.writerow([d] + [("" if d not in data[s] else repr(data[s][d])) for s in SERIES])
    meta = {
        "retrieved_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "last_observation": {s: max(data[s].keys()) for s in SERIES},
        "first_observation": {s: min(data[s].keys()) for s in SERIES},
    }
    with open("data/meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Wrote data/fred.csv with {len(dates)} dates")
    for s in SERIES:
        print(f"  {s}: {meta['first_observation'][s]} to {meta['last_observation'][s]} ({len(data[s])} obs)")


if __name__ == "__main__":
    main()
