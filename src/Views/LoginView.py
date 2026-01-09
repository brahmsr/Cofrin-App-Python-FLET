import flet as ft

class LoginView(ft.View):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success
        self.bgcolor = ft.Colors.GREEN_ACCENT_700
        
        # Função de login
        def fazer_login(e):
            from Services.AuthService import fazer_login
            
            usuario, erro = fazer_login(self.login_field.value, self.senha_field.value, self.page)
            
            if erro:
                self.error_text.value = erro
                self.error_text.visible = True
                self.page.update()
            else:
                self.on_login_success(usuario)
        
        # Logo da aplicação
        self.image = ft.Image(
            src="/LogoSemMolduraVerde.png",
            width=100,
            height=100
        )
        
        # Input de login
        self.login_field = ft.TextField(
            prefix_icon=ft.Icons.PERSON,
            focused_border_color= ft.Colors.GREEN_ACCENT_700,
            label="Login",
            width=300,
            autofocus=True
        )
        
        # Input de senha
        self.senha_field = ft.TextField(
            prefix_icon=ft.Icons.LOCK,
            focused_border_color= ft.Colors.GREEN_ACCENT_700,
            label="Senha",
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        # Texto de erro
        self.error_text = ft.Text(color=ft.Colors.RED, visible=False)
        
        # Botão de login
        self.botao_login = ft.ElevatedButton(
            "Entrar",
            on_click=fazer_login,
            icon=ft.Icons.LOGIN,
            icon_color=ft.Colors.GREEN_ACCENT_700,
            color= ft.Colors.WHITE,
            width=300,
            bgcolor=ft.Colors.INDIGO_ACCENT_700
        )
        
        # Rota para cadastrar
        self.botao_registrar = ft.TextButton(
            icon= ft.Icons.GROUP_ADD,
            text="Cadastre-se",
            on_click=lambda e: self.page.go("/register")
        )
                
        self.route = "/login"
        self.controls = [
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                self.image,
                                self.login_field,
                                self.senha_field,
                                self.error_text,
                                self.botao_login,
                                self.botao_registrar
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20
                        ),
                        padding=40,
                    ),
                    elevation=10,
                    width=400,
                    height=450,
                    shadow_color=ft.Colors.BLACK54
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
        
