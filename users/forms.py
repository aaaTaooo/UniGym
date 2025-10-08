from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser, Availability, GroupFitnessClass, TrainerProfile


# Member registration form
class GymMemberRegistrationForm(UserCreationForm):
    age = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'age']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'member'
        user.is_approved = False
        if commit:
            user.save()
        return user

# Trainer registration form
class PersonalTrainerRegistrationForm(UserCreationForm):
    certificate = forms.CharField(max_length=255, required=True)
    experience = forms.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'certificate', 'experience']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'trainer'
        user.is_approved = False
        if commit:
            user.save()
        return user

# Trainer update availability form
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']

# Trainer update profile form
class TrainerUpdateForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['photo', 'price_per_hour', 'specialization' ,'bio', 'email']

# Admin create group fitness class form
class GroupFitnessClassForm(forms.ModelForm):
    class Meta:
        model = GroupFitnessClass
        fields = ['title', 'description', 'date', 'location', 'capacity', 'trainer']
        widgets = {'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}