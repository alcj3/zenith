from pydantic import BaseModel, Field
from typing import List

class SeriesPoint(BaseModel):
    t: str
    alt_deg: float

class BestWindow(BaseModel):
    start: str
    end: str

class Target(BaseModel):
    name: str
    ra_deg: float
    dec_deg: float
    vmag: float | None = None
    peak_altitude_deg: float
    best_window: BestWindow
    series: List[SeriesPoint] = Field(default_factory=list)