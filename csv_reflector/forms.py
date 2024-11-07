from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='SELECT A CSV / EXCEL FILE')
