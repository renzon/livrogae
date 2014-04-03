# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from curso.negocio import matricular_usuario


def matricular(curso_id, usuario_key):
    '''
    Função que efetua a matrícula de uma entidade em um curso
    Retorna um modelo do tipo Matricula
    '''
    return matricular_usuario(curso_id,usuario_key)