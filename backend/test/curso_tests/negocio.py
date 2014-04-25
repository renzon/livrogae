# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from curso.model import Curso
from curso.negocio import PesquisarCursoCmd
from util import GAETestCase


class PesquisarCursoTest(GAETestCase):
    def test_execute(self):
        curso=Curso(nome='PyPrático')
        curso.put()
        curso_id_str=str(curso.key.id())
        comando=PesquisarCursoCmd(curso_id_str)
        comando.execute()
        curso_encontrado=comando.result
        self.assertEqual(curso.key, curso_encontrado.key)
