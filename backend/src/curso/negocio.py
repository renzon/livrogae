# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from curso.model import Curso, Matricula
from gaebusiness.business import Command


def matricular_usuario(curso_id, usuario_key):
    curso_key = ndb.Key(Curso, int(curso_id))
    matricula = Matricula(curso=curso_key, usuario=usuario_key)
    matricula.put()
    return matricula


class PesquisarCursoCmd(Command):
    def __init__(self, curso_id):
        super(PesquisarCursoCmd, self).__init__()
        curso_id = int(curso_id)
        self.curso_key = ndb.Key(Curso, curso_id)
        self.__curso_future = None

    def set_up(self):
        self.__curso_future = self.curso_key.get_async()

    def do_business(self, stop_on_error=True):
        self.result = self.__curso_future.get_result()
