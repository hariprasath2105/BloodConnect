from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import User, DonorProfile, BloodRequest
from .forms import UserRegistrationForm, UserProfileForm, DonorProfileForm, BloodRequestForm
from django.views.decorators.http import require_http_methods

def home(request):
    """Home page view"""
    donors_count = DonorProfile.objects.count()
    pending_requests = BloodRequest.objects.filter(status='pending').count()
    recent_requests = BloodRequest.objects.filter(status='pending').order_by('-created_at')[:6]
    return render(request, 'bloodconnectapp/home.html', {
        'donors_count': donors_count,
        'pending_requests': pending_requests,
        'recent_requests': recent_requests
    })

@require_http_methods(['GET', 'POST'])
def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data.get('user_type')
            if user_type not in ['donor', 'receiver']:
                messages.error(request, 'Invalid user type selected.')
                return render(request, 'bloodconnectapp/register.html', {'form': form})
            
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('bloodconnectapp:login_view')
    else:
        form = UserRegistrationForm()
    return render(request, 'bloodconnectapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('bloodconnectapp:home')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'bloodconnectapp/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('bloodconnectapp:home')

@login_required
def profile(request):
    """User profile view"""
    user = request.user
    donor_profile = None
    if user.user_type == 'donor':
        donor_profile = DonorProfile.objects.filter(user=user).first()
    
    # Get all blood requests related to the user
    blood_requests = BloodRequest.objects.filter(
        Q(requester=user) | Q(donor__user=user)
    ).order_by('-created_at')
    
    return render(request, 'bloodconnectapp/profile.html', {
        'user': user,
        'donor_profile': donor_profile,
        'blood_requests': blood_requests
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('bloodconnectapp:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'donor_profile': getattr(request.user, 'donorprofile', None),
        'blood_requests': BloodRequest.objects.filter(
            Q(requester=request.user) | Q(donor__user=request.user)
        ).order_by('-created_at')
    }
    return render(request, 'bloodconnectapp/edit_profile.html', context)

@login_required
def register_donor(request):
    """Donor registration view"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Only users with donor type can register as donors.')
        return redirect('bloodconnectapp:profile')
    
    if hasattr(request.user, 'donorprofile'):
        messages.info(request, 'You are already registered as a donor.')
        return redirect('bloodconnectapp:profile')
    
    if request.method == 'POST':
        form = DonorProfileForm(request.POST)
        if form.is_valid():
            donor_profile = form.save(commit=False)
            donor_profile.user = request.user
            donor_profile.save()
            messages.success(request, 'Donor registration successful!')
            return redirect('bloodconnectapp:profile')
    else:
        form = DonorProfileForm()
    
    return render(request, 'bloodconnectapp/register_donor.html', {'form': form})

@login_required
def donor_profile(request):
    if request.user.user_type != 'donor':
        messages.error(request, 'Only users registered as donors can access this page.')
        return redirect('bloodconnectapp:profile')
    
    donor_profile = get_object_or_404(DonorProfile, user=request.user)
    return render(request, 'bloodconnectapp/donor_profile.html', {'donor_profile': donor_profile})

@login_required
def edit_donor_profile(request):
    """Edit donor profile view"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Only users registered as donors can access this page.')
        return redirect('bloodconnectapp:profile')
    
    donor_profile = get_object_or_404(DonorProfile, user=request.user)
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor profile updated successfully!')
            return redirect('bloodconnectapp:donor_profile')
    else:
        form = DonorProfileForm(instance=donor_profile)
    
    return render(request, 'bloodconnectapp/edit_donor_profile.html', {'form': form})

@login_required
def create_request(request):
    """Create blood request view"""
    if request.user.user_type != 'receiver':
        messages.error(request, 'Only users with receiver type can create blood requests.')
        return redirect('bloodconnectapp:request_list')
    
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            messages.success(request, 'Blood request created successfully!')
            return redirect('bloodconnectapp:request_detail', request_id=blood_request.id)
    else:
        form = BloodRequestForm()
    
    return render(request, 'bloodconnectapp/create_request.html', {'form': form})

def request_list(request):
    """List all pending blood requests"""
    requests = BloodRequest.objects.filter(status='pending').order_by('-created_at')
    
    # Apply filters
    blood_group = request.GET.get('blood_group')
    city = request.GET.get('city')
    urgency = request.GET.get('urgency')
    
    if blood_group:
        requests = requests.filter(blood_group=blood_group)
    if city:
        requests = requests.filter(requester__city__icontains=city)
    if urgency:
        requests = requests.filter(urgency=urgency)
    
    context = {
        'requests': requests,
        'blood_groups': DonorProfile.BLOOD_GROUP_CHOICES,
        'urgency_levels': BloodRequest.URGENCY_CHOICES
    }
    return render(request, 'bloodconnectapp/request_list.html', context)

def request_detail(request, request_id):
    """View blood request details"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    can_accept = (
        request.user.is_authenticated and
        request.user.user_type == 'donor' and
        blood_request.status == 'pending' and
        hasattr(request.user, 'donorprofile') and
        request.user.donorprofile.is_available
    )
    
    context = {
        'request': blood_request,
        'can_accept': can_accept
    }
    return render(request, 'bloodconnectapp/request_detail.html', context)

@login_required
def accept_request(request, request_id):
    """Accept blood request view"""
    if request.user.user_type != 'donor':
        messages.error(request, 'Only donors can accept blood requests.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    if blood_request.status != 'pending':
        messages.error(request, 'This request is no longer available.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    donor_profile = get_object_or_404(DonorProfile, user=request.user)
    if not donor_profile.is_available:
        messages.error(request, 'You are currently marked as unavailable.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    blood_request.donor = donor_profile
    blood_request.status = 'accepted'
    blood_request.save()
    
    messages.success(request, 'You have accepted the blood request.')
    return redirect('bloodconnectapp:request_detail', request_id=request_id)

@login_required
def complete_request(request, request_id):
    """Mark blood request as completed"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if blood_request.status != 'accepted':
        messages.error(request, 'This request cannot be marked as completed.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    if request.user != blood_request.requester and request.user != blood_request.donor.user:
        messages.error(request, 'You are not authorized to complete this request.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    blood_request.status = 'completed'
    blood_request.save()
    
    messages.success(request, 'Blood request marked as completed.')
    return redirect('bloodconnectapp:request_detail', request_id=request_id)

@login_required
def cancel_request(request, request_id):
    """Cancel blood request"""
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if blood_request.status != 'pending':
        messages.error(request, 'This request cannot be cancelled.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    if request.user != blood_request.requester:
        messages.error(request, 'You are not authorized to cancel this request.')
        return redirect('bloodconnectapp:request_detail', request_id=request_id)
    
    blood_request.status = 'cancelled'
    blood_request.save()
    
    messages.success(request, 'Blood request cancelled successfully.')
    return redirect('bloodconnectapp:request_list')
