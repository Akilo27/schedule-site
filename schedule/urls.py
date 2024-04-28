from django.urls import path

from schedule import views

urlpatterns = [
    path('', views.ScheduleView.as_view(), name='schedule'),
    path('pdfs/',views.pdfs, name='pdfs'),
    path('upload_file/', views.upload_file),
    path('sidebar/', views.sidebar),
    path('<path:pdf_detail>/', views.pdf_detail, name='pdf_detail'),
]
