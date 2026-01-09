import flet as ft
from Views.LoginView import LoginView
from Views.RegisterView import RegisterView
from Views.DashboardView import DashboardView
from Context.DbContext import DbContext
from Services.AuthService import carregar_sessao


def main(page: ft.Page):
    DbContext()  # Inicializa o banco de dados e cria as tabelas, se necessário
    page.window.frameless = True
    page.window.center()
    page.window.icon = "/icon.png"
    page.title = "Cofrin App"
    page.bgcolor = ft.Colors.GREEN_ACCENT_400
    
    def on_login_success(usuario):
        page.go("/dashboard")
    
    success_message = None
    
    def on_register_success(usuario):
        nonlocal success_message
        success_message = f"Cadastro realizado com sucesso! Faça login para continuar."
        page.go("/login")
    
    def route_change(route):
        nonlocal success_message
        page.views.clear()
        
        if page.route == "/login":
            login_view = LoginView(page, on_login_success)
            if success_message:
                login_view.error_text.value = success_message
                login_view.error_text.color = ft.Colors.GREEN
                login_view.error_text.visible = True
                success_message = None
            page.views.append(login_view)
        elif page.route == "/register":
            page.views.append(RegisterView(page, on_register_success))
        elif page.route == "/dashboard":
            page.views.append(DashboardView(page))
        
        page.update()
    
    page.on_route_change = route_change
    
    # Verificar se há sessão salva
    usuario_logado = carregar_sessao(page)
    if usuario_logado:
        page.go("/dashboard")
    else:
        page.go("/login")

ft.app(main)