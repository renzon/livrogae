# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import webapp2

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Olá Mundo!')



app = webapp2.WSGIApplication([
    ('/', HomeHandler)
], debug=True)
