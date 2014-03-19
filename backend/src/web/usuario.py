# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router
from usuario.model import UsuarioGoogle, Usuario, UsuarioFacebook


def index(_write_tmpl, pagina_atual=1):
    pagina_atual = int(pagina_atual)
    offset = int(pagina_atual) - 1
    TAMANHO_DA_PAGINA = 2

    #Busca assíncrona por usuários
    query = Usuario.query().order(Usuario.nome)
    usuarios_future = query.fetch_async(offset=offset, limit=TAMANHO_DA_PAGINA)

    #Setup de numeração de páginas
    pagina_inicial = max(1, pagina_atual - 2)
    pagina_final = pagina_inicial + 4
    pagina_anterior = max(pagina_inicial, pagina_atual - 1)

    #Construção de parâmetros a serem renderizados pelo template
    dct = {'adicionar_usuario_google_path': router.to_path(google),
           'adicionar_usuario_face_path': router.to_path(face),
           'home_path': router.to_path(index),
           'pagina_atual': pagina_atual,
           'pagina_inicial': pagina_inicial,
           'pagina_final': pagina_final,
           'pagina_anterior': pagina_anterior,
           'pagina_posterior': pagina_atual + 1,
           'usuarios': usuarios_future.get_result()}

    _write_tmpl("/templates/usuario_home.html", dct)


def google(_write_tmpl):
    dct = {'salvar_url': router.to_path(salvar_google)}
    _write_tmpl("/templates/usuario_google.html", dct)


def salvar_google(_handler, nome, email, google_id):
    UsuarioGoogle(nome=nome, email=email, google_id=google_id).put()
    _handler.redirect(router.to_path(index))


def face(_write_tmpl):
    dct = {'salvar_url': router.to_path(salvar_face)}
    _write_tmpl("/templates/usuario_face.html", dct)


def salvar_face(_handler, nome, email, face_id):
    UsuarioFacebook(nome=nome, email=email, face_id=face_id).put()
    _handler.redirect(router.to_path(index))