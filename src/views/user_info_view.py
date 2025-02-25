import flet as ft

def user_info_view(page):
    
    info = ft.Container(
                ft.Column([
                    ft.Text("Информация", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200),
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON, size=20, color=ft.Colors.GREEN_600),
                        ft.Text("ФИО:", size=16, text_align=ft.TextAlign.LEFT, color=ft.Colors.GREEN_600),
                        ft.Text("Александр Рыженков Александрович", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.WHITE, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=ft.Colors.PURPLE_600),
                        ft.Text("Дата рожд.:", size=16, color=ft.Colors.PURPLE_600),
                        ft.Text("31/10/1988", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.WHITE, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Icon(ft.Icons.PHONE, size=20, color=ft.Colors.RED_600),
                        ft.Text("Телефон:", size=16, color=ft.Colors.RED_600),
                        ft.Text("+3 999 999 99 99", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.WHITE, width=page.width * 0.5),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]), adaptive = True,
            )
            


    return info
