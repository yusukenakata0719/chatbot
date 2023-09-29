from django.urls import path
from . import views

urlpatterns = [
    path('select_data/', views.select_data, name='select_data'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('pdf_list/', views.PDFListView.as_view(), name='pdf_list'),
    path('delete_pdf/<int:pk>/', views.delete_pdf, name='delete_pdf'),
    path('dealing_pdf/', views.dealing_pdf, name='dealing_pdf'),
    path('delete_all_pdf/', views.delete_all_pdf, name='delete_all_pdf'),
    path('upload_web/', views.upload_web, name='upload_web'),
    path('dealing_web/', views.dealing_web, name='dealing_web'),
    path('ask/', views.ask_questions, name='ask_questions'),
    path('home/', views.home, name='home'),
    path('setting/', views.setting, name='setting'),
    path('delete_all/', views.delete_all, name='delete_all'),
    path('confirm_delete_all/', views.confirm_delete_all, name='confirm_delete_all'),
    path('complete_delete_all/', views.complete_delete_all, name='complete_delete_all'),
]
