# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from usuario.negocio import PesquisaUsuariosPorNome


def pesquisar_usuarios_por_nome(nome=''):
    '''
    Retorna comando para pesquisa de usuário por nome
    O resultado da busca se encontra no atributo result após execução do comando
    '''
    return PesquisaUsuariosPorNome(nome)