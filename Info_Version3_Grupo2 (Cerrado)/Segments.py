# Segments.py
from segment import Segment

class NavSegment(Segment):
    def __init__(self, origin_number: int, destination_number: int, distance: float):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance
