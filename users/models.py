from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
#User model
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

#Group fitness class model
class GroupFitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()

    #only admin account can create group  fitness class
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})

    def __str__(self):
        return f"{self.title} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def spots_left(self):
        booked = self.bookings.count()
        return self.capacity - booked

    @property
    def booked_count(self):
        return self.bookings.count()

class Booking(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'member'})
    fitness_class = models.ForeignKey(GroupFitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member.username} booked {self.fitness_class.title}"