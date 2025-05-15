from NavPoints import NavPoint
from Segments import NavSegment
from Airports import NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []

    def load_navpoints(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                number = int(parts[0])
                name = parts[1]
                lat = float(parts[2])
                lon = float(parts[3])
                self.navpoints.append(NavPoint(number, name, lat, lon))

    def load_navsegments(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                origin = int(parts[0])
                destination = int(parts[1])
                distance = float(parts[2])
                self.navsegments.append(NavSegment(origin, destination, distance))

    def load_navairports(self, filename):
        with open(filename, 'r') as f:
            current_airport = None
            for line in f:
                name = line.strip()
                if not name:
                    continue
                if not name.endswith(".D") and not name.endswith(".A"):
                    if current_airport:
                        self.navairports.append(current_airport)
                    current_airport = NavAirport(name)
                else:
                    point = self.get_navpoint_by_name(name)
                    if point and current_airport:
                        current_airport.add_point(point)
            if current_airport:
                self.navairports.append(current_airport)

    def load_all(self, nav_file, seg_file, aer_file):
        self.load_navpoints(nav_file)
        self.load_navsegments(seg_file)
        self.load_navairports(aer_file)

    def get_navpoint_by_number(self, number):
        return next((p for p in self.navpoints if p.number == number), None)

    def get_navpoint_by_name(self, name):
        return next((p for p in self.navpoints if p.name == name), None)

    def get_airport_by_name(self, name):
        return next((a for a in self.navairports if a.name == name), None)