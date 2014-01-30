# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import webapp2


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Olá Mundo!')


class OutroHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Olá Wepapp2!')


class ParametrosHandler(webapp2.RequestHandler):
    def get(self):
        nome = self.request.get('nome')
        sobrenome = self.request.get('sobrenome')
        self.response.write('Olá %s %s!' % (nome, sobrenome))


app = webapp2.WSGIApplication([('/', HomeHandler),
                               ('/outra', OutroHandler),
                               ('/parametros', ParametrosHandler)
                              ],
                              debug=True)
