import flet as ft

def user_info_view(page):
    title = ft.Container(
        content=ft.Text("KIVI Retail DEV", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
        padding=ft.Padding(top=10, right=10, bottom=10, left=10)
    )
    subtitle = ft.Container(
        content=ft.Text("Олександр Риженков", size=26, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREEN_600),
        padding=ft.Padding(top=10, right=10, bottom=10, left=10)
    )
    info = ft.Row(
        alignment="center",
        controls=[
            ft.Column(
                [
                    title,
                    subtitle,
                ],
                alignment="spaceBetween",
                expand=True
            ),
        ],
    )
    return info
