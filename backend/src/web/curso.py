# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from itertools import izip
from google.appengine.ext import ndb
from curso.model import Curso, Matricula
from tekton import router
from usuario.model import Usuario


def index(_write_tmpl):
    query = Curso.query_ordenada_por_nome()
    cursos = query.fetch()
    dct = {'lista_cursos': cursos,
           'matricula_url': router.to_path(matricula),
           'salvar_url': router.to_path(salvar)}
    _write_tmpl('/templates/curso_home.html', dct)


def salvar(_handler, nome):
    curso = Curso(nome=nome)
    curso.put()
    path = router.to_path(index)
    _handler.redirect(path)


def matricula(_write_tmpl, curso_id):
    #pesquisa de curso
    curso_id = int(curso_id)
    curso = Curso.get_by_id(curso_id)

    #pesquisa de todos usuários
    query = Usuario.query_por_nome()
    usuarios = query.fetch(50)

    #pesquisa de matrículas
    query = Matricula.query_matriculas_de_curso(curso.key)
    matriculas = query.fetch()
    chaves_usuarios_matriculados = [m.usuario for m in matriculas]
    usuarios_matriculados = ndb.get_multi(chaves_usuarios_matriculados)

    #construção de path base para matricula e desmatricula
    matricula_path = router.to_path(matricular, curso_id)
    desmatricula_path = router.to_path(desmatricular, curso_id)

    #construção de lista de alunos não matriculados
    usuarios_nao_matriculados = [usuario for usuario in usuarios
                                 if usuario.key not in chaves_usuarios_matriculados]

    dct = {'curso': curso,
           'usuarios_matriculados': usuarios_matriculados,
           'usuarios_nao_matriculados': usuarios_nao_matriculados,
           'matricula_path': matricula_path,
           'desmatricula_path': desmatricula_path}
    _write_tmpl('/templates/matricula.html', dct)


def matricular(_handler, curso_id, usuario_id):
    curso_key = ndb.Key(Curso, int(curso_id))
    usuario_key = ndb.Key(Usuario, int(usuario_id))
    Matricula(curso=curso_key, usuario=usuario_key).put()
    _handler.redirect(router.to_path(matricula, curso_id))


def desmatricular(_handler, curso_id, usuario_id):
    curso_key = ndb.Key(Curso, int(curso_id))
    usuario_key = ndb.Key(Usuario, int(usuario_id))
    query = Matricula.query_matricula(curso=curso_key, usuario=usuario_key)
    matricula_key = query.get(keys_only=True)
    matricula_key.delete()
    _handler.redirect(router.to_path(matricula, curso_id))
