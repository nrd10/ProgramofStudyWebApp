"""programofstudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    #ajax_select urls
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^select2/', include('django_select2.urls')),
    path('', RedirectView.as_view(url='/POS/', permanent=True)),
    path('admin/', admin.site.urls),
    path('POS/', include('shared.urls')),
    path('meng/', include('meng.urls')),
    path('ms/', include('ms.urls')),
    path('phd/', include('phd.urls')),
    path('administration/', include('administration.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
