# Generated by Django 3.2 on 2023-09-27 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0011_alter_pdfdocument_pdf_content'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PDFDocument',
            new_name='PDFIndex',
        ),
    ]