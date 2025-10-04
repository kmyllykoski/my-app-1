from django.http import HttpResponse

def healthz_view(request):
    return HttpResponse("OK")