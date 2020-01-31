from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ForgotLog)
class ForgotLogAdmin(admin.ModelAdmin):
    list_display = ('username',)
    search_fields = ('username',)