from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in ,user_login_failed, user_logged_out
from django.dispatch import receiver

@receiver(user_logged_in, sender= User )
def login_success(sender , request , user , **kwargs):
    print("----user login successfully---")
    print("sender :", sender )
    print("username", user.username)
    
    
@receiver(user_login_failed)
def login_fail(sender , request , user , **kwargs):
    print("---user login fail-----")
    print("sender :", sender )
    print("username", user.username)
    
    
@receiver(user_logged_out, sender= User )
def logout_success(sender , request , user , **kwargs):
    print("---user logout successfully----")
    print("sender :", sender )
    print("username", user.username)
