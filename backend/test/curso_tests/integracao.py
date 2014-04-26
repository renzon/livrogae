# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from curso.model import Curso
from mock import Mock
import tmpl
from util import GAETestCase
from web import curso


class IndexTests(GAETestCase):
    def test_nenhum_curso_cadastrado(self):
        write_tmpl_mock = Mock()
        curso.index(write_tmpl_mock)
        template = '/templates/curso_home.html'
        dct = {'lista_cursos': [],
               'matricula_url': '/curso/matricula',
               'salvar_url': '/curso/salvar'}

        # testando se mock foi chamado com parâmetros esperados
        write_tmpl_mock.assert_called_once_with(template, dct)

        # testando se não há erros na renderização do template
        try:
            tmpl.render(template, dct)
        except:
            self.fail('Renderizaçao do template %s com problemas' % template)

    def test_cursos_cadastrados(self):
        cursos = [Curso(nome='PyPrático'), Curso(nome='Python para quem Sabe Python')]
        ndb.put_multi(cursos)
        write_tmpl_mock = Mock()
        curso.index(write_tmpl_mock)
        template = '/templates/curso_home.html'
        dct = {'lista_cursos': cursos,
               'matricula_url': '/curso/matricula',
               'salvar_url': '/curso/salvar'}

        # testando se mock foi chamado com parâmetros esperados
        write_tmpl_mock.assert_called_once_with(template, dct)

        # testando se não há erros na renderização do template
        try:
            tmpl.render(template, dct)
        except:
            self.fail('Renderizaçao do template %s com problemas' % template)