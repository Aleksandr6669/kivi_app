import flet as ft

def create_login_view(on_login_success):
    """
    Создает представление страницы входа.

    Args:
        on_login_success (function): Функция обратного вызова, вызываемая при успешном входе.
    """
    username_field = ft.TextField(
        label="Имя пользователя",
        autofocus=True,
        width=300,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.INDIGO_200
    )
    
    password_field = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.INDIGO_200
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED_500, visible=False)

    async def login_clicked(e):
        # Простая проверка: если поля не пустые, считаем вход успешным
        if username_field.value and password_field.value:
            error_text.visible = False
            await on_login_success()
        else:
            error_text.value = "Пожалуйста, введите имя пользователя и пароль."
            error_text.visible = True
        e.page.update()

    login_button = ft.ElevatedButton(
        text="Войти",
        on_click=login_clicked,
        width=300,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.INDIGO_700,
        )
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Авторизация", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color="transparent"),
                username_field,
                password_field,
                login_button,
                error_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        alignment=ft.alignment.center,
        expand=True
    )