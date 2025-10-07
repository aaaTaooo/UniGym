from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),


    path('register/gym_member/', views.gm_register, name='gm_register'),
    path('register/personal_trainer/', views.pt_register, name='pt_register'),


    path('dashboard/member/', views.member_dashboard, name='member_dashboard'),
    path('dashboard/member/book/<int:class_id>/', views.book_class, name='book_class'),
    path('dashboard/member/cancel/<int:class_id>/', views.cancel_booking, name='cancel_booking'),


    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),


    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/classes/', views.manage_group_fitness_class, name='manage_group_fitness_class'),
    path('dashboard/admin/classes/add/', views.add_group_fitness_class, name='add_group_fitness_class'),
    path('dashboard/admin/classes/edit/<int:class_id>/', views.edit_group_fitness_class, name='edit_group_fitness_class'),
    path('dashboard/admin/classes/delete/<int:class_id>/', views.delete_group_fitness_class, name='delete_group_fitness_class'),
    path('dashboard/admin/boookings/', views.view_bookings, name='view_bookings'),
    path('dashboard/admin/bookings/<int:booking_id>/cancel/', views.admin_cancel_booking, name='admin_cancel_booking'),


    path('fitness/classes/', views.group_fitness_list, name='group_fitness_list'),
    path('fitness/book/<int:class_id>/', views.book_class, name='book_class'),

    path("trainers/", views.trainer_list, name="trainer_list"),
    path("trainers/<int:trainer_id>/", views.trainer_detail, name='trainer_detail'),
]