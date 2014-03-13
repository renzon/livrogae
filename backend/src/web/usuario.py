# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router
from usuario.model import UsuarioGoogle, Usuario, UsuarioFacebook


def index(_write_tmpl):
    dct = {'adicionar_usuario_google_path': router.to_path(google),
           'adicionar_usuario_face_path': router.to_path(face)}
    query = Usuario.query().order(Usuario.nome)
    dct['usuarios'] = query.fetch()
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