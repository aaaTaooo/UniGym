from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, GroupFitnessClass, Booking


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_approved', 'is_staff', 'is_active')
    fieldsets = ((None, {'fields': ('username', 'password', 'email', 'role', 'is_approved')}),
                 ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                 ('Important dates', {'fields': ('last_login', 'date_joined')}),
                 )
    add_fieldsets = ((None, {'classes': ('wide',),
                             'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}),
                     )
    search_fields = ('username', 'email')
    ordering = ('username',)

    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        queryset.update(is_approved=True)
    approve.short_description = 'Approve selected users'

    def reject(self, request, queryset):
        queryset.update(is_approved=False)
    reject.short_description = 'Reject selected users'

class GroupFitnessClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'capacity', 'spots_left', 'created_by')
    list_filter = ('date','location')
    search_fields = ('title','description')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('member', 'fitness_class', 'booked_at')
    list_filter = ('booked_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(GroupFitnessClass, GroupFitnessClassAdmin)
admin.site.register(Booking, BookingAdmin)