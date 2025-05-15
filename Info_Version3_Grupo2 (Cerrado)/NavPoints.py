import math
from node import Node

class NavPoint(Node):
    def __init__(self, number: int, name: str, lat: float, lon: float):
        self.number = number
        self.lat = lat
        self.lon = lon

        x = lon * math.cos(math.radians(lat))
        y = lat

        self.name = name
        self.x = x
        self.y = y