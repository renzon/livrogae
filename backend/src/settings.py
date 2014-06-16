# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.middleware import CSRFInputToDependency, CSRFMiddleware
from gaepermission.middleware import LoggedUserMiddleware, PermissionMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.json_middleware import JsonMiddleare
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies
from tmpl_middleware import TemplateMiddleware

SENDER_EMAIL = 'renzon@gmail.com'
WEB_BASE_PACKAGE = "web"
MIDDLEWARES = [LoggedUserMiddleware,
               TemplateMiddleware,
               JsonMiddleare,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               CSRFInputToDependency,
               RouterMiddleware,
               CSRFMiddleware,
               PermissionMiddleware,
               ExecutionMiddleware]
