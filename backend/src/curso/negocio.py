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


class PesquisarMatriculasDeCursoCmd(Command):
    def __init__(self, curso_key):
        super(PesquisarMatriculasDeCursoCmd, self).__init__()
        self.__query = Matricula.query_matriculas_de_curso(curso_key)
        self.__future = None

    def set_up(self):
        self.__future = self.__query.fetch_async()

    def do_business(self, stop_on_error=True):
        self.result = self.__future.get_result()


class PesquisarUsuariosDeMatriculas(Command):
    def __init__(self, matriculas):
        super(PesquisarUsuariosDeMatriculas, self).__init__()
        self.chaves_usuarios_matriculados = [m.usuario for m in matriculas]
        self.__futures = None

    def set_up(self):
        self.__futures = ndb.get_multi_async(self.chaves_usuarios_matriculados)

    def do_business(self, stop_on_error=True):
        self.result = [f.get_result() for f in self.__futures]


class FiltrarUsuariosMatriculadosCmd(Command):
    def __init__(self, usuarios, chaves_matriculados):
        super(FiltrarUsuariosMatriculadosCmd, self).__init__()
        self.chaves_matriculados = chaves_matriculados
        self.usuarios = usuarios

    def do_business(self, stop_on_error=True):
        self.result = [usuario
                       for usuario in self.usuarios
                       if usuario.key not in self.chaves_matriculados]