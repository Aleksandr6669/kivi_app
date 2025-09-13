import flet as ft
import asyncio
from components.test_item import create_test_item
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite
from components.database_manager import get_assigned_tests_for_user

# Класс для фильтра и сортировки
class FilterOptions(ft.Column):
    def __init__(self, on_filter_applied):
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
        )
        self.on_filter_applied = on_filter_applied
        
        # Переменные для хранения состояния фильтров
        self.sort_by = "date_desc"
        self.show_count = "all"
        self.completed_only = False


        self.sort_by_dropdown = ft.Dropdown(
            # border=ft.InputBorder.UNDERLINE,
            border_radius=ft.border_radius.all(10),
            border_color=ft.Colors.INDIGO_200,
            label="Сортувати за",
            width=200,
            options=[
                ft.dropdown.Option("date_desc", text="Спочатку нові"),
                ft.dropdown.Option("date_asc", text="Спочатку старі"),
                ft.dropdown.Option("status", text="Статусом"),
            ],
            value=self.sort_by,
            on_change=self.handle_change,
        )

        self.show_count_dropdown = ft.Dropdown(
            border_radius=ft.border_radius.all(10),
            border_color=ft.Colors.INDIGO_200,
            label="Показувати",
            width=200,
            options=[
                ft.dropdown.Option("10", text="10 останніх"),
                ft.dropdown.Option("20", text="20 останніх"),
                ft.dropdown.Option("50", text="50 останніх"),
                ft.dropdown.Option("all", text="Усі"),
            ],
            value=self.show_count,
            on_change=self.handle_change,
        )
        
        self.completed_only_switch = ft.Switch(
            label="Тільки не пройдені",
            value=self.completed_only,
            on_change=self.handle_change,
        )

        self.controls = [
            self.sort_by_dropdown,
            self.show_count_dropdown,
            self.completed_only_switch,
        ]

    async def handle_change(self, e):
        # Обновляем состояние
        self.sort_by = self.sort_by_dropdown.value
        self.show_count = self.show_count_dropdown.value
        self.completed_only = self.completed_only_switch.value
        # Вызываем функцию из родительского класса
        await self.on_filter_applied()

class HistoryView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, visible=False, padding=ft.padding.all(10))
        self.page = page
        self.tests_data = []

        self.loading_indicator = ft.Column(
            [
                ft.ProgressRing(width=32, height=32),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        self.history_list_view = ft.ListView(expand=True, spacing=10)
        self.filter_options = FilterOptions(self.apply_filters)

        tab = page.width >= page.height
        if tab:
            widtn_d = 220
        else:
            widtn_d = 0

        self.main_content = ft.Column(
            expand=True,
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Історія Тестів", size=24, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.UPDATE,
                            tooltip="Оновити дані",
                            icon_size=30,
                            icon_color=ft.Colors.BLUE_200,
                            on_click=self.refresh_data
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=self.history_list_view,
                            expand=True,
                        ),
                        # ft.VerticalDivider(width=1, color=ft.Colors.GREY_300),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Card(
                                        content=ft.Container(
                                            content=ft.Row( 
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.SETTINGS,
                                                        color=ft.Colors.INDIGO_300, 
                                                        size=20,
                                                    ),
                                                    ft.Text(
                                                        "Опції",
                                                        weight=ft.FontWeight.BOLD,
                                                        size=16,
                                                        text_align=ft.TextAlign.CENTER,
                                                        color=ft.Colors.ON_SURFACE, 
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER, 
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            padding=10,
                                            # bgcolor=ft.Colors.INDIGO_50, # Фоновый цвет контейнера, например, светло-индиго
                                            border_radius=ft.border_radius.all(10), # Скругляем углы
                                        ),
                                    ),
                                    ft.Card(
                                        content=ft.Container(
                                            padding=10,
                                            content=self.filter_options,
                                        ),
                                    ),
                                ],
                            ),
                            width=widtn_d,
                        )
                    ]
                )
            ]
        )
        self.content = self.main_content

    async def initialize_data(self):
        self.content = self.loading_indicator
        self.update()

        current_username = self.page.session.get("username")
        if current_username:
            self.tests_data = await asyncio.to_thread(get_assigned_tests_for_user, current_username)
        
        self.content = self.main_content
        await self.apply_filters()
        self.update()

    async def apply_filters(self):
        # Фильтрация по статусу
        if self.filter_options.completed_only:
            filtered_tests = [t for t in self.tests_data if t["status"] in ["failed"] and t["item_type"] == "test"]
        else:
            filtered_tests = [t for t in self.tests_data if t["status"] in ["passed","failed"] and t["item_type"] == "test"]

        # Сортировка
        if self.filter_options.sort_by == "date_desc":
            filtered_tests.sort(key=lambda t: t.get("updated_at", ""), reverse=True)
        elif self.filter_options.sort_by == "date_asc":
            filtered_tests.sort(key=lambda t: t.get("updated_at", ""), reverse=False)
        elif self.filter_options.sort_by == "status":
            filtered_tests.sort(key=lambda t: t.get("status", ""), reverse=False)

        # Ограничение количества
        if self.filter_options.show_count != "all":
            limit = int(self.filter_options.show_count)
            filtered_tests = filtered_tests[:limit]

        # Обновление ListView
        self.history_list_view.controls.clear()
        self.history_list_view.controls.extend(
            [create_test_item(t, on_click=self.handle_test_click) for t in filtered_tests]
        )
        self.update()

    async def refresh_data(self, e):
        await self.initialize_data()
        
    async def handle_test_click(self, e: ft.ControlEvent):
        test_data = e.control.data
        if self.page.views and isinstance(self.page.views[-1], (TestDetailsView, UserEdite)):
            self.page.views.pop()
        
        details_view = TestDetailsView(page=self.page, test_data=test_data, parent_view=self)
        self.page.views.append(details_view)
        
        self.page.update()