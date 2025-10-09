from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'UniGym/home_page.html')

def about_page(request):
    return render(request, 'UniGym/about_page.html')

def service_page(request):
    return render(request, 'UniGym/service_page.html')

def contact_page(request):
    return render(request, 'UniGym/contact_page.html')

def login_page(request):
    return render(request, 'users/login.html')