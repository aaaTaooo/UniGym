from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/gym_member/', views.gm_register, name='gm_register'),
    path('register/personal_trainer/', views.pt_register, name='pt_register'),

    path('dashboard/member/', views.member_dashboard, name='member_dashboard'),
    path('dashboard/member/book/<int:class_id>/', views.book_class, name='book_class'),
    path('dashboard/member/cancel/<int:class_id>/', views.cancel_booking, name='cancel_booking'),
    path('dashboard/trainer/', views.trainer_dashboard, name='trainer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    #path('fitness/classes/', views.group_fitness_list, name='group_fitness_list'),
    #path('fitness/book/<int:class_id>/', views.book_class, name='book_class'),

    path('logout/', views.custom_logout, name='logout'),
]