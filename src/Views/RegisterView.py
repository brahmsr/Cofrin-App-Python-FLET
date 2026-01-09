import flet as ft

class RegisterView(ft.View):
    def __init__(self, page: ft.Page, on_register_success):
        super().__init__()
        self.page = page
        self.on_register_success = on_register_success
        self.bgcolor = ft.Colors.GREEN_ACCENT_700
        
        # Função de registro
        def fazer_registro(e):
            from Services.AuthService import fazer_registro
            
            usuario, erro = fazer_registro(login=self.login_field.value, senha=self.senha_field.value, nome=self.nome_field.value, email=self.email_field.value)
            
            if erro:
                self.error_text.value = erro
                self.error_text.visible = True
                self.page.update()
            else:
                self.on_register_success(usuario)
        
        # Logo da aplicação
        self.image = ft.Image(
            src="/LogoSemMolduraVerde.png",
            width=100,
            height=100
        )
        
        # Input de nome
        self.nome_field = ft.TextField(
            capitalization=ft.TextCapitalization.WORDS,
            prefix_icon=ft.Icons.PERSON,
            focused_border_color= ft.Colors.GREEN_ACCENT_700,
            label="Nome",
            width=300,
            autofocus=True
        )
        
        
        # Input de login
        self.login_field = ft.TextField(
            prefix_icon=ft.Icons.PERSON,
            focused_border_color= ft.Colors.GREEN_ACCENT_700,
            label="Login",
            width=300
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
        
        # Input de email
        self.email_field = ft.TextField(
            prefix_icon=ft.Icons.EMAIL,
            focused_border_color= ft.Colors.GREEN_ACCENT_700,
            label="Email",
            width=300,
            keyboard_type=ft.KeyboardType.EMAIL,
            on_submit=fazer_registro
        )
        
        # Texto de erro
        self.error_text = ft.Text(color=ft.Colors.RED, visible=False)
        
        # Botão de registro
        self.botao_registrar = ft.ElevatedButton(
            "Registrar",
            on_click=fazer_registro,
            icon=ft.Icons.GROUP_ADD,
            icon_color=ft.Colors.GREEN_ACCENT_700,
            color= ft.Colors.WHITE,
            width=300,
            bgcolor=ft.Colors.INDIGO_ACCENT_700
        )
                 
        self.route = "/register"
        self.controls = [
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            ft.Column(
                                [
                                    self.image,
                                    self.nome_field,
                                    self.login_field,
                                    self.senha_field,
                                    self.email_field,
                                    self.error_text,
                                    self.botao_registrar],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=20
                                ),
                                padding=40,
                        ),
                        elevation=10,
                        width=400,
                        height=550,
                        shadow_color=ft.Colors.BLACK54
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        