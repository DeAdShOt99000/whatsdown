from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View
from django.db.models import Q
from .models import Chat

# Create your views here.

class Index(View, LoginRequiredMixin):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'chat/index.html', {'users': users})
    
class ChatView(View, LoginRequiredMixin):
    def get(self, request, pk):
        friend = get_object_or_404(User, pk=pk)
        all_chat = Chat.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('date_time')
        return render(request, 'chat/chat.html', {'friend': friend, 'all_chat': all_chat})
    def post(self, request, pk):
        sender = request.user
        receiver = get_object_or_404(User, pk=pk)
        message = request.POST['message']
        newchat = Chat(message=message, sender=sender, receiver=receiver)
        if newchat.is_valid():
            newchat.save()
            return redirect(reverse('chat:chat-window'))