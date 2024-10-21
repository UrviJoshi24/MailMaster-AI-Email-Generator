from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'myapp/index.html')

def dashboard(request):
    return render(request, 'myapp/dashboard.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Create a new user
        user = User(username=username, password=make_password(password), email=email)
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect('/')

    return render(request, 'myapp/index.html')

# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = authenticate(username=username, password=password)
        print(password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')

# Handle user logout
def logout_view(request):
    print("hello   ")
    # Django's logout function clears the session
    logout(request)
    # Redirect to the login page after logout
    return redirect('/')  # Replace 'index' with your login page URL name

def trash_view(request):
    return render(request, 'myapp/trash.html')

@login_required
def account_view(request):
    user = request.user  # Get logged-in user
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
    }
    return render(request, 'myapp/account.html', context)