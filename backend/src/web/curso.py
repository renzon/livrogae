# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router


class Curso(object):
    def __init__(self, nome='', slug=''):
        self.slug = slug
        self.nome = nome


cursos = [Curso(nome, slug) for nome, slug in (('PyPrático', 'pypratico'),
                                               ('Objetos Pythônicos', 'objetos-pythonicos'),
                                               ('Python para quem sabe Python', 'pythor-para-quem-sabe-python'))]

cursos_dct = {curso.slug: curso for curso in cursos}


def index(_write_tmpl):
    dct = {'lista_cursos': cursos,
           'matricula_url': router.to_path(matricula)}
    _write_tmpl('/templates/curso_home.html', dct)


def matricula(_write_tmpl, curso_slug):
    dct = {'curso': cursos_dct[curso_slug]}
    _write_tmpl('/templates/matricula.html', dct)
