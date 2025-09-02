from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from users.forms import GymMemberRegistrationForm, PersonalTrainerRegistrationForm


# Create your views here.
# registration page
def gm_register(request):
    if request.method == 'POST':
        form = GymMemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membership account created successfully! Please wait admin to approve.')
            return redirect('login')
    else:
        form = GymMemberRegistrationForm()
    return render(request,'users/gm_register.html',{'form':form})

def pt_register(request):
    if request.method == 'POST':
        form = PersonalTrainerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trainer account created successfully! Please wait admin to approve.')
            return redirect('login')
    else:
        form = PersonalTrainerRegistrationForm()
    return render(request, 'users/pt_register.html', {'form':form})

# user login page
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_approved:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Your registration is not approved yet.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request,'users/login.html')