import uuid

from django.core.exceptions import ValidationError
from django.http import Http404

from .models import QRCode


def get_code_from_uuid_or_short(uid, queryset=None):
    if queryset is None:
        queryset = QRCode.objects.all()
    try:
        try:
            short_uuid = uuid.UUID(uid)
            return queryset.get(uuid=short_uuid)
        except ValueError:
            return queryset.get(short_uuid=uid)
    except QRCode.DoesNotExist or ValidationError:
        raise Http404
