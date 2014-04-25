# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest


class ExemploDeTeste(unittest.TestCase):
    def test_adicao(self):
        resultado_obtido=1+2
        self.assertEqual(3,resultado_obtido)