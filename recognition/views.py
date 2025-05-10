# recognition/views.py

from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Recognition home page.")
