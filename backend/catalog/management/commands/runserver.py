from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands.runserver import BaseRunserverCommand
from django.conf import settings

"""
CHU Y : 
    lenh nay chi chay khi app 'catalog' duoc khai bao truoc app ''django.contrib.staticfiles' 
    trong INSTALL_APPS trong settings.py

    vi app 'django.contrib.staticfiles' cung override lenh 'runserver' nen no se dung lenh 'runserver'
    khai bao trong app nay
"""

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