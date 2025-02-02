from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,
                  'index.html')


# login view
def user_login(request):
    return render(request,
                  'login.html')

# sign up page
def user_signup(request):
    return render(request,
                  'signup.html')

# logout view
def user_logout(request):
    pass

