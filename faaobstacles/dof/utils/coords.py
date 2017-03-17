import math

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

        for i in range( len(self.__airports) - 1 ):
            self.__leg_indexes.append( (start, end,) )
            start += 1
            end += 1

    # Calculate points for each leg in the trip. With the slope of the line
    # between the two points in the leg you can use trig to get the coordinate
    # changes that need to get applied to the coordinates.
    def __calculate_legs(self):
        for leg_index in list(self.__leg_indexes):

            start_airport = self.__airports[ leg_index[0] ]
            end_airport = self.__airports[ leg_index[1] ]

            coords = [point for point in self.__generate_coordinates(
                start_airport, end_airport
            )]

            for i in coords:
                print("{0},{1}".format(i[0],i[1]))


    # This generator will build the list of coordinates that we can query
    # against the database to build the collection of Obstacles.
    def __generate_coordinates(self, start_location, end_location, increment_miles=2):
        results = []

        # Step that we will use to increment our h
        degrees_increment = increment_miles * 0.0144927

        start = start_location.location.get_coords()
        end = end_location.location.get_coords()

        distance_to_travel = math.sqrt(
            math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2)
        )

        distance_traveled = 0.00

        # Calculate slope and theta
        theta = math.atan( (end[1] - start[1]) / (end[0] - start[0]) )
        slope_x_dir = -1 if (start[0] > end[0]) else 1
        slope_y_dir = -1 if (start[1] > end[1]) else 1

        while distance_traveled < distance_to_travel:
            calculated_delta = (math.cos(theta) * distance_traveled * slope_x_dir, math.sin(theta) * distance_traveled * slope_y_dir,)
            new_point = (start[0]+calculated_delta[0], start[1]+calculated_delta[1],)

            results.append(new_point)

            distance_traveled += degrees_increment

            if abs(distance_traveled) >= distance_to_travel:
                break

        results.append(end)

        return results

    # Entrypoint to calculate the points and pull the nearby Obstacles from the
    # backend.
    def calculate(self):

        self.__get_legs()
        self.__calculate_legs()
