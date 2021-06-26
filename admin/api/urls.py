from django.conf.urls import url
from django.urls import path
from .views import GrowUnitViewSet, index

urlpatterns = [
    path('provision/<str:host_name>', index, name='provision'),
    url(r'^grow-unit$', GrowUnitViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }
    )),
    url(r'^grow-units$', GrowUnitViewSet.as_view(
        {
            'get': 'list',
        }
    ))
]
