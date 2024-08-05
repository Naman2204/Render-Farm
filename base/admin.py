from django.contrib import admin

from .models import FileData, Suggestions

# Register your models here.
admin.site.register(Suggestions)
admin.site.register(FileData)
