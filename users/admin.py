from django.contrib import admin
from .models import User, UserMessages

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',)

class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ('reciever', 'sender', 'message',)


admin.site.register(User, UserAdmin)
admin.site.register(UserMessages, UserMessagesAdmin)