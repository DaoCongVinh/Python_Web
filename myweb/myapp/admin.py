from django.contrib import admin
from myapp.models import Student

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email')

admin.site.register(Student, StudentAdmin)
