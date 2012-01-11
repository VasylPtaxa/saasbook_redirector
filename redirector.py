#!/usr/bin/env python

import urllib
from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
import logging
import re

class RedirectHandler(webapp.RequestHandler):
    def make_target(self):
        target = self.request.path
        logging.debug("Path is " + target)
        method_regexp = re.compile(r"^/(https?)[^/]+//(.*)$")
        target = method_regexp.sub(r'\1://\2', target)
        logging.debug("New path is " + target)
        if self.request.query_string:
            target += ('?' + self.request.query_string) 
        logging.debug("Sending to " + target)
        return(target)

    def get(self):
        target = self.make_target()
        self.redirect(target)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication(
          [('/.*$', RedirectHandler)],
          debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
  main()
