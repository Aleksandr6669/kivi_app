import flet as ft
import asyncio
import json
from components.data import fetch_data_from_api
from components.database_manager import get_all_profiles_with_username, create_or_update_user_profile, delete_user_from_db, get_user_profile, get_assigned_tests_for_user
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite

class UsersView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.page = page
        self.loading_indicator = ft.Column(
            [
                ft.ProgressRing(width=32, height=32),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
        self.content = self.loading_indicator
        
        # Заглушка для даних користувачів
        self.users_data = []

    async def initialize_data(self):
        """Асинхронно завантажує дані користувачів."""
        self.loading_indicator.visible = True
        self.page.update() # Змінено
         
        # Умовні дані користувачів
        self.users_data = await asyncio.to_thread(get_all_profiles_with_username)
        
        self.build_view()
        self.page.update() # Змінено

    def build_view(self):
        """Збирає всі компоненти на сторінці."""

        def create_user_card(user):
            """Створює картку для одного користувача."""
            return ft.Card(
                elevation=4,
                content=ft.Container(
                    padding=ft.padding.all(15),
                    border_radius=ft.border_radius.all(10),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        name=ft.Icons.ACCOUNT_CIRCLE,
                                        size=40,
                                        color=ft.Colors.ON_SURFACE_VARIANT
                                    ),
                                    # Эта колонка расширяется и при необходимости обрезает текст
                                    ft.Column(
                                        controls=[
                                            ft.Text(user.get("username", "N/A"), weight=ft.FontWeight.BOLD, size=16, overflow=ft.TextOverflow.ELLIPSIS),
                                            ft.Text(user.get("full_name", "N/A"), size=14, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                            ft.Text(user.get("email", "N/A"), size=12, color=ft.Colors.ON_SURFACE_VARIANT, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                            ft.Text(user.get("phone", "N/A"), size=12, color=ft.Colors.ON_SURFACE_VARIANT, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                        ],
                                        spacing=2,
                                        expand=True # <--- Главное изменение здесь
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15,
                                expand=True 
                            ),
                            # Кнопки действий остаются на своем месте
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Редагувати",
                                        icon_color=ft.Colors.BLUE_400,
                                        on_click=lambda e: self.handle_edit_user(user),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Видалити",
                                        icon_color=ft.Colors.RED_400,
                                        on_click=lambda e: self.handle_delete_user(user),
                                    ),
                                ],
                                tight=True
                            )
                        ]
                    )
                )
            )

        self.users_list_view = ft.Column(
            spacing=10,
            controls=[create_user_card(user) for user in self.users_data],
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

        def filter_users(e):
            query = e.control.value.lower()
            filtered_list = [
                create_user_card(user) for user in self.users_data
                if query in user.get("username", "").lower() or query in user.get("email", "").lower() or query in user.get("full_name", "").lower() or query in user.get("phone", "").lower()
            ]
            self.users_list_view.controls = filtered_list
            self.users_list_view.update()

        self.content = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(controls=[
                        ft.Text("Користувачі", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                            ft.IconButton(icon=ft.Icons.PERSON_ADD, tooltip="Додати користувача",icon_color=ft.Colors.GREEN_500, icon_size=30,on_click=self.handle_add_user),
                            ft.IconButton(icon=ft.Icons.UPDATE, tooltip="Оновити дані", icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                      )  
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.TextField(
                        adaptive=False,
                        label="Пошук користувачів",
                        on_change=filter_users,
                        border=ft.border.all(4, ft.Colors.OUTLINE),
                        border_radius=ft.border_radius.all(20),
                        content_padding=ft.padding.only(left=20, right=20),
                    ),
                    self.users_list_view,
                ]
            )
        )

    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.page.update() # Змінено
        await self.initialize_data()

    async def handle_add_user(self, e):
        print("Натиснуто кнопку 'Додати користувача'")
        # `isinstance` проверяет тип объекта, а не конкретный экземпляр
        if self.page.views and isinstance(self.page.views[-1], (TestDetailsView, UserEdite)):
            print("Старое представление уже открыто. Удаляем его.")
            self.page.views.pop()

        # Создаём новое View для редактирования, передавая данные и callback для сохранения
        edit_view = UserEdite(page=self.page, parent_view=self )
        
        self.page.views.append(edit_view)
        self.page.update()

    def handle_delete_user(self, user):
        print("Натиснуто кнопку 'Додати користувача'")
        

    def handle_edit_user(self, user):
        print(f"Открываем страницу для редактирования пользователя: {user.get('username')}")

        # `isinstance` проверяет тип объекта, а не конкретный экземпляр
        if self.page.views and isinstance(self.page.views[-1], (TestDetailsView, UserEdite)):
            print("Старое представление уже открыто. Удаляем его.")
            self.page.views.pop()

        # Создаём новое View для редактирования, передавая данные и callback для сохранения
        edit_view = UserEdite(page=self.page, user_data=user, parent_view=self )
        
        self.page.views.append(edit_view)
        self.page.update()


