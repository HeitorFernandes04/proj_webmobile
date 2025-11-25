from django.contrib import admin
from django.urls import path, include
from courses.views import landing_page, home  # vamos criar home já já

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', landing_page, name='landing'),       # Página de vendas
    path('home/', home, name='home'),             # Home da plataforma

    path('accounts/', include('accounts.urls')),  # login/cadastro/logout
    path('payment/', include('billing.urls')),    # página de pagamento
]
