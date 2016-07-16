from __future__ import absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile, User
from .forms import UserChangeForm, UserCreationForm


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'


class UserAdmin(BaseUserAdmin):
    """
    Custom User admin based on original UserAdmin, available for customizations.

    See custom User model docstring for details.
    """

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    inlines = (UserProfileInline, )

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # add_fieldsets is a non standard UserAdmin setting, used by add_form.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

    def get_inline_instances(self, request, obj=None):
        """Overridden to prevent showing of UserProfile inline in add_form."""
        if obj is None:
            # When obj==None, it means it was called from self.add_view().
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj=obj)

admin.site.register(User, UserAdmin)
