import web
import json
import shelve
import kdtree as k
import imaging

urls = ( 
         '/add', 'add',
         '/match', 'match'
       )

app = web.application(urls, globals())

db = shelve.open('./tree', writeback = True)

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
    #colorListYUV = paletteAnalysis(url)
    colorListYUV = [ {'value': (1,2)} , {'value': (4,7)}, {'value': (3, 4)} ]
    for color in colorListYUV:
      print "here's a new color"
      store(color['value'], {'url': url}, treeName)
    callback = str(i.callback)
    return "%s(%s)" % (callback, json.dumps({'status': 'ok'}))

class match:
  def GET(self):
    i = web.input()
    colors = str(i.colors)
    limit = int(i.limit)
    treeName = str(i.treeName)
    for c in colors:
      RGB = imaging.hex_to_rgb(c)
      color = imaging.rgb_to_yuv(RGB)
      response = lookup(color['value'], limit, treeName)
    if(i.callback != None):
      callback = str(i.callback)
      response = json.dumps(response)
      return "%s(%s)" % (callback, response)
    else:
      return response

def lookup(point, limit, treeName):
  tree = db[treeName]
  nearest = tree.query(point, t=4)
  return nearest.data
  

def store(tup,data,treeName):
  if (treeName in db):
    tree = db[treeName]
    print tree.root_node.right
    tree.add(k.Point(tup, data))
    #db[treeName] = tree
  else: 
    tree = k.KDTree.construct_from_data(None)
    tree.add(k.Point(tup, data))
    db[treeName] = tree
  db.sync() 

def paletteAnalysis(url):
  colorListRGB = fetch_and_extract_colors(url)
  colorListYUV = []
  for color in colorList:
    #construct YUV object
    YUV = imaging.rgb_to_yuv(color['value'])
    colorListYUV.append(YUV)
  return colorListYUV


if __name__ == "__main__":
  app.run()
