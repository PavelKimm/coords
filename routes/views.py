from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from coords.pagination import DefaultPagination
from routes.models import Point, Route
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
