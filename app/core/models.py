from django.db import models

# Requirements to extend the Django model
# import the abstract base user 
# import the base user manager 
# import the permissions mixing 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    # **extra_fields allows us to not have to specify additional fields 
    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email: 
            raise ValueError('The user must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    # Creating a super user of the application 
    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        # user the create user method to create superuser 
        user              = self.create_user(email, password)
        user.is_staff     = True
        user.is_superuser = True
        user.save(using=self._db)
        return user  

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email           = models.EmailField(max_length=255, unique=True)
    name            = models.CharField(max_length=255)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    # Assign the user manager to the object attribute 
    objects         = UserManager()

    

