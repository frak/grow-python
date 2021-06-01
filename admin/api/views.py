from django.shortcuts import render, get_object_or_404

from rest_framework.viewsets import ModelViewSet
from .models import GrowUnit
from .serializers import GrowUnitSerializer


class GrowUnitViewSet(ModelViewSet):
    serializer_class = GrowUnitSerializer

    def get_queryset(self):
        return GrowUnit.objects.all().order_by('joined_at')

    def get_object(self):
        return get_object_or_404(GrowUnit, host=self.request.query_params.get('host'))
