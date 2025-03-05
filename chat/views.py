from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# User Registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat_home")  # Redirect to chat page
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})

# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("chat_home")  # Redirect to chat page
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

# User Logout
def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page

@login_required
def chat_room(request, room_name):
    return render(request, 'chatroom.html', {'room_name': room_name})
