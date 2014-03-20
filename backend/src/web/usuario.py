# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext.ndb.query import Cursor
from tekton import router
from usuario.model import UsuarioGoogle, Usuario, UsuarioFacebook




def index(_write_tmpl, pagina_origem=1, direcao_busca='FRENTE',
          cursor_urlsafe='None', pagina_destino=1):
    BUSCA_FRENTE = 'FRENTE'
    BUSCA_TRAS = 'TRAS'
    #tranformacao e calculo de parametros
    pagina_origem = int(pagina_origem)
    pagina_destino = int(pagina_destino)
    TAMANHO_DA_PAGINA = 2
    nova_direcao_busca = BUSCA_TRAS if (pagina_destino - pagina_origem) < 0 else BUSCA_FRENTE

    if cursor_urlsafe == 'None':
        cursor_urlsafe = None
    cursor = Cursor(urlsafe=cursor_urlsafe)

    # Funcao para definir se o usuario esta decrementando ou incrimentando a pagina
    def direcao_pesquisa_mudou():
        return direcao_busca != nova_direcao_busca

    #Calculo do offset de acordo com mudanca de direcao na busca
    offset = 0
    if cursor_urlsafe is not None:
        offset = abs(pagina_destino - pagina_origem)
        offset = offset if direcao_pesquisa_mudou() else max(offset - 1, 0)
        offset *= TAMANHO_DA_PAGINA

    #Funcao de pesquisa de usuarios
    def pesquisar_usuarios(query, cursor, offset):
        if direcao_pesquisa_mudou() and cursor:
            cursor = cursor.reversed()
        return query.fetch_page_async(TAMANHO_DA_PAGINA,
                                      offset=offset,
                                      start_cursor=cursor)

    #Pesquisa assincrona de usuarios de acordo com direcao da busca
    if nova_direcao_busca == BUSCA_TRAS:
        query = Usuario.query().order(-Usuario.nome)
        usuarios_future = pesquisar_usuarios(query, cursor, offset)
    else:
        query = Usuario.query().order(Usuario.nome)
        usuarios_future = pesquisar_usuarios(query, cursor, offset)

    #Setup de numeração de páginas
    pagina_inicial = max(1, pagina_destino - 2)
    pagina_final = pagina_inicial + 4
    pagina_anterior = max(pagina_inicial, pagina_destino - 1)

    #Construção de parâmetros a serem renderizados pelo template
    dct = {'adicionar_usuario_google_path': router.to_path(google),
           'adicionar_usuario_face_path': router.to_path(face),
           'pagina_atual': pagina_destino,
           'pagina_inicial': pagina_inicial,
           'pagina_final': pagina_final,
           'pagina_anterior': pagina_anterior,
           'pagina_posterior': pagina_destino + 1}

    usuarios, cursor, mais_resultados = usuarios_future.get_result()

    # revertando resultado para manter ordem crescente na visualizacao de busca
    if nova_direcao_busca == BUSCA_TRAS:
        usuarios.reverse()

    cursor_urlsafe = cursor.urlsafe() if cursor else 'None'
    dct['home_path'] = router.to_path(index,
                                      pagina_destino,
                                      nova_direcao_busca, cursor_urlsafe)
    dct['usuarios'] = usuarios
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