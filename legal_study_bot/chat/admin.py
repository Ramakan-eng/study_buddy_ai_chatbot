from django.contrib import admin
from .models import CachedResponse

# Register your models here.
admin.site.register(CachedResponse)

list_display = ('case_name', 'query', 'response')

class CachedResponseAdmin(admin.ModelAdmin):
    list_display = list_display
