# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def index(_write_tmpl):
    class Curso(object):
        def __init__(self, nome=''):
            self.nome = nome

    cursos = [Curso(nome) for nome in ('PyPrático',
                                       'Objetos Pythônicos',
                                       'Python para quem sabe Python')]

    dct = {'lista_cursos': cursos}
    _write_tmpl('/templates/curso_home.html', dct)
