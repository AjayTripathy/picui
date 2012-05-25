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
    for f in i:
      print f
    url = str(i.url)
    print url
    treeName = str(i.treeName)
    colorListYUV = paletteAnalysis(url)
    for color in colorListYUV:
      store(color['value'], {'url': url, 'score': color['score']}, treeName)
    return json.dumps({'status':'ok'})
  def GET(self):
    i = web.input()
    url = str(i.url)
    treeName = str(i.treeName)
    callback = str(i.callback)
    colorListYUV = paletteAnalysis(url)
    #colorListYUV = [ {'value': (1,2)} , {'value': (4,7)}, {'value': (3, 4)} ]
    for color in colorListYUV:
      store(color['value'], {'url': url, 'score' : color['score'] }, treeName)
    return "%s(%s)" % (callback, json.dumps({'status': 'ok'}))

class match:
  def GET(self):
    i = web.input()
    colors = str(i.colors)
    print colors
    colors = json.loads(colors)
    limit = int(i.limit)
    treeName = str(i.treeName)
    for c in colors:
      RGB = imaging.hex_to_rgb(c)
      color = imaging.rgb_to_yuv(RGB)
      matchList = lookup(color['value'], limit, treeName)
      matchList.sort(key = lambda color: color['score'], reverse = True)
      checkDuplicates = set()
      response = []
      for col in matchList:
        if (not (col['url'] in checkDuplicates)):
           checkDuplicates.add(col['url'])
           response.append(col)

      response = json.dumps(response)
    if('callback' in dir(i)):
      callback = str(i.callback)
      return "%s(%s)" % (callback, response)
    else:
      return response

def lookup(point, limit, treeName):
  tree = db[treeName]
  nearest = tree.query(point, t=limit)
  retList = []
  for point in nearest:
    retList.append(point.data)
  return retList
  

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
  colorListRGB = imaging.fetch_and_extract_colors(url)
  colorListYUV = []
  for color in colorListRGB:
    #construct YUV object
    YUV = imaging.rgb_to_yuv(color)
    colorListYUV.append(YUV)
  return colorListYUV


if __name__ == "__main__":
  app.run()
