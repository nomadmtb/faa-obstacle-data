from .coords import RouteCalculator
from dof.models import Airport

def test():
    route = [
        Airport.objects.get(iata="RDD"),
        Airport.objects.get(iata="SFO"),
        Airport.objects.get(iata="AUS"),
        #Airport.objects.get(iata="AUS"),
        #Airport.objects.get(iata="JFK"),
        #Airport.objects.get(iata="SEA"),
    ]

    calculator = RouteCalculator(route)
    return calculator.calculate()
