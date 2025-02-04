from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import assemblyai as aai
import openai
import yt_dlp

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
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error':'failed to get transcription..'},status=500)
        
        blog_content = get_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': 'failed to generate blog ..'}, status=500)
        
        return JsonResponse({'content':blog_content})
    else:
        return JsonResponse({
            'error':'invalid request method'
        },status=405)
        
# func for yt title
def yt_title(link):
    ydl_opts = {
        'quiet': True,  # Suppress output
        'extract_flat': True  # Only extract metadata (no download)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'No title found')
    except Exception as e:
        title = "Error fetching title"
        print(f"Error fetching YouTube title: {e}")

    return title
# download the audio of the video
def download_audio(link):
    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best audio format
        'extractaudio': True,  # Only extract audio, no video
        # Output template with file name in MEDIA_ROOT
        'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',  # Convert to mp3 using FFmpeg
            'preferredcodec': 'mp3',  # Output format mp3
            'preferredquality': '192',  # Quality setting
        }],
        'quiet': True,  # Suppress output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                link, download=True)  # Download the audio
            file_path = ydl.prepare_filename(
                info_dict)  # Get the temporary file path
            # Change extension to .mp3
            mp3_file = file_path.replace(info_dict['ext'], 'mp3')
            os.rename(file_path, mp3_file)  # Rename to mp3
    except Exception as e:
        print(f"Error downloading audio: {e}")
        mp3_file = None
        
    return mp3_file

#  transcript for the audio file
def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = settings.ASSEMBLY_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    return transcript.text

# get the blog from the transcript
def get_blog_from_transcription(transcription):
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )

    generated_content = response.choices[0].text.strip()

    return generated_content

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

