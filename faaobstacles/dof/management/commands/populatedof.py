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

            id = int(raw_line[3:8])
            country = YOU ARE HERE

        dof_file.close()


    def handle(self, *args, **options):
        self.__process_dof_file(options['dof_filepath'][0])
