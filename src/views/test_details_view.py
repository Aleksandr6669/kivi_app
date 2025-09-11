import flet as ft
import asyncio
from components.data import fetch_data_from_api
from components.database_manager import db, update_related_tests_status, get_content_for_material, get_test_questions, update_assignment


class TestDetailsView(ft.View):
    def __init__(self, page: ft.Page, test_data: dict, parent_view: ft.Container):
        super().__init__()
        self.page = page
        self.test_data = test_data
        self.parent_view = parent_view
        # self.platform = page.platform
    
        print(self.page.platform.name)

        if page.platform.name == "IOS" or "MacOS":
            self.top_pading = 30
        else:
            self.top_pading = 0

        self.app_bar = ft.AppBar(
            title=ft.Text(self.test_data.get('title', 'Деталі')),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_400),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=self.close_view,
                tooltip="Назад"
            )
        )
        self.controls = [self.app_bar]
        
        self.content_area = ft.Column(
            [ft.Container(
                content=ft.ProgressRing(width=32, height=32),
                alignment=ft.alignment.center,
                expand=True
            )], 
            expand=True
        )
        self.controls.append(self.content_area)

        item_type = self.test_data.get("item_type")
        attempts_left = self.test_data.get("attempts_used", 0)
        if item_type == "material":
            self.current_step = 0
            self.material_steps = []
            self.page.run_task(self.load_material_content)
        elif item_type == "test":
            self.current_step = 0
            self.test_questions = []
            self.user_answers = {}
            self.is_answered = False
            self.is_checked = False
            if attempts_left == 0:
                self.page.run_task(self.load_test_content)
            else:
                self.page.run_task(self.show_results_start_view)
        else:
            self.controls.append(self.build_simple_test_view())

    # --- МЕТОДЫ ДЛЯ МАТЕРИАЛОВ ---

    async def load_material_content(self):
        title = self.test_data.get("title")
        material_steps = []
        if title:
            material_steps = await asyncio.to_thread(get_content_for_material, title)
        
        if material_steps:
            self.material_steps = material_steps
            self.build_material_view()
        else:
            error_msg = "Вміст для цього матеріалу ще не додано."
            self.content_area.controls = [
                ft.Container(
                    content=ft.Text(error_msg, text_align=ft.TextAlign.CENTER, size=18),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        self.update()

    def build_material_view(self):
        self.step_title = ft.Text(weight=ft.FontWeight.BOLD, size=26, text_align=ft.TextAlign.CENTER)
        self.my_style_sheet = ft.MarkdownStyleSheet(
            p_text_style=ft.TextStyle(size=14), p_padding=ft.padding.only(bottom=10),
            h2_text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD), h2_padding=ft.padding.only(top=10, bottom=5),
            strong_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_ACCENT_400),
            blockquote_padding=ft.padding.all(10), blockquote_text_style=ft.TextStyle(color=ft.Colors.BLACK45, italic=True),
            list_bullet_text_style=ft.TextStyle(color=ft.Colors.CYAN_ACCENT_400, weight=ft.FontWeight.BOLD),
            block_spacing=10
        )
        self.step_content_column = ft.Column(scroll=ft.ScrollMode.HIDDEN, spacing=15)
        self.progress_text = ft.Text(color=ft.Colors.BLUE_400)
        # self.prev_button = ft.IconButton(icon=ft.Icons.NAVIGATE_BEFORE, on_click=self.prev_step, icon_color=ft.Colors.BLUE_400, icon_size=20, padding=0,  tooltip="Попередній крок")
        self.prev_button = ft.ElevatedButton(text=" Назад",color=ft.Colors.BLUE_400, icon_color = ft.Colors.BLUE_400, icon = ft.Icons.NAVIGATE_BEFORE, on_click=self.prev_step, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.symmetric(horizontal=16)))
        self.next_button = ft.ElevatedButton(on_click=self.next_step, text="Далі", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=ft.padding.symmetric(horizontal=16)))

        navigation_panel = ft.Container(
            padding=ft.padding.only(left=15, right=15),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        controls=[self.prev_button, self.progress_text, self.next_button],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ]
            )
        )
        self.content_area.padding = 0
        self.content_area.controls = [
            ft.Container(
                content=self.step_content_column,
                expand=True,
                padding=ft.padding.only(top=self.top_pading, left=15, right=15)
            ),
            navigation_panel
        ]
        self.update_step_content()

    def update_step_content(self):
        if not self.material_steps: return
        step_data = self.material_steps[self.current_step]
        self.step_content_column.controls.clear()
        self.step_title.value = step_data.get("title", "")
        self.step_content_column.controls.append(self.step_title)
        
        content_blocks = step_data.get("content_blocks", [])
        for block in content_blocks:
            block_type = block.get("type")
            block_value = block.get("value")
            if block_type == "text" and block_value:
                self.step_content_column.controls.append(ft.Markdown(block_value, extension_set=ft.MarkdownExtensionSet.COMMON_MARK, md_style_sheet=self.my_style_sheet, selectable=True))
            elif block_type == "image" and block_value:
                self.step_content_column.controls.append(ft.Image(src=block_value, border_radius=ft.border_radius.all(10), fit=ft.ImageFit.CONTAIN))
        
        self.progress_text.value = f"Крок {self.current_step + 1} з {len(self.material_steps)}"
        self.prev_button.visible = self.current_step > 0
        is_last_step = self.current_step == len(self.material_steps) - 1
        if is_last_step:
            self.next_button.text = "Завершити"
            self.next_button.color = ft.Colors.GREEN_300
            self.next_button.icon = ft.Icons.CHECK_CIRCLE_OUTLINE
            self.next_button.icon_color = ft.Colors.GREEN_300 
            self.next_button.on_click = self.complete_material
        else:
            self.next_button.text = "Далі"
            self.next_button.color = ft.Colors.BLUE_400
            self.next_button.icon = ft.Icons.NAVIGATE_NEXT
            self.next_button.icon_color = ft.Colors.BLUE_400
            self.next_button.on_click = self.next_step

        self.update()
       
    def next_step(self, e):
        if self.current_step < len(self.material_steps) - 1:
            self.current_step += 1
            self.update_step_content()
            self.step_content_column.scroll_to(offset=0, duration=200)
            self.update()
 
    def prev_step(self, e):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_content()
            self.step_content_column.scroll_to(offset=0, duration=200)
            self.update()

    
    async def complete_material(self, e):
        print(f"Материал '{self.test_data.get('title')}' завершен.")

        # Обновляем статус самого материала
        await asyncio.to_thread(
            update_assignment,
            username=self.test_data['user'],
            test_title=self.test_data['title'],
            new_data={"status": "learned"}
        )
        self.test_data['status'] = 'learned'

        await asyncio.to_thread(update_related_tests_status, self.test_data.get('title'), self.test_data['user'])

        await self.close_view(e)

    # --- МЕТОДЫ ДЛЯ ТЕСТОВ ---

    async def load_test_content(self):
        title = self.test_data.get("title")

        test_questions = []
        if title:
            test_questions = await asyncio.to_thread(get_test_questions, title)

        if test_questions:
            self.test_questions = test_questions
            self.user_answers = {i: [] for i, q in enumerate(test_questions)}
            self.build_test_view()
            self.update_test_content()
        else:
            error_msg = "Вміст для цього тесту ще не додано."
            self.content_area.controls = [
                ft.Container(
                    content=ft.Text(error_msg, text_align=ft.TextAlign.CENTER, size=18),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        self.update()

    def build_test_view(self):
        self.question_card = ft.Card(content=ft.Container(padding=15))
        self.answers_column = ft.Column(spacing=15)
        self.progress_text_test = ft.Text(color=ft.Colors.BLUE_400)
        self.feedback_text = ft.Text(size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
        self.explanation_text = ft.Text(size=14, color=ft.Colors.BLUE_GREY_200, italic=True)

        self.dynamic_controls_panel = ft.Row(
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[]
        )
        
        self.content_area.padding = 0
        self.content_area.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        self.question_card,
                        self.answers_column,
                        self.feedback_text,
                        self.explanation_text
                    ],
                    scroll=ft.ScrollMode.HIDDEN,
                    expand=True,
                    spacing=20
                ),
                padding=ft.padding.only(top=self.top_pading, left=15, right=15),
                expand=True
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[self.progress_text_test],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        self.dynamic_controls_panel
                    ]
                )
            )
        ]

    def _on_answer_select(self, e):
        if self.is_checked: return
        
        current_question_data = self.test_questions[self.current_step]
        
        if current_question_data.get("question_type") == "single_choice":
            answer_text = e.control.value
            self.user_answers[self.current_step] = [answer_text]
        else:
            checkbox_value = e.control.value
            answer_text = e.control.data['answer_text']
            
            self.user_answers.setdefault(self.current_step, [])
            if answer_text in self.user_answers[self.current_step] and not checkbox_value:
                self.user_answers[self.current_step].remove(answer_text)
            elif answer_text not in self.user_answers[self.current_step] and checkbox_value:
                self.user_answers[self.current_step].append(answer_text)

        self.is_answered = bool(self.user_answers.get(self.current_step))
        self.update_test_content()

    def _check_answer(self, e):
        current_question_data = self.test_questions[self.current_step]
        
        correct_answers = {a['answer_text'] for a in current_question_data['answers'] if a['is_correct']}
        user_selected = set(self.user_answers.get(self.current_step, []))
        
        is_correct = (correct_answers == user_selected)
        
        self.is_checked = True
        
        if is_correct:
            self.feedback_text.value = "Вірно!"
            self.feedback_text.color = ft.Colors.GREEN
            self.explanation_text.value = ""
        else:
            self.feedback_text.value = "Не вірно."
            self.feedback_text.color = ft.Colors.RED
            self.explanation_text.value = f"Вірна відповідь: {', '.join(sorted(list(correct_answers)))}"
            
        self.update_test_content()

    def _next_question(self, e):
        self.is_checked = False
        self.is_answered = bool(self.user_answers.get(self.current_step + 1))
        self.feedback_text.value = ""
        self.explanation_text.value = ""
        
        if self.current_step < len(self.test_questions) - 1:
            self.current_step += 1
            self.update_test_content()
        else:
            self.complete_test(e)
            
        self.update()

    def update_test_content(self):
        if not self.test_questions: return
        
        question_data = self.test_questions[self.current_step]
        
        self.question_card.content.content = ft.Column(
            [ft.Text(f"Питання {self.current_step + 1} з {len(self.test_questions)}", size=12, color=ft.Colors.BLUE_GREY_400),
            ft.Text(question_data.get("question_text", ""), weight=ft.FontWeight.BOLD, size=18)], spacing=5
        )
        
        self.answers_column.controls.clear()
        question_type = question_data.get("question_type")
        
        if question_type == "single_choice":
            radio_group = ft.RadioGroup(
                content=ft.Column(spacing=15),
                value=self.user_answers.get(self.current_step, [None])[0] if self.user_answers.get(self.current_step) else None,
                on_change=self._on_answer_select,
            )
            for answer in question_data.get("answers", []):
                is_correct = answer['is_correct']
                bgcolor = None
                textcolor = None
                if self.is_checked:
                    if is_correct:
                        bgcolor = ft.Colors.GREEN_100
                        textcolor = ft.Colors.BLACK
                    elif answer['answer_text'] in self.user_answers.get(self.current_step, []) and not is_correct:
                        bgcolor = ft.Colors.RED_100
                        textcolor = ft.Colors.BLACK
                
                control = ft.Radio(value=answer['answer_text'], data=answer, disabled=self.is_checked)
                
                card_content = ft.Container(
                    # on_click=lambda e, value=answer['answer_text']: setattr(radio_group, 'value', value) or self.update() if not self.is_checked else None,
                    content=ft.Row(
                        controls=[
                            control,
                            ft.Text(answer['answer_text'], max_lines=None, overflow=ft.TextOverflow.VISIBLE, color=textcolor, expand=True)
                        ],
                        # vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    padding=ft.padding.only(left=10, right=10, top=15, bottom=15),
                    bgcolor=bgcolor,
                    border_radius=10,
                )
                
                radio_group.content.controls.append(ft.Card(content=card_content))
                
            self.answers_column.controls.append(radio_group)

        elif question_type == "multiple_choice":
            for answer in question_data.get("answers", []):
                is_selected = answer['answer_text'] in self.user_answers.get(self.current_step, [])
                is_correct = answer['is_correct']
                
                bgcolor = None
                textcolor = None
                if self.is_checked:
                    if is_correct:
                        bgcolor = ft.Colors.GREEN_100
                        textcolor = ft.Colors.BLACK
                    elif is_selected and not is_correct:
                        bgcolor = ft.Colors.RED_100
                        textcolor = ft.Colors.BLACK
                
                control = ft.Checkbox(
                    value=is_selected,
                    on_change=self._on_answer_select,
                    disabled=self.is_checked,
                    data=answer
                )
                
                card_content = ft.Container(
                    # on_click=lambda e, checkbox=control: setattr(checkbox, 'value', not checkbox.value) or self.update() if not self.is_checked else None,
                    content=ft.Row(
                        controls=[
                            control,
                            ft.Text(answer['answer_text'], max_lines=None, overflow=ft.TextOverflow.VISIBLE, color=textcolor, expand=True)
                        ],
                        # vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    padding=ft.padding.only(left=5, right=5, top=5, bottom=5),
                    bgcolor=bgcolor,
                    border_radius=10
                )

                card = ft.Card(content=card_content)
                self.answers_column.controls.append(card)

        self.dynamic_controls_panel.controls.clear()
        
        if not self.is_checked:
            check_button = ft.ElevatedButton(
                text="Перевірити",
                on_click=self._check_answer,
                disabled=not self.is_answered
            )
            self.dynamic_controls_panel.controls.append(check_button)
        else:
            is_last_question = self.current_step == len(self.test_questions) - 1
            if is_last_question:
                next_button = ft.ElevatedButton(text="Завершити", on_click=self.complete_test)
            else:
                next_button = ft.ElevatedButton(text="Наступне питання", on_click=self._next_question)
            
            self.dynamic_controls_panel.controls.append(next_button)

        self.progress_text_test.value = f"Питання {self.current_step + 1} з {len(self.test_questions)}"

        self.update()

    async def restart_test(self, e):
        # Явно очищаємо controls і показуємо прогрес
        self.content_area.controls.clear()
        self.update()
        self.app_bar = ft.AppBar(
            title=ft.Text(self.test_data.get('title', 'Деталі')),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_GREY_400),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=self.close_view,
                tooltip="Назад"
            )
        )
        self.controls = [self.app_bar]
        
        self.content_area = ft.Column(
            [ft.Container(
                content=ft.ProgressRing(width=32, height=32),
                alignment=ft.alignment.center,
                expand=True
            )], 
            expand=True
        )
        self.controls.append(self.content_area)

        
        # Скидаємо всі стани
        self.current_step = 0
        self.user_answers = {}
        self.is_answered = False
        self.is_checked = False
        
        # Завантажуємо тест
        await self.load_test_content()
        self.update()

    def show_results_view(self, correct_count, total_questions):
        self.controls.clear()
        self.controls.append(self.app_bar)

        result_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        # Отримання даних про спроби з self.test_data
        total_attempts = self.test_data['total_attempts']
        attempts_used = self.test_data['attempts_used']
        attempts_left = total_attempts - attempts_used

        # Логіка відображення
        is_passed = result_percentage >= self.test_data['passing_score']
        can_retry = not is_passed and attempts_left > 0

        if is_passed:
            result_message = ft.Text(
                f"Вітаємо, тест пройдено! Поріг: {self.test_data['passing_score']}%",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREEN_400
            )
            congratulation_icon = ft.Icon(name=ft.Icons.CELEBRATION, color=ft.Colors.GREEN_400, size=50)
            result_buttons = ft.ElevatedButton(
                text="Завершити",
                on_click=self.close_view,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )

        else:
            result_message = ft.Text(
                f"Тест не пройдено. Поріг: {self.test_data['passing_score']}%",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.RED_400
            )
            congratulation_icon = ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.RED_400, size=50)

            buttons_row = [
                ft.ElevatedButton(
                    text="Завершити",
                    on_click=self.close_view,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ]
            if can_retry:
                buttons_row.insert(0, ft.ElevatedButton(
                    text="Повторити тест",
                    on_click=self.restart_test,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ))

            result_buttons = ft.Row(
                controls=buttons_row,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )

        score_text = ft.Text(
            f"Ваш результат: {correct_count} з {total_questions}",
            size=22,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.BLUE_GREY_200
        )

        percentage_text = ft.Text(
            f"{result_percentage:.0f}%",
            size=50,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_400 if result_percentage >= 70 else (ft.Colors.ORANGE_400 if result_percentage >= 50 else ft.Colors.RED_400),
            text_align=ft.TextAlign.CENTER
        )

        attempts_info = ft.Text(
            f"Спроб використано: {attempts_used} з {total_attempts}",
            size=16,
            color=ft.Colors.BLUE_GREY_200
        )

        results_content = ft.Card(
            elevation=10,  # Задаємо тінь для картки
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        congratulation_icon,
                        result_message,
                        score_text,
                        ft.Container(height=20),
                        percentage_text,
                        attempts_info,
                        ft.Container(height=50),
                        result_buttons
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                padding=30,  # Відступи всередині картки
                border_radius=15, # Закруглені кути
            )
        )
        main_column = ft.Column(
            [
                ft.Container(height=50),  # Додаємо відступ зверху
                results_content,
                ft.Container(height=50)   # Додаємо відступ знизу
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        self.controls.append(main_column)
        self.update()
        

    async def show_results_start_view(self):
        self.controls.clear()
        self.controls.append(self.app_bar)
        result_percentage = self.test_data.get('percentage_score', 0)
        
        if result_percentage is not None:
            result_percentage = int(result_percentage)
        else:
            result_percentage = 0
        
        total_attempts = self.test_data.get('total_attempts', 0)
        attempts_used = self.test_data.get('attempts_used', 0)
        attempts_left = total_attempts - attempts_used

        is_passed = result_percentage >= self.test_data.get('passing_score', 0)
        can_retry = not is_passed and attempts_left > 0

        if is_passed:
            result_message = ft.Text(
                f"Вітаємо, тест пройдено! Поріг: {self.test_data.get('passing_score', 0)}%",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.GREEN_400
            )
            congratulation_icon = ft.Icon(name=ft.Icons.CELEBRATION, color=ft.Colors.GREEN_400, size=50)
            result_buttons = ft.ElevatedButton(
                text="Завершити",
                on_click=self.close_view,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )
        else:
            result_message = ft.Text(
                f"Тест не пройдено. Поріг: {self.test_data.get('passing_score', 0)}%",
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                color=ft.Colors.RED_400
            )
            congratulation_icon = ft.Icon(name=ft.Icons.WARNING, color=ft.Colors.RED_400, size=50)
            buttons_row = [
                ft.ElevatedButton(
                    text="Завершити",
                    on_click=self.close_view,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ]
            if can_retry:
                buttons_row.insert(0, ft.ElevatedButton(
                    text="Повторити тест",
                    on_click=self.restart_test,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_400,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                ))
            result_buttons = ft.Row(
                controls=buttons_row,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )

        score_text = ft.Text(
            f"Ваш результат: {self.test_data.get('score', 0)}",
            size=22,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.BLUE_GREY_200
        )

        percentage_text = ft.Text(
            f"{result_percentage:.0f}%",
            size=50,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_400 if result_percentage >= 70 else (ft.Colors.ORANGE_400 if result_percentage >= 50 else ft.Colors.RED_400),
            text_align=ft.TextAlign.CENTER
        )

        attempts_info = ft.Text(
            f"Спроб використано: {attempts_used} з {total_attempts}",
            size=16,
            color=ft.Colors.BLUE_GREY_200
        )

        if self.page.platform.name in ["Windows", "MACOS"]:
            width_t=450
            height_t=480
        else:
            width_t=320
            height_t=360

        results_content = ft.Card(
            width=width_t,
            # height=height_t,
            elevation=10,  # Задаємо тінь для картки
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=30),
                        congratulation_icon,
                        result_message,
                        score_text,
                        ft.Container(height=20),
                        percentage_text,
                        attempts_info,
                        ft.Container(height=30),
                        result_buttons
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                padding=30,  # Відступи всередині картки
                border_radius=15, # Закруглені кути
            )
        )

        main_column = ft.Column(
            [
                ft.Container(height=50),  # Додаємо відступ зверху
                results_content,
                ft.Container(height=50)   # Додаємо відступ знизу
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        self.controls.append(main_column)
        self.update()

    def next_question(self, e):
        self._next_question(e)

    def prev_question(self, e):
        self.current_step -= 1
        self.is_checked = False
        self.is_answered = bool(self.user_answers.get(self.current_step))
        self.update_test_content()

    
        
    def _calculate_results(self):
        """Вычисляет количество правильных ответов."""
        correct_count = 0
        total_questions = len(self.test_questions)
        for i, question_data in enumerate(self.test_questions):
            correct_answers = {a['answer_text'] for a in question_data['answers'] if a['is_correct']}
            user_selected = set(self.user_answers.get(i, []))
            
            if correct_answers == user_selected:
                correct_count += 1
        
        return correct_count, total_questions
    
    async def complete_test(self, e):
        correct_count, total_questions = self._calculate_results()
        result_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        # Оновлюємо дані в базі
        status = "passed" if result_percentage >= self.test_data['passing_score'] else "failed"
        update_assignment(
            username=self.test_data['user'], 
            test_title=self.test_data['title'],
            new_data={
                "status": status,
                "score": f"{correct_count}/{total_questions}",
                "percentage_score": round(result_percentage, 2),
                "increment_attempts": True
            }
        )
        # Оновлюємо self.test_data для відображення
        self.test_data['status'] = status
        self.test_data['score'] = f"{correct_count}/{total_questions}"
        self.test_data['percentage_score'] = round(result_percentage, 2)
        self.test_data['attempts_used'] += 1
        self.show_results_view(correct_count, total_questions)

    def build_simple_test_view(self):
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
        data.cancel = True
        self.update()
    
    async def close_view(self, e=None):
        self.parent_view.visible = True
        
        if hasattr(self.parent_view, 'refresh_data'):
            await self.parent_view.refresh_data(e)
        
        self.page.views.pop()
        self.page.update()