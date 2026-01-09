import flet as ft
import Models.Categoria as CategoriaModel
from Services.AuthService import obter_usuario_logado


class CategoriasView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.Colors.GREEN_ACCENT_400

        # Lista de ícones disponíveis
        self.icones_disponiveis = [
            ft.Icons.ACCOUNT_BALANCE,
            ft.Icons.CREDIT_CARD,
            ft.Icons.PAID,
            ft.Icons.RECEIPT_LONG,
            ft.Icons.HOME_WORK,
            ft.Icons.COMMUTE,
            ft.Icons.SHOPPING_BAG,
            ft.Icons.FASTFOOD,
            ft.Icons.SUBSCRIPTIONS,
            ft.Icons.HEALTH_AND_SAFETY,
            ft.Icons.SELF_IMPROVEMENT,
            ft.Icons.SCHOOL,
            ft.Icons.WORK,
            ft.Icons.SAVINGS,
            ft.Icons.TRENDING_UP,
            ft.Icons.EMOJI_EVENTS,
            ft.Icons.PETS,
            ft.Icons.FLIGHT_TAKEOFF,
            ft.Icons.CARD_GIFTCARD,
            ft.Icons.AUTO_AWESOME,
            ft.Icons.MOVIE,
        ]

        # Cores disponíveis
        self.cores_disponiveis = [
            ft.Colors.RED,
            ft.Colors.GREEN,
            ft.Colors.ORANGE,
            ft.Colors.PURPLE,
            ft.Colors.PINK,
            ft.Colors.CYAN,
            ft.Colors.BROWN,
            ft.Colors.GREY,
            ft.Colors.LIME,
            ft.Colors.INDIGO,
            ft.Colors.TEAL,
            ft.Colors.AMBER,
            ft.Colors.LIGHT_BLUE,
            ft.Colors.LIGHT_GREEN,
        ]

        self.icone_selecionado = self.icones_disponiveis[0]
        self.cor_selecionada = self.cores_disponiveis[0]
        
        self.pagina_atual = 1
        self.itens_por_pagina = 8
        self.total_categorias = 0
        
        self.lista_categorias = ft.Column(spacing=0)
        self.texto_paginacao = ft.Text("", size=14)
        self.carregar_categorias()

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Categorias", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Nova Categoria",
                                icon=ft.Icons.ASSIGNMENT_ADD,
                                on_click=self.abrir_modal_adicionar,
                            ),
                            padding=ft.padding.only(right=10, top=10),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Card(
                    content=ft.Container(
                        content=self.lista_categorias,
                        padding=10,
                    ),
                ),
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=self.pagina_anterior,
                        ),
                        self.texto_paginacao,
                        ft.IconButton(
                            icon=ft.Icons.ARROW_FORWARD,
                            on_click=self.proxima_pagina,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            spacing=20,
        )

        self.route = "/categorias"
        self.controls = [self.content]
    
    def carregar_categorias(self):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return
        
        todas_categorias = CategoriaModel.Categoria.find_all_by_usuario_id(usuario_logado.id)
        self.total_categorias = len(todas_categorias)
        
        inicio = (self.pagina_atual - 1) * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        categorias = todas_categorias[inicio:fim]
        
        self.lista_categorias.controls.clear()
        
        for i, cat in enumerate(categorias):
            if i > 0:
                self.lista_categorias.controls.append(ft.Divider(height=1))
            
            self.lista_categorias.controls.append(
                ft.ListTile(
                    leading=ft.Icon(cat.icone if cat.icone else ft.Icons.CATEGORY, color=cat.cor if cat.cor else ft.Colors.GREY),
                    title=ft.Text(cat.nome),
                    subtitle=ft.Text(cat.descricao),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Editar", data=cat.id, on_click=self.abrir_modal_editar),
                            ft.PopupMenuItem(text="Excluir", data=cat.id, on_click=self.excluir_categoria),
                        ],
                    ),
                )
            )
        
        total_paginas = (self.total_categorias + self.itens_por_pagina - 1) // self.itens_por_pagina
        self.texto_paginacao.value = f"Página {self.pagina_atual} de {total_paginas} ({self.total_categorias} itens)"
    
    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_categorias()
            self.page.update()
    
    def proxima_pagina(self, e):
        total_paginas = (self.total_categorias + self.itens_por_pagina - 1) // self.itens_por_pagina
        if self.pagina_atual < total_paginas:
            self.pagina_atual += 1
            self.carregar_categorias()
            self.page.update()

    # ------------------ Modais ------------------ #

    def excluir_categoria(self, e):
        categoria = CategoriaModel.Categoria.find_by_id(e.control.data)
        if categoria:
            categoria.delete()
            self.carregar_categorias()
            self.page.update()
    
    def abrir_modal_editar(self, e):
        categoria = CategoriaModel.Categoria.find_by_id(e.control.data)
        if not categoria:
            return
        self.abrir_modal_adicionar(e, categoria)

    def abrir_modal_adicionar(self, e, categoria=None):
        self.icone_selecionado = categoria.icone if categoria and categoria.icone else self.icones_disponiveis[0]
        self.cor_selecionada = categoria.cor if categoria and categoria.cor else self.cores_disponiveis[0]
        
        nome_field = ft.TextField(label="Nome", width=350, value=categoria.nome if categoria else "")
        descricao_field = ft.TextField(label="Descrição", width=400, multiline=True, value=categoria.descricao if categoria else "")

        icone_preview = ft.Icon(
            self.icone_selecionado, color=self.cor_selecionada, size=40
        )

        def atualizar_preview(e=None):
            icone_preview.name = self.icone_selecionado
            icone_preview.color = self.cor_selecionada
            self.page.update()

        def selecionar_icone(icone):
            self.icone_selecionado = icone
            atualizar_preview()

        def selecionar_cor(cor):
            self.cor_selecionada = cor
            atualizar_preview()

        icones_grid = ft.GridView(
            runs_count=5,
            max_extent=60,
            child_aspect_ratio=1,
            spacing=5,
            run_spacing=5,
            height=200,
        )

        for icone in self.icones_disponiveis:
            icones_grid.controls.append(
                ft.IconButton(
                    icon=icone,
                    on_click=lambda e, i=icone: selecionar_icone(i),
                )
            )

        cores_row = ft.Row(
            wrap=True,
            spacing=10,
        )

        for cor in self.cores_disponiveis:
            cores_row.controls.append(
                ft.IconButton(
                    icon=ft.Icons.CIRCLE,
                    icon_color=cor,
                    icon_size=30,
                    on_click=lambda e, c=cor: selecionar_cor(c),
                )
            )

        def salvar(e):
            # Validação
            if not nome_field.value or nome_field.value.strip() == "":
                nome_field.error_text = "Nome é obrigatório"
                self.page.update()
                return

            if not descricao_field.value or descricao_field.value.strip() == "":
                descricao_field.error_text = "Descrição é obrigatória"
                self.page.update()
                return

            # Limpar erros
            nome_field.error_text = None
            descricao_field.error_text = None
            
            usuario_logado = obter_usuario_logado(self.page)
            if not usuario_logado:
                print("Erro: Nenhum usuário logado")
                return

            if categoria:
                categoria.nome = nome_field.value
                categoria.descricao = descricao_field.value
                categoria.icone = self.icone_selecionado
                categoria.cor = self.cor_selecionada
                categoria.save()
            else:
                nova_categoria = CategoriaModel.Categoria(
                    nome=nome_field.value,
                    descricao=descricao_field.value,
                    icone=self.icone_selecionado,
                    cor=self.cor_selecionada,
                    usuario_id=usuario_logado.id,
                )
                nova_categoria.save()
            
            self.carregar_categorias()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Categoria" if categoria else "Nova Categoria"),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            icone_preview,
                            nome_field,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    descricao_field,
                    ft.Text("Ícone:", weight=ft.FontWeight.BOLD),
                    icones_grid,
                    ft.Text("Cor:", weight=ft.FontWeight.BOLD),
                    cores_row,
                ],
                tight=True,
                width=400,
                height=500,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: setattr(dialog, "open", False)
                    or self.page.update(),
                ),
                ft.ElevatedButton("Salvar", on_click=salvar),
            ],
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
