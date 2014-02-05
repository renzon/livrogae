# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def index(_resp):
    _resp.write("Página do Usuário")


def ola(_resp, nome):
    _resp.write("Olá %s" % nome)

