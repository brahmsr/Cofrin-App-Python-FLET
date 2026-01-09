import flet as ft

def NavigationRail(on_navigate):
    return ft.NavigationRail(
        selected_index=0,
        indicator_color=ft.Colors.WHITE,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.ASSESSMENT,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ACCOUNT_BALANCE_WALLET,
                label="Movimentações"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ASSIGNMENT,
                label="Categorias"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BOOK,
                label="Subcategorias",
            ),
        ],
        on_change=on_navigate,
        bgcolor=ft.Colors.GREEN_ACCENT_400,
    )