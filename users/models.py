from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


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
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()


    #only admin account can create group  fitness class
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})

    #Each group fitness class need to assign to one personal trainer
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'trainer'},
        related_name='group_classes'
    )
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
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='confirmed')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'member'})
    fitness_class = models.ForeignKey(GroupFitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'fitness_class')

    def __str__(self):
        return f"{self.member.username} booked {self.fitness_class.title}"

class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='member_profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    # membership_end = models.DateField(default=lambda: timezone.now().date() + timedelta(days=365))
    #is_approved = models.BooleanField(default=False)

    # def is_active(self):
    #     from datetime import date
    #     return self.membership_end >= date.today()

    def __str__(self):
        return self.user.username

class TrainerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='trainer_profile')
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    price_per_hour = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    #is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Availability(models.Model):
    trainer = models.ForeignKey("users.TrainerProfile", on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateTimeField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.date} {self.start_time} - {self.end_time}"
