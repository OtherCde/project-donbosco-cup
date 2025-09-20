from django.shortcuts import render


def index(request):
    """Vista para la página principal del torneo"""
    return render(request, "index.html")


def ayuda(request):
    """Vista para la página de ayuda y guía de uso"""
    return render(request, "help.html")
