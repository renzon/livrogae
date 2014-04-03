# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from curso.model import Curso, Matricula


def matricular_usuario(curso_id, usuario_key):
    curso_key = ndb.Key(Curso, int(curso_id))
    matricula = Matricula(curso=curso_key, usuario=usuario_key)
    matricula.put()
    return matricula