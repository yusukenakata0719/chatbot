from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


class PDFDocument(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/',null=True)
    def __str__(self):
        return self.name
    
@receiver(pre_delete, sender=PDFDocument)
def delete_pdf_file(sender, instance, **kwargs):
    if instance.pdf_file:
        # ファイルのパスを取得
        file_path = instance.pdf_file.path
        # ファイルを削除
        if os.path.exists(file_path):
            os.remove(file_path)


class UploadedURL(models.Model):
    url = models.URLField(max_length=2000)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

