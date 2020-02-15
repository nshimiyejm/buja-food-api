import time 

from django.db import connections 
from django.db.utils import OperationalError 
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    # This function contains data that is used when the management command is called

    def handle(self, *args, **options):
        # Print content to the screen as standard output 
        self.stdout.write('Waiting for database...')

        db_conn = None
        while not db_conn: 
            try: 
                db_conn = connections['default']
            except OperationalError: 
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # Use the success to style the message in green that the connection was successful 
        self.stdout.write(self.style.SUCCESS('Database available!'))