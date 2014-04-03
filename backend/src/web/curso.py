# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from curso import fachada
from curso.fachada import pesquisar_curso, pesquisar_matriculas_de_curso, pesquisar_usuarios_de_matriculas, \
    filtrar_usuarios_matriculados
from curso.model import Curso, Matricula
from tekton import router
from usuario.fachada import pesquisar_usuarios_por_nome
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
    pesquisar_curso_cmd, curso_key = pesquisar_curso(curso_id)
    pesquisar_usuarios_cmd = pesquisar_usuarios_por_nome(pesquisa)
    pesquisar_matriculas_cmd = pesquisar_matriculas_de_curso(curso_key)

    lista_de_comandos = pesquisar_curso_cmd + \
                        pesquisar_usuarios_cmd + \
                        pesquisar_matriculas_cmd

    # Execução de todos comandos
    lista_de_comandos.execute()

    #extração de resultados
    curso = pesquisar_curso_cmd.result
    usuarios = pesquisar_usuarios_cmd.result
    matriculas = pesquisar_matriculas_cmd.result

    #construção de lista de alunos matriculados e não matriculados

    pesquisar_matriculados_cmd, chaves_matriculados = \
        pesquisar_usuarios_de_matriculas(matriculas)
    filtrar_matriculados_cmd = filtrar_usuarios_matriculados(usuarios,
                                                             chaves_matriculados)
    lista_de_comandos_2 = pesquisar_matriculados_cmd + filtrar_matriculados_cmd
    lista_de_comandos_2.execute()

    usuarios_matriculados = pesquisar_matriculados_cmd.result
    usuarios_nao_matriculados = filtrar_matriculados_cmd.result

    #construção de paths
    matricula_path = router.to_path(matricular, curso_id)
    desmatricula_path = router.to_path(desmatricular, curso_id)
    matricula_home_path = router.to_path(matricula, curso_id)
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
