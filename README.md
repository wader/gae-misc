Misc Google App Engine snippets.

addslash.py
===========

Simple add-slash-at-end redictor, usefull to get /directory to redirect to /directory/

	handlers:
	- url: /directory
	  script: addslash.py


api.py
======

JSON(P) API helper

	handlers:
	- url: /api/.*
	  script: api.py

Example:

	from google.appengine.ext import webapp
	from google.appengine.ext.webapp.util import run_wsgi_app
	from api import APIHandler

	class TestAPIHandler(APIHandler):
	  required_args = ["reply", "times"]
	  def do(self):
	    self.value = [self.request.get("reply")] * int(self.request.get("times"))

	def main():
	  application = webapp.WSGIApplication([("/api/1/test(\..+)?", TestAPIHandler)],
			       debug=True)
	  run_wsgi_app(application)

	if __name__ == '__main__':
	  main()


Requesting `/api/1/test.jsonp?cb=somecb&reply=two&times=2` will return:

        somecb(["two", "two"]);
