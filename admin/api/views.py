import json

from django.http import HttpResponse, JsonResponse, Http404
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


def index(request):
    remote_host = request.META['REMOTE_HOST']
    if "" == remote_host:
        action = 'unset'
    else:
        try:
            get_object_or_404(GrowUnit, host=remote_host)
            action = 'exists'
        except Http404 as e:
            unit = GrowUnit(host=remote_host)
            unit.save()
            action = f"persisted {unit.id}"

    return JsonResponse({'provisioning': action})
