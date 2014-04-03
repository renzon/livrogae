# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import Command
from usuario.model import Usuario


class PesquisaUsuariosPorNome(Command):
    def __init__(self, nome):
        super(PesquisaUsuariosPorNome, self).__init__()
        self.nome = nome
        self.__future = None

    def set_up(self):
        query = Usuario.query_por_nome(self.nome)
        self.__future = query.fetch_async(50)

    def do_business(self, stop_on_error=True):
        self.result = self.__future.get_result()

