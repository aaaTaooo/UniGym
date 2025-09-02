from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
    ('member', 'Member'),
    ('trainer', 'Trainer'),
    ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='member')
    # for new user registration
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.role})'