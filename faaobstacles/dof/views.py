from django.shortcuts import render
from django.views import View
from .models import Airport
from dof.utils.coords import RouteCalculator
from django.http import JsonResponse


# Create your views here.
class CalculateRouteView(View):

    def get(self, request):
        raw_path = request.GET.get('route', None)
        airport_results = None

        if raw_path:
            airport_results = self.__get_airport_route(raw_path)

            if airport_results['malformed']:
                return self.MALFORMED_AIRPORT_RESPONSE(airport_results)

            elif len(airport_results['airports']) == 1:
                return self.SINGLE_AIRPORT_RESPONSE()

            elif airport_results['airports']:

                my_route = RouteCalculator(airport_results['airports']).calculate()

                return self.SUCCESSFUL_QUERY_RESPONSE(my_route)

        else:
            return self.MISSING_PATH_RESPONSE()

        return self.GENERAL_ERROR_RESPONSE()


    # Merge and cleanup the raw_route string to an acceptable array of airport
    # codes.
    def __validate_codes(self, raw_route):

        codes = raw_route.split(',')
        codes = [code.upper().lstrip().rstrip() for code in codes]

        # we also want to remove two airport codes that appear next to eachother.
        for i in range(len(codes) - 1):
            if codes[i] == codes[i+1]:
                codes[i] = None

        codes = [c for c in codes if c]

        return codes[:5]

    # Get the airport objects with the parsed airport codes from the HTTP Get
    # params. Build dictionary of results in case some don't resolve.
    def __get_airport_route(self, raw_route):

        results = {
            'airports': [],
            'malformed': [],
        }

        codes = self.__validate_codes(raw_route)

        if codes:

            codes = [code.upper().strip() for code in codes]
            codes = codes[:5]
            unique_codes = set()

            for code in codes:

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

        return results


    def MALFORMED_AIRPORT_RESPONSE(self, airports):
        airports['status'] = False
        airports['description'] = 'Non-existent airport codes detected'
        airports['airports'] = [a.iata if hasattr(a, 'iata') else None for a in airports['airports']]
        return JsonResponse(airports, status=406)

    def SUCCESSFUL_QUERY_RESPONSE(self, airports):
        airports['obstacles'] = [obs.to_dict for obs in airports['obstacles']]
        airports['airports'] = [a.to_dict for a in airports['airports']]
        airports['status'] = True
        airports['description'] = 'Successfull calculation'
        return JsonResponse(airports, status=200)

    def MISSING_PATH_RESPONSE(self):
        data = {}
        data['status'] = False
        data['description'] = 'Missing airport path'
        return JsonResponse(data, status=406)

    def SINGLE_AIRPORT_RESPONSE(self):
        data = {}
        data['status'] = False
        data['description'] = 'Route must be more than one known airport code'
        return JsonResponse(data, status=406)

    def GENERAL_ERROR_RESPONSEs(self):
        data = {}
        data['status'] = False
        data['description'] = 'Unknown error occurred'
        return JsonResponse(data, status=406)
