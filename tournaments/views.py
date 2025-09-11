from django.shortcuts import render

def index(request):
    """Vista para la página principal del torneo"""
    return render(request, 'index.html')