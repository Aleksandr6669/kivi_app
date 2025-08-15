import flet as ft
import asyncio
from components.data import fetch_data_from_api # Убедитесь, что этот импорт правильный

class TestDetailsView(ft.View):
    """
    View для отображения детальной информации о тесте или пошагового
    просмотра учебного материала.
    """
    def __init__(self, page: ft.Page, test_data: dict):
        super().__init__()
        self.page = page
        self.test_data = test_data
        
        # Настройка AppBar
        self.app_bar = ft.AppBar(
            title=ft.Text(self.test_data.get('title', 'Деталі')),
            bgcolor=ft.Colors.with_opacity(0.85, ft.Colors.BLUE_GREY_900),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=self.close_view,
                tooltip="Назад"
            )
        )
        self.controls = [self.app_bar]

        # Логика отображения в зависимости от типа элемента
        item_type = self.test_data.get("item_type")

        if item_type == "material":
            # Для материалов показываем загрузку и начинаем получать контент
            self.current_step = 0
            self.material_steps = []
            self.loading_ring = ft.ProgressRing(width=32, height=32)
            self.content_area = ft.Column(
                [ft.Container(self.loading_ring, alignment=ft.alignment.center, expand=True)], 
                expand=True
            )
            self.controls.append(self.content_area)
            self.page.run_task(self.load_material_content)
        else:
            # Для тестов просто показываем основную информацию
            self.controls.append(self.build_simple_test_view())

    # --- Методы для УЧЕБНЫХ МАТЕРИАЛОВ ---

    async def load_material_content(self):
        """Асинхронно загружает шаги материала из API."""
        title = self.test_data.get("title")
        if title:
            api_response = await asyncio.to_thread(fetch_data_from_api, "get_material_details", title=title)
            
            if isinstance(api_response, list) and len(api_response) > 0:
                self.material_steps = api_response
                self.build_material_view()
            else:
                error_msg = api_response.get("error", "Для цього матеріалу ще не додано кроків.") if isinstance(api_response, dict) else "Для цього матеріалу ще не додано кроків."
                self.content_area.controls = [ft.Container(content=ft.Text(error_msg, text_align=ft.TextAlign.CENTER), alignment=ft.alignment.center, expand=True)]

        self.loading_ring.visible = False
        self.update()

    def build_material_view(self):
        """Строит UI для пошагового просмотра материала."""
        self.step_title = ft.Text(weight=ft.FontWeight.BOLD, size=16, text_align=ft.TextAlign.CENTER)
        self.step_image = ft.Image(border_radius=10, fit=ft.ImageFit.COVER)
        self.step_text = ft.Text(size=16)
        self.progress_text = ft.Text(color=ft.Colors.WHITE70)

        self.prev_button = ft.IconButton(icon=ft.Icons.NAVIGATE_BEFORE, on_click=self.prev_step, icon_size=20, tooltip="Попередній крок")
        self.next_button = ft.ElevatedButton(on_click=self.next_step, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.symmetric(horizontal=16)))

        navigation_panel = ft.Container(
            padding=ft.padding.symmetric(horizontal=15, vertical=5),
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.Colors.with_opacity(0.0, ft.Colors.BLUE_GREY_900), ft.Colors.with_opacity(0.9, ft.Colors.BLUE_GREY_900)]
            ),
            content=ft.Row(
                [self.prev_button, self.progress_text, self.next_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.content_area.padding = 0
        self.content_area.controls = [
            ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=15),
                        content=ft.Column(
                            [
                                ft.Container(height=30),
                                self.step_title,
                                self.step_image,
                                self.step_text,
                                ft.Container(height=80), 
                            ],
                            scroll=ft.ScrollMode.ADAPTIVE,
                            spacing=10,
                        )
                    ),
                    ft.Container(
                        content=navigation_panel,
                        alignment=ft.alignment.bottom_center,
                    )
                ]
            )
        ]
        self.update_step_content()

    def update_step_content(self):
        """Обновляет контент в соответствии с текущим шагом."""
        if not self.material_steps: return

        step_data = self.material_steps[self.current_step]
        self.step_title.value = step_data.get("title")
        self.step_image.src = step_data.get("image_url")
        self.step_text.value = step_data.get("text")
        self.progress_text.value = f"Крок {self.current_step + 1} з {len(self.material_steps)}"
        self.prev_button.visible = self.current_step > 0

        is_last_step = self.current_step == len(self.material_steps) - 1

        if is_last_step:
            self.next_button.text = "Завершити"
            self.next_button.icon = ft.Icons.CHECK_CIRCLE_OUTLINE
            self.next_button.on_click = self.complete_material
        else:
            self.next_button.text = "Далі"
            self.next_button.icon = ft.Icons.NAVIGATE_NEXT
            self.next_button.on_click = self.next_step
        
        self.update()

    def next_step(self, e):
        if self.current_step < len(self.material_steps) - 1:
            self.current_step += 1
            self.update_step_content()

    def prev_step(self, e):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_content()
    
    def complete_material(self, e):
        print(f"Материал '{self.test_data.get('title')}' завершен.")
        self.close_view(e)

    # --- Метод для отображения ТЕСТОВ ---

    def build_simple_test_view(self):
        """Строит простое View для отображения информации о тесте."""
        return ft.Container(
            expand=True,
            padding=15,
            alignment=ft.alignment.center,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(f"Назва: {self.test_data.get('title', 'N/A')}", size=18),
                    ft.Text(f"Статус: {self.test_data.get('status', 'N/A')}", size=18),
                    ft.Text(f"Оцінка: {self.test_data.get('score', 'N/A')}", size=18, weight=ft.FontWeight.BOLD),
                ]
            )
        )
    
    def close_view(self, e):
        self.page.views.pop()
        self.page.update()