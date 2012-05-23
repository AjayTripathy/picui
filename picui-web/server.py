import web


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
    return 'Success' 

class match:
  def GET(self):
    i = web.input()
    color = str(i.color) 


if __name__ == "__main__":
  app.run()
