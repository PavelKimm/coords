from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

api_patterns = [
    path('login/', views.obtain_auth_token),
    path('routes/', include('routes.urls'))
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_patterns)),
]
