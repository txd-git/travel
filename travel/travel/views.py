from django.shortcuts import render
from django.http import HttpResponse

def travel(request):
    return render(request, 'index.html')

def travel2(request):
    return render(request, 'index2.html')
