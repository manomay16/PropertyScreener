import requests

GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"


def geocode_address(address: str):
    params = {
        "address": address,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "format": "json",
    }
    response = requests.get(GEOCODER_URL, params=params)
    data = response.json()

    matches = data["result"]["addressMatches"]
    if not matches:
        return None

    match = matches[0]
    census_tract = match["geographies"]["Census Tracts"][0]["GEOID"]
    latitude = match["coordinates"]["y"]
    longitude = match["coordinates"]["x"]

    return {
        "census_tract": census_tract,
        "latitude": latitude,
        "longitude": longitude,
    }