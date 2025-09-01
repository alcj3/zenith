from astropy import coordinates, time
import astropy.units as u
import numpy as np 
from datetime import datetime, timedelta, timezone

# TODO fix the type: ignore  
def build_visibility(
    ra_deg: float, 
    dec_deg: float,
    lat: float,
    lon: float,
    date: str,
    step_minutes: int = 5,
    hours: int = 12,
    min_alt: float = 30.0
    ) -> dict:
    """Compute an altitude time series and visibility window for a star

    Args:
        ra_deg (float): right ascension of the star in degrees
        dec_deg (float): declination of the star, in degrees
        lat (float): observer latitude in degrees (south -, north +) 
        lon (float): observer longitude in degrees (west -, east +)
        date (str): UTC date string in yyyy-mm-dd format
        step_minutes (int, optional): spacing between samples. Defaults to 5
        hours (int, optional): total span length. Defaults to 12
        min_alt (float, optional): visibility cutoff in degrees. Defaults to 30.0
    
    Returns:
        dict: contains the constructed series, peak altitude in degrees, and best window
    """
    y, m, d = parse_inputs(date, lat, lon, min_alt, step_minutes, hours)
    times = build_time_grid(y, m, d, step_minutes, hours)
    t_astropy, loc, altaz_frame = build_coordinate_frames(times, lat, lon)
    alts = transform_angles(ra_deg, dec_deg, altaz_frame)
    series, peak, best = compute_outputs(times, alts, min_alt)

    return {
        'series': series,
        'peak_altitude_deg': peak,
        'best_window': best
    }

def parse_inputs(
        date: str, 
        lat: float,
        lon: float,
        min_alt: float,
        step_minutes: int,
        hours: int
        ) -> tuple[int, int, int]:
    """Validate inputs and parse data

    Args:
        date (str): UTC date string 'YYYY-MM-DD' 
        lat (float): latitude in degrees (-90 to 90)
        lon (float): longitude in degrees (-180 to 180)
        min_alt (float): visibility threshold (0 to 90 degrees) 
        step_minutes (int): spacing between samples. Defaults to 5
        hours (int): total span length. Defaults to 12 

    Returns:
        tuple[int, int, int]: parsed year, month, day as integers
    """
    # splits and converts to int
    y, m, d = map(int, date.split('-'))
    
    if not -90 <= lat <= 90:
        raise ValueError(f'Latitude must be between -90 and 90 degrees, got {lon}')

    if not -180 <= lon <= 180:
        raise ValueError(f'Longitude must be between -180 and 180 degrees, got {lat}')

    if not 0 <= min_alt <= 90:
        raise ValueError(f'Minimum altitude must be between 0 and 90 degrees, got {min_alt}')
    
    if not 0 < step_minutes <= 60:
        raise ValueError(f'Step minutes must be between 0 and 60, got {step_minutes}')

    if not 1 < hours <= 24:
        raise ValueError(f'Hours must be between 1 and 24, got {hours}')

    return y, m, d

def build_time_grid(y: int, m: int, d: int, step_minutes: int, hours: int) -> list:
    # TODO change time zone later
    """Build a UTC time grid for the given date

    Args:
        y (int): year
        m (int): month
        d (int): day
        step_minutes (int): spacing between samples. Defaults to 5
        hours (int): total span length. Defaults to 12 

    Returns:
        list: list of timezone aware UTC datetimes
    """    
    start = datetime(year=y, month=m, day=d, hour=18, minute=0, second=0, tzinfo=timezone.utc)
    n_steps = int((60 / step_minutes) * hours)
    times = [start + timedelta(minutes=i*step_minutes) for i in range(n_steps)]
    
    return times

def build_coordinate_frames(
        times: list,
        lat: float,
        lon: float
        ) -> tuple[time.Time, coordinates.EarthLocation, coordinates.AltAz]:
    """Create Astropy time, observer location, and AltAz frame objects.

    Args:
        times (list): list of timezone aware UTC
        lat (float): observer latitude in degrees
        lon (float): observer longitude in degrees

    Returns:
        (t_astropy, loc, altaz_frame):
            - t_astropy (Time): astropy.time.Time array for the given times
            - loc (EarthLocation): astropy.coordinates.EarthLocation for the observer
            - altaz_frame (AltAz): astropy.coordinates.AltAz frame with obstime+location 
    """    
    t_astropy = time.Time(times)
    loc = coordinates.EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m ) # type: ignore
    altaz_frame = coordinates.AltAz(obstime=t_astropy, location=loc)
    return t_astropy, loc, altaz_frame

def transform_angles(ra_deg: float, dec_deg: float, altaz_frame: coordinates.AltAz) -> np.ndarray:
    """Transforms a stars fixed position into altitude values over time.

    Args:
        ra_deg (float): right ascension in degrees
        dec_deg (float): declination in degrees
        altaz_frame (coordinates.AltAz): prebuilt AltAz fram (has times + location)

    Returns:
        alts (ndarray: 1D numpy array of altitudes in degrees 
    """    
    sky = coordinates.SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg) # type: ignore
    altaz = sky.transform_to(altaz_frame)
    alts = np.array(altaz.alt.deg, dtype=float) # type: ignore
    
    return alts

def compute_outputs(times: list[datetime], alts: np.ndarray, min_alt: float) -> tuple[list[dict], float, dict|None]:
    """Buld the ouput series, peak altitude, and best visibility window

    Args:
        times (list): python datetimes corresponding to the altitude samples
        alts (float): altitudes in degrees for each time
        min_alt (dict): visibility threshold in degrees; points below are ignored for the window

    Returns:
        (series, peak, best):
            - series: list of {'t': ISO-8601 UTC, 'alt_deg': float}
            - peak: maximum altitude (nan if all values are NaN)
            - best: {'start': ISO, 'end': ISO}
    """    
    series = []
    for ts, a in zip(times, alts):
        iso = ts.isoformat().replace('+00:00', 'Z')
        series.append({'t': iso, 'alt_deg': float(a)})

    if np.isnan(alts).all():
        peak = float('nan')
    else:
        peak = float(np.nanmax(alts))
    
    idx = np.where(alts >= min_alt)[0]
    if idx.size == 0:
        best = None
    else:
        start_iso = times[int(idx[0])].isoformat().replace("+00:00", "Z")
        end_iso   = times[int(idx[-1])].isoformat().replace("+00:00", "Z")
        best = {"start": start_iso, "end": end_iso}

    return series, peak, best