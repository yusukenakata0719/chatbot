# Generated by Django 3.2 on 2023-09-27 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0008_auto_20230926_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdfdocument',
            name='pdf_file',
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='pdf_content',
            field=models.BinaryField(default=None),
        ),
        migrations.AddField(
            model_name='pdfdocument',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
