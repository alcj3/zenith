from fastapi import FastAPI
from typing import List
from api.models.target import Target
from api.services.exo_client import fetch_hosts
from api.services.astro import build_visibility

app = FastAPI()

@app.get('/')
def root():
    return{'welcome':'!'}

@app.get('/hello')
def say_hello():
    return {"message": "Hello stars!"}

@app.get('/health')
def say_status():
    return {'ok': True}

@app.get('/api/targets', response_model=List[Target])
async def targets(lat: float, lon: float, date: str, min_alt: float = 30) -> List[Target]:
    host_star_rows = await fetch_hosts()
    out = []
    for row in host_star_rows:
        name = str(row.get('hostname', '')).lower()
        ra_deg = float(row['ra'])
        dec_deg = float(row['dec'])
        vmag = row.get('sy_vmag')
        # # fake series for now
        # series = [
        #     {"t": f"{date}T05:00:00Z", "alt_deg": 12.0},
        #     {"t": f"{date}T06:00:00Z", "alt_deg": 35.0},
        # ]
        # peak_altitude_deg = max(p['alt_deg'] for p in series)
        # above = [p for p in series if p["alt_deg"] >= min_alt]
        # best_window = (
        #     {"start": above[0]["t"], "end": above[-1]["t"]}
        #     if above else None
        # )
        # if not best_window:
        #     continue
        vis = build_visibility(ra_deg, dec_deg, lat, lon, date, step_minutes=5, hours=12, min_alt=min_alt)
        if vis['best_window'] is None or vis['peak_altitude_deg'] < min_alt:
            continue

        out.append(
            {
            "name": name,
            "ra_deg": ra_deg,
            "dec_deg": dec_deg,
            "vmag": vmag,
            "peak_altitude_deg": vis['peak_altitude_deg'],
            "best_window": vis['best_window'],
            "series": vis['series'],
            }
        )
    
    out.sort(key=lambda d: (-d["peak_altitude_deg"], d["vmag"] if d["vmag"] is not None else 99))
    return out[:25]

