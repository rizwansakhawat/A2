# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label="Enter your password" ,widget=forms.PasswordInput)
#     password2 = forms.CharField(label="enter confirm password" ,widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name']
#         labels = {
#             "username":"Enter username",
#             "email":"Enter your Email",
#             "first_name":"enter your first name",
#             "last_name":"enter your last name",
#         }

#     def clean(self):
#         cleaned = super().clean()
#         p1 = cleaned.get('password1')
#         p2 = cleaned.get('password2')
#         username = cleaned.get('username')
#         if username == User.objects.get('username'):
#             raise ValidationError("A user with that username already exists")
#         if not username or not p1 or not p2:
#             raise ValidationError("Username, password, and repeat password are must required.")
#         if p1 != p2:
#             raise ValidationError("The two password fields didn't match")
#         if len(p1) < 8:
#             raise ValidationError("This password is too short. It must contain at least 8 characters")
#         # if 
#         return cleaned

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user


# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
