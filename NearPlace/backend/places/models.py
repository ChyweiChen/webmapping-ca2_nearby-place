from django.db import models
from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=128)
    location = models.PointField()
    address = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    category = models.CharField(max_length=128)

    def get_distance(self):
        self.get_waypoint()
        try:
            distance = self.distance
        except Exception as e:
            return ''
        else:
            return distance

    def get_waypoint(self):
        return {'lat': self.location.y, 'lng': self.location.x}

