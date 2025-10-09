from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),


    path('register/gym_member/', views.gm_register, name='gm_register'),
    path('register/personal_trainer/', views.pt_register, name='pt_register'),

    # Member dashboard urls
    path('dashboard/member/', views.member_dashboard, name='member_dashboard'),
    path('dashboard/member/class/', views.member_class, name='member_class'),
    path('dashboard/member/bookings/', views.member_booking, name='member_booking'),
    path('dashboard/member/book/<int:class_id>/', views.book_class, name='book_class'),
    path('dashboard/member/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/member/trainers/', views.member_trainer_list, name="member_trainer_list"),
    path('dashboard/member/trainers/<int:trainer_id>/', views.member_trainer_detail, name='member_trainer_detail'),
    path('dashboard/member/update', views.update_member_profile, name='update_member_profile'),


    # Trainer dashboard urls
    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('dashboard/trainer/class/', views.trainer_class, name='trainer_class'),
    path('dashboard/trainer/availability/', views.trainer_availability, name='trainer_availability'),
    path('dashboard/trainer/update/', views.update_trainer_profile, name='update_trainer_profile'),


    # Admin dashboard urls
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/application', views.manage_pending_user, name='manage_pending_user'),
    path('dashboard/admin/classes/', views.manage_group_fitness_class, name='manage_group_fitness_class'),
    path('dashboard/admin/classes/add/', views.add_group_fitness_class, name='add_group_fitness_class'),
    path('dashboard/admin/classes/edit/<int:class_id>/', views.edit_group_fitness_class, name='edit_group_fitness_class'),
    path('dashboard/admin/classes/delete/<int:class_id>/', views.delete_group_fitness_class, name='delete_group_fitness_class'),
    path('dashboard/admin/boookings/', views.view_bookings, name='view_bookings'),
    path('dashboard/admin/bookings/<int:booking_id>/cancel/', views.admin_cancel_booking, name='admin_cancel_booking'),


    # path('fitness/book/<int:class_id>/', views.book_class, name='book_class'),


]