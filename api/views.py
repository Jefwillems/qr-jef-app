from django.urls import reverse
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import ApiHit, QRCode, LinkUrl
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView
import random
from generator.qrcode import create_qr_code
import base64

from .util import get_code_from_uuid_or_short


def download_code(request, short_uuid):
    code = get_code_from_uuid_or_short(short_uuid)

    img_format = request.GET.get('format', 'svg')
    img_light = request.GET.get('light', None)
    img_dark = request.GET.get('dark', None)

    code_url = request.build_absolute_uri(reverse("qrcode-detail", kwargs=dict(short_uuid=code.short_uuid)))
    qr, content_type = create_qr_code(code_url, kind=img_format, dark_hex=img_dark, light_hex=img_light)

    response = HttpResponse(qr.getvalue(), content_type=content_type)
    response['Content-Length'] = len(response.content)
    response['Content-Disposition'] = f'attachment; filename="{code.title}.{img_format}"'
    return response


class CodeView(DetailView):
    template_name = 'api/qrcode/code.html'
    pk_url_kwarg = 'short_uuid'
    queryset = QRCode.objects.all()
    context_object_name = 'code'

    def get_object(self, queryset=None):
        uid = self.kwargs.get(self.pk_url_kwarg)
        return get_code_from_uuid_or_short(uid, queryset)

    def get_qr_string(self, code):
        code_url = self.request.build_absolute_uri(reverse('qrcode-detail', kwargs=dict(short_uuid=code.short_uuid)))
        qr, content_type = create_qr_code(code_url, kind='svg')
        image = base64.b64encode(qr.getvalue())
        image = image.decode('utf8')
        return image, content_type

    def get_context_data(self, **kwargs):
        context = super(CodeView, self).get_context_data(**kwargs)
        img, content_type = self.get_qr_string(context[self.context_object_name])
        context['img'] = img
        context['content_type'] = content_type
        return context


class QRCodeDetails(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = []
    pk_url_kwarg = 'short_uuid'

    def get_object(self, queryset=None):
        uid = self.kwargs.get(self.pk_url_kwarg)
        return get_code_from_uuid_or_short(uid, queryset)

    def get(self, request, short_uuid=None, format=None):
        qrcode = self.get_object()

        if request.accepted_renderer.format == 'json' or format == 'json':
            if request.user.is_authenticated:
                hit = ApiHit(
                    code=qrcode, action=ApiHit.ACTION_CHOICES.JSON)
                hit.save()
                return redirect(to=reverse('api-code-detail', kwargs={'pk': qrcode.id}), permanent=False)
            else:
                raise NotAuthenticated

        if request.accepted_renderer.format == 'html' or format == 'html':
            if qrcode.urls.count() == 0:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.BASIC_INFO)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')

            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.REDIRECT:
                hit = ApiHit(
                    code=qrcode, action=ApiHit.ACTION_CHOICES.REDIRECT)
                hit.save()
                return redirect(qrcode.urls.first().url, permanent=False)
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.KIOSK:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.KIOSK)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/kiosk.html')
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.INFO_PAGE:
                hit = ApiHit(code=qrcode, action=ApiHit.ACTION_CHOICES.BASIC_INFO)
                hit.save()
                return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')
            if qrcode.mode == QRCode.REDIRECT_MODE_CHOICES.CHANCE_REDIRECT:
                urls = LinkUrl.objects.filter(code=qrcode).all()
                url_count = urls.count()
                avgs = [x.priority / url_count for x in urls]
                choice = random.choices(urls, avgs, k=1)
                return HttpResponse(choice[0].name)

            return Response({'qrcode': qrcode}, template_name='api/qrcode/index.html')

        hit = ApiHit(
            code=qrcode, action=ApiHit.ACTION_CHOICES.JSON)
        hit.save()
        return redirect(to=reverse('api-code-detail', kwargs={'pk': qrcode.id}), permanent=False)
