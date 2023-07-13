import haversine as hs
from haversine import Unit


def getDifferenceBetweenTwoPoints(location_a : tuple, location_b : tuple) -> float:
    return hs.haversine(location_a, location_b, unit=Unit.KILOMETERS)
