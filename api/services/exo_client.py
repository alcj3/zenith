import httpx

ADQL = """
SELECT TOP 60 hostname, ra, dec, sy_vmag
FROM ps
WHERE ra IS NOT NULL AND dec IS NOT NULL
ORDER BY sy_vmag NULLS LAST
"""

async def fetch_hosts(limit: int = 60) -> list[dict]:
    query = ADQL.replace('TOP 60', f'TOP {limit}')
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params={'query': query, 'format': 'json'})
        resp.raise_for_status()
        return resp.json()