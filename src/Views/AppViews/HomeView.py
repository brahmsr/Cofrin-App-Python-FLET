import flet as ft
import Models.Operacao as OperacaoModel
import Models.Categoria as CategoriaModel
import Models.Recorrencia as RecorrenciaModel
from Services.AuthService import obter_usuario_logado
from datetime import datetime


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.Colors.GREEN_ACCENT_400

        self.lista_resumo = ft.Column(spacing=10)
        self.texto_balanco = ft.Text(
            "0,00",
            size=40,
            weight=ft.FontWeight.BOLD,
        )
        self.texto_despesas = ft.Text(
            "0,00",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_400,
        )
        self.texto_cofrinho = ft.Text(
            "0,00",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_600,
        )
        
        self.texto_ganhos = ft.Text(
            "0,00",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_400,
        )
        
        self.grafico = ft.LineChart(
            data_series=[],
            border=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                left=ft.BorderSide(1, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=500,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1,
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1,
            ),
            left_axis=ft.ChartAxis(labels_size=40),
            bottom_axis=ft.ChartAxis(labels=[], labels_size=40),
            min_y=0,
            expand=True,
        )

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        # Card de ganhos
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.CALCULATE,
                                                    size=20,
                                                    color=ft.Colors.GREEN_400,
                                                ),
                                                ft.Text(
                                                    "Ganhos do mês",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREEN_400,
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "R$",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREEN_400,
                                                ),
                                                self.texto_ganhos,
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                            width=300,
                            height=130,
                        ),
                        
                        # Card do cofrinho
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.SAVINGS,
                                                    size=25,
                                                    color=ft.Colors.BLUE_600,
                                                ),
                                                ft.Text(
                                                    "Dinheiro guardado",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_600,
                                                ),
                                            ],
                                            vertical_alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "R$",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_600,
                                                ),
                                                self.texto_cofrinho,
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                            width=300,
                            height=130,
                        ),
                        
                        # Card de despesas do mês
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.CALCULATE,
                                                    size=20,
                                                    color=ft.Colors.RED_400,
                                                ),
                                                ft.Text(
                                                    "Despesas do mês",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.RED_400,
                                                ),
                                            ]
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "R$",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.RED_400,
                                                ),
                                                self.texto_despesas,
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                            width=255,
                            height=130,
                        ),
                        
                        # Card do balanço mensal
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.CURRENCY_EXCHANGE,
                                                    size=25,
                                                    color=ft.Colors.GREEN_600,
                                                ),
                                                ft.Text(
                                                    "Balanço mensal",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREEN_600,
                                                ),
                                            ],
                                            vertical_alignment=ft.MainAxisAlignment.CENTER,
                                        ),
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "R$",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREEN_600,
                                                ),
                                                self.texto_balanco,
                                            ],
                                            alignment=ft.MainAxisAlignment.END,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                            width=260,
                            height=130,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.BAR_CHART,
                                                    size=25,
                                                    color=ft.Colors.GREY_800,
                                                ),
                                                ft.Text(
                                                    "Ganhos e gastos por mês",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.GREY_800,
                                                ),
                                            ]
                                        ),
                                        self.grafico,
                                    ],
                                    spacing=10,
                                ),
                                padding=20,
                                width=600,
                                height=450,
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Resumo Financeiro Mensal",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Container(
                                            content=self.lista_resumo,
                                            expand=True,
                                        ),
                                        ft.Container(
                                            content=ft.TextButton(
                                                "Ver todos",
                                                on_click=self.ir_para_movimentacoes,
                                                icon=ft.Icons.ARROW_FORWARD_IOS,
                                                icon_color=ft.Colors.GREEN_ACCENT_700,
                                            ),
                                            alignment=ft.alignment.center,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=20,
                                width=520,
                                height=450,
                            )
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.route = "/"
        self.controls = [self.content]
        self.carregar_resumo()

    def ir_para_movimentacoes(self, e):
        # Buscar o DashboardView na pilha de views
        for view in self.page.views:
            if hasattr(view, "navegar_para_movimentacoes"):
                view.navegar_para_movimentacoes()
                break

    def carregar_resumo(self):
        usuario_logado = obter_usuario_logado(self.page)
        if not usuario_logado:
            return

        hoje = datetime.now()
        operacoes = OperacaoModel.Operacao.find_all_by_usuario_id(usuario_logado.id)
        recorrencias = RecorrenciaModel.Recorrencia.find_all_ativas_by_usuario_id(
            usuario_logado.id
        )

        # Filtrar operações do mês atual
        operacoes_mes = []
        for op in operacoes:
            try:
                data_op = datetime.strptime(op.data, "%d/%m/%Y")
                if data_op.month == hoje.month and data_op.year == hoje.year:
                    operacoes_mes.append(op)
            except:
                pass

        # Adicionar recorrências do mês atual
        for rec in recorrencias:
            try:
                rec_inicio = datetime.strptime(rec.data_inicio, "%d/%m/%Y")
                if rec.data_fim:
                    rec_fim = datetime.strptime(rec.data_fim, "%d/%m/%Y")
                    if (
                        rec_inicio.replace(day=1)
                        <= hoje.replace(day=1)
                        <= rec_fim.replace(day=1)
                    ):
                        operacoes_mes.append(rec)
                else:
                    if rec_inicio.replace(day=1) <= hoje.replace(day=1):
                        operacoes_mes.append(rec)
            except:
                pass

        self.lista_resumo.controls.clear()

        # Calcular balanço mensal
        total_entradas = 0
        total_saidas = 0

        for item in operacoes_mes:
            if item.tipo == "entrada":
                total_entradas += item.valor
            else:
                total_saidas += item.valor
        
        # Calcular poupança de todos os períodos
        total_poupanca = 0
        for op in operacoes:
            categoria = CategoriaModel.Categoria.find_by_id(op.categoria_id)
            if categoria and categoria.nome.lower() == "poupança":
                total_poupanca += op.valor
        
        for rec in recorrencias:
            categoria = CategoriaModel.Categoria.find_by_id(rec.categoria_id)
            if categoria and categoria.nome.lower() == "poupança":
                total_poupanca += rec.valor

        balanco = total_entradas - total_saidas
        self.texto_balanco.value = (
            f"{balanco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        self.texto_balanco.color = ft.Colors.GREEN if balanco >= 0 else ft.Colors.RED
        
        self.texto_despesas.value = (
            f"{total_saidas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        self.texto_ganhos.value = (
            f"{total_entradas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        self.texto_cofrinho.value = (
            f"{total_poupanca:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Calcular dados do gráfico (últimos 4 meses)
        from dateutil.relativedelta import relativedelta
        meses_nomes = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
        
        dados_entradas = []
        dados_saidas = []
        labels = []
        
        for i in range(3, -1, -1):
            mes_ref = hoje - relativedelta(months=i)
            
            total_ent = 0
            total_sai = 0
            
            for op in operacoes:
                try:
                    data_op = datetime.strptime(op.data, "%d/%m/%Y")
                    if data_op.month == mes_ref.month and data_op.year == mes_ref.year:
                        if op.tipo == "entrada":
                            total_ent += op.valor
                        else:
                            total_sai += op.valor
                except:
                    pass
            
            for rec in recorrencias:
                try:
                    rec_inicio = datetime.strptime(rec.data_inicio, "%d/%m/%Y")
                    if rec.data_fim:
                        rec_fim = datetime.strptime(rec.data_fim, "%d/%m/%Y")
                        if rec_inicio.replace(day=1) <= mes_ref.replace(day=1) <= rec_fim.replace(day=1):
                            if rec.tipo == "entrada":
                                total_ent += rec.valor
                            else:
                                total_sai += rec.valor
                    else:
                        if rec_inicio.replace(day=1) <= mes_ref.replace(day=1):
                            if rec.tipo == "entrada":
                                total_ent += rec.valor
                            else:
                                total_sai += rec.valor
                except:
                    pass
            
            dados_entradas.append(ft.LineChartDataPoint(3-i, round(total_ent, 2)))
            dados_saidas.append(ft.LineChartDataPoint(3-i, round(total_sai, 2)))
            labels.append(ft.ChartAxisLabel(
                value=3-i,
                label=ft.Container(
                    ft.Text(
                        meses_nomes[mes_ref.month - 1],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                    ),
                    margin=ft.margin.only(top=10),
                ),
            ))
        
        self.grafico.data_series = [
            ft.LineChartData(
                data_points=dados_entradas,
                stroke_width=4,
                color=ft.Colors.GREEN,
                point=True,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=dados_saidas,
                stroke_width=4,
                color=ft.Colors.RED_400,
                point=True,
                curved=True,
                stroke_cap_round=True,
            ),
        ]
        self.grafico.bottom_axis.labels = labels

        for item in operacoes_mes[:6]:  # Limitar a 6 itens
            categoria = CategoriaModel.Categoria.find_by_id(item.categoria_id)
            cor = ft.Colors.GREEN if item.tipo == "entrada" else ft.Colors.RED
            icone = (
                ft.Icons.TRENDING_UP
                if item.tipo == "entrada"
                else ft.Icons.TRENDING_DOWN
            )
            sinal = "+" if item.tipo == "entrada" else "-"

            # Verificar se é recorrência
            titulo = f"{categoria.nome if categoria else 'Sem categoria'}"
            if hasattr(item, "data_inicio"):
                titulo += " (Recorrente)"

            self.lista_resumo.controls.append(
                ft.ListTile(
                    leading=ft.Icon(icone, color=cor),
                    title=ft.Text(titulo, size=16),
                    trailing=ft.Text(
                        f"{sinal} R$ {item.valor:,.2f}".replace(",", "X")
                        .replace(".", ",")
                        .replace("X", "."),
                        size=16,
                        color=cor,
                    ),
                )
            )
