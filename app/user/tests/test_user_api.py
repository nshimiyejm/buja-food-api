from django.test import TestCase 
from django.contrib.auth import get_user_model
from django.urls import reverse 

from rest_framework.test import APIClient
from rest_framework import status


# Value will not change 
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

# Unauthenticated 
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    # Create new user 
    def test_create_valid_user_success(self):
        """Test create user with valid payload is successful"""
        payload = {
            'email': 'jmn@mcbh.com',
            'password': '1234545', 
            'name': 'jmn',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', res.data)

    # Create a duplicate user 
    def test_user_exisits(self):
        """Test creating a user the already exits"""
        payload = {
            'email':'jmn@mcbh.com',
            'password':'1234545', 
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    # Password is too short 
    def test_password_too_short(self):
        """Test that the password must be more than 8 characters"""
        payload = {
            'email':'jmn@mcbh.com',
            'password':'12', 
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exits = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exits)


    # Create Authentication Tokens 

    # Create a success token creation 
    def test_create_token_for_user(self):
        """Test that the token is created for a user"""
        payload = {
            'email':'jmn@mcbh.com',
            'password':'1234545', 
        }

        # Create a user that will be tested 
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response is 200
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK) 

    # Check if invalid cred
    def test_create_token_invalid_credentials(self):
        """Test that the token is not created if invalid creds are passed"""
        create_user(email='jmn@mcbh.com', password='12345')
        payload = {'email': 'jmn@mcbh.com', 'password':'wrong'}

        # Get a bad request 
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response is 400 
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    # Check if user doesn't exist request 
    def test_create_token_no_user(self):
        """Test that the token is not created if user doesn't exits"""
        payload = {'email': 'jmn@mcbh.com', 'password':'12345'}

        # Get a bad request 
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response is 400 
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    # Check if password was not provided 
    def test_create_token_missing_feild(self):
        """Test that email and password are rtequired to create the token"""
        payload = {'email': 'jmn@mcbh.com', 'password':''}

        # Get a bad request 
        res = self.client.post(TOKEN_URL, payload)

        # Assert that the response is 400 
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test that the authtentication is required for the endpoint 
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# Add authenticated requests to the endpoint 
# Private classes will require authentication before the endpoints can be used 
class PrivateUserApiTests(TestCase):
    """Test API requests that require the user to be authenticated"""

    def setUp(self):
        self.user = create_user(
            email = 'jmn@mcbh.com',
            password = '12345', 
            name = 'name' 
        )

        self.client = APIClient()
        # Use the force auth function to require the user to authenticate
        # By simulating authentication requests  
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name, 
            'email':self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {'name': 'new name', 'password':'newpassword'}

        # Use patch instead of post 
        res = self.client.patch(ME_URL, payload)

        # update user data
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
