import flet as ft
import asyncio
from components.test_item import create_test_item
from components.progress_bar import create_progress_bar
from components.data import fetch_data_from_api

class HomeView(ft.Container):
    def __init__(self):
        super().__init__(expand=True, visible=False, padding=ft.padding.only(left=10, right=10, top=10))
        
        self.loading_indicator = ft.Column(
            [
                ft.Text("Завантаження головної сторінки...", color=ft.Colors.BLUE_GREY_400),
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
        # Завантаження даних
        self.user_info = await asyncio.to_thread(fetch_data_from_api, "user_info")
        self.tests_data = await asyncio.to_thread(fetch_data_from_api, "tests_data")
        
        # Побудова UI після завантаження
        self.build_view()
        self.update()

    def build_view(self):
        passed_count = len([t for t in self.tests_data if t.get("status") == "passed"])
        failed_count = len([t for t in self.tests_data if t.get("status") == "failed"])
        assigned_count = len([t for t in self.tests_data if t.get("status") == "assigned"])
        total_tests = len(self.tests_data)

        user_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_GREY_800,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("Вітаємо,", size=20, color=ft.Colors.WHITE70),
                            ft.Text(self.user_info.get("name", ""), size=24, weight=ft.FontWeight.BOLD),
                            ft.Text(self.user_info.get("role", ""), size=14, color=ft.Colors.WHITE70),
                        ]),
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60, color=ft.Colors.BLUE_200)
                    ]
                )
            )
        )

        progress_bars = ft.Column(
            spacing=5,
            controls=[
                create_progress_bar("Пройдено", passed_count, total_tests, ft.Colors.GREEN),
                create_progress_bar("Не пройдено", failed_count, total_tests, ft.Colors.RED),
                create_progress_bar("Призначено", assigned_count, total_tests, ft.Colors.BLUE),
            ]
        )

        chart_container = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=10,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_GREY_800,
                content=ft.Column([
                    ft.Text("Прогрес Тестів", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    progress_bars,
                    ft.Container(height=10),
                    ft.Text(f"Усього тестів: {total_tests}", text_align=ft.TextAlign.RIGHT, color=ft.Colors.WHITE70, size=12)
                ])
            )
        )
        
        assigned_tests = [t for t in self.tests_data if t.get("status") == "assigned"]
        test_list_view = ft.Column(
            spacing=10,
            controls=[create_test_item(t) for t in assigned_tests[:2]]
        )

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Головна сторінка", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                user_card,
                chart_container,
                ft.Row(controls=[ft.Text("Призначені завдання", size=18, weight=ft.FontWeight.BOLD)]),
                test_list_view,
            ]
        )

    async def refresh_data(self, e):
        self.content = self.loading_indicator
        self.update()
        await self.initialize_data()