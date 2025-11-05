from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/view/', views.ProfileView.as_view(), name='profile_view'),
    path('profile/edit/', views.EditProfileView.as_view(), name='profile_edit'),
]
