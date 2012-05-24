import colorific
from StringIO import StringIO
import urllib2


def fetch_and_extract_colors(url):
    response = urllib2.urlopen(url)
    virtual_file = StringIO(response.read())

    [{'value':color.value, 'score':color.prominence}for color in colorific extract_colors(virtual_file)]


def hex_to_rgb(hexstr):
    hexstr = hexstr[1:]
    rgb = tuple(ord(c) for c in hexstr.decode('hex'))
    return {'value': rgb, 'score': None}


def rgb_to_hex(color):
    rgb = color["value"]
    return '#%.02x%.02x%.02x' % rgb


def rgb_to_yuv(color):
    rgb = color["value"]
    y = (0.299 * rgb[0]) + (0.587 * rgb[1]) + (0.114 * rgb[2])
    u = (-0.14713 * rgb[0]) + (-0.28886 * rgb[1]) + (0.436 * rgb[2])
    v = (0.615 * rgb[0]) + (-0.51499 * rgb[1]) + (-0.10001 * rgb[2])
    return {'value': (y, u, v), 'score': color['score']}
