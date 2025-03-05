from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
