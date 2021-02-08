from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    '''Model for User Profiles'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        '''Method for string representation'''
        return str(f'{self.user.username} profile')
