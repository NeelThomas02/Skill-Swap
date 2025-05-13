# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import LogoutOnGetView
from .views import ProfileUpdateView
from .views import ProfileDetailView

app_name = 'users'

urlpatterns = [
    # signup
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # login/logout (using Django’s built-ins)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # profile detail
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', LogoutOnGetView.as_view(), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='detail'),
]
