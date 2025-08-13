import flet as ft
import asyncio
from components.data import fetch_data_from_api

class ProfileView(ft.Container):
    def __init__(self, on_logout):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.loading_indicator = ft.Column(
            [
                ft.Text("Завантаження профілю...", color=ft.Colors.BLUE_GREY_400),
                ft.Container(height=10),  # Отступ снизу
                ft.Container(
                    content=ft.ProgressBar(
                        color=ft.Colors.BLUE, bgcolor=ft.Colors.BLUE_GREY_100, height=10,
                        border_radius=ft.border_radius.all(5),
                    ),
                    # width=200,
                ),
                ft.Container(height=10)  # Отступ снизу
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )
        self.content = self.loading_indicator

        self.on_logout = on_logout

    async def initialize_data(self):
        self.user_info = await asyncio.to_thread(fetch_data_from_api, "user_info")
        self.build_view()
        self.update()

    def build_view(self):
        async def logout_clicked(e):
            await self.on_logout()

        logout_button = ft.ElevatedButton(
            text="Вийти",
            on_click=logout_clicked,
            width=300,
            height=40,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE
            )
        )

        self.content = ft.Column(
            spacing=15,
            controls=[
                ft.Row(controls=[
                    ft.Text("Профіль", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.BLUE_200),
                                ft.Column([
                                    ft.Text(self.user_info.get("name", "Невідомо"), size=20, weight=ft.FontWeight.BOLD),
                                    ft.Text(self.user_info.get("role", "Невідомо"), size=14, color=ft.Colors.WHITE70),
                                ])
                            ], alignment=ft.MainAxisAlignment.START),
                            ft.Divider(height=10, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                            ft.Text("Контактна інформація", size=16, weight=ft.FontWeight.BOLD),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PHONE),
                                title=ft.Text(self.user_info.get("phone", "Невідомо"), size=14),
                                subtitle=ft.Text("Телефон", size=12)
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.EMAIL),
                                title=ft.Text(self.user_info.get("email", "Невідомо"), size=14),
                                subtitle=ft.Text("Електронна пошта", size=12)
                            ),
                            ft.Divider(height=10, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                            ft.Text("Про себе", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(self.user_info.get("about", "Невідомо"), size=14),
                        ])
                    )
                ),
                ft.Divider(height=20, color="transparent"),
                logout_button
            ]
        )

    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.update()
        await self.initialize_data()
