from django import forms
from .models import Document, Student

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'category', 'tags']
        
    category = forms.ChoiceField(choices=Document.CATEGORY_CHOICES)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'grade_level']