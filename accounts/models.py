from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from universities.models import University  # Import the University model

class Profile(models.Model):
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefer_not_to_say')
    avatar = models.ImageField(upload_to='uploads/avatars', blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    is_university_rep = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'


# ✅ Signal to create Profile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# ✅ Signal to save Profile whenever User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
