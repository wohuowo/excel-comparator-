from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import ExcelUpload
from .models import ExcelFiles


class Home(TemplateView):
    template_name = 'index.html'


def excel_list(request):
    cells = ExcelFiles.objects.all()
    return render(request, 'excel_list.html', {'cells': cells})


def upload_book(request):
    if request.method == 'POST':
        form = ExcelUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('excel_list')
    else:
        form = ExcelUpload()
    return render(request, 'updated_excel.html', {'form': form})
