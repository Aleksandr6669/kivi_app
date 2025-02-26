import flet as ft

def news_feed_view(page):
    info = ft.Row([
        ft.Container(
            ft.Container(
                ft.Column([
                    ft.Text("Информация", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=20, color=ft.Colors.GREEN_600),
                        ft.Text("ФИО:", size=16, text_align=ft.TextAlign.LEFT, color=ft.Colors.GREEN_600),
                        ft.Text("Александр Рыженков Александрович", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=ft.Colors.PURPLE_600),
                        ft.Text("Дата рождения:", size=16, color=ft.Colors.PURPLE_600),
                        ft.Text("31/10/1988", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=20, color=ft.Colors.RED_600),
                        ft.Text("Телефон:", size=16, color=ft.Colors.RED_600),
                        ft.Text("+3 999 999 99 99", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                bgcolor=ft.Colors.GREY_200,
                border_radius=24,
                padding=14  
            ),
            bgcolor=ft.Colors.GREY_200,
            width=page.width * 0.9,
            border_radius=24,
            margin=ft.Margin(left=5, right=5, top=5, bottom=5)  
        )
    ], alignment=ft.MainAxisAlignment.CENTER)

    news = ft.ListView(
        height=page.height,
        controls=[info, info, info, info],
        on_scroll=True,
        expand=True,
        spacing=10
    )

    return ft.Column([news], expand=True)
