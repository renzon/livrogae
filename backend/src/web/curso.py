# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from curso.model import Curso
from tekton import router


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


def matricula(_write_tmpl, curso_id):
    curso_id = int(curso_id)
    curso = Curso.get_by_id(curso_id)
    dct = {'curso': curso}
    _write_tmpl('/templates/matricula.html', dct)
