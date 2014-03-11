# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from curso.model import Curso
from tekton import router


class CursoFake(object):
    def __init__(self, nome='', slug=''):
        self.slug = slug
        self.nome = nome


cursos = [CursoFake(nome, slug) for nome, slug in (('PyPrático', 'pypratico'),
                                                   ('Objetos Pythônicos', 'objetos-pythonicos'),
                                                   ('Python para quem sabe Python', 'pythor-para-quem-sabe-python'))]

cursos_dct = {curso.slug: curso for curso in cursos}


def index(_write_tmpl):
    query = Curso.query_ordenada_por_nome()
    cursos = query.fetch()
    dct = {'lista_cursos': cursos,
           'matricula_url': router.to_path(matricula),
           'salvar_url': router.to_path(salvar)}
    _write_tmpl('/templates/curso_home.html', dct)


def salvar(_handler, nome):
    curso = Curso(nome=nome)
    curso.put()
    path = router.to_path(index)
    _handler.redirect(path)


def matricula(_write_tmpl, curso_key_urlsafe):
    key = ndb.Key(urlsafe=curso_key_urlsafe)
    curso = key.get()
    dct = {'curso': curso}
    _write_tmpl('/templates/matricula.html', dct)
