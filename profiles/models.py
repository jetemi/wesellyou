'''Models for 'profiles' app - user profile'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField

# Create your models here.
class UserProfile(models.Model):
    """
    User Profile model, extending User model with onetoone relationship.
    1. Saves default delivery info - fields optional as don't need to save.
    2. Show order history - user profile attached to orders when created.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Choose country from dropdown', null=True, blank=True)

    def __str__(self):
        '''string method, return user name'''
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    '''
    Create instance of UserProfile each time instance of User is created.
    Update UserProfile when User is updated.
    Only one signal so including in model file instead of signals.py file.
    '''
    
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()