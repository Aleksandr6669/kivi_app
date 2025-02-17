import flet as ft

def order_view(page):
    return ft.Column([
        ft.Text("Здесь вы можете управлять заказами", size=16, text_align=ft.TextAlign.CENTER),
        ft.ElevatedButton("Создать заказ", on_click=lambda e: page.snack_bar(ft.SnackBar(ft.Text("Заказ создан!"))))
    ], expand=True)
