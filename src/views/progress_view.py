import flet as ft
import asyncio
from components.test_item import create_test_item
from components.progress_bar import create_progress_bar
from components.data import fetch_data_from_api
from components.database_manager import get_user_profile, get_assigned_tests_for_user
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite

class ProgressView(ft.Container):
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

        # Шаг 1: Получаем множество названий всех заданий со статусом 'learned'.
        # Это ключевая информация для наших правил.
        learned_titles = {t['title'] for t in self.tests_data if t.get('status') == 'learned'}

        # Шаг 2: Создаем список активных заданий, применяя правила для каждого элемента.
        self.active_items = []
        for t in self.tests_data:
            status = t.get("status")
            title = t.get("title")

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
        passed_count = len([t for t in self.tests_data if t.get('status')  == "passed"])
        failed_count = len([t for t in self.tests_data if t.get('status')  == "failed"])
        total_tests = len([t for t in self.tests_data if t.get('status')  != "assigned_learned" and t.get('status')  != "learned" ])
        tests_with_results = [t for t in self.tests_data if t.get('status') in ['passed', 'failed']]
        assigned_count = len(self.active_items)

        summ_count_failed = failed_count/(passed_count + failed_count)*100
        summ_count_passed = passed_count/(passed_count + failed_count)*100
        

        if tests_with_results:
            # Получаем список всех процентных баллов
            scores = [t.get('percentage_score') for t in self.tests_data if t.get('percentage_score') is not None]
            
            # Вычисляем сумму баллов и их количество
            total_score = sum(scores)
            count = len(scores)

            
            # Возвращаем среднее значение
            tests_results = total_score / count
        else:
            # Возвращаем 0, чтобы избежать ошибки деления на ноль
            tests_results = 0
        
        color_tests_results = ft.Colors.BLACK  # Цвет по умолчанию, если не подходит ни одно условие

        if tests_results >= 90:
            color_tests_results = ft.Colors.GREEN  # Отличный результат
        elif tests_results >= 75:
            color_tests_results = ft.Colors.LIGHT_GREEN  # Хороший результат
        elif tests_results >= 60:
            color_tests_results = ft.Colors.YELLOW_600 # Средний результат
        elif tests_results >= 40:
            color_tests_results = ft.Colors.ORANGE  # Неудовлетворительный результат
        else:
            color_tests_results = ft.Colors.RED  # Очень низкий результат


        self.content = ft.Column(
            expand=True, 
            spacing=10,
            controls=[
                ft.Row(controls=[
                    ft.Text("Навчання", size=24, weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.Icons.UPDATE, tooltip="Оновити дані", icon_size=30, icon_color=ft.Colors.BLUE_200, on_click=self.refresh_data)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text("Прогрес завдань", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(height=5),
                            create_progress_bar("Пройдено", passed_count, total_tests, ft.Colors.GREEN),
                            create_progress_bar("Не пройдено", failed_count, total_tests, ft.Colors.RED),
                            create_progress_bar("Призначено/ не вивчено", assigned_count, total_tests, ft.Colors.BLUE),
                            ft.Container(height=5),
                            ft.Divider(height=5, thickness=3),
                            ft.Row(
                                expand=True,
                                controls=[
                                    ft.Text("Середній результат: ", size=14, weight=ft.FontWeight.BOLD, color = color_tests_results),
                                    ft.Text(f"{round(tests_results,1)} %", size=14, weight=ft.FontWeight.BOLD, color = color_tests_results),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ft.Row(
                                expand=True,
                                controls=[
                                    ft.Text("Не пройдених", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                                    ft.Text(f"{round(summ_count_failed,1)} %", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ft.Row(
                                expand=True,
                                controls=[
                                    ft.Text("Пройдених", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                                    ft.Text(f"{round(summ_count_passed,1)} %", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ft.Text(f"Усього завдань: {total_tests}", text_align=ft.TextAlign.RIGHT, color=ft.Colors.BLUE_GREY_400, size=12)
                        ])
                    )
                ),
                ft.Text("Усі завданя", size=20, weight=ft.FontWeight.BOLD),
                ft.ListView(
                    expand=True,
                    spacing=10,
                    # VVV ИСПРАВЛЕНИЕ ЗДЕСЬ VVV
                    controls=[
                        # Теперь передаем метод напрямую, без lambda
                        create_test_item(t, on_click=self.handle_test_click)
                        for t in self.active_items
                    ],
                    
                )
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
