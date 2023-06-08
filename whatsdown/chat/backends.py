from django.contrib.auth.backends import ModelBackend
from .models import User

class UserModelBackend(ModelBackend):
    def authenticate(self, request, password, **kwargs):
        try:
            user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None