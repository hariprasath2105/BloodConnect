from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DonorProfile, BloodRequest

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_type', 'password1', 'password2'),
        }),
    )

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'gender', 'age', 'is_available', 'last_donation_date')
    list_filter = ('blood_group', 'gender', 'is_available')
    search_fields = ('user__email', 'user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'blood_group', 'units_needed', 'urgency', 'status', 'required_date', 'created_at')
    list_filter = ('blood_group', 'urgency', 'status')
    search_fields = ('requester__email', 'requester__username', 'hospital_name', 'reason')
    raw_id_fields = ('requester', 'donor')
    date_hierarchy = 'created_at'
