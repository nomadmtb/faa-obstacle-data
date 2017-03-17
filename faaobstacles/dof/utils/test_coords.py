from .coords import RouteCalculator
from dof.models import Airport

def test():
    route = [
        Airport.objects.get(iata="RDD"),
        Airport.objects.get(iata="SEA"),
        Airport.objects.get(iata="AUS"),
        Airport.objects.get(iata="JFK"),
    ]

    calculator = RouteCalculator(route)
    calculator.calculate()
