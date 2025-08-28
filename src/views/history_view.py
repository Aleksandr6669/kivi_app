import flet as ft
import asyncio
from components.test_item import create_test_item
from components.data import fetch_data_from_api
from views.test_details_view import TestDetailsView
from components.database_manager import get_user_profile, get_assigned_tests_for_user

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
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
        self.completed_tests = [t for t in tests_data if t["status"] in ["passed", "failed"] and t["item_type"] in ["test"]]
        self.build_view()
        self.update()

    def build_view(self):
        self.history_list_view = ft.ListView(
            expand=True,
            spacing=10,
            # controls=[create_test_item(t) for t in self.completed_tests],
            controls=[create_test_item(t, on_click=self.handle_test_click) for t in self.completed_tests],
        )

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Історія Тестів", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Ви не можете повторно відкрити тест.", size=16, weight=ft.FontWeight.BOLD),
                self.history_list_view
            ]
        )


    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.update()

        await self.initialize_data()

        
    async def handle_test_click(self, e: ft.ControlEvent):
        test_data = e.control.data
        print(f'handle_test_click called for test: {test_data.get("title", "Unknown Test")}')

        # Шаг 1: Проверяем, является ли текущий верхний View уже окном деталей
        # `isinstance` проверяет тип объекта, а не конкретный экземпляр
        if self.page.views and isinstance(self.page.views[-1], TestDetailsView):
            print("An old TestDetailsView is already open. Removing it first.")
            self.page.views.pop()

        # Шаг 2: Создаем и добавляем новый View деталей
        details_view = TestDetailsView(page=self.page, test_data=test_data, parent_view=self )
        self.page.views.append(details_view)
        
        # Шаг 3: Обновляем страницу, чтобы показать новый View
        self.page.update()
