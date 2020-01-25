from django.test import TestCase
from django.contrib.auth import get_user_model

# Create a test class that will be used to test the Models 
class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email successfully """
        # Setup 
        email = 'test@mcbh.com'
        password = 'test12345'
        user = get_user_model().objects.create_user(
            email = email, 
            password = password
        )


        # Assert
        self.assertEqual(user.email, email)
        # Since the password is encrypted, use true to validate the answer
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email of the new user is normalized"""
        email='test@MCBH.COM'
        user = get_user_model().objects.create_user(email = email, password = 'test12345')

        self.assertEqual(user.email, email.lower())

    def test_new_user_validation(self):
        """Test that an email is being passed"""
        with self.assertRaises(ValueError):
            """Any line beyond this point will bring raise the value error"""
            get_user_model().objects.create_user(None, password = 'test12345')

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        email    = 'testdev@mcbh.com'
        password = 'test12345'
        user     = get_user_model().objects.create_superuser(email = email, password = password)
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

