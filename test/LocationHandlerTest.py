from src.LocationHandler import LocationHandler


class LocationHandlerTest:
    def __init__(self):
        self.locHandler = LocationHandler()  # Create the LocationHandler
        # Invoke all the tests
        self.getDistanceTest()



    def getDistanceTest(self):
        """Tests the getDistance() function with various values."""
        addresses = ["9790 Dragonfly Dr, Frisco, TX",
                     "11560 Glen Rose Dr, Frisco, TX",
                     "750 Synergy Park Blvd, Richardson, TX"]
        print(self.locHandler.getDistance(addresses[0], addresses[1]))
        print(self.locHandler.getDistance(addresses[1], addresses[2]))


LocationHandlerTest()
