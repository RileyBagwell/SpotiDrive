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
                     "750 Synergy Park Blvd, Richardson, TX",
                     "3736 Virginia Beach Blvd, Virginia Beach, VA",
                     "1155 Union Cir, Denton, TX"]
        i = 1
        while (i < len(addresses)):
            print(self.locHandler.getDistance(addresses[i], addresses[i-1]))
            i += 1


LocationHandlerTest()
