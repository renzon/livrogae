# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware import Middleware
import tmpl


class TemplateMiddleware(Middleware):
    def set_up(self):
        def write_tmpl(template_name, values=None):
            values = values or {}
            if '_csrf_code' in self.dependencies:
                values['_csrf_code'] = self.dependencies['_csrf_code']
            return self.handler.response.write(tmpl.render(template_name, values))

        self.dependencies["_write_tmpl"] = write_tmpl
        self.dependencies["_render"] = tmpl.render