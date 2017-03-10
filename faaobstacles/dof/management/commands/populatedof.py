from django.core.management.base import BaseCommand, CommandError
from dof.models import Obstacle

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

        for raw_line in dof_file:
            self.stdout.write(raw_line)

            id = int((raw_line[3:9]).rstrip())
            country = (raw_line[12:14]).rstrip()
            state = (raw_line[15:17]).rstrip()
            city = (raw_line[18:35]).rstrip()

            lat_deg = int((raw_line[35:37]).rstrip())
            lat_min = int((raw_line[38:40]).rstrip())
            lat_sec = float((raw_line[41:46]).rstrip())

            long_deg = int((raw_line[48:51]).rstrip())
            long_min = int((raw_line[52:54]).rstrip())
            long_sec = float((raw_line[55:60]).rstrip())

            type_desc = (raw_line[62:74]).rstrip())
            quantity = int(raw_line[75])
            agl_height = int((raw_line[77:82]).rstrip())
            amsl_height = int((raw_line[83:88]).rstrip())
            lighting = (raw_line[89]).rstrip()

            horizontal_accuracy = YOU ARE HERE


        dof_file.close()


    def handle(self, *args, **options):
        self.__process_dof_file(options['dof_filepath'][0])
