from django.db import transaction
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from coords.pagination import DefaultPagination
from routes.models import Point, Route, UserRoute
from routes.serializers import PointListSerializer


class PointListView(generics.ListAPIView):
    serializer_class = PointListSerializer
    pagination_class = DefaultPagination
    queryset = Point.objects.all()


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_directions(request):
    """
    start - id of start Point
    end - id of end Point
    """
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    if not start or not end:
        return Response({"detail": 'start and end points must be provided'}, status=HTTP_400_BAD_REQUEST)
    try:
        route_points = Route.get_directions(start, end)
    except Exception as e:
        return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)
    return Response({'message': route_points}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def save_route(request):
    """
    save points in route object
    """
    route_number = request.data.get('route_number')
    points = request.data.get('points')
    if not route_number:
        return Response({"detail": 'route_number must be provided'}, status=HTTP_400_BAD_REQUEST)
    if not points:
        return Response({"detail": 'points must be provided'}, status=HTTP_400_BAD_REQUEST)
    try:
        with transaction.atomic():
            route = Route.objects.create(number=route_number)
            route.points.set(points)
            user_route = UserRoute.objects.create(user=request.user, route=route)
    except Exception as e:
        return Response({"detail": str(e)}, status=HTTP_400_BAD_REQUEST)
    return Response({'message': f'{user_route} was created'}, status=HTTP_200_OK)
