import flet as ft
import asyncio
from components.database_manager import initialize_database
from views.home_view import HomeView
from views.search_view import SearchView
from views.history_view import HistoryView
from views.profile_view import ProfileView
from views.progress_view import ProgressView
from views.login_view import create_login_view
from views.test_details_view import TestDetailsView
from views.user_view_edite import UserEdite


from views.user_view import UsersView

async def main(page: ft.Page):
    # 1. СИНХРОННАЯ ЧАСТЬ: Настройка страницы и инициализация базы данных
    page.title = "Школа KIVI"
    # page.theme_mode = ft.ThemeMode.LIGHT
    # page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.adaptive = True
    page.overlay.append(ft.HapticFeedback())
    initialize_database()

    async def theme_changed(e):

        if page.views and isinstance(page.views[-1], (TestDetailsView, UserEdite)):
            page.views.pop()
        # Переключаем тему
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        
        # Обновляем текст на переключателе
        c.label = (
            "Світла тема" if page.theme_mode == ft.ThemeMode.LIGHT else "Темна тема"
        )

        if page.theme_mode == ft.ThemeMode.DARK:
            tems_dark = True
        else:
            tems_dark = False

        # Сохраняем выбранную тему в локальное хранилище
        await page.client_storage.set_async("theme_mode", tems_dark)

        # Обновляем страницу, чтобы применить изменения
        page.update()
    
    # 1. Загружаем сохраненную тему из локального хранилища при запуске
    saved_theme = await page.client_storage.get_async("theme_mode")

    if saved_theme:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        # Если тема не найдена, используем светлую по умолчанию
        page.theme_mode = ft.ThemeMode.LIGHT
        
    # 2. Создаем переключатель с правильным названием и состоянием
    c = ft.Switch(
        label="Світла тема" if page.theme_mode == ft.ThemeMode.LIGHT else "Темна тема",
        # label_position=ft.LabelPosition.LEFT,
        value=(page.theme_mode == ft.ThemeMode.DARK), # Устанавливаем начальное состояние переключателя
        on_change=theme_changed
    )

    # 2. ВСЕ АСИНХРОННЫЕ ФУНКЦИИ ОПРЕДЕЛЯЮТСЯ ЗДЕСЬ
    #    Это гарантирует, что они будут доступны для вызова.
    async def show_login_view():
        page.controls.clear()
        if page.views and isinstance(page.views[-1], (TestDetailsView, UserEdite)):
            page.views.pop()

        async def on_login_success():
            await show_main_view()
        
        login_view = create_login_view(page, on_login_success=on_login_success)
        
        page.add(login_view)
        page.update()

    # Создаем все представления, передавая page
    home_view = HomeView(page)
    search_view = SearchView(page)
    history_view = HistoryView(page)
    profile_view = ProfileView(page, on_logout=show_login_view)
    progress_view = ProgressView(page)
    users_view = UsersView(page)

    more_card = ft.Card(
        elevation=4,
        content=ft.Container(
                padding=10,
                border_radius=10,
                # bgcolor=ft.Colors.BLUE_GREY_100,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.ListTile(
                                title=ft.Text(
                                    "Сторінки",
                                    weight=ft.FontWeight.BOLD,
                                    size=20,
                                    color=ft.Colors.ON_SURFACE, # Цвет текста, можно изменить
                                    ),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.HISTORY, color=ft.Colors.BLUE_400),
                                title=ft.Text("Історія"),
                                on_click=lambda e: page.run_task(on_nav_change_more,"Історія")
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.BLUE_400),
                                title=ft.Text("Профіль"),
                                on_click=lambda e: page.run_task(on_nav_change_more,"Профіль")
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.GROUP_OUTLINED, color=ft.Colors.BLUE_400),
                                title=ft.Text("Користувачі"),
                                on_click=lambda e: page.run_task(on_nav_change_more,"Користувачі")
                            ),
                            ft.ListTile(
                                title=ft.Text(
                                    "Тема",
                                    weight=ft.FontWeight.BOLD,
                                    size=20,
                                    color=ft.Colors.ON_SURFACE, # Цвет текста, можно изменить
                                    ),
                            ),
                            ft.ListTile(
                                c,
                            ),
                            ft.Container(
                                    height=30,
                                    content=ft.Text(
                                        "© 2025 KIVI UA. Усі права захищено.",
                                        size=10,
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                            
                        ], expand=True
                        ),
                    ]
                )
            ),
        )

        
    more_view = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                        [
                            ft.Text(
                                "Додаткові опції",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ON_PRIMARY_CONTAINER,
                            ),
                            ft.Divider(height=5, color="transparent"),
                            more_card
                        ],
                        spacing=5,
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                   
                    border_radius=15,
                    margin=10,
                    expand=True,
                    
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            visible=False
        )



    page.views_list = [home_view, search_view, history_view, profile_view, progress_view, users_view, more_view]

    views = {
            "Головна": home_view,
            "Пошук": search_view,
            "Історія": history_view,
            "Навчання": progress_view,
            "Профіль": profile_view,
            "Користувачі": users_view,
            "Ще": more_view,
        }

    async def on_nav_change_more(selected_wiev):
        selected_label = views[selected_wiev]

        for view in views.values():
            view.visible = (view == selected_label)

        page.update()

        if hasattr(selected_label, 'refresh_data'):
            await selected_label.refresh_data(None)


    async def show_main_view():
        page.controls.clear()
        if page.views and isinstance(page.views[-1], (TestDetailsView, UserEdite)):
            page.views.pop()


        async def on_nav_change(e):
            page.overlay[0].heavy_impact()
            selected_label = views[navigation.destinations[e.control.selected_index].label]

            for view in views.values():
                view.visible = (view == selected_label)

            page.update()

            if hasattr(selected_label, 'refresh_data'):
                await selected_label.refresh_data(None)

        async def logout_clicked(e):
            e.page.session.clear()
            e.page._invoke_method("clientStorage:remove", {"key": "username"}, wait_for_result=False)
            await show_login_view()

        tab = page.width >= page.height

        # tab = False
        if tab:
            app_bar = ft.Container(
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.MENU_BOOK, color=ft.Colors.BLUE_400, size=28),
                                ft.Text(
                                    "Школа KIVI",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                                ),
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        # Заполнитель, чтобы сдвинуть кнопку выхода вправо
                        ft.Container(expand=True),
                        c,
                        # Кнопка выхода
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            tooltip="Вийти",
                            icon_color=ft.Colors.ON_PRIMARY_CONTAINER,
                            on_click=logout_clicked,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=15),
                height=50,
                bgcolor=ft.Colors.PRIMARY_CONTAINER, # Легкий цвет фона
            )

            navigation = ft.NavigationRail(
                selected_index=0,
                on_change=on_nav_change,
                label_type=ft.NavigationRailLabelType.ALL,
                extended=True,
                min_width=100,
                min_extended_width=200,
                leading=ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.MENU, color=ft.Colors.BLUE_400),
                                    ft.Text(
                                        "Меню додатку",
                                        size=16,
                                        weight=ft.FontWeight.W_600
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            ft.Divider(
                                height=5,
                                thickness=5,
                                color=ft.Colors.GREY,
                            )
                        ],
                        spacing=10,  # Відступ між заголовком і розділювачем
                    ),
                    padding=ft.padding.only(left=10, top=20, bottom=10),
                    alignment=ft.alignment.center_left
                ),
                destinations=[
                    ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_400), label="Головна"),
                    ft.NavigationRailDestination(icon=ft.Icons.SEARCH, selected_icon=ft.Icon(ft.Icons.YOUTUBE_SEARCHED_FOR_SHARP, color=ft.Colors.BLUE_400), label="Пошук"),
                    ft.NavigationRailDestination(icon=ft.Icons.GRAPHIC_EQ, selected_icon=ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.Colors.BLUE_400), label="Навчання"),
                    ft.NavigationRailDestination(icon=ft.Icons.HISTORY, selected_icon=ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF, color=ft.Colors.BLUE_400), label="Історія"),
                    ft.NavigationRailDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400), label="Профіль"),
                    ft.NavigationRailDestination(icon=ft.Icons.GROUP_OUTLINED, selected_icon=ft.Icon(ft.Icons.GROUP, color=ft.Colors.BLUE_400), label="Користувачі"),
                    
                ]
            )

            if page.platform.name in ["Windows", "MACOS"]:
                page.add(app_bar,
                ft.Row([navigation, home_view, search_view, history_view, progress_view, profile_view, users_view],
                                expand=True, alignment=ft.MainAxisAlignment.CENTER,),
                                ft.Container(
                                    height=30,
                                    content=ft.Text(
                                        "© 2025 KIVI UA. Усі права захищено.",
                                        size=10,
                                    ),
                                    alignment=ft.alignment.center,
                                ))
            else:
                page.add(ft.Row([navigation, home_view, search_view, history_view, progress_view, profile_view, users_view],
                                expand=True, alignment=ft.MainAxisAlignment.CENTER,), ft.Container(height=20))

        else:

            navigation = ft.NavigationBar(
                selected_index=0,
                on_change=on_nav_change,
                animation_duration=500,
                animate_opacity=500,
                label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_400), label="Головна"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, selected_icon=ft.Icon(ft.Icons.YOUTUBE_SEARCHED_FOR_SHARP, color=ft.Colors.BLUE_400), label="Пошук"),
                    ft.NavigationBarDestination(icon=ft.Icons.GRAPHIC_EQ, selected_icon=ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.Colors.BLUE_400), label="Навчання"),
                    # ft.NavigationBarDestination(icon=ft.Icons.HISTORY, selected_icon=ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF, color=ft.Colors.BLUE_400), label="Історія"),
                    # ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400), label="Профіль"),
                    ft.NavigationBarDestination(icon=ft.Icons.MORE_HORIZ, selected_icon=ft.Icon(ft.Icons.MORE_HORIZ, color=ft.Colors.BLUE_400), label="Ще"),
                    # ft.NavigationRailDestination(icon=ft.Icons.PERSON, selected_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400), label="Користувачі")
                ],
            )

            

            page.add(ft.Column([home_view, search_view, history_view, progress_view, profile_view, users_view, more_view, navigation],
                            expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,))

        
        
        home_view.visible = True
        search_view.visible = False
        history_view.visible = False
        progress_view.visible = False
        profile_view.visible = False
        users_view.visible = False
        more_view.visible = False

        page.update()

        await asyncio.gather(home_view.initialize_data(),
                             search_view.initialize_data(),
                             history_view.initialize_data(),
                             profile_view.initialize_data(),
                             progress_view.initialize_data(),
                             users_view.initialize_data())


    
    # 3. ОСНОВНАЯ ЛОГИКА ЗАПУСКА ПРИЛОЖЕНИЯ
    saved_username = await page.client_storage.get_async("username")
    if saved_username:
        page.session.set("username", saved_username)
        await show_main_view()
        # await show_main_view_tab()
    else:
        await show_login_view()
    
if __name__ == "__main__":
    ft.app(target=main, port=9002, assets_dir='assets', view=ft.WEB_BROWSER)
    # ft.app(target=main)