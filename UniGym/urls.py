
from django.urls import path
from UniGym import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.about_page, name='about_page'),
    path('service/', views.service_page, name='services_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('login/',views.login_page, name='login_page'),

]