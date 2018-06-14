from django.core.management.base import BaseCommand, CommandError
"""
    usage: 
        python manage.py hello_world --delete hello_id
    or
        python manage.py hello_world hello_id
    to see the difference
"""

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Django admin custom command hello world make by xuananh.'
 
    def add_arguments(self, parser):
        # Positional arguments      <--------------------- it's required
        parser.add_argument('hello_id')

        # Named (optional) arguments <--------------------- it's not required
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write("________________delete")    
        self.stdout.write("Hello World")

        try:
            # do something
            pass
        except Exception as e:
            raise CommandError(e)