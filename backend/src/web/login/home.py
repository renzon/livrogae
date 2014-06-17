# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router
from web.login import google


@login_not_required
@no_csrf
def index(_write_tmpl, ret_path='/'):
    g_path = router.to_path(google.index, ret_path=ret_path)
    dct = {'login_google_path': users.create_login_url(g_path)}
    _write_tmpl('login/home.html', dct)