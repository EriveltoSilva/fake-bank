""" signals module"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    """Create a profile when a user is created"""

    if created:
        Profile.objects.create(user=instance, full_name=instance.full_name)
    elif instance.full_name != instance.profile.full_name:
        instance.profile.full_name = instance.full_name
        instance.profile.save()
