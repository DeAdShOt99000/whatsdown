from typing import Optional
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from datetime import datetime, timedelta
import json

from .models import User, Chat
from .forms import UserForm

def clean_dt(date_time: datetime):
    date = date_time.date()
    if date == datetime.today().date():
        clean_date = 'Today'
    elif date == (datetime.today().date() - timedelta(days=1)):
        clean_date = 'Yesterday'
    else:
        months = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                  4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep',
                  10: 'Oct', 11: 'Nov', 12: 'Dec'}
        clean_day = str(date.day)
        if clean_day[0] == '0':
            clean_day = clean_day[1]
        clean_date = f'{months[date.month]} {clean_day}, {date.year}'
    
    clean_minute = date_time.minute
    if len(str(clean_minute)) < 2:
        clean_minute = f'0{clean_minute}'
        
    if date_time.hour < 13:
        clean_time = f'{date_time.hour}:{clean_minute} AM'
    else:
        clean_hour = date_time.hour - 12
        clean_time = f'{clean_hour}:{clean_minute} PM'
    return (clean_date, clean_time)

# Create your views here.

class LoginView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse('home'))
    
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'chat/login_page.html')
        return redirect(reverse('home'))
    def post(self, request):
        user_or_email = request.POST['user_or_email']
        password = request.POST['password']
        user = authenticate(request, password=password, username=user_or_email)
        if not user:
            user = authenticate(request, password=password, email=user_or_email)
        if user:
            login(request, user)
            return redirect(reverse('home'))
        return HttpResponse('<h1>Login Failed.</h1>')

class SignupView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse('home'))
    
    def get(self, request):
        if not request.user.is_authenticated:
            form = UserForm()
            return render(request, 'chat/signup_page.html', {'form': form})
        return redirect(reverse('home'))
    def post(self, request):
        # firstname = request.POST['first_name']
        # lastname = request.POST['last_name']
        # username = request.POST['username']
        # email = request.POST['email']
        # password = request.POST['password']
        form = UserForm(request.POST, request.FILES or None)
        if form.is_valid():            
            form.save()
            user = User.objects.get(username=request.POST['username'])
            login(request, user, backend='chat.backends.UserModelBackend')
            return redirect(reverse('home'))
        return HttpResponse('<h1>Sign up failed.</h1>')
        
def logout_view(request):
    logout(request)
    return redirect(reverse('login_view'))

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        if search:
            query = Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search)
            all_friends = request.user.friends.filter(query)
        else:
            all_friends = request.user.friends.all()
        return render(request, 'chat/home_page.html', {'all_friends': all_friends, 'search': search})
    def post(self, request):
        new_friend = get_object_or_404(User, email=request.POST['email'])
        request.user.friends.add(new_friend)
        new_friend.friends.add(request.user)
        return redirect(reverse('home'))
    
class ChatView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            friend = request.user.friends.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse("<h1>Doesn't exist.</h1>")
        
        chat_history = Chat.objects.filter(sent_by=request.user, received_by=friend).order_by('-sent_at')
        
        ch_dict_lst = []
        for chat in chat_history:
            date_time = clean_dt(chat.sent_at)
            dict_entry = vars(chat)
            del dict_entry['_state']
            dict_entry.update({
                'date': date_time[0],
                'time': date_time[1]
            })
            ch_dict_lst.append(dict_entry)
        # print(ch_dict_lst)     
        
        # ch = chat_history[0].sent_at
        # print(ch.hour == 12)
        # print(ch, type(ch))
        return render(request, 'chat/chat_page.html', {'friend': friend, 'chat_history': chat_history})
    def post(self, request, pk):
        try:
            friend = request.user.friends.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse("<h1>Doesn't exist.</h1>")
        text_message = json.loads(request.body)['text-message']
        
        Chat.objects.create(
            text = text_message,
            sent_by = request.user,
            received_by = friend,
        )
        # return redirect(reverse('chat_view', args=[pk]))
        return JsonResponse({'message': 'Data received successfully'})
    
class ChatJSON(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            friend = request.user.friends.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse("<h1>Doesn't exist.</h1>")
        
        query = Q(sent_by=request.user, received_by=friend) | Q(sent_by=friend, received_by=request.user)
        chat_history = Chat.objects.filter(query).order_by('sent_at')
        
        ch_dict_lst = []
        for chat in chat_history:
            date_time = clean_dt(chat.sent_at)
            dict_entry = vars(chat)
            del dict_entry['_state']
            dict_entry.update({
                'date': date_time[0],
                'time': date_time[1]
            })
            ch_dict_lst.append(dict_entry)
        # result = {}
        # for chat in chat_history:
        #     date_time = clean_dt(chat.sent_at)
        #     result += {
        #         'text'
        #     }
        #     result.append([chat.text, *date_time])
        return JsonResponse(ch_dict_lst, safe=False)
    
def stream_file(request, pk):
    pic = get_object_or_404(User, pk=pk)
    response = HttpResponse()
    response['content-type'] = pic.content_type
    response['content-length'] = len(pic.profile_pic)
    response.write(pic.profile_pic)
    return response