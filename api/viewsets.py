from rest_framework.viewsets import GenericViewSet

from api.serializers import QRCodeSerializer, ApiHitSerializer, LinkUrlSerializer
from api.models import ApiHit, QRCode, LinkUrl
from rest_framework import viewsets, mixins
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, DateTimeFilter, NumberFilter


class CodeViewSet(viewsets.ModelViewSet):
    serializer_class = QRCodeSerializer
    queryset = QRCode.objects.order_by('-last_updated')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('mode', 'title', 'created', 'last_updated', 'uuid')


class ApiHitFilterSet(FilterSet):
    action = CharFilter(field_name='action', lookup_expr='icontains')
    hit_date = DateTimeFilter(field_name='hit_date')
    code_id = NumberFilter(field_name='code__id', lookup_expr='exact', label='Code id')


class ApiHitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApiHitSerializer
    queryset = ApiHit.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = ApiHitFilterSet


class LinkUrlViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    serializer_class = LinkUrlSerializer
    queryset = LinkUrl.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('code',)
