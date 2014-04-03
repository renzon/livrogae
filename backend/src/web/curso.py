# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from itertools import izip
from google.appengine.ext import ndb
from curso import fachada
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


def matricula(_write_tmpl, curso_id, pesquisa=''):
    #pesquisa de curso
    curso_id = int(curso_id)
    curso_key = ndb.Key(Curso, curso_id)
    curso_future = curso_key.get_async()

    #pesquisa de usuários por nome
    query = Usuario.query_por_nome(pesquisa)
    usuarios_future = query.fetch_async(50)

    #pesquisa de matrículas
    query = Matricula.query_matriculas_de_curso(curso_key)
    matriculas = query.fetch()
    chaves_usuarios_matriculados = [m.usuario for m in matriculas]
    usuarios_matriculados_future = ndb.get_multi_async(chaves_usuarios_matriculados)

    #construção de paths
    matricula_path = router.to_path(matricular, curso_id)
    desmatricula_path = router.to_path(desmatricular, curso_id)
    matricula_home_path = router.to_path(matricula, curso_id)

    #construção de lista de alunos não matriculados
    usuarios = usuarios_future.get_result()
    usuarios_nao_matriculados = [usuario for usuario in usuarios
                                 if usuario.key not in chaves_usuarios_matriculados]

    curso = curso_future.get_result()
    usuarios_matriculados = [future.get_result() for future in usuarios_matriculados_future]
    dct = {'curso': curso, 'pesquisa': pesquisa,
           'usuarios_matriculados': usuarios_matriculados,
           'usuarios_nao_matriculados': usuarios_nao_matriculados,
           'matricula_path': matricula_path,
           'matricula__home_path': matricula_home_path,
           'desmatricula_path': desmatricula_path}
    _write_tmpl('/templates/matricula.html', dct)


def matricular(_handler, curso_id, usuario_id):
    usuario_key = ndb.Key(Usuario, int(usuario_id))
    fachada.matricular(curso_id, usuario_key)
    _handler.redirect(router.to_path(matricula, curso_id))


def matricular_api(_json, curso_id, usuario_id):
    usuario_key = ndb.Key(Usuario, int(usuario_id))
    matricula = fachada.matricular(curso_id, usuario_key)
    dct = {'id': str(matricula.key.id())}
    _json(dct)


def desmatricular(_handler, curso_id, usuario_id):
    curso_key = ndb.Key(Curso, int(curso_id))
    usuario_key = ndb.Key(Usuario, int(usuario_id))
    query = Matricula.query_matricula(curso=curso_key, usuario=usuario_key)
    matricula_key = query.get(keys_only=True)
    matricula_key.delete()
    _handler.redirect(router.to_path(matricula, curso_id))
