from django import forms
from .models import PDFDocument

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField()

class URLUploadForm(forms.Form):
    url = forms.URLField(max_length=2000)

