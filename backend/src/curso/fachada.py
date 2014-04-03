# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from curso.negocio import matricular_usuario, PesquisarCursoCmd


def matricular(curso_id, usuario_key):
    '''
    Função que efetua a matrícula de uma entidade em um curso
    Retorna um modelo do tipo Matricula
    '''
    return matricular_usuario(curso_id, usuario_key)


def pesquisar_curso(curso_id):
    '''
    Retorna uma tupla com um Command que pesquisa o curso dado seu id como primeiro elemento
    E a chave do curso como segundo elemento
    O curso retornado se encontra no atributo result do Comando após sua execução
    '''
    cmd = PesquisarCursoCmd(curso_id)
    return cmd, cmd.curso_key