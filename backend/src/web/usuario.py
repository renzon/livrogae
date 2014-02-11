# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def index(_resp):
    _resp.write("Página do Usuário")


def redirecionar(_handler):
    url=r'/usuario/ola/Renzo/Nuccitelli'
    _handler.redirect(url)


def ola(_resp, nome, sobrenome):
    _resp.write("Olá %s %s" % (nome, sobrenome))

