"""
URL configuration for unified_tool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('protegioTools/', include('apps.protegioTools.urls')),
    path('checker/', include('apps.checker.urls')),
    path('scanner/', include('apps.scanner.urls')),
    path('dns_tool/', include('apps.dns_tool.urls')),
    path('perforNet/', include('apps.perforNet.urls')),
    path('integrations/', include('apps.integrations.urls')),
    path('reports/', include('apps.reports.urls')),
    path('sqlmap/', include('apps.sqlmap.urls')),
    path('nikto/', include('apps.NIKTO.urls')),
    path('NIKTO/', RedirectView.as_view(url='/nikto/', permanent=True)),
    path('burp-suite/', include(('apps.burp-suite.urls', 'burp_suite'), namespace='burp_suite')),
]

# Servir les fichiers statiques et médias en développement uniquement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
