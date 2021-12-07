from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print('Created')
        UserProfile.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    # because user is onetoone field, the userprofile may not exist.
    try:
        instance.userprofile.save()
    except ObjectDoesNotExist:
        UserProfile.objects.create(user = instance)
