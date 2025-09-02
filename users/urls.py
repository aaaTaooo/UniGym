from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/gym_member/', views.gm_register, name='gm_register'),
    path('register/personal_trainer/', views.pt_register, name='pt_register'),
]