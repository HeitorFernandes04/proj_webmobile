from django.contrib import admin
from django.urls import path, include
from courses.views import landing_page  # vamos criar essa view já já

urlpatterns = [
    path('admin/', admin.site.urls),

    # landing / página de vendas
    path('', landing_page, name='landing'),

    # futuramente:
    # path('accounts/', include('accounts.urls')),
    # path('courses/', include('courses.urls')),
    # path('api/', include('api.urls')),
]
