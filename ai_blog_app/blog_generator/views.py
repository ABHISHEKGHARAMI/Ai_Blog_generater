from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    return render(request,
                  'index.html')

# for generate the blog
def generate_blog(request):
    pass
# login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            error_message = 'unfortunately username or password does not match'
            return render(request,'login.html',
                          {
                              'error_message':error_message
                          })
    return render(request,
                  'login.html')

# sign up page
def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatPassword = request.POST.get('repeatPassword')
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request,user)
                return redirect('/')
            except Exception:
                error_message = 'error creating the user profile..'
                return render(request,
                              'signup.html',
                              {
                                  'error_message':error_message
                              })
        else:
            error_message = 'password does not match'
            return render(request,
                          'signup.html',{
                              'error_message':error_message
                          })
    return render(request,
                  'signup.html')

# logout view
def user_logout(request):
    logout(request)
    return redirect('/')

