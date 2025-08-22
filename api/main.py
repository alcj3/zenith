from fastapi import FastAPI

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

@app.get('/api/targets')
def targets(lat: float, lon: float, date: str, min_alt: float = 30) -> list[dict]:
    # fake values for now
    return [
        {
            "name": "HD 189733",
            "ra_deg": 300.18,
            "dec_deg": 22.71,
            "vmag": 7.7,
            "peak_altitude_deg": 68.3,
            "best_window": {
                "start": "2025-08-21T05:10:00Z",
                "end": "2025-08-21T10:15:00Z"
            },
            "series": [
                {"t": "2025-08-21T05:00:00Z", "alt_deg": 12.3},
                {"t": "2025-08-21T05:05:00Z", "alt_deg": 15.8},
                {"t": "2025-08-21T05:10:00Z", "alt_deg": 20.0}

            ]
        }
    ]
