from django.urls import path
from . import views

app_name = 'bloodconnectapp'

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    
    # User Profile Management
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Donor Management
    path('donor/register/', views.register_donor, name='register_donor'),
    path('donor/profile/', views.donor_profile, name='donor_profile'),
    path('donor/profile/edit/', views.edit_donor_profile, name='edit_donor_profile'),
    
    # Blood Request Management
    path('requests/', views.request_list, name='request_list'),
    path('requests/create/', views.create_request, name='create_request'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('requests/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('requests/<int:request_id>/complete/', views.complete_request, name='complete_request'),
    path('requests/<int:request_id>/cancel/', views.cancel_request, name='cancel_request'),
] 