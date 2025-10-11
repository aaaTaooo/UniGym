
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
# User model
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

# Member Profile model
class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='member_profile')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              blank=True, null=True)
    fitness_goal = models.CharField(max_length=100, blank=True, null=True)
    height = models.FloatField(blank=True, null=True, help_text='Height in cm')
    weight = models.FloatField(blank=True, null=True, help_text='Weight in kg')
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Trainer Profile model
class TrainerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='trainer_profile')
    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    price_per_hour = models.FloatField(blank=True, null=True)
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              blank=True, null=True)

    def __str__(self):
        return self.user.username

#Group fitness class model
class GroupFitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    duration = models.IntegerField(default=30)
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
                                  default='easy')
    equipment = models.CharField(max_length=100, default='None')
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('finished', 'Finished')],default='available')

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

    def check_date(self):
        if self.date < timezone.now() and self.status != 'finished':
            self.status = 'finished'
            self.save(update_fields=['status'])

# Group fitness class booking model
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

# Trainer Availability model
class Availability(models.Model):
    trainer = models.ForeignKey("users.TrainerProfile", on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.trainer.user.username} - {self.date} {self.start_time} - {self.end_time}"
