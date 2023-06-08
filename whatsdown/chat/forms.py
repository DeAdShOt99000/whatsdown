from django import forms
from django.contrib.auth.hashers import make_password
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    profile_pic = forms.FileField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'profile_pic']
    
    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.password = make_password(inst.password)
        p = inst.profile_pic
        if isinstance(p, InMemoryUploadedFile):
            inst.content_type = p.content_type
            inst.profile_pic = p.read() # Byte array
        if commit:
            return inst.save()
        return inst
