"""pbl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from users import views as page_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',page_view.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('',page_view.home,name='homepage'),
    path('profile/',page_view.profile,name='profile'),
    path('scan/',page_view.scan,name='Scanpage'),
    path('camera',page_view.site_load,name="site_load"),
    path('camera',page_view.save_image,name="save_image"),
    path('thankyou',page_view.typage,name="thankyou_page"),
    path('ty_redirect',page_view.ty_redirect,name="ty_redirect"),
    

]
if settings.DEBUG:

    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)