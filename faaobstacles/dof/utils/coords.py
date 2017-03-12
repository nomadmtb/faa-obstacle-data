
def deg_min_sec_to_decimal(deg, min, sec):
    direction = 1.0
    if sec.endswith( ('S', 'W',) ):
        direction = -1.0
    seconds = float(sec[:len(sec)-1])
    return (deg + (min/60.0) + (seconds/3600.0)) * direction


class RouteCalculator(object):

    def __init__(self, airports):

        self.__route = airports

    def get_nearby_objects(self):
        return None
