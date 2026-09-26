"""Hosted EV charger search API backed by clearly labelled demo data."""

from math import asin, cos, radians, sin, sqrt

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="EV Location Finder API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


class Charger(BaseModel):
    id: str
    name: str
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    connector_types: list[str]
    power_kw: float = Field(gt=0)
    available: bool
    distance_km: float | None = None


# Demo records only: replace this list with a trusted provider before production use.
CHARGERS = [
    Charger(
        id="blr-001",
        name="Indiranagar Fast Charge (Demo)",
        address="100 Feet Road, Bengaluru",
        latitude=12.9719,
        longitude=77.6412,
        connector_types=["CCS2", "Type 2"],
        power_kw=60,
        available=True,
    ),
    Charger(
        id="blr-002",
        name="Whitefield Charge Hub (Demo)",
        address="ITPL Main Road, Bengaluru",
        latitude=12.9868,
        longitude=77.7353,
        connector_types=["CCS2"],
        power_kw=120,
        available=True,
    ),
    Charger(
        id="blr-003",
        name="Koramangala Community Charger (Demo)",
        address="80 Feet Road, Bengaluru",
        latitude=12.9352,
        longitude=77.6245,
        connector_types=["Type 2"],
        power_kw=22,
        available=False,
    ),
]


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance between two coordinates."""
    earth_radius_km = 6371.0
    lat_delta = radians(lat2 - lat1)
    lon_delta = radians(lon2 - lon1)
    a = sin(lat_delta / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(
        lon_delta / 2
    ) ** 2
    return earth_radius_km * 2 * asin(sqrt(a))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"name": app.title, "docs": "/docs", "health": "/health"}


@app.get("/api/v1/chargers", response_model=list[Charger])
def list_chargers(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(25, gt=0, le=200),
    connector: str | None = Query(None, min_length=2, max_length=20),
    available_only: bool = False,
) -> list[Charger]:
    """Find demo chargers near a location, optionally applying connector filters."""
    results = []
    for charger in CHARGERS:
        if available_only and not charger.available:
            continue
        if connector and connector not in charger.connector_types:
            continue
        distance = distance_km(latitude, longitude, charger.latitude, charger.longitude)
        if distance <= radius_km:
            results.append(charger.model_copy(update={"distance_km": round(distance, 2)}))
    return sorted(results, key=lambda charger: charger.distance_km or 0)
