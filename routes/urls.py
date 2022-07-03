from django.urls import path

from routes.views import get_directions

urlpatterns = [
    path('points/', get_directions),
    path('get-directions/', get_directions),
]
