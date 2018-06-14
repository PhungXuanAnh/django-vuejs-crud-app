from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import BaseRunserverCommand
from django.conf import settings

class Command(BaseRunserverCommand):
    
    def add_arguments(self, parser):    
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--dev',
            action='store_true',
            dest='dev',
            help='Start dev server',
        )

    def handle(self, *args, **options):
        if options['dev']:
            self.stdout.write("_________________dev")
            # settings.IS_PRODUCTION = False  
        self.stdout.write('___________________xuananh')
        super(Command, self).handle(*args, **options)