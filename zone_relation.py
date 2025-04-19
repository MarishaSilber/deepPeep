import os
import openrouteservice
from shapely.geometry import shape
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

mAPI_KEY= os.getenv("MAP_API_KEY")


def calculate_coverage(target_coords, target_time, cand_coords, cand_time, api_key=mAPI_KEY, profile='foot-walking'):
    """
    Calculate the coverage ratio of intersection area between two isochrones to target isochrone area.

    Args:
        target_coords: Tuple of (lon, lat) for target location
        target_time: Time in minutes for target isochrone
        cand_coords: Tuple of (lon, lat) for candidate location
        cand_time: Time in minutes for candidate isochrone
        api_key: OpenRouteService API key
        profile: Transportation profile (default: 'foot-walking')

    Returns:
        float: Ratio of intersection area to target area
    """
    client = openrouteservice.Client(key=api_key)

    # Convert minutes to milliseconds
    target_time_ms = target_time * 60
    cand_time_ms = cand_time * 60

    # Get target isochrone
    target_iso = client.isochrones(
        locations=[target_coords],
        profile=profile,
        range=[target_time_ms],
        units='m',
        location_type='start',
        interval=target_time_ms
    )

    # Get candidate isochrone
    cand_iso = client.isochrones(
        locations=[cand_coords],
        profile=profile,
        range=[cand_time_ms],
        units='m',
        location_type='start',
        interval=cand_time_ms
    )

    # Convert to Shapely polygons
    target_poly = shape(target_iso['features'][0]['geometry'])
    cand_poly = shape(cand_iso['features'][0]['geometry'])

    # Calculate areas and intersection
    target_area = target_poly.area
    intersection_area = target_poly.intersection(cand_poly).area

    return intersection_area / target_area
