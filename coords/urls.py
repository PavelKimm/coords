from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth
    path('login/', views.obtain_auth_token),
]
