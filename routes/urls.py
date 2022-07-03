from django.urls import path

from routes.views import get_directions, save_route, PointListView

urlpatterns = [
    path('points/', PointListView.as_view()),
    path('get-directions/', get_directions),

    path('save-route/', save_route)
]
