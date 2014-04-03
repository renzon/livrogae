# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from curso.negocio import matricular_usuario, PesquisarCursoCmd, PesquisarMatriculasDeCursoCmd, \
    PesquisarUsuariosDeMatriculas, FiltrarUsuariosMatriculadosCmd


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


def pesquisar_matriculas_de_curso(curso_key):
    '''
    Retorna comando que pesquisa mastriculas respectivas a um curso
    O resultado se encontra no atributo result do comando após sua execução
    '''
    return PesquisarMatriculasDeCursoCmd(curso_key)


def pesquisar_usuarios_de_matriculas(matriculas):
    '''
    Retorna uma tupla contendu comando que pesquisa usuarios respectivos a uma lista de matriculas
    como primeiro elemento e a lista de chaves dos usuário como segundo elemento

    O resultado da pesquisa se encontra no atributo result do comando após sua execução
    '''
    cmd = PesquisarUsuariosDeMatriculas(matriculas)
    return cmd, cmd.chaves_usuarios_matriculados


def filtrar_usuarios_matriculados(usuarios, chaves_matriculados):
    '''
    Retorna comando que filtra usuarios não matriculdos de uma lista de usuários

    O resultado da filtragem se encontra no atributo result do comando após sua execução
    '''
    return FiltrarUsuariosMatriculadosCmd(usuarios, chaves_matriculados)