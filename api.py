from google.appengine.ext import webapp
import string
from django.utils import simplejson
import datetime

class DateTimeJSONEncoder(simplejson.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.strftime('%Y-%m-%dT%H:%M:%S')
    else:
      return simplejson.JSONEncoder.default(self, obj)

class APIHandler(webapp.RequestHandler):
  accepted_formats = ["json", "jsonp"]
  format = "json"
  required_args = []
  value = None
  raw = False

  def set_error(self, message):
    self.response.set_status(400)
    self.value = {"error": message}

  def verify(self):
    for arg in self.required_args:
      if arg not in self.request.arguments():
        return self.set_error("%s argument is missing" % arg)

      if self.request.get(arg).strip() == "":
        return self.set_error("%s argument is empty" % arg)

  def result(self):
    if self.raw:
      self.response.out.write(self.value)
      return

    if self.format not in self.accepted_formats:
      self.set_error("Format %s not accepted" % self.format)
      self.format = "json"

    if self.value is None:
      self.value = True

    if self.format is None or self.format == "json" or self.format == "jsonp":
      json = DateTimeJSONEncoder().encode(self.value)
      if self.format == "jsonp":
        json = self.request.get("cb", "cb") + "(" + json + ");"
        self.response.headers["Content-Type"] = "application/javascript"
      else:
        self.response.headers["Content-Type"] = "application/json"
      self.response.out.write(json)
    else:
      self.response.out.write("unknown format %s" % self.format)

  def _do(self, *args, **kw):
    self.verify()

    # if last group is an extension (eg: .json) set it as format and remove group
    if args[-1] is not None and len(args[-1]) > 0 and args[-1][0] == ".":
      self.format = args[-1][1:]
    args = args[0:-1]

    if self.value is None:
      self.do(*args, **kw)
    self.result()

  def get(self, *args, **kw):
    self._do(*args, **kw)

  def post(self, *args, **kw):
    self._do(*args, **kw)
