from django.db.models import Q
from dof.models import Obstacle
import math, pdb


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

    # Init our calculator class. The distance you can see at 35,000 feet is
    # about 230 miles in each direction.
    def __init__(self, airports, search_radius_mi=230, query_point_resolution_mi=75):
        self.__query_point_resolution_mi = query_point_resolution_mi
        self.__search_radius_miles = search_radius_mi
        self.__airports = airports
        self.__query_set = Q()
        self.__query_points = []
        self.__leg_indexes = []
        self.__results = []

        self.__DEGREES_TO_MILES = 0.0144927

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

        for leg_index in range(len(self.__leg_indexes)):

            self.__query_points.append([])

            start_airport = self.__airports[ self.__leg_indexes[leg_index][0] ]
            end_airport = self.__airports[ self.__leg_indexes[leg_index][1] ]

            coords = [point for point in self.__generate_coordinates(
                start_airport, end_airport
            )]

            for i in coords:
                self.__query_points[ leg_index ].append(i)


    # This function will build the list of coordinates that we can query
    # against the database to build the collection of Obstacles.
    def __generate_coordinates(self, start_location, end_location, increment_miles=230):
        results = []

        # Step that we will use to increment our h
        degrees_increment = self.__query_point_resolution_mi * self.__DEGREES_TO_MILES

        start = start_location.location
        end = end_location.location

        distance_to_travel = math.sqrt(
            math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2)
        )

        distance_traveled = 0.00

        # Calculate slope and theta
        theta = math.atan( (end[1] - start[1]) / (end[0] - start[0]) )

        is_decreasing = 1 if end[1] > start[1] else -1
        direction = -1*is_decreasing if (math.degrees(theta) < 0.00) else 1*is_decreasing


        while distance_traveled < distance_to_travel:

            calculated_delta = (math.cos(theta) * distance_traveled, math.sin(theta) * distance_traveled,)
            new_point = (start[0]+(calculated_delta[0] * direction), (start[1]+calculated_delta[1] * direction),)

            results.append(new_point)

            distance_traveled += degrees_increment

            if abs(distance_traveled) >= distance_to_travel:
                break

        results.append(end)

        return results

    # This function will build the appropriate query_set to match the Obstacles
    # in the database. Will use filter() on this set to pull Obstacles along the
    # route.
    def __build_query_set(self):

        for leg_index in range(len(self.__query_points)):

            start_point = self.__query_points[leg_index][0]
            end_point = self.__query_points[leg_index][-1]

            # Want a 25% overlap on filters. If floor is < 1 set h_offset to 1.
            h_offset = 0.00
            if math.floor(self.__search_radius_miles * 0.25) < 1:
                h_offset = 1
            else:
                h_offset = math.floor(self.__search_radius_miles * 0.25)

            theta = math.atan( (end_point[1] - start_point[1]) / (end_point[0] - start_point[0]) )
            calculated_delta = (abs(math.cos(theta) * h_offset), abs(math.sin(theta) * h_offset),)

            # Change the calculated_delta from miles to degrees...
            calculated_delta = (calculated_delta[0] * self.__DEGREES_TO_MILES, calculated_delta[1] * self.__DEGREES_TO_MILES,)

            for point in self.__query_points[ leg_index ]:
                # point = (5.343234234, -122.123123212)
                new_q = Q(
                    latitude__gte=(point[0] - calculated_delta[0]),
                    latitude__lte=(point[0] + calculated_delta[0]),
                    longitude__gte=(point[1] - calculated_delta[1]),
                    longitude__lte=(point[1] + calculated_delta[1]),
                )

                # append new Q to our query_set
                self.__query_set.add(new_q, Q.OR)


    # Use the generated query_set to pull the appropriate Obstacles from the
    # backend model.
    def __get_obstacles(self):

        result = {}

        result['leg_indexes'] = self.__leg_indexes
        result['airports'] = self.__airports

        result['obstacles'] = Obstacle.objects.filter(self.__query_set).distinct()

        return result


    # Entrypoint to calculate the points and pull the nearby Obstacles from the
    # backend.
    def calculate(self):

        self.__get_legs()
        self.__calculate_legs()
        self.__build_query_set()

        return self.__get_obstacles()
