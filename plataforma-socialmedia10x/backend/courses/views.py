from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    """
    Página de vendas pública.
    """
    return render(request, "landing.html")


@login_required
def home(request):
    """
    Home da plataforma (área do aluno).
    Depois vamos listar módulos e progresso aqui.
    """
    return render(request, "courses/home.html")
