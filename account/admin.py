from django.contrib import admin
from account.models import User


# Register your models here.
@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_id','username', 'birth_date', 'profile_image', 'email')
    list_filter = ['username']
