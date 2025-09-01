import httpx

ADQL = """
SELECT TOP 60 hostname, ra, dec, sy_vmag
FROM ps
WHERE ra IS NOT NULL AND dec IS NOT NULL
ORDER BY sy_vmag NULLS LAST
"""

async def fetch_hosts(limit: int = 60) -> list[dict]:
    """Query the NASA Exoplanet Archive for host stars with RA/DEC and visual magnitude.
    
    This function sends an ADQL query to the archives TAP service (`/TAP/sync`)
    requesting up to `limit` host stars that have valid right ascension (RA),
    declination (Dec), and visual magnitude (sy_vmag). Results are returned in JSON.

    Args:
        limit (int, optional): maximum number of host starts to fetch. Defaults to 60.

    Returns:
        list[dict]: A list of host star records, where each dict typicaly contains
            - 'hostname' (str): host star identifier
            - 'ra' (float): right ascension in degrees
            - 'dec' (float): declination in degrees
            - 'sy_mag' (float | None): visual magnitude (brightness)
    """    
    query = ADQL.replace('TOP 60', f'TOP {limit}')
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, params={'query': query, 'format': 'json'})
        resp.raise_for_status()
        return resp.json()