from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import GymMemberRegistrationForm, PersonalTrainerRegistrationForm
from users.models import GroupFitnessClass, Booking


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

                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'member':
                    return redirect('member_dashboard')
                elif user.role == 'trainer':
                    return redirect('trainer_dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Your registration is not approved yet.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request,'users/login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def member_dashboard(request):
    available_classes = GroupFitnessClass.objects.exclude(bookings__member=request.user).order_by('date')
    booked_classes = GroupFitnessClass.objects.filter(bookings__member=request.user).order_by('date')
    return render(request, 'users/member_dashboard.html', {'available_classes':available_classes,
                                                           'booked_classes':booked_classes})

@login_required
def trainer_dashboard(request):
    return render(request, 'users/trainer_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

#group class list for gym member
@login_required
def group_fitness_list(request):
    classes = GroupFitnessClass.objects.all().order_by('date')
    return render(request, 'fitness/group_fitness_list.html', {'classes':classes})

#booking group class
@login_required
def book_class(request, class_id):
    fitness_class = get_object_or_404(GroupFitnessClass, id=class_id)

    if fitness_class.spots_left <= 0:
        messages.error(request, 'Sorry, this class is already full.')
        return redirect('member_dashboard')

    #booking and avoid double booking
    booking, created = Booking.objects.get_or_create(member = request.user, fitness_class = fitness_class)
    if not created:
        messages.warning(request, 'You already booked this class.')
    else:
        messages.success(request, f'Your booking of {fitness_class.title} was successful.')

    return redirect('member_dashboard')

@login_required
def cancel_booking(request, class_id):
    fitness_class = get_object_or_404(GroupFitnessClass, id=class_id)
    booking = Booking.objects.filter(member = request.user, fitness_class = fitness_class).first()

    if booking:
        booking.delete()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.warning(request, 'Booking cancel failed.')

    return redirect('member_dashboard')