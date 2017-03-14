from django.shortcuts import render
from django.views import View
from .models import Airport
from dof.utils.coords import RouteCalculator


# Create your views here.
class CalculateRouteView(View):

    def get(self, request):
        raw_path = request.GET.get('route', None)
        airports = None

        if raw_path:
            airports = self.__get_airport_route(raw_path)

        if airports:
            my_route = RouteCalculator(airports)
            my_route.calculate()


        return HttpResponse('result')

    # Get the airport objects with the parsed airport codes from the HTTP Get
    # params. Build dictionary of results in case some don't resolve.
    def __get_airport_route(self, raw_route):

        results = {
            'airports': [],
            'malformed': [],
        }

        for code in raw_route.split(','):
            code = code.upper()

            if code.isalpha() and len(code) < 5:
                new_airport = None

                try:
                    new_airport = Airport.objects.get(iata=code)
                except Airport.DoesNotExist:
                    pass

                if not new_airport:
                    try:
                        new_airport = Airport.objects.get(icao=code)
                    except Airport.DoesNotExist:
                        pass

                if new_airport:
                    results['airports'].append(new_airport)

                else:
                    results['malformed'].append(code)
            else:
                pass

        return results
