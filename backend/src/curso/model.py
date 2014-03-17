# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from usuario.model import Usuario


class Curso(ndb.Model):
    nome = ndb.StringProperty(required=True)

    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(cls.nome)


class Matricula(ndb.Model):
    curso = ndb.KeyProperty(Curso, required=True)
    usuario = ndb.KeyProperty(Usuario, required=True)
    criacao = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_matriculas_de_curso(cls, curso_key):
        return cls.query(cls.curso == curso_key)

    @classmethod
    def query_matricula(cls, curso, usuario):
        return cls.query(cls.curso == curso, cls.usuario == usuario)
