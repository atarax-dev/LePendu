"""LePendu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from LePendu.views import home_view, create_user, pendu_view, log_user, logout_user, ranking_view, \
    login_view, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    path('', home_view, name='home'),
    path('create_user', create_user, name='create_user'),
    path('pendu', pendu_view, name='pendu'),
    path('log_user', log_user, name='log_user'),
    path('logout_user', logout_user, name='logout_user'),
    path('ranking', ranking_view, name='ranking'),
    path('login', login_view, name='login'),
    path('profile', profile_view, name='profile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
