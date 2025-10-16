import flet as ft
import asyncio
from components.database_manager import create_or_update_user_profile, register_user

class UserEdite(ft.View):
    def __init__(self, page: ft.Page, parent_view, user_data: dict = None):

        is_editing = user_data is not None
        super().__init__() 
        self.page = page
        self.parent_view = parent_view
        self.user_data = user_data

        def clear_error(e):
            e.control.error_text = None
            e.control.border_color = None
            self.page.update()
        
        # Динамічний текст для заголовка та кнопки
        page_title = "Редагування профілю" if is_editing else "Додавання користувача"
        card_title = "Картка користувача" if is_editing else "Створення нового користувача"
        button_text = "Зберегти зміни" if is_editing else "Додати користувача"
        
        # Поля форми
        self.username_field = ft.TextField(
            adaptive=False,
            label="Системне ім'я *",
            value=self.user_data.get("username", "") if is_editing else "",
            disabled=is_editing, # Забороняємо редагування імені користувача
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            on_change=clear_error
            
        )
        self.full_name_field = ft.TextField(
            adaptive=False,
            label="Повне ім\'я *",
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            on_change=clear_error,
            value=self.user_data.get("full_name", "") if is_editing else ""
            
        )
        self.email_field = ft.TextField(
            adaptive=False,
            label="Електронна пошта",
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            on_change=clear_error,
            value=self.user_data.get("email", "") if is_editing else ""
        )
        self.phone_field = ft.TextField(
            adaptive=False,
            label="Телефон",
            prefix_icon=ft.Icons.PHONE_OUTLINED,
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            on_change=clear_error,
            value=self.user_data.get("phone", "") if is_editing else ""
        )
        self.password_field = ft.TextField(
            adaptive=False,
            label="Пароль *",
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            hint_text="Залиште пустим, щоб не змінювати" if is_editing else "Обов'язковий для нового користувача",
            password=True,
            can_reveal_password=True,
            on_change=clear_error
        )
        self.about_field = ft.TextField(
            adaptive=False,
            label="Про себе",
            multiline=True,
            width=300,
            height=45,
            border_radius=ft.border_radius.all(10),
            text_size=12,
            text_vertical_align=ft.VerticalAlignment.CENTER,
            on_change=clear_error,
            value=self.user_data.get("about", "") if is_editing else ""
        )
        
        self.submit_button = ft.ElevatedButton(
            text=button_text,
            on_click=self.submit_form,
            icon=ft.Icons.SAVE if is_editing else ft.Icons.ADD,
            # style=ft.ButtonStyle(
            #     bgcolor=ft.Colors.BLUE_400,
            #     color=ft.Colors.WHITE,
            #     shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)),
            #     padding=ft.padding.symmetric(horizontal=25, vertical=15)
            # ),
            # icon_color=ft.Colors.WHITE
        )

        self.error_text = ft.Text(value="", color=ft.Colors.RED_500, visible=False)
        self.info_text = ft.Text(value="Поле з * обов\'язкове для заповнення", color=ft.Colors.RED_500)


        def create_field_container(field):
            return ft.Container(content=field, height=45, width=300)
        
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(card_title, size=20, weight=ft.FontWeight.BOLD),
                        self.info_text,
                        create_field_container(self.username_field),
                        create_field_container(self.full_name_field),
                        create_field_container(self.email_field),
                        create_field_container(self.phone_field),
                        create_field_container(self.password_field),
                        create_field_container(self.about_field),
                        self.error_text
                    ],
                    spacing=15,
                    expand=True,
                    scroll=ft.ScrollMode.HIDDEN
                ),
                padding=25,
            ),
            elevation=10,
            expand=True,
        )


        

        self.controls = [
            ft.AppBar(title=ft.Text(page_title)),
            # self.submit_button,
            ft.Row(
                [   
                    
                    ft.Container(
                        # expand=True,
                        content=form_card,
                        # width=350,
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(vertical=20),
                    ),
                    # ft.Container(
                    #     # expand=True,
                    #     content=form_card,
                    #     # width=350,
                    #     alignment=ft.alignment.center,
                    #     padding=ft.padding.symmetric(vertical=20),
                    # ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            
            ft.Row(
                    [self.submit_button],
                    # height=50,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ft.Container(height=20)
                
        ]

    

    async def submit_form(self, e):
        is_editing = self.user_data is not None
        error_found = False
        self.error_text.visible = False
        
        if not self.username_field.value:
                self.username_field.border_color = ft.Colors.RED
                # self.username_field.error_text = "Поле 'Системне ім\'я не може бути порожнім"
                error_found = True
                # self.error_text.value = "Поле 'Системне ім\'я' не може бути порожнім"
                self.error_text.visible = True

        if not self.full_name_field.value:
            self.full_name_field.border_color = ft.Colors.RED
            # self.full_name_field.error_text = "Поле 'Повне ім\'я' не може бути порожнім"
            error_found = True
            # self.error_text.value = "Поле 'Повне ім\'я' не може бути порожнім"
            self.error_text.visible = True

        # Проверка обязательных полей только для новых пользователей
        if not is_editing:
            if not self.password_field.value:
                self.password_field.border_color = ft.Colors.RED
                # self.password_field.error_text = "Пароль є обов\'язковим для нового користувача!"
                error_found = True
                # self.error_text.value = "Пароль є обов\'язковим для нового користувача!"
                self.error_text.visible = True

        if error_found:
            self.error_text.value = "Треба заповнити обовь\'язкові поля"
            self.page.update()
            return


        updated_data = {

            "username": self.username_field.value,
            "full_name": self.full_name_field.value,
            "email": self.email_field.value,
            "phone": self.phone_field.value,
            "about": self.about_field.value,
        }
        
        if self.password_field.value:
            updated_data["password"] = self.password_field.value

        # self.page.update()


        


        def close_dlg(e):
            self.page.close(error_password)
            self.page.update()

        error_password = ft.AlertDialog(
            adaptive=False,
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.ORANGE_800),
                ft.Text("Помилка"),
            ], alignment=ft.MainAxisAlignment.START),
            content=ft.Column([
                ft.Text("Пароль є обов'язковим для нового користувача!"),
            ], spacing=10, tight=True),
            actions=[
                ft.TextButton(
                    "Зрозуміло",
                    on_click=close_dlg,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_GREY_100,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=5),
                    )
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )


        
        
        if is_editing:
            await asyncio.to_thread(create_or_update_user_profile, updated_data["username"], updated_data)
        else:
            if updated_data.get("password"):
                await asyncio.to_thread(register_user, updated_data["username"], updated_data["password"])
                await asyncio.to_thread(create_or_update_user_profile, updated_data["username"], updated_data)
            else:
                self.page.open(error_password)
                self.page.update()
                return

                
        self.parent_view.visible = True
        if hasattr(self.parent_view, 'refresh_data'):
            await self.parent_view.refresh_data(e)
            
        self.page.views.pop()
        self.page.update()