from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings

# Create your views here.
@login_required
def index(request):
    return render(request,
                  'index.html')

# for generate the blog
@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data['link']
            return JsonResponse({'content':yt_link})
        except {KeyError,JSONDecodeError}:
            return JsonResponse({
            'error':'invalid data sent'
        },status=400)
            
            
        '''
        get the title of the video
        get the transcript of the video
        get the blog using the openApi
        save the blog in the database
        return the blog as json response 
        '''
        title = yt_title(yt_link)
    else:
        return JsonResponse({
            'error':'invalid request method'
        },status=405)
        
# func for yt title
def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title
# download the audio of the video
def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
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

