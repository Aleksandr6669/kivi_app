import flet as ft
import asyncio
from components.test_item import create_test_item
from components.progress_bar import create_progress_bar
from components.data import fetch_data_from_api
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite
from views.history_view import HistoryView
from components.database_manager import get_user_profile, get_assigned_tests_for_user

class HomeView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True, visible=False, padding=ft.padding.only(left=10, right=10, top=10))
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
        # Завантаження даних
        # Получаем логин текущего пользователя из сессии
        current_username = self.page.session.get("username")
        
        user_info = None
        if current_username:
            # Если пользователь залогинен, загружаем его профиль из базы данных
            user_info = await asyncio.to_thread(get_user_profile, current_username)

        # Если профиль не найден (или пользователь не вошел), используем "заглушку"
        
        self.user_info = user_info

        tests_data = []
        if current_username:
            tests_data = await asyncio.to_thread(get_assigned_tests_for_user, current_username)
        
        self.tests_data = tests_data

        # Шаг 1: Получаем множество названий всех заданий со статусом 'learned'.
        # Это ключевая информация для наших правил.
        learned_titles = {t['title'] for t in self.tests_data if t.get('status') == 'learned'}

        # Шаг 2: Создаем список активных заданий, применяя правила для каждого элемента.
        self.active_items = []
        for t in self.tests_data:
            status = t.get("status")
            title = t.get("title")
            item_type = t.get("item_type")

            # Правило для 'not_learned'
            if status == "not_learned":
                self.active_items.append(t)
                continue  # Переходим к следующему элементу

            # Правило для обычного 'assigned'
            if status == "assigned" and title not in learned_titles:
                self.active_items.append(t)
                continue

            # НОВОЕ ПРАВИЛО для 'assigned_learned'
            if status == "assigned_learned" and title in learned_titles:
                self.active_items.append(t)
                continue

            

        self.build_view()
        self.update()
        

    def build_view(self):
        passed_count = len([t for t in self.tests_data if t.get('status') == "passed"])
        failed_count = len([t for t in self.tests_data if t.get('status') == "failed"])
        total_tests = len([t for t in self.tests_data if t.get('status')  != "assigned_learned" and t.get('status') != "learned" ])
        assigned_count = len(self.active_items)

        user_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=10,
                border_radius=10,
                # bgcolor=ft.Colors.BLUE_GREY_100,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        # Этот `Column` будет занимать всё свободное место
                        ft.Column([
                            ft.Text("Вітаємо,", size=20),
                            ft.Text(
                                self.user_info.get("full_name", ""),
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                expand=True,
                            ),
                            ft.Text(self.user_info.get("role", ""), size=14, color=ft.Colors.BLUE_GREY_400),
                        ], expand=True), 
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60)
                    ]
                )
            )
        )
        progress_bars = ft.Column(
            spacing=5,
            controls=[
                create_progress_bar("Пройдено", passed_count, total_tests, ft.Colors.GREEN),
                create_progress_bar("Не пройдено", failed_count, total_tests, ft.Colors.RED),
                create_progress_bar("Призначено/ не вивчено", assigned_count, total_tests, ft.Colors.BLUE),
            ]
        )

        chart_container = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=10,
                border_radius=10,
                # bgcolor=ft.Colors.BLUE_GREY_100,
                content=ft.Column([
                    ft.Text("Прогрес завдань", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    progress_bars,
                    ft.Container(height=10),
                    ft.Text(f"Усього завдань: {total_tests}", text_align=ft.TextAlign.RIGHT, color=ft.Colors.BLUE_GREY_400, size=12)
                ])
            )
        )
        
        
        test_list_view = ft.Column(
            controls=[create_test_item(t, on_click=self.handle_test_click) for t in self.active_items[:2]]
        )

        show_all_button = ft.Container(
            # Оборачиваем Stack в кликабельный контейнер
            # on_click=self.go_to_progress,
            border_radius=8,
            ink=True, # Добавляем эффект "ряби" при нажатии
            padding=ft.padding.only(top=14, right=14), # Даем место для кружка уведомления
            content=ft.Stack(
                clip_behavior=ft.ClipBehavior.NONE,
                controls=[
                    # 1. Нижний слой: Текст
                    ft.Text(
                        "Усі завдання",
                        color=ft.Colors.BLUE_300,
                        weight=ft.FontWeight.W_500
                    ),

                    # 2. Верхний слой: Кружок уведомления
                    ft.Container(
                        content=ft.Text(
                            f"{assigned_count}",
                            size=10,
                            color="white",
                            text_align=ft.TextAlign.CENTER
                        ),
                        width=18,
                        height=18,
                        bgcolor=ft.Colors.RED_ACCENT_700,
                        shape=ft.BoxShape.CIRCLE,
                        alignment=ft.alignment.center,
                        # Позиционируем кружок в правом верхнем углу
                        right=-14,
                        top=-5,
                    ),
                ]
            )
        )

        self.content = ft.Column(
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Головна сторінка", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, tooltip="Оновити дані", icon_size=30, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                user_card,
                chart_container,
                ft.Row(controls=[ft.Text("Завдяння", size=18, weight=ft.FontWeight.BOLD)]),
                # test_list_view,
                ft.ListView(
                    expand=True,
                    spacing=10,
                    controls=[test_list_view]
                ),
                show_all_button if assigned_count > 0 else ft.Container()
                
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
        if self.page.views and isinstance(self.page.views[-1], (TestDetailsView, UserEdite)):
            print("Старое представление уже открыто. Удаляем его.")
            self.page.views.pop()

        # Шаг 2: Создаем и добавляем новый View деталей
        details_view = TestDetailsView(page=self.page, test_data=test_data, parent_view=self)
        self.page.views.append(details_view)
        
        # Шаг 3: Обновляем страницу, чтобы показать новый View
        self.page.update()