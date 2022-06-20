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


class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_routes')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_users')

    class Meta:
        ordering = ('-id',)
        unique_together = ('route', 'user')

    def __str__(self):
        return f'{self.user} – {self.route}'
