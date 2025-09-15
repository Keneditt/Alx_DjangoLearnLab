# advanced_features_and_security/your_app_name/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Add other fields here as needed
    
    def __str__(self):
        return self.username
    
   # advanced_features_and_security/your_app_name/models.py

from django.db import models
from django.conf import settings

class YourOtherModel(models.Model):
    # This is an example of a foreign key to the custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Add other fields here as needed 