from django.contrib import admin
from .models import Student, Document

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'student_id', 'grade_level')
    search_fields = ('last_name', 'student_id')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'uploaded_by', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('tags',)
