import flet as ft

def create_progress_bar(title, value, total, color):
    return ft.Column(
        spacing=5,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(f"{title}"),
                    ft.Text(f"{value}/{total}")
                ]
            ),
            ft.ProgressBar(value=value/total if total > 0 else 0, color=color, bgcolor=ft.Colors.with_opacity(0.2, color)),
        ]
    )