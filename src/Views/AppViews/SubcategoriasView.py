import flet as ft
import Models.SubCategoria as SubcategoriaModel
import Models.Categoria as CategoriaModel
from Services.AuthService import obter_usuario_logado

class SubcategoriasView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.Colors.GREEN_ACCENT_400
        
        # Lista de ícones disponíveis
        self.icones_disponiveis = [
            ft.Icons.WATER_DROP, ft.Icons.LIGHTBULB, ft.Icons.RESTAURANT,
            ft.Icons.LOCAL_GROCERY_STORE, ft.Icons.HOME,
            ft.Icons.DIRECTIONS_CAR, ft.Icons.LOCAL_GAS_STATION, ft.Icons.MOVIE,
            ft.Icons.PHONE, ft.Icons.WIFI, ft.Icons.FAVORITE, ft.Icons.STAR, ft.Icons.BOOK,
            ft.Icons.SCHOOL, ft.Icons.FITNESS_CENTER, ft.Icons.MEDICAL_SERVICES, ft.Icons.PETS,
            ft.Icons.FLIGHT, ft.Icons.HOTEL, ft.Icons.MUSIC_NOTE, ft.Icons.SPA,
        ]
        
        # Cores disponíveis
        self.cores_disponiveis = [
            ft.Colors.RED, ft.Colors.GREEN, ft.Colors.ORANGE, ft.Colors.PURPLE,
            ft.Colors.PINK, ft.Colors.CYAN, ft.Colors.BROWN, ft.Colors.GREY,
            ft.Colors.LIME, ft.Colors.INDIGO, ft.Colors.TEAL, ft.Colors.AMBER, ft.Colors.LIGHT_BLUE, ft.Colors.LIGHT_GREEN,
        ]
        
        self.icone_selecionado = self.icones_disponiveis[0]
        self.cor_selecionada = self.cores_disponiveis[0]
        
        self.pagina_atual = 1
        self.itens_por_pagina = 8
        self.total_subcategorias = 0
        
        self.lista_subcategorias = ft.Column(spacing=0)
        self.texto_paginacao = ft.Text("", size=14)
        self.carregar_subcategorias()
        
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Subcategorias", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "Nova Subcategoria",
                                icon=ft.Icons.BOOKMARK_ADD,
                                on_click=self.abrir_modal_adicionar,
                            ),
                            padding=ft.padding.only(right=10, top=10),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Card(
                    content=ft.Container(
                        content=self.lista_subcategorias,
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
        
        self.route = "/subcategorias"
        self.controls = [self.content]
    
    def carregar_subcategorias(self):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return
        
        todas_subcategorias = SubcategoriaModel.Subcategoria.find_all_by_usuario_id(usuario_logado.id)
        self.total_subcategorias = len(todas_subcategorias)
        
        inicio = (self.pagina_atual - 1) * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        subcategorias = todas_subcategorias[inicio:fim]
        
        self.lista_subcategorias.controls.clear()
        
        for i, subcat in enumerate(subcategorias):
            if i > 0:
                self.lista_subcategorias.controls.append(ft.Divider(height=1))
            
            categoria = CategoriaModel.Categoria.find_by_id(subcat.categoria_id)
            categoria_nome = categoria.nome if categoria else "Sem categoria"
            
            self.lista_subcategorias.controls.append(
                ft.ListTile(
                    leading=ft.Icon(subcat.icone if subcat.icone else ft.Icons.LABEL, color=subcat.cor if subcat.cor else ft.Colors.GREY),
                    title=ft.Text(subcat.nome),
                    subtitle=ft.Text(f"Categoria: {categoria_nome}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(text="Editar", data=subcat.id, on_click=self.abrir_modal_editar),
                            ft.PopupMenuItem(text="Excluir", data=subcat.id, on_click=self.excluir_subcategoria),
                        ],
                    ),
                )
            )
        
        total_paginas = (self.total_subcategorias + self.itens_por_pagina - 1) // self.itens_por_pagina
        self.texto_paginacao.value = f"Página {self.pagina_atual} de {total_paginas} ({self.total_subcategorias} itens)"
    
    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_subcategorias()
            self.page.update()
    
    def proxima_pagina(self, e):
        total_paginas = (self.total_subcategorias + self.itens_por_pagina - 1) // self.itens_por_pagina
        if self.pagina_atual < total_paginas:
            self.pagina_atual += 1
            self.carregar_subcategorias()
            self.page.update()
    
    # ------------------ Modais ------------------ #
    
    def excluir_subcategoria(self, e):
        subcategoria = SubcategoriaModel.Subcategoria.find_by_id(e.control.data)
        if subcategoria:
            subcategoria.delete()
            self.carregar_subcategorias()
            self.page.update()
    
    def abrir_modal_editar(self, e):
        subcategoria = SubcategoriaModel.Subcategoria.find_by_id(e.control.data)
        if not subcategoria:
            return
        self.abrir_modal_adicionar(e, subcategoria)
        
    def abrir_modal_adicionar(self, e, subcategoria=None):
        self.icone_selecionado = subcategoria.icone if subcategoria and subcategoria.icone else self.icones_disponiveis[0]
        self.cor_selecionada = subcategoria.cor if subcategoria and subcategoria.cor else self.cores_disponiveis[0]
        
        nome_field = ft.TextField(label="Nome", width=350, value=subcategoria.nome if subcategoria else "")
        descricao_field = ft.TextField(label="Descrição", width=400, multiline=True, value=subcategoria.descricao if subcategoria else "")
        
        # Buscar categorias do usuário
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return
        
        categorias = CategoriaModel.Categoria.find_all_by_usuario_id(usuario_logado.id)
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            width=400,
            options=[ft.dropdown.Option(key=str(cat.id), text=cat.nome) for cat in categorias],
            value=str(subcategoria.categoria_id) if subcategoria else None
        )
        
        icone_preview = ft.Icon(self.icone_selecionado, color=self.cor_selecionada, size=40)
        
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
            
            if not categoria_dropdown.value:
                categoria_dropdown.error_text = "Categoria é obrigatória"
                self.page.update()
                return
            
            # Limpar erros
            nome_field.error_text = None
            descricao_field.error_text = None
            categoria_dropdown.error_text = None
            
            usuario_logado = obter_usuario_logado(self.page)
            if not usuario_logado:
                return
            
            if subcategoria:
                subcategoria.nome = nome_field.value
                subcategoria.descricao = descricao_field.value
                subcategoria.icone = self.icone_selecionado
                subcategoria.cor = self.cor_selecionada
                subcategoria.categoria_id = int(categoria_dropdown.value)
                subcategoria.save()
            else:
                nova_subcategoria = SubcategoriaModel.Subcategoria(
                    nome=nome_field.value,
                    descricao=descricao_field.value,
                    icone=self.icone_selecionado,
                    cor=self.cor_selecionada,
                    categoria_id=int(categoria_dropdown.value),
                    usuario_id=usuario_logado.id,
                )
                nova_subcategoria.save()
            
            self.carregar_subcategorias()
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text("Editar Subcategoria" if subcategoria else "Nova Subcategoria"),
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
                    categoria_dropdown,
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
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Salvar", on_click=salvar),
            ],
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
