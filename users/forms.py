from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser, Availability, GroupFitnessClass


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

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']

class GroupFitnessClassForm(forms.ModelForm):
    class Meta:
        model = GroupFitnessClass
        fields = ['title', 'description', 'date', 'location', 'capacity']
        widgets = {'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}