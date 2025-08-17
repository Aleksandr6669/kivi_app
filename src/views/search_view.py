import flet as ft
import asyncio
from components.test_item import create_test_item
from components.data import fetch_data_from_api
from views.test_details_view import TestDetailsView

class SearchView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.loading_indicator = ft.Column(
            [
                ft.Text("Завантаження пошуку...", color=ft.Colors.BLUE_GREY_400),
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

    async def initialize_data(self):
        tests_data = await asyncio.to_thread(fetch_data_from_api, "tests_data")
        self.educational_materials = [t for t in tests_data if t["item_type"] in ["material"]]
        self.build_view()
        self.update()

    def build_view(self):
        self.search_list_view = ft.Column(
            spacing=10,
            controls=[create_test_item(t, on_click=self.handle_item_click) for t in self.educational_materials],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

        def filter_materials(e):
            query = e.control.value.lower()
            filtered_list = [
                create_test_item(t) for t in self.educational_materials 
                if query in t.get("title", "").lower()
            ]
            self.search_list_view.controls = filtered_list
            e.page.update()

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Навчальний матеріал", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.TextField(
                    label="Пошук...",
                    on_change=filter_materials,
                    border=ft.border.all(4, ft.Colors.OUTLINE),
                    border_radius=ft.border_radius.all(10),
                    content_padding=ft.padding.only(left=20, right=20),
                ),
                self.search_list_view
            ]
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
        if self.page.views and isinstance(self.page.views[-1], TestDetailsView):
            print("An old TestDetailsView is already open. Removing it first.")
            self.page.views.pop()

        # Шаг 2: Создаем и добавляем новый View деталей
        details_view = TestDetailsView(page=self.page, test_data=test_data)
        self.page.views.append(details_view)
        
        # Шаг 3: Обновляем страницу, чтобы показать новый View
        self.page.update()