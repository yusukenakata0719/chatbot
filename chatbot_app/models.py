from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
from django.contrib.auth.models import User
from django.conf import settings

class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/', null=True)  # ファイル名は自動的に生成されます

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ファイルがアップロードされた場合に、nameフィールドにファイル名を設定
        if self.pdf_file:
            self.name = self.pdf_file.name

        super(PDFDocument, self).save(*args, **kwargs)

    def get_upload_path(instance, filename):
        # ユーザーごとにディレクトリを作成
        user_directory = str(instance.user.id)
        return os.path.join('pdfs', user_directory, filename)

    pdf_file.upload_to = get_upload_path

@receiver(pre_delete, sender=PDFDocument)
def delete_pdf_file(sender, instance, **kwargs):
    if instance.pdf_file:
        # ファイルのパスを取得
        file_path = instance.pdf_file.path
        # ファイルを削除
        if os.path.exists(file_path):
            os.remove(file_path)


class UploadedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    url = models.URLField(max_length=2000)

    def __str__(self):
        return self.url


class JSONDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    json_file = models.FileField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ファイルがアップロードされた場合に、nameフィールドにファイル名を設定
        if self.json_file:
            self.name = self.json_file.name
        super(JSONDocument, self).save(*args, **kwargs)

