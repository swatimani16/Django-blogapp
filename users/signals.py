#this signal gets fired after an object gets saved
from django.db.models.signals import post_save
#We want a post_save signal once a user gets created
from django.contrib.auth.models import User
#we will create a reciever function which will recieve this signal and performs some task
from django.dispatch import receiver
#import the profile because we want to create a new profile inside of the recieve function
from .models import Profile 

@receiver(post_save, sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)
        

@receiver(post_save, sender = User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()
        