import flet as ft
import asyncio
# Импортируем только функцию для входа
from components.database_manager import login_user

def create_login_view(page: ft.Page, on_login_success):
    """
    Создает представление страницы входа.
    """
    username_field = ft.TextField(
        adaptive=False,
        label="Логін",
        width=300,
        border_radius=ft.border_radius.all(20),
        border_color=ft.Colors.INDIGO_200
    )
    
    password_field = ft.TextField(
        adaptive=False,
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=ft.border_radius.all(20),
        border_color=ft.Colors.INDIGO_200
    )
    
    error_text = ft.Text(value="", color=ft.Colors.RED_500, visible=False)

    async def login_clicked(e):
        error_text.visible = False
        e.page.update()

        if not username_field.value or not password_field.value:
            error_text.value = "Будь ласка, введіть логін та пароль"
            error_text.visible = True
            e.page.update()
            return
        
        # Показываем индикатор загрузки на кнопке
        login_button.disabled = True
        login_button.content = ft.ProgressRing(width=20, height=20, stroke_width=2)
        e.page.update()
        
        # Вызываем функцию входа, которая возвращает True или False
        is_success = await asyncio.to_thread(
            login_user, 
            username_field.value, 
            password_field.value
        )

        if is_success:
            # Сохраняем логин в сессии и переходим на главный экран
            await page.client_storage.set_async("username", username_field.value)
            e.page.session.set("username", username_field.value)
            await on_login_success()
        else:
            # В случае ошибки показываем сообщение и возвращаем кнопку
            error_text.value = "Невірний логін або пароль"
            error_text.visible = True
            login_button.disabled = False
            login_button.content = ft.Text("УВІЙТИ")
            e.page.update()

    login_button = ft.ElevatedButton(
        content=ft.Text("УВІЙТИ"),
        on_click=login_clicked,
        width=150,
        height=40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=ft.Colors.INDIGO_700,
            color=ft.Colors.BLUE_200,
        ),
    )

    login_view_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.INDIGO_700),
                            ft.Text("Авторизація", size=28, weight=ft.FontWeight.BOLD),
                            ft.Divider(height=5, color="transparent"),
                            username_field,
                            password_field,
                            login_button,
                            error_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
                    ),
                    padding=ft.padding.all(10),
                ),
                ft.Text("© 2025 KIVI UA. Усі права захищено.", size=10)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    return login_view_container