import flet as ft
import asyncio
from components.test_item import create_test_item
from components.data import fetch_data_from_api

class HistoryView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.loading_indicator = ft.Column(
            [
                ft.Text("Завантаження історії...", color=ft.Colors.BLUE_GREY_400),
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
        self.completed_tests = [t for t in tests_data if t["status"] in ["passed", "failed"]]
        self.build_view()
        self.update()

    def build_view(self):
        self.history_list_view = ft.ListView(
            expand=True,
            spacing=10,
            controls=[create_test_item(t) for t in self.completed_tests],
        )

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Історія Тестів", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.history_list_view
            ]
        )


    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.update()
        await self.initialize_data()