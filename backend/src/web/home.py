# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton import router

@no_csrf
@login_not_required
def index(_write_tmpl):
    _write_tmpl('templates/home.html')
