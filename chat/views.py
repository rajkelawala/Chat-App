from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print("DEBUG: Form Submitted")  

        if password != confirm_password:
            print("DEBUG: Passwords do not match!")  
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            print("DEBUG: Username already exists!")  
            messages.error(request, "Username already exists!")
            return redirect("register")

        # ✅ Create User properly (Django will hash password automatically)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()  

        print(f"DEBUG: User Created - {user.username}")
        print(f"DEBUG: Stored Hashed Password - {user.password}")

        # ✅ Ensure password verification is working
        stored_user = User.objects.get(username=username)
        if check_password(password, stored_user.password):
            print("DEBUG: Password verification successful!")
        else:
            print("DEBUG: Password verification failed!")
            return redirect("register")  # Stop execution if password fails

        # ✅ Authenticate and login
        user = authenticate(username=username, password=password)
        if user:
            print("DEBUG: User Authenticated Successfully!")
            login(request, user)
            return redirect("chat_page", user_id=authenticated_user.id)
        else:
            print("DEBUG: Authentication Failed!")
            messages.error(request, "Authentication failed!")
            return redirect("register")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # ✅ Manual input le raha hai
        password = request.POST.get("password")

        print(f"DEBUG: Trying to login with {username}")  # 🔴 Debugging

        user = authenticate(username=username, password=password)

        if user is not None:
            print("DEBUG: User authenticated successfully")  # 🔴 Debugging
            login(request, user)
            return redirect("chat_page", user_id=user.id)  # ✅ Redirect to chat page
        else:
            print("DEBUG: Authentication failed")  # 🔴 Debugging
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")  # ✅ Ensure correct template

# User Logout
def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page

@login_required
def chat_room(request, user_id):
    receiver = User.objects.get(id=user_id)
    return render(request, 'chatroom.html',{"receiver": receiver})

@login_required
def get_chat_messages(request, user_id):
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user))
    ).order_by("timestamp")

    messages_data = [
        {"sender": msg.sender.username, "message": msg.message, "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
        for msg in messages
    ]

    return JsonResponse({"messages": messages_data})

@login_required
def chat_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)  # ✅ Handle 404 error
    return render(request, 'chat.html', {'receiver': receiver})