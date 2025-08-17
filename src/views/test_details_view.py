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
        
        
        # ШАГ 1: Кнопка "Назад" просто инициирует возврат, ничего больше.
        # Это стандартный и безопасный способ Flet.
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


        # Остальная логика __init__ без изменений
        item_type = self.test_data.get("item_type")
        if item_type == "material":
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
            self.controls.append(self.build_simple_test_view())


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
        self.step_title = ft.Text(weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER)
        my_style_sheet = ft.MarkdownStyleSheet(
                # Стиль для основного текста (параграфов)
                p_text_style=ft.TextStyle(
                    size=14, 
                    color=ft.Colors.WHITE70
                ),
                # Отступ для основного текста
                p_padding=ft.padding.only(bottom=10),

                # Стиль для заголовков второго уровня (## Заголовок)
                h2_text_style=ft.TextStyle(
                    size=20, 
                    weight=ft.FontWeight.BOLD
                ),
                h2_padding=ft.padding.only(top=10, bottom=5),

                # Стиль для жирного текста (**текст**)
                strong_text_style=ft.TextStyle(
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.CYAN_ACCENT_400
                ),

                # Стиль для цитат (> Цитата)
                blockquote_padding=ft.padding.all(10),
                blockquote_text_style=ft.TextStyle(
                    color=ft.Colors.BLACK45,
                    italic=True
                ),
                
                # Стиль для маркеров списка (- Пункт)
                list_bullet_text_style=ft.TextStyle(
                    color=ft.Colors.CYAN_ACCENT_400,
                    weight=ft.FontWeight.BOLD
                ),

                # Отступы для всего блока
                block_spacing=10,
            )

        self.step_image = ft.Image(border_radius=10, fit=ft.ImageFit.COVER, visible=False)
        self.step_text = ft.Markdown(extension_set=ft.MarkdownExtensionSet.COMMON_MARK, md_style_sheet=my_style_sheet)
        self.step_image_2 = ft.Image(border_radius=10, fit=ft.ImageFit.COVER, visible=False)
        self.step_text_2 = ft.Markdown(extension_set=ft.MarkdownExtensionSet.COMMON_MARK, md_style_sheet=my_style_sheet)
        self.step_image_3 = ft.Image(border_radius=10, fit=ft.ImageFit.COVER, visible=False)
        self.step_text_3 = ft.Markdown(extension_set=ft.MarkdownExtensionSet.COMMON_MARK, md_style_sheet=my_style_sheet)

        self.progress_text = ft.Text(color=ft.Colors.WHITE70)

        self.progress_bar = ft.ProgressBar(
            value=0, 
            height=2,
            color=ft.Colors.CYAN_ACCENT_400,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
        )

        self.prev_button = ft.IconButton(icon=ft.Icons.NAVIGATE_BEFORE, on_click=self.prev_step, icon_size=20, tooltip="Попередній крок")
        self.next_button = ft.ElevatedButton(on_click=self.next_step, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.symmetric(horizontal=16)))

        navigation_panel = ft.Container(
            padding=ft.padding.only(left=15, right=15, bottom=5, top=10),
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))),
            content=ft.Column(
                spacing=5,
                controls=[
                    # self.progress_bar,
                    ft.Row(
                        [self.prev_button, self.progress_text, self.next_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ]
            )
        )


        self.content_area.padding = 0
        self.content_area.controls = [
         
            ft.Container(
                expand=True,
                padding=ft.padding.symmetric(horizontal=15), 
                content=ft.Column(                           
                    [
                        ft.Container(height=25),
                        self.step_title,
                        
                        self.step_text,
                        self.step_image,
                        
                        self.step_text_2,
                        self.step_image_2,
                        
                        self.step_text_3,
                        self.step_image_3,
                        ft.Container(height=2), 
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                    spacing=10

                )
            ),

            navigation_panel
        ]
        self.update_step_content()

    def update_step_content(self):
        """Обновляет контент в соответствии с текущим шагом."""
        if not self.material_steps: return

        step_data = self.material_steps[self.current_step]
        
        # --- Вспомогательная функция для обновления виджета (чтобы не повторять код) ---
        def update_widget(widget, data_key, is_image=False):
            # Получаем данные из словаря для текущего шага
            data = step_data.get(data_key)
            
            # Если данные есть (не пустые), показываем виджет и заполняем его
            if data:
                if is_image:
                    widget.src = data
                else:
                    widget.value = data
                widget.visible = True
            # Если данных нет, прячем виджет
            else:
                widget.visible = False

        # --- Обновляем все виджеты с помощью новой функции ---
        self.step_title.value = step_data.get("title", "")
        update_widget(self.step_image, "image_url", is_image=True)
        update_widget(self.step_text, "text")
        update_widget(self.step_image_2, "image_url_2", is_image=True)
        update_widget(self.step_text_2, "text_2")
        update_widget(self.step_image_3, "image_url_3", is_image=True)
        update_widget(self.step_text_3, "text_3")

        # --- Логика навигации остается без изменений ---
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

    def on_back_gesture(self, data):
        """
        Этот метод вызывается Flet при попытке "вернуться назад" (свайп или системная кнопка).
        Мы говорим системе, что мы сами обработали это событие, и отменяем действие по умолчанию.
        """
        print("Swipe gesture blocked by on_back_gesture.")
        data.cancel = True # <-- Это команда "отменить стандартное действие"
        self.update()
    
    def close_view(self, e):
        self.page.views.pop()
        self.page.update()