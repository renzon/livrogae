# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router


@no_csrf
@login_not_required
def index(_write_tmpl):
    _write_tmpl('login/passwordless_info.html')


@login_not_required
def enviar_email(_handler, email, ret_path='/'):
    url = 'https://livrogae.appspot.com' + router.to_path(checar, ret_path=ret_path)
    facade.send_passwordless_login_link(email, url, 'pt_BR').execute()
    _handler.redirect(router.to_path(index))


@no_csrf
@login_not_required
def checar(_handler, _resp, ticket, ret_path='/'):
    facade.login_passwordless(ticket, _resp).execute()
    _handler.redirect(ret_path)


@no_csrf
def form(_write_tmpl):
    app = facade.get_passwordless_app_data().execute().result
    dct = {'salvar_app_path': router.to_path(salvar), 'app': app}
    _write_tmpl('login/passwordless_form.html', dct)


def salvar(_handler, app_id, token):
    facade.save_or_update_passwordless_app_data(app_id, token).execute()
    _handler.redirect('/')