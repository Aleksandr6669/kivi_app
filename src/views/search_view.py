import flet as ft
import asyncio
from components.test_item import create_test_item
from components.data import fetch_data_from_api
from components.database_manager import get_user_profile, get_assigned_tests_for_user
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite

class SearchView(ft.Container):
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

    async def initialize_data(self):
        current_username = self.page.session.get("username")
        tests_data = []
        if current_username:
            tests_data = await asyncio.to_thread(get_assigned_tests_for_user, current_username)
        
        self.tests_data = tests_data

        self.educational_materials = [t for t in tests_data if t["item_type"] in ["material"]]
        self.build_view()
        self.update()

    def build_view(self):
        self.search_list_view = ft.Column(
            spacing=10,
            controls=[create_test_item(t, on_click=self.handle_item_click) for t in self.educational_materials],
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
        )

        def filter_materials(e):
            query = e.control.value.lower()
            filtered_list = [
                create_test_item(t, on_click=self.handle_item_click) for t in self.educational_materials 
                if query in t.get("title", "").lower()
            ]
            self.search_list_view.controls = filtered_list
            self.search_list_view.update()

        self.content = ft.Container(
            content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Навчальний матеріал", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, tooltip="Оновити дані", icon_size=30, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.TextField(
                    adaptive=False,
                    label="Пошук",
                    on_change=filter_materials,
                    border=ft.border.all(4, ft.Colors.OUTLINE),
                    border_radius=ft.border_radius.all(10),
                    content_padding=ft.padding.only(left=20, right=20),
                ),
                self.search_list_view,
            ]
        )
        )

    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.update()

        await self.initialize_data()



    async def handle_item_click(self, e: ft.ControlEvent):
        test_data = e.control.data
        print(f'handle_test_click called for test: {test_data.get("title", "Unknown Test")}')

        # Шаг 1: Проверяем, является ли текущий верхний View уже окном деталей
        # `isinstance` проверяет тип объекта, а не конкретный экземпляр
        if self.page.views and isinstance(self.page.views[-1], (TestDetailsView, UserEdite)):
            print("Старое представление уже открыто. Удаляем его.")
            self.page.views.pop()

        # Шаг 2: Создаем и добавляем новый View деталей
        details_view = TestDetailsView(page=self.page, test_data=test_data, parent_view=self)
        self.page.views.append(details_view)
        
        # Шаг 3: Обновляем страницу, чтобы показать новый View
        self.page.update()