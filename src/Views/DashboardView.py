import flet as ft
from Elements.NavigationRail import NavigationRail
from Services.AuthService import fazer_logout
from Views.AppViews.HomeView import HomeView
from Views.AppViews.MovimentacoesView import MovimentacoesView
from Views.AppViews.CategoriasView import CategoriasView
from Views.AppViews.SubcategoriasView import SubcategoriasView

class DashboardView(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.Colors.GREEN_ACCENT_700
        self.padding = ft.padding.all(0)
        self.spacing = 0
        
        # Container para o conteúdo dinâmico
        self.content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=5,
        )

        def on_navigate(e):
            index = e.control.selected_index
            self.content_container.controls.clear()
            
            if index == 0:  # Dashboard
                view = HomeView(page)
                self.content_container.controls = [view.content]
            elif index == 1:  # Movimentações
                view = MovimentacoesView(page)
                self.content_container.controls = [view.content]
            elif index == 2:  # Categorias
                view = CategoriasView(page)
                self.content_container.controls = [view.content]
            elif index == 3:  # Subcategorias
                view = SubcategoriasView(page)
                self.content_container.controls = [view.content]
            page.update()

        
        self.navigation_rail = NavigationRail(on_navigate)
        
        def fechar_janela(e):
            page.window.close()
            return
            
        def minimizar_janela(e):
            page.window.minimized = True
            page.update()
            return
                    
        def on_logout(e):
            fazer_logout(page)
            page.go("/login")
            return
            
        view = HomeView(page)
        self.content_container.controls = [view.content]

        self.route = "/dashboard"
        self.controls = [
            # Barra de controle
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Text("Cofrin App", size=16, weight=ft.FontWeight.W_500, color=ft.Colors.WHITE),
                            padding=ft.padding.only(left=10),
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.LOGOUT,
                                    tooltip="Sair",
                                    on_click=on_logout,
                                    icon_color=ft.Colors.WHITE,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.MINIMIZE,
                                    tooltip="Minimizar app",
                                    on_click=lambda e: minimizar_janela(e),
                                    icon_color=ft.Colors.WHITE,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    tooltip="Fechar app",
                                    on_click=lambda e: fechar_janela(e),
                                    icon_color=ft.Colors.WHITE,
                                )
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.Colors.INDIGO_ACCENT_400,
            ),
            # Corpo do dashboard
            ft.Row(
                [
                    self.navigation_rail,
                    # ft.VerticalDivider(width=1),
                    ft.Container(
                        content=self.content_container,
                        padding=10,
                        expand=True,
                    )
                ],
                expand=True,
            ),
        ]
    
    def navegar_para_movimentacoes(self):
        self.content_container.controls.clear()
        view = MovimentacoesView(self.page)
        self.content_container.controls = [view.content]
        self.navigation_rail.selected_index = 1
        self.page.update()
