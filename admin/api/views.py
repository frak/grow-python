from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from .models import GrowUnit
from .serializers import GrowUnitSerializer


class GrowUnitViewSet(ModelViewSet):
    serializer_class = GrowUnitSerializer

    def get_queryset(self):
        return GrowUnit.objects.all().order_by('joined_at')

    def get_object(self):
        return get_object_or_404(GrowUnit, host=self.request.query_params.get('host'))


def index(request, host_name):
    if "" == host_name:
        action = 'unset'
    else:
        try:
            get_object_or_404(GrowUnit, host=host_name)
            action = 'exists'
        except Http404 as e:
            unit = GrowUnit(host=host_name)
            unit.save()
            action = f"persisted {unit.id}"

    return JsonResponse({'provisioning': action})
