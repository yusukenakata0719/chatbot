from django.urls import path
from . import views

urlpatterns = [
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('dealing_pdf/', views.dealing_pdf, name='dealing_pdf'),
    path('confirm_upload/', views.confirm_upload, name='confirm_upload'),
    path('ask/', views.ask_questions, name='ask_questions'),
]
