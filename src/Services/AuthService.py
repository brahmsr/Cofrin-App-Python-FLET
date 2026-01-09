from Models.Usuario import Usuario
from datetime import datetime, timedelta

_sessao_atual = None
_expiracao = None


def salvar_sessao(page, usuario_id):
    page.client_storage.set("usuario_id", usuario_id)
    page.client_storage.set("expiracao", (datetime.now() + timedelta(days=30)).isoformat())


def carregar_sessao(page):
    usuario_id = page.client_storage.get("usuario_id")
    expiracao_str = page.client_storage.get("expiracao")

    if not usuario_id or not expiracao_str:
        return None

    expiracao = datetime.fromisoformat(expiracao_str)
    if datetime.now() >= expiracao:
        limpar_sessao(page)
        return None

    return Usuario.find_by_id(usuario_id)


def limpar_sessao(page):
    page.client_storage.remove("usuario_id")
    page.client_storage.remove("expiracao")


def fazer_login(login, senha, page=None):
    global _sessao_atual, _expiracao

    if not login or not senha:
        return None, "Preencha todos os campos"

    usuario = Usuario.find_by_login(login)

    if not usuario:
        return None, "Login ou senha inválidos"

    try:
        senha_valida = usuario.verificar_senha(senha)
    except Exception:
        return None, "Login ou senha inválidos"

    if senha_valida:
        _sessao_atual = usuario
        _expiracao = datetime.now() + timedelta(days=30)
        if page:
            salvar_sessao(page, usuario.id)
        return usuario, None
    else:
        return None, "Login ou senha inválidos"


def obter_usuario_logado(page=None):
    global _sessao_atual, _expiracao

    if _sessao_atual and _expiracao and datetime.now() < _expiracao:
        return _sessao_atual

    # Tentar carregar da sessão persistida
    if page:
        usuario = carregar_sessao(page)
        if usuario:
            _sessao_atual = usuario
            _expiracao = datetime.now() + timedelta(days=30)
            return usuario

    _sessao_atual = None
    _expiracao = None
    return None


def fazer_logout(page=None):
    global _sessao_atual, _expiracao
    _sessao_atual = None
    _expiracao = None
    if page:
        limpar_sessao(page)


def fazer_registro(login, senha, nome, email):
    if not login or not senha or not nome or not email:
        return None, "Preencha todos os campos"

    if Usuario.find_by_login(login):
        return None, "Login já existe"

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        login=login,
        senha=senha,
        saldo=0.0,
    )
    novo_usuario.save()

    return novo_usuario, None

