from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class AddSlashHandler(webapp.RequestHandler):
  def get(self):
    self.redirect(self.request.url + "/")
  
  def head(self):
    self.get()

def main():
  application = webapp.WSGIApplication([(".*", AddSlashHandler)])
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
