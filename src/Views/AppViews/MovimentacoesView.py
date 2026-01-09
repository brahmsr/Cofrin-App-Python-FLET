import flet as ft
import Models.Operacao as OperacaoModel
import Models.Categoria as CategoriaModel
import Models.SubCategoria as SubcategoriaModel
import Models.Recorrencia as RecorrenciaModel
from Services.AuthService import obter_usuario_logado
from datetime import datetime


class MovimentacoesView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.Colors.GREEN_ACCENT_400

        self.pagina_atual = 1
        self.itens_por_pagina = 7
        self.total_operacoes = 0
        self.filtro_periodo = "mes_atual"

        self.lista_movimentacoes = ft.Column(spacing=0)
        self.texto_paginacao = ft.Text("", size=14)
        
        self.btn_mes_atual = ft.ElevatedButton(
            "Mês Atual",
            icon=ft.Icons.TODAY,
            on_click=lambda e: self.aplicar_filtro("mes_atual"),
        )
        self.btn_3_meses = ft.ElevatedButton(
            "Últimos 3 Meses",
            icon=ft.Icons.DATE_RANGE,
            on_click=lambda e: self.aplicar_filtro("3_meses"),
        )
        self.btn_12_meses = ft.ElevatedButton(
            "Últimos 12 Meses",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.aplicar_filtro("12_meses"),
        )
        self.btn_todo_periodo = ft.ElevatedButton(
            "Todo Período",
            icon=ft.Icons.ALL_INCLUSIVE,
            on_click=lambda e: self.aplicar_filtro("todo_periodo"),
        )
        self.atualizar_estilo_botoes()

        self.content = ft.Column(
            [
                ft.Column(
                    [
                        ft.Row([
                            ft.Text("Movimentações", size=30, weight=ft.FontWeight.BOLD),
                            self.btn_mes_atual,
                            self.btn_3_meses,
                            self.btn_12_meses,
                            self.btn_todo_periodo,
                        ], spacing=5),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Nova Recorrência",
                                    icon=ft.Icons.REPEAT,
                                    on_click=self.abrir_modal_recorrente,
                                ),
                                ft.ElevatedButton(
                                    "Nova Movimentação",
                                    icon=ft.Icons.ADD_TASK,
                                    on_click=self.abrir_modal_adicionar,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Card(
                    content=ft.Container(
                        content=self.lista_movimentacoes,
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

        self.route = "/movimentacoes"
        self.controls = [self.content]
        self.carregar_movimentacoes()

    def aplicar_filtro(self, periodo):
        self.filtro_periodo = periodo
        self.pagina_atual = 1
        self.atualizar_estilo_botoes()
        self.carregar_movimentacoes()
        self.page.update()
    
    def atualizar_estilo_botoes(self):
        botoes = {
            "mes_atual": self.btn_mes_atual,
            "3_meses": self.btn_3_meses,
            "12_meses": self.btn_12_meses,
            "todo_periodo": self.btn_todo_periodo,
        }
        for key, btn in botoes.items():
            if key == self.filtro_periodo:
                btn.style = ft.ButtonStyle(bgcolor=ft.Colors.PRIMARY, color=ft.Colors.ON_PRIMARY)
            else:
                btn.style = None
    
    def carregar_movimentacoes(self):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return

        from datetime import timedelta
        import calendar
        hoje = datetime.now()
        
        todas_operacoes = OperacaoModel.Operacao.find_all_by_usuario_id(usuario_logado.id)
        recorrencias = RecorrenciaModel.Recorrencia.find_all_ativas_by_usuario_id(usuario_logado.id)
        
        if self.filtro_periodo == "mes_atual":
            data_inicio = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
            data_fim = hoje.replace(day=ultimo_dia, hour=23, minute=59, second=59, microsecond=999999)
        elif self.filtro_periodo == "3_meses":
            data_inicio = (hoje - timedelta(days=90)).replace(hour=0, minute=0, second=0, microsecond=0)
            data_fim = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        elif self.filtro_periodo == "12_meses":
            data_inicio = (hoje - timedelta(days=365)).replace(hour=0, minute=0, second=0, microsecond=0)
            data_fim = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            data_inicio = None
            data_fim = None
        
        operacoes_filtradas = []
        for op in todas_operacoes:
            if data_inicio is None:
                operacoes_filtradas.append(op)
            else:
                try:
                    data_op = datetime.strptime(op.data, '%d/%m/%Y').replace(hour=12, minute=0, second=0, microsecond=0)
                    if data_inicio <= data_op <= data_fim:
                        operacoes_filtradas.append(op)
                except:
                    pass
        
        recorrencias_filtradas = []
        for rec in recorrencias:
            try:
                rec_inicio = datetime.strptime(rec.data_inicio, '%d/%m/%Y')
                if rec.data_fim:
                    rec_fim_obj = datetime.strptime(rec.data_fim, '%d/%m/%Y')
                else:
                    rec_fim_obj = data_fim if data_fim else hoje
                
                # Definir limites de data
                limite_inicio = data_inicio if data_inicio else rec_inicio
                limite_fim = data_fim if data_fim else rec_fim_obj
                
                # Gerar registros mensais da recorrência
                data_atual = rec_inicio
                while data_atual <= min(rec_fim_obj, limite_fim):
                    if data_atual >= limite_inicio:
                        rec_copia = type('obj', (object,), {
                            'id': rec.id,
                            'tipo': rec.tipo,
                            'valor': rec.valor,
                            'data_inicio': data_atual.strftime('%d/%m/%Y'),
                            'data_fim': rec.data_fim,
                            'categoria_id': rec.categoria_id,
                            'subcategoria_id': rec.subcategoria_id,
                            'ativo': rec.ativo
                        })
                        recorrencias_filtradas.append(rec_copia)
                    
                    # Avançar 1 mês
                    mes = data_atual.month + 1
                    ano = data_atual.year
                    if mes > 12:
                        mes = 1
                        ano += 1
                    try:
                        data_atual = data_atual.replace(year=ano, month=mes)
                    except ValueError:
                        import calendar
                        ultimo_dia = calendar.monthrange(ano, mes)[1]
                        data_atual = data_atual.replace(year=ano, month=mes, day=ultimo_dia)
            except:
                pass
        
        self.total_operacoes = len(operacoes_filtradas) + len(recorrencias_filtradas)

        inicio = (self.pagina_atual - 1) * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        
        # Combinar operações e recorrências
        itens = list(operacoes_filtradas) + [(rec, True) for rec in recorrencias_filtradas]
        itens_paginados = itens[inicio:fim]

        self.lista_movimentacoes.controls.clear()

        for i, item in enumerate(itens_paginados):
            # Verificar se é recorrência
            if isinstance(item, tuple):
                rec, _ = item
                categoria = CategoriaModel.Categoria.find_by_id(rec.categoria_id)
                cor = ft.Colors.GREEN if rec.tipo == "entrada" else ft.Colors.RED
                sinal = "+" if rec.tipo == "entrada" else "-"

                if i > 0:
                    self.lista_movimentacoes.controls.append(ft.Divider(height=1))

                self.lista_movimentacoes.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.REPEAT, color=cor),
                        title=ft.Text(f"{categoria.nome if categoria else 'Sem categoria'} (Recorrente)"),
                        subtitle=ft.Text(f"Início: {rec.data_inicio}"),
                        trailing=ft.Row(
                            [
                                ft.Text(
                                    f"{sinal} R$ {rec.valor:,.2f}".replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                    color=cor,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Desativar",
                                            data=rec.id,
                                            on_click=self.desativar_recorrencia,
                                        ),
                                    ],
                                ),
                            ],
                            tight=True,
                        ),
                    )
                )
            else:
                op = item
                categoria = CategoriaModel.Categoria.find_by_id(op.categoria_id)
                
                if op.tipo == "entrada":
                    cor = ft.Colors.GREEN
                    icone = ft.Icons.TRENDING_UP
                    sinal = "+"
                elif op.tipo == "poupanca":
                    cor = ft.Colors.BLUE
                    icone = ft.Icons.SAVINGS
                    sinal = ""
                else:
                    cor = ft.Colors.RED
                    icone = ft.Icons.TRENDING_DOWN
                    sinal = "-"

                if i > 0:
                    self.lista_movimentacoes.controls.append(ft.Divider(height=1))

                self.lista_movimentacoes.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(icone, color=cor),
                        title=ft.Text(categoria.nome if categoria else "Sem categoria"),
                        subtitle=ft.Text(op.data),
                        trailing=ft.Row(
                            [
                                ft.Text(
                                    f"{sinal} R$ {op.valor:,.2f}".replace(",", "X")
                                    .replace(".", ",")
                                    .replace("X", "."),
                                    color=cor,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT,
                                    items=[
                                        ft.PopupMenuItem(
                                            text="Editar",
                                            data=op.id,
                                            on_click=self.abrir_modal_editar,
                                        ),
                                        ft.PopupMenuItem(
                                            text="Excluir",
                                            data=op.id,
                                            on_click=self.excluir_operacao,
                                        ),
                                    ],
                                ),
                            ],
                            tight=True,
                        ),
                    )
                )

        total_paginas = (self.total_operacoes + self.itens_por_pagina - 1) // self.itens_por_pagina
        self.texto_paginacao.value = f"Página {self.pagina_atual} de {total_paginas} ({self.total_operacoes} itens)"

    def pagina_anterior(self, e):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_movimentacoes()
            self.page.update()

    def proxima_pagina(self, e):
        total_paginas = (
            self.total_operacoes + self.itens_por_pagina - 1
        ) // self.itens_por_pagina
        if self.pagina_atual < total_paginas:
            self.pagina_atual += 1
            self.carregar_movimentacoes()
            self.page.update()

    def excluir_operacao(self, e):
        operacao = OperacaoModel.Operacao.find_by_id(e.control.data)
        if operacao:
            operacao.delete()
            self.carregar_movimentacoes()
            self.page.update()
    
    def desativar_recorrencia(self, e):
        recorrencia = RecorrenciaModel.Recorrencia.find_by_id(e.control.data)
        if recorrencia:
            recorrencia.ativo = 0
            recorrencia.save()
            self.carregar_movimentacoes()
            self.page.update()

    # ------------------ Modais ------------------ #

    def abrir_modal_recorrente(self, e):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return

        tipo_radio = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="entrada", label="Entrada"),
                    ft.Radio(value="saida", label="Saída"),
                ]
            ),
            value="entrada",
        )

        def formatar_moeda(e: ft.ControlEvent):
            numeros = "".join(filter(str.isdigit, e.control.value))
            if numeros == "":
                e.control.value = ""
            else:
                valor = int(numeros) / 100
                e.control.value = (
                    f"R$ {valor:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            e.control.update()

        valor_field = ft.TextField(
            label="Valor",
            width=190,
            prefix_icon=ft.Icons.MONETIZATION_ON,
            on_change=formatar_moeda,
        )

        def on_date_inicio_change(e):
            input_data_inicio.value = f"{e.control.value.strftime('%d/%m/%Y')}"
            input_data_inicio.update()

        calendario_inicio = ft.DatePicker(
            first_date=datetime(year=2000, month=1, day=1),
            last_date=datetime(year=2999, month=12, day=31),
            on_change=on_date_inicio_change,
        )

        input_data_inicio = ft.TextField(label="Data Início", width=150, read_only=True)
        btn_calendario_inicio = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.page.open(calendario_inicio),
        )

        duracao_meses_field = ft.TextField(
            label="Duração (meses)",
            width=190,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="Ex: 12",
        )

        categorias = CategoriaModel.Categoria.find_all_by_usuario_id(usuario_logado.id)
        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            width=190,
            options=[
                ft.dropdown.Option(
                    key=str(cat.id),
                    text=cat.nome,
                    leading_icon=cat.icone if cat.icone else ft.Icons.CATEGORY,
                )
                for cat in categorias
            ],
            prefix_icon=ft.Icons.FILTER_LIST,
        )

        # Subcategoria
        subcategoria_dropdown = ft.Dropdown(
            label="Subcategoria (opcional)",
            width=190,
            visible=True,
            value="--Nenhuma--",
            options=[ft.dropdown.Option(key="--Nenhuma--", text="--Nenhuma--")],
            disabled=True,
        )

        def on_categoria_change(e):
            if categoria_dropdown.value:
                # Atualizar ícone do dropdown
                categoria_selecionada = next(
                    (
                        cat
                        for cat in categorias
                        if str(cat.id) == categoria_dropdown.value
                    ),
                    None,
                )
                if categoria_selecionada and categoria_selecionada.icone:
                    categoria_dropdown.prefix_icon = categoria_selecionada.icone
                else:
                    categoria_dropdown.prefix_icon = ft.Icons.FILTER_LIST

                # Atualizar subcategorias
                subcategorias = SubcategoriaModel.Subcategoria.find_all_by_usuario_id(
                    usuario_logado.id
                )
                subcategorias_filtradas = [
                    s
                    for s in subcategorias
                    if str(s.categoria_id) == categoria_dropdown.value
                ]

                if subcategorias_filtradas:
                    subcategoria_dropdown.options = [
                        ft.dropdown.Option(key="--Selecionar--", text="--Selecionar--")
                    ] + [
                        ft.dropdown.Option(key=str(s.id), text=s.nome)
                        for s in subcategorias_filtradas
                    ]
                    subcategoria_dropdown.value = "--Selecionar--"
                    subcategoria_dropdown.disabled = False
                else:
                    subcategoria_dropdown.options = [
                        ft.dropdown.Option(key="--Nenhuma--", text="--Nenhuma--")
                    ]
                    subcategoria_dropdown.value = "--Nenhuma--"
                    subcategoria_dropdown.disabled = True

                self.page.update()

        categoria_dropdown.on_change = on_categoria_change

        def salvar_recorrente(e):
            if not tipo_radio.value:
                self.page.snack_bar = ft.SnackBar(ft.Text("Tipo é obrigatório"))
                self.page.snack_bar.open = True
                self.page.update()
                return

            if not valor_field.value or not valor_field.value.strip():
                valor_field.error_text = "Valor é obrigatório"
                self.page.update()
                return

            if not categoria_dropdown.value:
                categoria_dropdown.error_text = "Categoria é obrigatória"
                self.page.update()
                return

            if not input_data_inicio.value:
                input_data_inicio.error_text = "Data de início é obrigatória"
                self.page.update()
                return

            try:
                valor = float(
                    valor_field.value.replace(".", "")
                    .replace(",", ".")
                    .replace("R$ ", "")
                )
            except:
                valor_field.error_text = "Valor inválido"
                self.page.update()
                return

            # Calcular data_fim baseado na duração em meses
            data_fim = None
            if duracao_meses_field.value:
                try:
                    meses = int(duracao_meses_field.value)
                    data_inicio_obj = datetime.strptime(
                        input_data_inicio.value, "%d/%m/%Y"
                    )
                    # Adicionar meses à data de início
                    mes_fim = data_inicio_obj.month + meses
                    ano_fim = data_inicio_obj.year + (mes_fim - 1) // 12
                    mes_fim = ((mes_fim - 1) % 12) + 1
                    data_fim_obj = data_inicio_obj.replace(year=ano_fim, month=mes_fim)
                    data_fim = data_fim_obj.strftime("%d/%m/%Y")
                except:
                    duracao_meses_field.error_text = "Duração inválida"
                    self.page.update()
                    return

            subcategoria_id = None
            if subcategoria_dropdown.value and subcategoria_dropdown.value not in [
                "--Nenhuma--",
                "--Selecionar--",
            ]:
                subcategoria_id = int(subcategoria_dropdown.value)

            recorrencia = RecorrenciaModel.Recorrencia(
                tipo=tipo_radio.value,
                valor=valor,
                data_inicio=input_data_inicio.value,
                data_fim=data_fim,
                usuario_id=usuario_logado.id,
                categoria_id=int(categoria_dropdown.value),
                subcategoria_id=subcategoria_id,
            )
            recorrencia.save()

            dialog.open = False
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Recorrência criada com sucesso!")
            )
            self.page.snack_bar.open = True
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Nova Movimentação Recorrente"),
            content=ft.Column(
                [
                    ft.Text("Tipo:", weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            valor_field,
                            tipo_radio,
                        ]
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    categoria_dropdown,
                                ],
                                spacing=10,
                            ),
                            ft.Column(
                                [
                                    subcategoria_dropdown,
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [btn_calendario_inicio, input_data_inicio],
                                        spacing=0,
                                    ),
                                ]
                            ),
                            ft.Column(
                                [
                                    duracao_meses_field,
                                ]
                            ),
                        ]
                    ),
                ],
                tight=True,
                width=420,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda e: setattr(dialog, "open", False)
                    or self.page.update(),
                ),
                ft.ElevatedButton("Salvar", on_click=salvar_recorrente),
            ],
        )

        self.page.overlay.append(calendario_inicio)
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    # Modal da Operação
    # ------------------------------------------------------------------------------------------------------
    def abrir_modal_editar(self, e):
        operacao = OperacaoModel.Operacao.find_by_id(e.control.data)
        if not operacao:
            return
        self.abrir_modal_adicionar(e, operacao)

    def abrir_modal_adicionar(self, e, operacao=None):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return

        # Tipo (Entrada/Saída)
        tipo_radio = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="entrada", label="Entrada"),
                    ft.Radio(value="saida", label="Saída"),
                    ft.Radio(value="poupanca", label="Poupança"),
                ]
            ),
            value=operacao.tipo if operacao else "entrada",
        )

        # Calendario
        def on_date_change(e):
            input_data.value = f"{e.control.value.strftime('%d/%m/%Y')}"
            input_data.update()

        def on_date_dismiss(e):
            input_data.value = f""
            input_data.update()

        calendario = ft.DatePicker(
            first_date=datetime(year=2000, month=1, day=1),
            last_date=datetime(year=2999, month=12, day=31),
            data=datetime.now(),
            on_change=on_date_change,
            on_dismiss=on_date_dismiss,
        )
        input_data = ft.TextField(
            label="Data",
            width=150,
            read_only=True,
            value=operacao.data if operacao else "",
        )
        btn_calendario = ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH, on_click=lambda e: self.page.open(calendario)
        )

        # Valor da movimentação
        def formatar_moeda(e: ft.ControlEvent):
            numeros = "".join(filter(str.isdigit, e.control.value))
            if numeros == "":
                e.control.value = ""
            else:
                valor = int(numeros) / 100
                e.control.value = (
                    f"R$ {valor:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            e.control.update()

        valor_field = ft.TextField(
            label="Valor",
            width=190,
            prefix_icon=ft.Icons.MONETIZATION_ON,
            on_change=formatar_moeda,
            value=(
                f"R$ {operacao.valor:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                if operacao
                else ""
            ),
        )

        # Categoria
        categorias = CategoriaModel.Categoria.find_all_by_usuario_id(usuario_logado.id)

        # Definir ícone inicial
        icone_inicial = ft.Icons.FILTER_LIST
        if operacao and operacao.categoria_id:
            cat_inicial = CategoriaModel.Categoria.find_by_id(operacao.categoria_id)
            if cat_inicial and cat_inicial.icone:
                icone_inicial = cat_inicial.icone

        categoria_dropdown = ft.Dropdown(
            label="Categoria",
            width=190,
            options=[
                ft.dropdown.Option(
                    key=str(cat.id),
                    text=cat.nome,
                    leading_icon=cat.icone if cat.icone else ft.Icons.CATEGORY,
                )
                for cat in categorias
            ],
            prefix_icon=icone_inicial,
            value=str(operacao.categoria_id) if operacao else None,
        )

        # Subcategoria
        subcategorias = SubcategoriaModel.Subcategoria.find_all_by_usuario_id(
            usuario_logado.id
        )
        subcategorias_filtradas = (
            [
                s
                for s in subcategorias
                if str(s.categoria_id) == str(operacao.categoria_id)
            ]
            if operacao and operacao.categoria_id
            else []
        )

        subcategoria_dropdown = ft.Dropdown(
            label="Subcategoria (opcional)",
            width=190,
            visible=True,
            value=(
                str(operacao.subcategoria_id)
                if operacao and operacao.subcategoria_id
                else "--Nenhuma--"
            ),
            options=(
                [ft.dropdown.Option(key="--Nenhuma--", text="--Nenhuma--")]
                if not subcategorias_filtradas
                else [
                    ft.dropdown.Option(key=str(s.id), text=s.nome)
                    for s in subcategorias_filtradas
                ]
            ),
            disabled=not subcategorias_filtradas,
        )

        def on_categoria_change(e):
            if categoria_dropdown.value:
                # Atualizar ícone do dropdown
                categoria_selecionada = next(
                    (
                        cat
                        for cat in categorias
                        if str(cat.id) == categoria_dropdown.value
                    ),
                    None,
                )
                if categoria_selecionada and categoria_selecionada.icone:
                    categoria_dropdown.prefix_icon = categoria_selecionada.icone
                else:
                    categoria_dropdown.prefix_icon = ft.Icons.FILTER_LIST

                # Atualizar subcategorias
                subcategorias = SubcategoriaModel.Subcategoria.find_all_by_usuario_id(
                    usuario_logado.id
                )
                subcategorias_filtradas = [
                    s
                    for s in subcategorias
                    if str(s.categoria_id) == categoria_dropdown.value
                ]

                if subcategorias_filtradas:
                    subcategoria_dropdown.options = [
                        ft.dropdown.Option(key="--Selecionar--", text="--Selecionar--")
                    ] + [
                        ft.dropdown.Option(key=str(s.id), text=s.nome)
                        for s in subcategorias_filtradas
                    ]
                    subcategoria_dropdown.value = "--Selecionar--"
                    subcategoria_dropdown.disabled = False
                else:
                    subcategoria_dropdown.options = [
                        ft.dropdown.Option(key="--Nenhuma--", text="--Nenhuma--")
                    ]
                    subcategoria_dropdown.value = "--Nenhuma--"
                    subcategoria_dropdown.disabled = True

                self.page.update()

        categoria_dropdown.on_change = on_categoria_change

        def salvar(e):
            if not tipo_radio.value:
                self.page.snack_bar = ft.SnackBar(ft.Text("Tipo é obrigatório"))
                self.page.snack_bar.open = True
                self.page.update()
                return

            if not valor_field.value or not valor_field.value.strip():
                valor_field.error_text = "Valor é obrigatório"
                self.page.update()
                return

            if not categoria_dropdown.value:
                categoria_dropdown.error_text = "Categoria é obrigatória"
                self.page.update()
                return

            valor_field.error_text = None
            categoria_dropdown.error_text = None

            try:
                valor = float(
                    valor_field.value.replace(".", "")
                    .replace(",", ".")
                    .replace("R$ ", "")
                )
            except:
                valor_field.error_text = "Valor inválido"
                self.page.update()
                return

            subcategoria_id = None
            if subcategoria_dropdown.value and subcategoria_dropdown.value not in [
                "--Nenhuma--",
                "--Selecionar--",
            ]:
                subcategoria_id = int(subcategoria_dropdown.value)

            if operacao:
                operacao.tipo = tipo_radio.value
                operacao.valor = valor
                operacao.data = (
                    input_data.value
                    if input_data.value
                    else datetime.now().strftime("%d/%m/%Y")
                )
                operacao.categoria_id = int(categoria_dropdown.value)
                operacao.subcategoria_id = subcategoria_id
                operacao.save()
            else:
                nova_operacao = OperacaoModel.Operacao(
                    tipo=tipo_radio.value,
                    valor=valor,
                    data=(
                        input_data.value
                        if input_data.value
                        else datetime.now().strftime("%d/%m/%Y")
                    ),
                    usuario_id=usuario_logado.id,
                    categoria_id=int(categoria_dropdown.value),
                    subcategoria_id=subcategoria_id,
                )
                nova_operacao.save()

            self.carregar_movimentacoes()
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Movimentação" if operacao else "Nova Movimentação"),
            content=ft.Column(
                [
                    ft.Text("Tipo:", weight=ft.FontWeight.BOLD),
                    tipo_radio,
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    valor_field,
                                    ft.Row([btn_calendario, input_data], spacing=0),
                                ],
                                spacing=10,
                            ),
                            ft.Column(
                                [
                                    categoria_dropdown,
                                    subcategoria_dropdown,
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                tight=True,
                width=420,
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
