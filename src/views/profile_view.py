import flet as ft
import asyncio
from components.database_manager import get_user_profile, get_assigned_tests_for_user
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite

class ProfileView(ft.Container):
    def __init__(self, page: ft.Page, on_logout):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.page = page

        self.content = ft.Container(expand=True)

        self.loading_indicator = ft.Column(
            [
                ft.ProgressRing(width=32, height=32),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        self.content = self.loading_indicator
        self.on_logout = on_logout

    async def initialize_data(self):
        # Получаем логин текущего пользователя из сессии
        current_username = self.page.session.get("username")
        
        user_info = None
        if current_username:
            # Если пользователь залогинен, загружаем его профиль из базы данных
            user_info = await asyncio.to_thread(get_user_profile, current_username)
      
        self.user_info = user_info
        
        # Перестраиваем и обновляем интерфейс
        self.build_view()
        self.update()

    def build_view(self):
        async def logout_clicked(e):
            if self.page.views and isinstance(self.page.views[-1], TestDetailsView):
                self.page.views.pop()
            
            # Очищаем сессию на сервере
            e.page.session.clear()
            e.page._invoke_method("clientStorage:remove", {"key": "username"}, wait_for_result=False)
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
                    ft.IconButton(icon=ft.Icons.UPDATE, tooltip="Оновити дані", icon_size=30, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60),
                                ft.Column([
                                    ft.Text(self.user_info.get("full_name", "Невідомо"), size=20, weight=ft.FontWeight.BOLD, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(self.user_info.get("user_tupe", "Невідомо"), size=14, color=ft.Colors.BLUE_GREY_400),
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
