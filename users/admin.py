from django.contrib import admin

from users.models import UserProfile


class UserProfileAdmin(admin.TabularInline):
    model = UserProfile
    fields = ('gender', 'about_me')
    extra = 0           # удаляем доп поля


class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileAdmin,)
