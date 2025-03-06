from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path("chat/messages/<int:user_id>/", views.get_chat_messages, name="chat_messages"),
    path('chat/<int:user_id>/', views.chat_view, name='chat_page'),
]
