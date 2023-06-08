from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login', views.LoginView.as_view(), name='login_view'),
    path('accounts/signup', views.SignupView.as_view(), name='signup_view'),
    path('accounts/logout', views.logout_view, name='logout_view'),
    path('home', views.HomeView.as_view(), name='home'),
    path('home/chat/<int:pk>', views.ChatView.as_view(), name='chat_view'),
    path('home/chat/<int:pk>/chat-json', views.ChatJSON.as_view(), name='chat-json'),
    path('profile-pic/<int:pk>', views.stream_file, name='profile_pic'),
]