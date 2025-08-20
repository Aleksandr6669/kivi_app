import flet as ft
import asyncio
from components.data import fetch_data_from_api
from components.database_manager import get_content_for_material, get_test_questions

class TestDetailsView(ft.View):
    def __init__(self, page: ft.Page, test_data: dict, parent_view: ft.Container):
        super().__init__()
        self.page = page
        self.test_data = test_data
        self.parent_view = parent_view
        
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
            self.page.run_task(self.load_test_content)
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
        self.prev_button = ft.IconButton(icon=ft.Icons.NAVIGATE_BEFORE, on_click=self.prev_step, icon_color=ft.Colors.BLUE_400, icon_size=20, padding=0,  tooltip="Попередній крок")
        self.next_button = ft.ElevatedButton(on_click=self.next_step, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), icon_color=ft.Colors.BLUE_400, padding=ft.padding.symmetric(horizontal=16)))

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
                padding=ft.padding.only(top=35, bottom=20, left=15, right=15)
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
            self.next_button.text = ""
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
        await self.close_view(e)

    # --- МЕТОДЫ ДЛЯ ТЕСТОВ ---

    async def load_test_content(self):
        title = self.test_data.get("title")
        test_questions = []
        if title:
            test_questions = await asyncio.to_thread(get_test_questions, title)

        if test_questions:
            self.test_questions = test_questions
            self.user_answers = {q["step_number"]: [] for q in test_questions}
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
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
                padding=ft.padding.only(top=35, bottom=20, left=15, right=15),
                expand=True
            ),
            ft.Container(
                padding=ft.padding.all(15),
                content=ft.Column(
                    controls=[
                        ft.Row([self.progress_text_test]),
                        self.dynamic_controls_panel
                    ]
                )
            )
        ]

    def _on_answer_select(self, e):
        if self.is_checked: return
        
        current_question_data = self.test_questions[self.current_step]
        question_id = current_question_data.get("step_number")
        
        if current_question_data.get("question_type") == "single_choice":
            answer_text = e.control.value
            self.user_answers[question_id] = [answer_text]
        else:
            checkbox_value = e.control.value
            answer_text = e.control.data['answer_text']
            
            self.user_answers.setdefault(question_id, [])
            if answer_text in self.user_answers[question_id] and not checkbox_value:
                self.user_answers[question_id].remove(answer_text)
            elif answer_text not in self.user_answers[question_id] and checkbox_value:
                self.user_answers[question_id].append(answer_text)

        self.is_answered = bool(self.user_answers.get(question_id))
        self.update_test_content()

    def _check_answer(self, e):
        current_question_data = self.test_questions[self.current_step]
        question_id = current_question_data.get("step_number")
        
        correct_answers = {a['answer_text'] for a in current_question_data['answers'] if a['is_correct']}
        user_selected = set(self.user_answers.get(question_id, []))
        
        is_correct = (correct_answers == user_selected)
        
        self.is_checked = True
        
        if is_correct:
            self.feedback_text.value = "Правильно!"
            self.feedback_text.color = ft.Colors.GREEN
            self.explanation_text.value = ""
        else:
            self.feedback_text.value = "Неправильно."
            self.feedback_text.color = ft.Colors.RED
            self.explanation_text.value = f"Правильные ответы: {', '.join(sorted(list(correct_answers)))}"
            
        self.update_test_content()

    def _next_question(self, e):
        self.is_checked = False
        self.is_answered = False
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
        question_id = question_data.get("step_number")

        self.question_card.content.content = ft.Column(
            [ft.Text(f"Питання {self.current_step + 1} з {len(self.test_questions)}", size=12, color=ft.Colors.BLUE_GREY_400),
             ft.Text(question_data.get("question_text", ""), weight=ft.FontWeight.BOLD, size=18)], spacing=5
        )
        
        self.answers_column.controls.clear()
        question_type = question_data.get("question_type")
        
        if question_type == "single_choice":
            radio_group = ft.RadioGroup(
                content=ft.Column(spacing=15),
                value=self.user_answers.get(question_id, [None])[0] if self.user_answers.get(question_id) else None,
                on_change=self._on_answer_select,
            )
            for answer in question_data.get("answers", []):
                is_correct = answer['is_correct']
                bgcolor = None
                if self.is_checked:
                    if is_correct:
                        bgcolor = ft.Colors.GREEN_100
                    elif answer['answer_text'] in self.user_answers.get(question_id, []) and not is_correct:
                        bgcolor = ft.Colors.RED_100
                
                control = ft.Radio(value=answer['answer_text'], data=answer, disabled=self.is_checked)
                card_content = ft.ListTile(
                    title=ft.Text(answer['answer_text']),
                    leading=control,
                    on_click=lambda e: radio_group.on_change(ft.ControlEvent(target=radio_group, value=e.control.leading.value))
                )
                radio_group.content.controls.append(ft.Card(content=card_content))
            self.answers_column.controls.append(radio_group)
        elif question_type == "multiple_choice":
            for answer in question_data.get("answers", []):
                is_selected = answer['answer_text'] in self.user_answers.get(question_id, [])
                is_correct = answer['is_correct']
                
                bgcolor = None
                if self.is_checked:
                    if is_correct:
                        bgcolor = ft.Colors.GREEN_100
                    elif is_selected and not is_correct:
                        bgcolor = ft.Colors.RED_100
                
                control = ft.Checkbox(
                    value=is_selected,
                    label=answer['answer_text'],
                    on_change=self._on_answer_select,
                    disabled=self.is_checked,
                    data=answer
                )
                card = ft.Card(
                    content=ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(answer['answer_text']),
                            leading=control,
                            on_click=lambda e: self._on_answer_select(ft.ControlEvent(target=control, value=not control.value))
                        ),
                        padding=10,
                        bgcolor=bgcolor
                    )
                )
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

    def next_question(self, e):
        self._next_question(e)

    def prev_question(self, e):
        self.current_step -= 1
        self.is_checked = False
        self.is_answered = False
        self.update_test_content()
        
    async def complete_test(self, e):
        print(f"Тест '{self.test_data.get('title')}' завершен.")
        await self.close_view(e)

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