import colorific
from StringIO import StringIO
import phash
import urllib2

def fetch_image_as_file(url):
    response = urllib2.urlopen(url)
    pseudofile = StringIO(response.read())
    return pseudofile

def fetch_and_extract_colors(url):
    imfile = fetch_image_as_file(url)
    palette = colorific.extract_colors(imfile)
    colors = palette.colors
    return [{'value':color.value, 'score':color.prominence} for color in colors]


def image_similarity(url1, url2):
    return hamming_distance(blur_and_edge_hash(url1), edge_hash(url2))


def blur_and_edge_hash(url):
    imfile = fetch_image_as_file(url)
    return phash.ImageHash(imfile).blur_hash()


def edge_hash(url):
    imfile = fetch_image_as_file(url)
    return phash.ImageHash(imfile).edge_hash()


def hamming_distance(hash1, hash2):
    return phash.ImageHash(hash1, hash2)


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


def yuv_to_rgb(color):
    y, u, v = color["value"]
    r = y + (1.403 * v)
    g = y - (0.344 * u) - (0.714 * v)
    b = y + (1.770 * u)

    if (r < 0):
        r = 0
    elif (r > 255):
        r = 255

    if (g < 0):
        g = 0
    elif (g > 255):
        g = 255

    if (b < 0):
        b = 0
    elif (b > 255):
        b = 255

    return {'value': (r, g, b), 'score': color['score']}
