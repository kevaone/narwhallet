from enum import Enum


class content_type(Enum):
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    css = 'text/css'
    gif = 'image/gif'
    htm = 'text/html'
    html = 'text/html'
    ico = 'image/bmp'
    jpg = 'image/jpeg'
    jpeg = 'image/jpeg'
    js = 'application/javascript'
    png = 'image/png'
    txt = 'text/plain; charset=us-ascii'
    json = 'application/json'
    svg = 'image/svg+xml'
