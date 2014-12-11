from django.shortcuts import render
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'index.html')

