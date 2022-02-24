import requests
from math import cos, sin, asin, sqrt, radians
import heapq
import datetime as dt
import os

def get_geo_info() -> tuple:
    """convert zip code to latitude, longitude, and region code."""
    POSITIONSTACK_ENDPOINT = "http://api.positionstack.com/v1/forward"
    POSITIONSTACK_API_KEY = os.environ["POSITIONSTACK_API"]
    parameters = {
        "access_key": POSITIONSTACK_API_KEY,
        "query": input("Please enter your zip code.\n")
    }

    try:
        response = requests.get(url=POSITIONSTACK_ENDPOINT, params=parameters)
        response.raise_for_status()
        geo_data = response.json()["data"][0]
        return geo_data["latitude"], geo_data["longitude"]
    except requests.exceptions.RequestException:
        print(f"Error! {response.json()['error']['message']}.")
    
def distance_cal(lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> int:
    """return the distance (miles) using Haversine formula."""
    lat_a, lon_a, lat_b, lon_b = map(radians, [lat_a, lon_a, lat_b, lon_b])
    a = sin((lat_b - lat_a) / 2) ** 2 + cos(lat_a) * cos(lat_b) * sin((lon_b - lon_a) / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * 3959

def get_rc_spots() -> list:
    """return a heap containing rockclimbing spots within 150 miles."""
    geo_info = get_geo_info()
    if geo_info:
        lat, lon = geo_info
        CLIMBINGWEATHER_ENDPOINT = "https://api.climbingweather.com/country"
        response = requests.get(url=f"{CLIMBINGWEATHER_ENDPOINT}/USA/area")
        response.raise_for_status()
        data = response.json()
        # print(data)
        near_spots_heap = []
        for spot in data:
            # some data do not have latitude and longitude
            if spot["latitude"] != "None" and spot["longitude"] != "None":
                distance = round(distance_cal(lat, lon, float(spot["latitude"]), float(spot["longitude"])), 2)
                if distance <= 150:
                    # print(spot)
                    heapq.heappush(near_spots_heap, (distance, spot["areaId"], spot["name"], spot["adminArea"]))
        return near_spots_heap

def get_forecast() -> None:
    """print a list of rockclimbig spots with nice weather for the weekend."""
    plan, near_spots = [], get_rc_spots()
    if near_spots is None:
        print("Error! Did not get a valid list of climbing destinations.")
        return
    CLIMBINGWEATHER_ENDPOINT = "https://api.climbingweather.com/area"
    # for_check = []
    while len(plan) < 5 and near_spots:
        distance, area_ID, area_name, state = heapq.heappop(near_spots)
        response = requests.get(url=f"{CLIMBINGWEATHER_ENDPOINT}/{area_ID}/forecast")
        response.raise_for_status()
        data = response.json()["daily"]["data"]
        for day in data:
            date = dt.datetime.fromtimestamp(day['time'])
            if date.weekday() >= 5:
                if day["temperatureHigh"] <= 82 and day["temperatureLow"] >= 30:
                    if float(day['precipProbability']) <= 0.1:
                        if day["windSpeed"] <= 6:
                            # for_check.append(day)
                            plan.append((date, distance, area_name, state))
    # print(for_check)
    if len(plan) > 0:
        for spot in plan:
            print(f"{spot[2]}, {spot[3]} (distance: {spot[1]} miles) is good on {spot[0].strftime('%b-%d (%a)')}")
    else:
        print("It's not a good time to climb outdoors.")

get_forecast()
