from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("customer-report/", views.customer_report, name="customer_report"),
    path("upload-pdfs/", views.upload_pdfs, name="upload_pdfs"),
    path("clear-database/", views.clear_database, name="clear_database"),
]
