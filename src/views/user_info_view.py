import flet as ft

def user_info_view(page):
    info = ft.Row([
                    # Внешний контейнер с отступами
                    ft.Container(
                        # Внутренний контейнер для текста
                        ft.Container(
                            ft.Column([
                                ft.Row([
                                    ft.Text("Информация", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
                                    ft.Container(
                                            content=ft.Stack(
                                                [
                                                    ft.CircleAvatar(
                                                        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                                                    ),
                                                    ft.Container(
                                                        content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                                                        alignment=ft.alignment.bottom_left,
                                                    ),
                                                ],
                                                width=40,
                                                height=40,
                                            ),
                                            margin=ft.Margin(left=0, right=16, top=0, bottom=0),
                                            # on_click=  # Обработчик клика по аватару
                                        ),
                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(ft.Icons.PERSON, size=20, color=ft.Colors.GREEN_600),
                                        ft.Text("ФИО:", size=16, text_align=ft.TextAlign.LEFT, color=ft.Colors.GREEN_600),
                                    ], alignment=ft.MainAxisAlignment.START),
                                    ft.Text("Александр Рыженков Александрович", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, width=page.width * 0.5),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=20, color=ft.Colors.PURPLE_600),
                                        ft.Text("Дата рож...:", size=16, color=ft.Colors.PURPLE_600),
                                    ], alignment=ft.MainAxisAlignment.START),
                                    ft.Text("31/10/1988", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, width=page.width * 0.5),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(ft.Icons.PHONE, size=20, color=ft.Colors.RED_600),
                                        ft.Text("Телефон:", size=16, color=ft.Colors.RED_600),
                                    ], alignment=ft.MainAxisAlignment.START),
                                    ft.Text("+7 999 999 99 99", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, width=page.width * 0.5),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                                ft.Row([
                                    ft.Row([
                                        ft.Icon(ft.Icons.LOCATION_ON, size=20, color=ft.Colors.YELLOW_600),
                                        ft.Text("Прож...:", size=16, color=ft.Colors.YELLOW_600),
                                    ], alignment=ft.MainAxisAlignment.START),
                                    ft.Text("г. Днепропетровск, ул. Победа 9", text_align=ft.TextAlign.RIGHT, size=20, color=ft.Colors.BLACK, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS, width=page.width * 0.5),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                            ]),
                            bgcolor=ft.Colors.GREY_200,  # Цвет фона для текста
                            border_radius=24,
                            padding=14  # Внутренний отступ для текста
                        ),
                        bgcolor=ft.Colors.GREY_200,  # Цвет фона для внешнего контейнера
                        width=page.width * 0.9,
                        border_radius=24,
                        # height=container_height,  # Устанавливаем высоту фона
                        margin=ft.Margin(left=5, right=5, top=5, bottom=5)  # Отступы 10% по краям
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)

                            
    return ft.Column([info], expand=True)
