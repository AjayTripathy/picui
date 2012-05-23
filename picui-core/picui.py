import colorific
from StringIO import StringIO
import urllib2

def fetch_and_extract(url):
    response = urllib2.urlopen(url)
    virtual_file = StringIO(response.read())
    return colorific.extract_colors(virtual_file)
