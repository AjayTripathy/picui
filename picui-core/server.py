import web
import json
import shelve
import kdtree as k

urls = ( 
         '/add', 'add',
         '/match', 'match'
       )

app = web.application(urls, globals())

class add:
  def POST(self):
    i = web.input()
    url = str(i.url)
    colorListYUV = paletteAnalysis(url)
    for YUV in colorListYUV:
      store(YUV, {'url': url})
    return 'ok'
  def GET(self):
    i = web.input()
    url = str(i.url)
    callback = str(i.callback)
    return "%s(%s)" % (callback, json.dumps({'status': 'ok'})


class match:
  def GET(self):
    i = web.input()
    colors = str(i.colors)
    #TODO: import kd.tree. return closest matches
    if (i.callback ! = None):
      callback = str(i.callback)
      response = json.dumps(response)
      return "%s(%s)" % (callback, response)
    else:
      return response

def store(tup,data):
  k.add(k.Point(tup, data))
  

def paletteAnalysis(url):
  #colorList = picui(url)
  colorListYUV = []
  for color in colorList:
    #construct RGB tuple
    #transform from RGB to YUV tuple
    #YUV = rgbToYUV(RGB)
    #colorListYUV.append(YUV)
    #k.add(k.Point(YUV, {'url':url})) 
    pass
  return colorListYUV

def rgbToYUV(RGB):
  pass

if __name__ == "__main__":
  app.run()
