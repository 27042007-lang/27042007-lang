from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import CSVUploadForm
import pandas as pd

def csv_upload_view(request):
    form = CSVUploadForm()
    table_html = None
    error = None

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_extension = uploaded_file.name.split('.')[-1].lower()

            # Validate file type
            if file_extension not in ['csv', 'xlsx']:
                error = 'Please upload a CSV or Excel file.'
            else:
                # Save the uploaded file temporarily
                fs = FileSystemStorage()
                file_path = fs.save(uploaded_file.name, uploaded_file)
                full_path = fs.path(file_path)

                try:
                    # Process CSV and Excel files differently
                    if file_extension == 'csv':
                        data = pd.read_csv(full_path)
                    elif file_extension == 'xlsx':
                        data = pd.read_excel(full_path)

                    # Convert the data to HTML for display
                    table_html = data.to_html(classes='table table-bordered')

                except Exception as e:
                    error = f'Error processing file: {e}'
                finally:
                    # Clean up the uploaded file
                    fs.delete(file_path)

    return render(request, 'csv_reflector/index.html', {
        'form': form,
        'table_html': table_html,
        'error': error,
    })
