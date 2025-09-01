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
    """Return the brightest visible host stars for a given observer location and date

    Args:
        lat (float): observer latitude in degrees
        lon (float): observer longitude in degrees
        date (str): UTC date string in yyyy-mm-dd format
        min_alt (float, optional): visibility cutoff in degrees. Defaults to 30.0

    Returns:
        list[Target]: a list of up to 25 visible targets, each containing:
            - star metadata (name, ra/dec, visual magnitude)
            - computed visibility data (alt time series, peak alt, best viewing window)
    """    
    host_star_rows = await fetch_hosts()
    out = []
    for row in host_star_rows:
        name = str(row.get('hostname', '')).lower()
        ra_deg = float(row['ra'])
        dec_deg = float(row['dec'])
        vmag = row.get('sy_vmag')
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

