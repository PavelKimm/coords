from random import randint

from django.db import models
from rest_framework.authtoken.admin import User


class Point(models.Model):
    name = models.CharField(max_length=80)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        ordering = ('-id',)
        unique_together = ('name', 'lat', 'lng')

    def __str__(self):
        return self.name


class Route(models.Model):
    number = models.PositiveIntegerField(unique=True)
    points = models.ManyToManyField(Point)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'Route #{self.number}'

    def get_route_points(self):
        return self.points.all()

    @classmethod
    def get_directions(cls, start_id, end_id) -> list:
        """
        start_id - id of start Point
        end_id - id of end Point

        start and end points can be the same (a path)
        """
        if not start_id or not end_id:
            raise Exception('start_id and end_id must be provided')
        start_point = Point.objects.get(id=start_id)
        end_point = Point.objects.get(id=end_id)
        route_point_ids = [start_point.id]
        number_of_points_in_db = Point.objects.count()
        for _ in range(randint(2, 100)):  # random number of points in the route
            attempts = 0
            while True:
                attempts += 1
                if attempts > 100_000:
                    raise Exception('Too many attempts')
                route_point_id = Point.objects.all()[randint(0, number_of_points_in_db)].id
                if route_point_id in route_point_ids or route_point_id == end_point.id:
                    continue
                route_point_ids.append(route_point_id)
                break
        route_point_ids.append(end_point.id)
        return route_point_ids


class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_users')

    class Meta:
        ordering = ('-id',)
        unique_together = ('route', 'user')

    def __str__(self):
        return f'{self.user} ??? {self.route}'
