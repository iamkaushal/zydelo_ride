"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # default admin dashboard url
    path("admin/", admin.site.urls),

    # url to register new user
    path("register/", account_views.register, name="register"),

    # url to view user profile
    path("profile/", account_views.profile, name="profile"),

    # url to login users
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),

    # user to logout user
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/logout.html"),
        name="logout",
    ),

    # url sets including from accounts app
    path("user/", include("accounts.urls")),

    # url sets including from rides app
    path("", include("rides.urls")),
]

# adding media setting to urls
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
