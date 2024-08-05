import cloudinary
import cloudinary.uploader
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, LearnedWord

cloudinary.config(
    cloud_name=settings.CLOUDINARY['cloud_name'],
    api_key=settings.CLOUDINARY['api_key'],
    api_secret=settings.CLOUDINARY['api_secret']
)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

@login_required
def ar_interface(request):
    return render(request, 'ar_interface.html')

@csrf_exempt
@login_required
def analyze_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        upload_result = cloudinary.uploader.upload(image, timeout=120)
        public_id = upload_result['public_id']
        
        # Use Cloudinary AI to analyze the image
        analysis = cloudinary.api.resource(public_id, 
                                           colors=True, 
                                           faces=True, 
                                           tags=True, 
                                           detection='google_tagging')
        
        # Extract relevant information from the analysis
        tags = analysis.get('tags', [])
        
        return JsonResponse({'tags': tags})
    return JsonResponse({'error': 'No image provided'}, status=400)

@csrf_exempt
@login_required
def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        source_lang = request.POST.get('source', 'en')
        target_lang = request.POST.get('target', 'fr')
        
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        payload = {
            'q': text,
            'source': source_lang,
            'target': target_lang
        }
        
        response = requests.post(settings.LIBRETRANSLATE_API_URL, data=payload)
        
        if response.status_code == 200:
            translation = response.json()['translatedText']
            
            # Save the learned word
            LearnedWord.objects.create(
                user=request.user,
                word=text,
                translation=translation
            )
            
            return JsonResponse({'translation': translation})
        else:
            return JsonResponse({'error': 'Translation failed'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)