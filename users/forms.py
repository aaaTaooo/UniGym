import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from users.models import CustomUser, Availability, GroupFitnessClass, TrainerProfile, MemberProfile


# Member registration form
class GymMemberRegistrationForm(UserCreationForm):
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)
    fitness_goal = forms.CharField(required=False, max_length=100)
    height = forms.FloatField(required=False, help_text='Height in cm')
    weight = forms.FloatField(required=False, help_text='Weight in kg')
    emergency_contact_name = forms.CharField(required=False)
    emergency_contact_phone = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'member'
        user.is_approved = False
        if commit:
            user.save()
            MemberProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                email=self.cleaned_data.get('email'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                gender=self.cleaned_data.get('gender'),
                fitness_goal=self.cleaned_data.get('fitness_goal'),
                height=self.cleaned_data.get('height'),
                weight = self.cleaned_data.get('weight'),
                emergency_contact_name = self.cleaned_data.get('emergency_contact_name'),
                emergency_contact_phone = self.cleaned_data.get('emergency_contact_phone'),
            )
        return user

# Trainer registration form
class PersonalTrainerRegistrationForm(UserCreationForm):
    bio = forms.CharField(required=False)
    specialization = forms.CharField(max_length=100, required=False)
    price_per_hour = forms.FloatField(required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    certifications = forms.CharField(widget=forms.Textarea, required=False)
    years_of_experience = forms.IntegerField(required=False)
    languages = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'trainer'
        user.is_approved = False
        if commit:
            user.save()
            TrainerProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio'),
                specialization=self.cleaned_data.get('specialization'),
                price_per_hour=self.cleaned_data.get('price_per_hour'),
                email=self.cleaned_data.get('email'),
                phone=self.cleaned_data.get('phone'),
                certifications=self.cleaned_data.get('certifications'),
                years_of_experience=self.cleaned_data.get('years_of_experience'),
                languages=self.cleaned_data.get('languages'),
                gender=self.cleaned_data.get('gender'),
            )
        return user

# Member Update profile form
class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            'email',
            'phone',
            'fitness_goal',
            'height',
            'weight',
            'emergency_contact_name',
            'emergency_contact_phone',
        ]

# Trainer update profile form
class TrainerUpdateForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = [
            'bio',
            'specialization',
            'price_per_hour',
            'photo',
            'email',
            'phone',
            'certifications',
            'years_of_experience',
            'languages',
        ]

# Admin create group fitness class form
class GroupFitnessClassForm(forms.ModelForm):
    class Meta:
        model = GroupFitnessClass
        fields = ['title', 'description', 'date',
                  'location', 'capacity', 'duration',
                  'difficulty','equipment', 'trainer', 'status']
        widgets = {'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                   'description':forms.Textarea(attrs={'rows': 3}),}

    # Avoid choose date from the past
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now():
            raise forms.ValidationError('You cannot select a past date or time.')
        return date

# Trainer update availability form
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time', 'is_available']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if date:
            date_datetime = datetime.datetime.combine(date, datetime.time.min, tzinfo=timezone.get_current_timezone())
            if date_datetime < timezone.now():
                self.add_error('date', 'Date cannot be in the past')

        if start_time and end_time:
            if end_time <= start_time:
                self.add_error('end_time', 'End time must be after start time')

        return cleaned_data
