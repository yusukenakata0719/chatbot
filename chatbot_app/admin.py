from django.contrib import admin
from .models import PDFDocument, UploadedURL, JSONDocument


# Register your models here.
admin.site.register(PDFDocument)
admin.site.register(UploadedURL)
admin.site.register(JSONDocument)



