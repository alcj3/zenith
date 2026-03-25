# Zenith 🌟

> Find exoplanet host stars visible from your location tonight.

Zenith pulls live data from NASA's Exoplanet Archive and computes which host stars are actually visible from wherever you are, on any given night. Enter your coordinates, a date, and a minimum altitude — and get back the 25 best targets ranked by visibility, with altitude-over-time charts for each one.

![Zenith](https://img.shields.io/badge/stack-FastAPI%20%7C%20React%20%7C%20Astropy-blue)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What it does

- Queries NASA's Exoplanet Archive TAP service for real host star data (RA, Dec, magnitude)
- Builds a UTC visibility grid for your location and date using Astropy coordinate transforms
- Filters and ranks stars by peak altitude and brightness
- Returns up to 25 visible targets with best observation windows
- Renders altitude-over-time charts per star via Recharts

Each request computes ~8,640 altitude samples (60 stars × 144 time points) entirely server-side.

---

## The hard part

The core challenge was converting static astronomical coordinates into observer-specific visibility windows in real time.

The pipeline:
1. Fetch host stars with `ra`, `dec`, and `vmag` from NASA via ADQL
2. Build a UTC time grid (18:00Z start, 5-minute intervals, 12-hour span)
3. Create an `EarthLocation` from the user's lat/lon via Astropy
4. Transform each star's `SkyCoord` into the observer's `AltAz` frame
5. Extract altitude arrays with NumPy — find peak, first/last above threshold
6. Return summary + full series for frontend charting

---

## Stack

**Backend**
- Python 3.13, FastAPI, Uvicorn
- Astropy (coordinate transforms, time grids)
- NumPy (altitude array processing)
- httpx, Pydantic, Pytest, Pipenv

**Frontend**
- React 19, Vite
- Recharts (altitude-over-time line charts)
- Browser Fetch API

**Data Source**
- [NASA Exoplanet Archive TAP](https://exoplanetarchive.ipac.caltech.edu/TAP/sync) — live, no API key required

---

## Running locally

**Backend**
```bash
pipenv install
pipenv run uvicorn api.main:app --reload --port 8000
```

**Frontend**
```bash
cd web
npm install
npm run dev
```

Open `http://localhost:5173` — Vite proxies `/api` to the backend automatically.

---

## Project structure

```
api/
  main.py           # FastAPI app, routes, /api/targets orchestration
  models/target.py  # Pydantic response models
  services/
    exo_client.py   # NASA TAP client + ADQL query
    astro.py        # Visibility math pipeline
tests/
  test_main.py      # API tests
web/
  src/
    App.jsx         # Main UI, form, fetch, results table
    AltitudeChart.jsx # Recharts altitude chart
```

---

## Known limitations / what's next

- Visibility window uses a fixed 12-hour span starting at 18:00 UTC — not yet local-night aware
- No caching — every request hits NASA live (no retry/fallback if NASA is slow)
- No geolocation lookup — user must enter lat/lon manually

**Up next:**
- Browser geolocation / city search
- Mocked backend tests (currently depends on live NASA access)
- Local observing-night windows instead of UTC-only
- Result caching and pagination
- Visual polish

---

## Why I built this

I wanted a project that combined real scientific data processing with a full-stack architecture. The visibility computation problem turned out to be interesting: the same star looks completely different depending on where you are on Earth and what time of year it is.

---

*Data sourced from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), maintained by Caltech/IPAC.*
