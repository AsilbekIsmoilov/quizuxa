from django.contrib import admin
from .models import *
# Register your models here.

class TestResultAdmin(admin.ModelAdmin):
    list_display = ['intern','full_name','score','duration_minutes','created_at']

    
admin.site.register(Trainer)
admin.site.register(Intern)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TestResult,TestResultAdmin)
admin.site.register(InternAnswer)
