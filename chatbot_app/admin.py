from django.contrib import admin
from .models import PDFDocument, UploadedURL, User


# Register your models here.
admin.site.register(PDFDocument)
admin.site.register(UploadedURL)



