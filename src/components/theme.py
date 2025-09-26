import flet as ft

def get_active_theme(theme_mode):
    """
    Возвращает настроенные темы для приложения.
    """
    # Светлая тема
    light_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            # background=ft.Colors.GREY_300,  # Ярко-серый фон страницы
            # on_background=ft.Colors.BLACK,
            primary=ft.Colors.BLACK,
            on_primary=ft.Colors.WHITE,
            # surface=ft.Colors.WHITE        # Белые карточки
        )
    )

    # Тёмная тема
    dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            # background=ft.Colors.GREY_900,  # Темно-серый фон страницы
            # on_background=ft.Colors.WHITE,
            primary=ft.Colors.WHITE,
            on_primary=ft.Colors.BLACK,
            # surface=ft.Colors.GREY_800     # Темно-серые карточки
        )
    )

    if theme_mode == ft.ThemeMode.DARK:
        return dark_theme
    else:
        return light_theme

def get_active_cart(theme_mode):

    # if theme_mode != ft.ThemeMode.DARK:
    #     return ft.Colors.WHITE
    pass
   
