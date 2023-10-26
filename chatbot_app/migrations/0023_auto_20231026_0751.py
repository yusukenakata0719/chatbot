# Generated by Django 3.2 on 2023-10-26 07:51

import chatbot_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0022_jsondocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsondocument',
            name='json_file',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pdfdocument',
            name='pdf_file',
            field=models.FileField(null=True, upload_to=chatbot_app.models.PDFDocument.get_upload_path),
        ),
    ]