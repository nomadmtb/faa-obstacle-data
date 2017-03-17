from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point, fromstr
from dof.models import Obstacle, Airport
from dof.utils import conversions as conv
from dof.utils import coords
import csv, progressbar

# This command will drop and reload all Airports and Obstacles from the
# following positional arguments > DOF.DAT FAA file, Airport CSV data.
class Command(BaseCommand):
    help = 'Deletes and reloads all of the DOF Obstacle+Airport data'

    def add_arguments(self, parser):
        parser.add_argument('dof_filepath', nargs=1, type=str)
        parser.add_argument('airport_filepath', nargs=1, type=str)

    def __process_dof_file(self, dof_filepath):
        max_rows = 0

        with open(dof_filepath, 'r') as r_tmp:
            for row in r_tmp:
                max_rows += 1

        bar = progressbar.ProgressBar(max_value=max_rows)

        Obstacle.objects.all().delete()

        with open(dof_filepath, 'r') as dof_file:
            current_row = 0

            for raw_line in bar(dof_file):
                data = {}

                data['id'] = int((raw_line[3:9]).rstrip())
                data['country'] = (raw_line[12:14]).rstrip()
                data['state'] = (raw_line[15:17]).rstrip()
                data['city'] = (raw_line[18:35]).rstrip()

                lat_deg = int((raw_line[35:37]).rstrip())
                lat_min = int((raw_line[38:40]).rstrip())
                lat_sec = (raw_line[41:47]).rstrip()

                long_deg = int((raw_line[48:51]).rstrip())
                long_min = int((raw_line[52:54]).rstrip())
                long_sec = (raw_line[55:61]).rstrip()

                data['type_desc'] = (raw_line[62:74]).rstrip()
                data['quantity'] = int(raw_line[75])
                data['agl_height'] = int((raw_line[77:82]).rstrip())
                data['amsl_height'] = int((raw_line[83:88]).rstrip())
                data['lighting'] = (raw_line[89]).rstrip()

                data['horizontal_accuracy'] = conv.ACCURACY_CODE_TO_FEET[raw_line[91]]
                data['vertical_accuracy'] = conv.ACCURACY_CODE_TO_FEET[raw_line[93]]
                data['mark_indicator'] = raw_line[95]
                data['faa_study_id'] = None if not raw_line[97:111].rstrip() else raw_line[97:111].rstrip()

                data['action'] = (raw_line[112]).rstrip()

                action_date = raw_line[114:121]
                data['action_date'] = conv.julian_to_date(action_date)

                lat = coords.deg_min_sec_to_decimal(
                    lat_deg, lat_min, lat_sec
                )

                long = coords.deg_min_sec_to_decimal(
                    long_deg, long_min, long_sec
                )

                data['location'] = fromstr(
                    "POINT({0} {1})".format(
                        lat, long
                    )
                )

                new_obstacle = Obstacle(**data)
                new_obstacle.save()

                current_row += 1
                bar.update(current_row)


    def __process_airports(self, airport_filepath):
        max_rows = 0

        with open(airport_filepath, 'r') as a_tmp:
            for row in a_tmp:
                max_rows += 1

        bar = progressbar.ProgressBar(max_value=max_rows)

        Airport.objects.all().delete()

        with open(airport_filepath, 'r') as a_file:
            current_row = 0

            reader = csv.reader(a_file)

            for row in bar(reader):
                data = {}

                data['name'] = row[1]
                data['city'] = row[2] if row[2] else None
                data['country'] = row[3] if row[3] else None
                data['iata'] = row[4] if len(row[4]) > 2 else None
                data['icao'] = row[5] if len(row[5]) > 2 else None
                data['altitude'] = int(row[8])

                lat = float(row[6])
                long = float(row[7])

                data['location'] = fromstr(
                    "POINT({0} {1})".format(
                        lat, long
                    )
                )

                new_airport = Airport(**data)
                new_airport.save()

                current_row += 1
                bar.update(current_row)


    def handle(self, *args, **options):
        self.stdout.write('--> Loading Obstacles')
        self.__process_dof_file(options['dof_filepath'][0])

        self.stdout.write('--> Loading Airports')
        self.__process_airports(options['airport_filepath'][0])
