# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.ndb.polymodel import PolyModel


class Usuario(PolyModel):
    nome = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    criacao = ndb.DateTimeProperty(auto_now_add=True)

    def origem(self):
        raise NotImplementedError()

    @classmethod
    def query_por_nome(cls,nome=''):
        return cls.query(cls.nome>=nome).order(cls.nome)


class UsuarioFacebook(Usuario):
    face_id = ndb.StringProperty(required=True)

    def origem(self):
        return 'Facebook (%s)' % self.face_id

class UsuarioGoogle(Usuario):
    google_id = ndb.StringProperty(required=True)

    def origem(self):
        return 'Google (%s)' % self.google_id


