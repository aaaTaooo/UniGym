from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from users.forms import GymMemberRegistrationForm, PersonalTrainerRegistrationForm, GroupFitnessClassForm
from users.models import GroupFitnessClass, Booking, TrainerProfile, Availability, CustomUser, MemberProfile
from .forms import AvailabilityForm


# Create your views here.
# registration page
def gm_register(request):
    if request.method == 'POST':
        form = GymMemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'member':
                MemberProfile.objects.create(user=user)
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
    trainer_profile = request.user.trainer_profile
    availabilities = trainer_profile.availabilities.all()
    form = None

    if request.method == 'POST':
        #Delete availability
        if 'delete_id' in request.POST:
            availability_id = request.POST.get('delete_id')
            availability = get_object_or_404(Availability, id=availability_id, trainer=trainer_profile)
            availability.delete()
            return redirect('trainer_dashboard')

        #Edit availability
        elif'edit_id' in request.POST:
            availability_id = request.POST.get('edit_id')
            availability = get_object_or_404(Availability, id=availability_id, trainer=trainer_profile)
            form = AvailabilityForm(instance=availability)

        #Add and update availability
        elif 'availability_id' in request.POST or 'date' in request.POST:
            availability_id = request.POST.get('availability_id')
            if availability_id:
                availability = get_object_or_404(Availability, id=availability_id, trainer=trainer_profile)
                form = AvailabilityForm(request.POST, instance=availability)
            else:
                form = AvailabilityForm(request.POST)

            if form.is_valid():
                availability = form.save(commit=False)
                availability.trainer = trainer_profile
                availability.save()
                return redirect('trainer_dashboard')

    if not form:
        form = AvailabilityForm()

    return render(request, 'users/trainer_dashboard.html', {"trainer_profile": trainer_profile,
                                                                "availabilities": availabilities,
                                                                "form": form, })

def admin_check(user):
    return user.is_authenticated and user.role == 'admin'

def get_admin_stats():
    return {
        "stats": {
            "total_users": CustomUser.objects.count(),
            "total_trainers": TrainerProfile.objects.count(),
            "total_members": CustomUser.objects.filter(role='member').count(),
            "total_bookings": Booking.objects.count(),
            "total_classes": GroupFitnessClass.objects.count(),
        },
        "pending_members": MemberProfile.objects.filter(is_approved=False),
        "pending_trainers": TrainerProfile.objects.filter(is_approved=False),
    }
@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):
    context = get_admin_stats()

    if request.method == 'POST':
        if "approve_member" in request.POST:
            member_id = request.POST.get('approve_member')
            member = get_object_or_404(MemberProfile, id=member_id)
            member.is_approved = True
            member.save()
        elif "reject_member" in request.POST:
            member_id = request.POST.get('reject_member')
            member = get_object_or_404(MemberProfile, id=member_id)
            member.delete()
        elif "approve_trainer" in request.POST:
            trainer_id = request.POST.get('approve_trainer')
            trainer = get_object_or_404(TrainerProfile, id=trainer_id)
            trainer.is_approved = True
            trainer.save()
        elif "reject_trainer" in request.POST:
            trainer_id = request.POST.get('reject_trainer')
            trainer = get_object_or_404(TrainerProfile, id=trainer_id)
            trainer.delete()

        return redirect('admin_dashboard')
    return render(request, 'users/admin_dashboard.html', context)

#Group fitness class management for admin
@login_required
@user_passes_test(admin_check)
def manage_group_fitness_class(request):
    classes = GroupFitnessClass.objects.all().order_by('date')
    context = get_admin_stats()
    context['classes'] = classes
    return render(request, 'users/manage_group_fitness_class.html', context)

#Add group fitness class
@login_required
@user_passes_test(admin_check)
def add_group_fitness_class(request):
    context = get_admin_stats()
    if request.method == 'POST':
        form = GroupFitnessClassForm(request.POST)
        if form.is_valid():
            group_class = form.save(commit=False)
            group_class.created_by = request.user
            group_class.save()
            messages.success(request, 'Successfully added a new group fitness class')
            return redirect('manage_group_fitness_class')
    else:
        form = GroupFitnessClassForm()

    context['form'] = form
    context['action'] = 'Add'
    return render(request, 'users/group_fitness_class_form.html', context)

#Edit group fitness class
@login_required
@user_passes_test(admin_check)
def edit_group_fitness_class(request, class_id):
    context = get_admin_stats()
    group_class = get_object_or_404(GroupFitnessClass, id=class_id)
    if request.method == 'POST':
        form = GroupFitnessClassForm(request.POST, instance=group_class)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited group fitness class')
            return redirect('manage_group_fitness_class')
    else:
        form = GroupFitnessClassForm(instance=group_class)

    context['form'] = form
    context['action'] = 'Edit'
    return render(request, 'users/group_fitness_class_form.html', context)

#Delete group fitness class
@login_required
@user_passes_test(admin_check)
def delete_group_fitness_class(request, class_id):
    if request.method == 'POST':
        group_class = get_object_or_404(GroupFitnessClass, id=class_id)
        group_class.delete()
        messages.success(request, 'Successfully deleted group fitness class')
    return redirect('manage_group_fitness_class')

#Managing group fitness classes bookings for Admin
@login_required
@user_passes_test(admin_check)
def view_bookings(request):
    context = get_admin_stats()
    bookings = Booking.objects.select_related('member', 'fitness_class').all().order_by('booked_at')
    context['bookings'] = bookings

    return render(request, 'users/view_bookings.html', context)

@login_required
@user_passes_test(admin_check)
def admin_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking canceled by admin.')
    return redirect('view_bookings')





#group fitness class list for members
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

#cancel group class from member dashboard
@login_required
def cancel_booking(request, class_id):
    fitness_class = get_object_or_404(GroupFitnessClass, id=class_id)
    booking = get_object_or_404(Booking, member=request.user, fitness_class=fitness_class)
    booking.delete()
    messages.success(request, 'Booking canceled.')

    return redirect('member_dashboard')

#trainer profile
def trainer_list(request):
    trainers = TrainerProfile.objects.filter(user__role='trainer', user__is_approved=True)
    return render(request, "users/trainer_list.html", {'trainers':trainers})

def trainer_detail(request, trainer_id):
    trainer_profile = get_object_or_404(TrainerProfile, id=trainer_id)
    availabilities = trainer_profile.availabilities.all()
    return render(request, "users/trainer_detail.html", {"trainer_profile":trainer_profile,
                                                         "availabilities":availabilities})