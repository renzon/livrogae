# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaepermission import facade
from gaepermission.decorator import login_required


@login_required
def index(_handler, _resp):
    facade.logout(_resp).execute()
    _handler.redirect('/')