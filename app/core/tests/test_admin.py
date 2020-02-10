from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse 

class AdminSiteTests(TestCase):
    # Create a setup function that will be executed everytime a test function is called 
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@mcbh.com',
            password='password123'
        )
        # Use the client helper function that will allow the user to login with the django auth
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@mcbh.com',
            password='password1234',
            name='MCBH Test'
        )

    def test_users_listed(self):
        """Test that userse are listed on user page"""
        url = reverse('admin:core_user_changelist')
        # res uses the test client to perform an HTTP get on the url 
        res = self.client.get(url)

        # Will return a 200 result to confirm that 
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1 
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page renders correctly"""
        url = reverse('admin:core_user_add')
        # /admin/core/user/1 
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)