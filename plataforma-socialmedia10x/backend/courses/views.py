from django.shortcuts import render

def landing_page(request):
    """
    Página de vendas / landing page pública.
    Aqui vamos apresentar o curso e colocar o CTA para login/cadastro.
    """
    return render(request, "landing.html")
