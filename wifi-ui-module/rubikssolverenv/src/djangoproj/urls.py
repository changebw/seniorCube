"""
URL configuration for djangoproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from djangoproj.views import index,sendScramble,sendSolve,makeConnection,closeConnection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about', index, name='index'), #connect to diff react pages, all go to index since this is a SPA
    path('race', index, name='index'),
    path('learn', index, name='index'),
    path("makeConnection", makeConnection, name='index'),
    path("sendScramble", sendScramble),
    path("sendSolve", sendSolve),
    path("closeConnection", closeConnection),
]
