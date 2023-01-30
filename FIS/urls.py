"""FIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Web_View.views import \
    index, studentLogin, \
    studentRegistration, Logout, myList, moreDetails, MyListManager, student_application

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login', studentLogin, name='student-login'),
    path('register', studentRegistration, name='student-register'),
    path('register', studentRegistration, name='student-register'),
    path('field/<str:pk>', moreDetails, name='student-register'),
    path('logout', Logout, name='student-logout'),
    path('my-list', myList, name='student-list'),
    path('apply/<str:pk>', student_application, name='student-application'),

    path('api/list-manager', MyListManager.as_view(), name='list-manager')
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
