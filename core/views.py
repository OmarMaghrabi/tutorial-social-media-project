from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'index.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def upload(request):
    pass

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        new_image = request.FILES.get('image')
        
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        if new_image:
            user_profile.profileimg = new_image
            
        user_profile.bio = bio
        user_profile.location = location

        user_profile.save()
        return redirect('settings')
        
    return render(request, 'settings.html', {'user_profile': user_profile})

def signup(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')
        
        if not all([username, email, password, password_confirm]):
            messages.info(request, "All fields are required")
            return redirect('signup')
        # assert (password == password_confirm), messages.info(request, "Password isn't equal"); return redirect('signup.html')
        
        if password != password_confirm:
            messages.info(request, "Passwords do not match")
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email is taken")
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username is taken")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()  
    
            messages.success(request, "User created successfully")
    

            # Creation of user profile
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(user=user_model, id_user =user_model.id)

            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            return redirect('settings')
        
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect('signup')
        
        else:
            auth.login(request, user)
            return redirect('/')

        """
        Tried to do it on my own at first but this is way more insecure than using it 
        if not all([username, password]):
            messages.info(request, "All fields are required")
            redirect('signup')

        if(
            User.objects.filter(username=username, password=password)
        ):
            pass
        
        else:
            messages.error(request, "Wrong credentials")
        """   
    
    return render(request, "signin.html")

@login_required(login_url='signin')
def signout(request):
    auth.logout(request)
    return redirect('signin')