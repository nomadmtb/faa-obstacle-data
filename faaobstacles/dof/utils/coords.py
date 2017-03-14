def deg_min_sec_to_decimal(deg, min, sec):
    direction = 1.0
    if sec.endswith( ('S', 'W',) ):
        direction = -1.0
    seconds = float(sec[:len(sec)-1])
    return (deg + (min/60.0) + (seconds/3600.0)) * direction


# A RouteCalculator will take a set of airports and calculate the nearby
# Obstacles for each leg of the trip. Will return a dictionary with the results
# for each leg.
class RouteCalculator(object):

    # Init our calculator class
    def __init__(self, airports):
        self.__airports = airports
        self.__leg_indexes = []
        self.__results = []

    # Calculate the legs of the trip. We can calculate distances for each of
    # these. These are indexes into the self.__airports array.
    def __get_legs(self):
        start = 0
        end = 1

        for i in range( len(self.__airports) ):
            self.__leg_indexes.append( (start, end,) )
            start += 1
            end += 1

    # Calculate points for each leg in the trip. With the slope of the line
    # between the two points in the leg you can use trig to get the coordinate
    # changes that need to get applied to the coordinates.
    def __calculate_legs(self):
        for leg_index in self.__leg_indexes:
            start_airport = self.__airports[ leg_index[0] ]
            end_airport = self.__airports[ leg_index[1] ]


    # Entrypoint to calculate the points and pull the nearby Obstacles from the
    # backend.
    def calculate(self):

        self.__get_legs()
        self.__calculate_legs()
