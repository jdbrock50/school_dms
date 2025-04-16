from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Document
from .forms import DocumentForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import DetailView

def student_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        students = Student.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(student_id__icontains=search_query))
    else:
        students = Student.objects.all()
    return render(request, 'records/student_list.html', {'students': students, 'search_query': search_query})

@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    documents = Document.objects.filter(student=student)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = student
            doc.uploaded_by = request.user
            doc.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = DocumentForm()
    return render(request, 'records/student_detail.html', {'student': student, 'documents': documents, 'form': form})

@login_required
def upload_document(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = student
            doc.uploaded_by = request.user
            doc.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = DocumentForm()
    return render(request, 'records/upload_document.html', {'form': form, 'student': student})

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        document.delete()
        return redirect('student_detail', student_id=document.student.id)
    return render(request, 'records/delete_document.html', {'document': document})

@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'records/delete_student.html', {'student': student})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = StudentForm()
    return render(request, 'records/add_student.html', {'form': form})

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            return redirect('student_detail', student_id=student.id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'records/edit_student.html', {'form': form, 'student': student})

@login_required
def edit_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('student_detail', student_id=document.student.id)
    else:
        form = DocumentForm(instance=document)
    
    return render(request, 'records/edit_document.html', {'form': form, 'document': document})

@login_required
def document_detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    file_url = document.file.url
    file_name = document.file.name.lower()

    is_pdf = file_name.endswith('.pdf')
    is_image = any(file_name.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])

    context = {
        'document': document,
        'is_pdf': is_pdf,
        'is_image': is_image,
        'file_url': file_url
    }
    return render(request, 'records/document_detail.html', context)

class DocumentView(DetailView):
    model = Document
    template_name = 'records/document_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = self.get_object()
        file_url = document.file.url
        file_name = document.file.name.lower()

        is_pdf = file_name.endswith('.pdf')
        is_image = any(file_name.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])

        context['is_pdf'] = is_pdf
        context['is_image'] = is_image
        context['file_url'] = file_url
        return context