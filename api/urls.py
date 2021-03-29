from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from . import views
from . import viewsets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r'qrcodes', viewsets.CodeViewSet, basename='api-code')
router.register(r'apihits', viewsets.ApiHitViewSet, basename='api-apihit')
router.register(r'urls', viewsets.LinkUrlViewSet, basename='api-url')

urlpatterns = [
    path('code/<slug:short_uuid>/', views.CodeView.as_view(), name='code-detail'),
    path('code/<slug:short_uuid>/dl/', views.download_code, name='code-dl'),
]

urlpatterns += [path('api/', include(router.urls)),
                path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                path('openapi/', get_schema_view(
                    title="Qr code Toolkit API",
                    description="Stad Gent qr code toolkit",
                    version="1.0.0",
                    patterns=router.urls,
                    url='/api/'
                ), name='openapi-schema'),
                path('swui/', TemplateView.as_view(
                    template_name='api/swagger-ui.html',
                    extra_context={'schema_url': 'openapi-schema'}
                ), name='swagger-ui'),
                ]

suffixed_urlpatterns = [
    path('<slug:short_uuid>/', views.QRCodeDetails.as_view(), name='qrcode-detail')
]
suffixed_urlpatterns = format_suffix_patterns(suffixed_urlpatterns, allowed=['html', 'json'])

urlpatterns += suffixed_urlpatterns
