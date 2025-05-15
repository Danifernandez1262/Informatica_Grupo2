class NavAirport:
    def __init__(self, name: str):
        self.name = name
        self.sids = []
        self.stars = []

    def add_point(self, point):
        if point.name.endswith(".D"):
            self.sids.append(point)
        elif point.name.endswith(".A"):
            self.stars.append(point)