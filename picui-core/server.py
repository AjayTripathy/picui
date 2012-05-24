import web
import json
import shelve
import kdtree as k
import colorific

urls = ( 
         '/add', 'add',
         '/match', 'match'
       )

app = web.application(urls, globals())

db = shelve.open('./tree')

class add:
  def POST(self):
    i = web.input()
    url = str(i.url)
    treeName = str(i.treeName)
    colorListYUV = paletteAnalysis(url)
    for YUV in colorListYUV:
      store(YUV, {'url': url}, treeName)
    return 'ok'
  def GET(self):
    i = web.input()
    url = str(i.url)
    treeName = str(i.treeName)
    colorListYUV = paletteAnalysis(url)
    colorListYUV = [(1,2), (4,7), (3, 4)]
    for YUV in colorListYUV:
      store(YUV, {'url': url}, treeName)
      callback = str(i.callback)
    return "%s(%s)" % (callback, json.dumps({'status': 'ok'}))

class match:
  def GET(self):
    i = web.input()
    colors = str(i.colors)
    if(i.callback != None):
      callback = str(i.callback)
      response = json.dumps(response)
      return "%s(%s)" % (callback, response)
    else:
      return response

def store(tup,data,treeName):
  if (db[treeName] != None):
    tree = db[treeName]
    tree.add(k.Point(tup, data))
  else: 
    tree = k.KDTree.construct_from_data(None)
    tree.add(k.Point(tup, data))
    db[treeName] = tree
  db.sync() 

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
