from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import OrderItem, Order, Customer
from django import forms
from django.conf import settings
import os
from .utils.pdf_importer import parse_and_import_pdfs
from django.shortcuts import render
from django.db.models import Sum


def clear_database(request):
    if request.method == "POST":
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        return HttpResponseRedirect(reverse("home"))
    # Only show confirmation page on GET
    return render(request, "invoices/confirm_clear.html")


def home(request):
    return render(request, "home.html")


# PDF upload form (not used for widget, just for CSRF and validation)
class PDFUploadForm(forms.Form):
    pass


# PDF upload view
def upload_pdfs(request):
    message = None
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist("pdf_files")
        if files:
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_pdfs")
            os.makedirs(upload_dir, exist_ok=True)
            for f in files:
                file_path = os.path.join(upload_dir, f.name)
                with open(file_path, "wb+") as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            # Process uploaded PDFs
            parse_and_import_pdfs(upload_dir + os.sep)
            message = f"{len(files)} PDF file(s) uploaded and processed."
        else:
            message = "No files selected."
    else:
        form = PDFUploadForm()
    return render(
        request, "invoices/upload_pdfs.html", {"form": form, "message": message}
    )


def customer_report(request):
    customers = Customer.objects.all().annotate(total_bought=Sum("order__total"))
    return render(request, "invoices/customer_report.html", {"customers": customers})
