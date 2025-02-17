import flet as ft
from routes import route_change

def main(page: ft.Page):
    page.title = "Kivi Retail 1.4"
    page.theme_mode = ft.ThemeMode.SYSTEM # Системная тема (светлая/темная)

    # Функция для обработки клика по аватару
    def show_user_info(e):
        page.go("/user_info")  # Переход на страницу с информацией о пользователе

    # Аватар пользователя с обработкой клика
    avatar = ft.Container(
        content=ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        ),
        margin=ft.Margin(left=0, right=16, top=0, bottom=0),
        on_click=show_user_info  # Обработчик клика по аватару
    )
    
    # Панель с заголовком и аватаром
    appbar = ft.AppBar(
        title=ft.Text("Kivi Retail", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE_ACCENT),
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
        actions=[avatar]
    )

    # Панель навигации
    navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.INFO_OUTLINE, label="News feed"),
            ft.NavigationBarDestination(icon=ft.Icons.MAIL_OUTLINE, label="Order"),
            ft.NavigationBarDestination(icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="Favorites"),
        ],
        on_change=lambda e: page.go(["/news_feed", "/order", "/favorites"][e.control.selected_index])
    )
    
    # Контент страницы
    content = ft.Column(expand=True)
    
    # Добавляем элементы на страницу
    page.add(appbar, content, navigation_bar)
    
    # Обработка смены маршрута
    page.on_route_change = lambda e: route_change(e.route, content, page)
    page.go("/news_feed")  # Начальная страница

ft.app(main, view=ft.AppView.WEB_BROWSER)
