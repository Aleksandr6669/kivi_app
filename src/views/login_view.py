import flet as ft
import asyncio
import flet_lottie as fl
from components.theme import get_active_cart

import random
import string
import hashlib
import base64

# Импортируем только функцию для входа
from components.database_manager import login_user

def create_login_view(page: ft.Page, on_login_success):
 
    username_title = ft.Text("Login", size=16)
    
    password_title = ft.Text("Password", size=16)

    username_field = ft.TextField(
        adaptive=False,
        # label="Логін",
        hint_text="User123",
        width=300,
        height=45,
        border_radius=ft.border_radius.all(10),
        autofill_hints=[ft.AutofillHint.EMAIL],
        text_size=12,
        text_vertical_align=ft.VerticalAlignment.CENTER,
        # filled=True,
        # border=ft.InputBorder.UNDERLINE
        # border_color=ft.Colors.INDIGO_200
    )
    
    password_field = ft.TextField(
        adaptive=False,
        # label="Пароль",
        hint_text="password",
        password=True,
        can_reveal_password=True,
        width=300,
        height=45,
        border_radius=ft.border_radius.all(10),
        text_size=12,
        text_vertical_align=ft.VerticalAlignment.CENTER,
        # border=ft.InputBorder.UNDERLINE
        # border_color=ft.Colors.INDIGO_200
    )

    logo = ft.Container(
            width=120,
            content=fl.Lottie(
                src="lottiefiles/Back to school!.json",
                reverse=False,
                animate=True,
            ),
            padding=0
        )

    error_text = ft.Text(value="", color=ft.Colors.RED_500, visible=False)

    async def login_clicked(e):
        error_text.visible = False
        e.page.update()

        if not username_field.value or not password_field.value:
            error_text.value = "Please enter your login and password"
            error_text.visible = True
            e.page.update()
            return
        
        # Показываем индикатор загрузки на кнопке
        login_button.disabled = True
        login_button.content = ft.ProgressRing(width=20, height=20, stroke_width=2)
        e.page.update()


        platform_name = page.platform.name
        user_agent = page.client_user_agent

        combined_string = f"{platform_name}||{user_agent}"

        saved_device = await page.client_storage.get_async("device")
        if not saved_device:
                
            characters = string.ascii_letters + string.digits
            device = ''.join(random.choice(characters) for i in range(32))

            await page.client_storage.set_async("device", device)
            combined_string = f"{platform_name}||{user_agent}||{device}"

        else:
            combined_string = f"{platform_name}||{user_agent}||{saved_device}"

        id_device = base64.b64encode(combined_string.encode('utf-8')).decode('utf-8')

        is_success = await asyncio.to_thread(
                login_user, 
                username_field.value, 
                password_field.value,
                id_device,
            )
        
        # Вызываем функцию входа, которая возвращает True или False
        

        if is_success:
            # Сохраняем логин в сессии и переходим на главный экран
            await page.client_storage.set_async("username", username_field.value)
            e.page.session.set("username", username_field.value)

            await page.client_storage.set_async("is_success", is_success)

            await on_login_success()
        else:
            # В случае ошибки показываем сообщение и возвращаем кнопку
            error_text.value = "Incorrect login or password"
            error_text.visible = True
            login_button.disabled = False
            login_button.content = ft.Text("Login")
            e.page.update()

    login_button = ft.CupertinoFilledButton(
        content=ft.Text("Login"),
        padding=0,
        on_click=login_clicked,
        width=300,
        height=45,
        disabled_bgcolor=False
        # text="Login"
        
    )


    if page.platform.name in ["Windows", "MACOS"]:
        width_t=350
        height_t=380
    else:
        width_t=320
        height_t=360
    
    colors_cart=get_active_cart(page.theme_mode)
    print(colors_cart)
    
    login_view_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            # ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color=ft.Colors.INDIGO_700),
                            logo,
                            ft.Card(
                                color=colors_cart,
                                elevation=1,
                                width=width_t,
                                height=height_t,
                                content=ft.Container(
                                    padding=20,
                                    border_radius=5,
                                    content=ft.Column([
                                        
                                        ft.Text("Welcome to VivaLearn.", size=22, weight=ft.FontWeight.BOLD),
                                        # ft.Divider(height=5, color="transparent"),
                                        ft.Text("Please log in", size=14),
                                        # ft.Text(page.client_ip, size=14),
                                        
                                        ft.Column([
                                            username_title,
                                            username_field,
                                            ]),
                                        ft.Column([
                                            password_title,
                                            password_field,
                                            ]),
                                        ft.Divider(height=10, color="transparent"),
                                        login_button,
                                        error_text,
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER, spacing=5,
                                    ),
                                ),

                            ),
                            
                            
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.CENTER, spacing=10,
                    ),
                    padding=ft.padding.all(10),
                ),
                ft.Text("© 2025 VIVALEARN. All rights reserved.", size=10)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        alignment=ft.alignment.center,
        expand=True
    )

    return login_view_container