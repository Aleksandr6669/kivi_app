import flet as ft

def favorites_view(page):
    return ft.Column([
        ft.Text("Ваши избранные товары", size=16, text_align=ft.TextAlign.CENTER),
        ft.ElevatedButton("Добавить в избранное", on_click=lambda e: page.snack_bar(ft.SnackBar(ft.Text("Добавлено в избранное!"))))
    ], expand=True)
