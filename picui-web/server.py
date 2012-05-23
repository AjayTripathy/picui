import web
import json


urls = ( 
         '/upload', 'upload',
         '/match', 'match'
       )

app = web.application(urls, globals())

class upload:
  def POST(self):
    i = web.input()
    url = str(i.url)
    #colorList = picui(url)
    #TODO: Put list of colors in database    
    return url

class match:
  def GET(self):
    i = web.input()
    color = str(i.color)
    callback = str(i.callback)
    #TODO: find appropriate colors in the database
    response = {'color': color}
    response = json.dumps(response)
    return "%s(%s)" % (callback, response) 

if __name__ == "__main__":
  app.run()
