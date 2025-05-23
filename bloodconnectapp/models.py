from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for BloodConnect"""
    USER_TYPE_CHOICES = (
        ('donor', 'Donor'),
        ('receiver', 'Receiver'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class DonorProfile(models.Model):
    """Model for storing donor-specific information"""
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    medical_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_group}"
    
    class Meta:
        verbose_name = _('donor profile')
        verbose_name_plural = _('donor profiles')

class BloodRequest(models.Model):
    """Model for storing blood donation requests"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    URGENCY_CHOICES = (
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    )
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=3, choices=DonorProfile.BLOOD_GROUP_CHOICES)
    units_needed = models.PositiveIntegerField(default=1)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    reason = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='normal')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    required_date = models.DateField()
    donor = models.ForeignKey(DonorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='donation_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request from {self.requester.get_full_name()} - {self.blood_group}"
    
    class Meta:
        verbose_name = _('blood request')
        verbose_name_plural = _('blood requests')
        ordering = ['-created_at']
