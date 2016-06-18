from django.contrib import admin

# Register your models here.
from .models import UserProfile, Subject, Activity

admin.site.register(Subject)
admin.site.register(UserProfile)
admin.site.register(Activity)