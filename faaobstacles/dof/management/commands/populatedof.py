from django.core.management.base import BaseCommand, CommandError
from dof.models import Obstacle
from dof.utils import conversions as conv
from dof.utils import coords

class Command(BaseCommand):
    help = 'Deletes and reloads all of the DOF Obstacle data'

    def add_arguments(self, parser):
        parser.add_argument('dof_filepath', nargs=1, type=str)

    def __process_dof_file(self, dof_filepath):
        dof_file = None

        try:
            dof_file = open(dof_filepath, 'r')
        except:
            raise
            raise CommandError(
                "Can't open the dof dat file @ {0}".format(
                    dof_filepath
                )
            )

        Obstacle.objects.all().delete()

        rows_added = 0

        for raw_line in dof_file:
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

            data['lat'] = coords.deg_min_sec_to_decimal(
                lat_deg, lat_min, lat_sec
            )
            data['long'] = coords.deg_min_sec_to_decimal(
                long_deg, long_min, long_sec
            )

            new_obstacle = Obstacle(**data)
            new_obstacle.save()

            rows_added = rows_added + 1

            self.stdout.write(200*"\n")
            self.stdout.write("Processed {0} obstacles".format(rows_added))


        dof_file.close()


    def handle(self, *args, **options):
        self.__process_dof_file(options['dof_filepath'][0])
