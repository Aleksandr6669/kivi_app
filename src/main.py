import flet as ft
import asyncio
from routes import route_change
from views.user_info_view import user_info_view

def main(page: ft.Page):
    page.title = "Kivi Retail TEST"
    page.version = "0.0.2"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Системная тема (светлая/темная)
    page.horizontal_alignment = 'center'  # Выравнивание по центру
    page.vertical_alignment = 'center'  # Выравнивание по центру
    page.adaptive = True

    expanded = False

    def _expand_click(event):
        nonlocal expanded
        # Toggle expansion state
        expanded = not expanded
        # Update the height and radius based on the state
        new_top_height = page.height * 0.7 if expanded else page.height * 0.15
        _top_container.height = new_top_height
        _top_container.update()

    def _top():
        global _top_container
        info = user_info_view(page)
        _top_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_right,
                end=ft.alignment.top_left,
                colors=["grey800", "grey900"],
            ),
            border_radius=ft.BorderRadius(top_left=15, top_right=15, bottom_left=15, bottom_right=15),
            animate=ft.animation.Animation(duration=350, curve="decelerate"),
            on_click=_expand_click,
            content=ft.Column(
                alignment="start",
                controls=[info],
            ),
            margin=ft.Margin(left=0, top=0, right=0, bottom=10),
        )
        return _top_container

    def home_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=[
                    _top() for i in range(10)  # Alternate between _top and _bottom
                ]+ [ft.Container(height=100)],  # Add spacing at the end
                on_scroll=True,
            )
        )

    def search_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.Text("Search Page", size=24, weight=ft.FontWeight.BOLD)
        )

    def notifications_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.Text("Notifications Page", size=24, weight=ft.FontWeight.BOLD)
        )

    async def on_nav_change(e):
        selected_index = e.control.selected_index
        for i, container in enumerate(page.controls[1:4]):
            container.height = page.height if i == selected_index else 0
            container.update()
        await asyncio.sleep(0.5)  # Задержка для плавного перехода

    top_appbar = ft.AppBar(
        title=ft.Text("KIVI Retail DEV", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
        actions=[
            ft.IconButton(ft.cupertino_icons.INFO, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )

    bottom_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.HOME, size=20), 
                label="Home"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.SEARCH, size=20), 
                label="Search"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.NOTIFICATIONS, size=20),
                label="Notifications"
            ),
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        on_change=on_nav_change
    )

    # Добавляем элементы на страницу
    page.add(top_appbar)
    page.add(home_page())  # Начальная страница
    page.add(search_page())
    page.add(notifications_page())
    page.add(bottom_navigation_bar)

    # Устанавливаем начальную высоту для первой страницы
    page.controls[1].height = page.height
    page.controls[1].update()

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")

# ft.app(main, view=ft.AppView.WEB_BROWSER)
