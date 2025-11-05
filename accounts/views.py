from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        context = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

        # Required checks
        if not username or not password1 or not password2:
            context['error'] = "This field is required"
            return render(request, 'accounts/register.html', context)

        # Password match
        if password1 != password2:
            context['error'] = "The two password fields didn't match"
            return render(request, 'accounts/register.html', context)

        # Password length
        if len(password1) < 8:
            context['error'] = "This password is too short. It must contain at least 8 characters"
            return render(request, 'accounts/register.html', context)

        # Email validation
        if email and '@' not in email:
            context['error'] = "Enter a valid email address"
            return render(request, 'accounts/register.html', context)

        # Username exists
        if User.objects.filter(username=username).exists():
            context['error'] = "A user with that username already exists"
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(
            username=username,
            password=password1,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        return redirect('/accounts/login/')
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/accounts/profile/view/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is invalid'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/login/')




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        return render(request, 'accounts/edit_profile.html', {'user': request.user})

    def post(self, request):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        try:
            if user.email:
                validate_email(user.email)
        except ValidationError:
            return render(request, 'accounts/edit_profile.html', {'error': "Enter a valid email address"})

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if password1:
            if password1 != password2:
                return render(request, 'accounts/edit_profile.html', {'error': "The two password fields didn't match"})
            if len(password1) < 8:
                return render(request, 'accounts/edit_profile.html', {'error': "This password is too short. It must contain at least 8 characters"})
            user.set_password(password1)
            # re-login user after password change
            user.save()
            login(request, user)
        else:
            user.save()

        return redirect('/accounts/profile/view/')
