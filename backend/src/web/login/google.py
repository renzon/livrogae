# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission import facade
from gaepermission.decorator import login_not_required
from tekton import router
from web.login import pendente


@login_not_required
@no_csrf
def index(_handler, _resp, _write_tmpl, ret_path='/'):
    usuario_google = users.get_current_user()
    if usuario_google:
        cmd = facade.login_google(usuario_google, _resp).execute()
        if cmd.pending_link:
            pendente_path = router.to_path(pendente.index, cmd.pending_link.key.id())
            facade.send_passwordless_login_link(usuario_google.email(),
                                                'https://livrogae.appspot.com' + pendente_path,
                                                'pt_BR').execute()
            _write_tmpl('login/pendente.html', {'provedor': 'Google', 'email': usuario_google.email()})
            return
    _handler.redirect(ret_path)