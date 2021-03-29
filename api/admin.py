from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from django.urls import path, reverse
import requests
import io
import zipfile

from api.models import ApiHit, LinkUrl, QRCode


@admin.register(ApiHit)
class ApiHitAdmin(admin.ModelAdmin):
    readonly_fields = ('hit_date', 'action', 'code', 'message')
    list_display = ('code', 'hit_date', 'action', 'message')
    change_list_template = 'api/apihit/change_list.html'

    def get_list_display(self, request):
        return super(ApiHitAdmin, self).get_list_display(request)


class LinkUrlInline(admin.StackedInline):
    model = LinkUrl
    extra = 1


@admin.register(QRCode)
class QRCodeAdmin(VersionAdmin):
    list_display = ('title',
                    'get_code_url', 'get_code_image_url')
    search_fields = ('title',)
    inlines = [LinkUrlInline]
    change_list_template = 'api/qrcode/change_list.html'
    actions = ['download_codes', ]
    readonly_fields = ('uuid',)

    def get_model_perms(self, request):
        return super(QRCodeAdmin, self).get_model_perms(request)

    def get_code_image_url(self, obj):
        return mark_safe(f'<span><a href="/code/{obj.short_uuid}">/code/{obj.short_uuid}</a></span>')

    def get_code_url(self, obj):
        return mark_safe(f'<span><a href="/{obj.short_uuid}">/{obj.short_uuid}</a></span>')

    get_code_image_url.short_description = 'Code image'
    get_code_url.short_description = 'Code url'

    def download_codes(self, request, queryset):
        zip_filename = 'archive.zip'
        s = io.BytesIO()

        zf = zipfile.ZipFile(s, mode='w', compression=zipfile.ZIP_DEFLATED)

        downloaded_files = []
        for code in queryset.all():
            url = request.build_absolute_uri(reverse('code-dl', kwargs=dict(short_uuid=code.uuid)))
            res = requests.get(url)
            zf.writestr(f'{code.title}-{code.uuid}.svg', res.content)
            downloaded_files.append(code.title)

        zf.close()

        resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        resp['Content-Disposition'] = f'attachment; filename={zip_filename}'

        message = f'Downloaded zip with files: {", ".join(downloaded_files)}'
        self.message_user(request, message=message)
        return resp

    def get_urls(self):
        urls = super(QRCodeAdmin, self).get_urls()
        custom_urls = [
            path('scan/', self.admin_site.admin_view(self.scan_view))
        ]
        return custom_urls + urls

    def scan_view(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            is_nav_sidebar_enabled=False,
            title='Scan qr code'
        )

        return TemplateResponse(request, 'api/qrcode/scanner.html', context)


admin.site.site_header = 'Qr Jef Administration'
admin.site.site_title = 'Qr Jef admin'
admin.site.site_url = '/api/'
