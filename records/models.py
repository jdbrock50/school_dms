from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    grade_level = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.student_id})"



class Document(models.Model):
    CATEGORY_CHOICES = [
        ('transcripts', 'Transcripts'),
        ('report_cards', 'Report Cards'),
        ('iep', 'IEP'),
        ('letters_of_recommendation', 'Letters of Recommendation'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    file = models.FileField(upload_to='students/%Y/%m/%d/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags (e.g. 'Fall 2024, Final')")
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.category} - {self.uploaded_at}"

    def get_file_url(self):
        return self.file.url

