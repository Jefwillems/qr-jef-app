import segno
import io


def _get_content_type_for_kind(kind):
    if kind == 'svg':
        return 'image/svg+xml'
    if kind == 'png':
        return 'image/png'
    if kind == 'pdf':
        return 'application/pdf'
    raise ValueError('Wrong kind was sent to qr generator')


def create_qr_code(data, kind='svg', dark_hex=None, light_hex=None):
    """
    Create a qr code with optional customisation
    :param data: The data to encode
    :param kind: kind of image to generate options are: 'svg', 'png', 'pdf'
    :param dark_hex: hex color for the dark modules in the qr code (default None = black)
    :param light_hex: hex color for the background (default None = transparent)
    :return: io.BytesIO
    """
    if dark_hex is None:
        dark_hex = '#000000'
    out = io.BytesIO()
    qr = segno.make(data)
    qr.save(out, kind=kind, dark=dark_hex, light=light_hex, scale=3)
    return out, _get_content_type_for_kind(kind)
