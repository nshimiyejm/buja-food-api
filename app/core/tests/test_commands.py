# Use the patch functionality to Mock the behavior of the Django wait for DB 
from unittest.mock import patch

from django.core.management import call_command 
from django.db.utils import OperationalError
from django.test import TestCase

class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # if no operational error then the db is available else it is not 
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')

            # Check that the wait command was called at least once 
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # if no operational error then the db is available else it is not 
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Raise an operational error 5 times 
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            # Check that the wait command was called at least once 
            self.assertEqual(gi.call_count, 6)    
