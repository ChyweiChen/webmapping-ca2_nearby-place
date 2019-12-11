from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

import django_filters
from rest_framework import mixins, viewsets

from .models import Place
from .serializers import PlaceSerializer


class DistanceFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        value = value.split(',')
        if value and len(value) == 2:
            lon = float(value[0])
            lat = float(value[1])
            try:
                user_location = Point(lon, lat, srid=4326)
                qs = qs.annotate(distance=Distance('location', user_location)).order_by(
                    'distance')
            except Exception as e:
                raise django_filters.exceptions.FieldLookupError
        return qs


class CategoryFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(category=value).all()
        return qs


class PlaceFilter(django_filters.FilterSet):
    category = CategoryFilter()
    location = DistanceFilter()  # lng, lat


class PlaceViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
    filterset_class = PlaceFilter
