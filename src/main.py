import flet as ft
from routes import route_change
from views.user_info_view import user_info_view

def main(page: ft.Page):
    page.title = "Kivi Retail TEST"
    page.version = "0.0.1"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Системная тема (светлая/темная)
    page.horizontal_alignment = 'center'  # Выравнивание по центру
    page.vertical_alignment = 'center'  # Выравнивание по центру

    expanded = False
    radius_avatar = page.height * 0.05

    def _expand_click(e):
        nonlocal expanded, radius_avatar
        # Toggle expansion state
        expanded = not expanded
        # Update the height and radius based on the state
        new_height = page.height * 0.8 if expanded else page.height * 0.15
        radius_avatar = page.height * 0.1 if expanded else page.height * 0.05
        _top_container.height = new_height
        _avatar.radius = radius_avatar
        _title.content.size = 36 if expanded else 32
        _subtitle.content.size = 28 if expanded else 26
        _top_container.update()

    def _top():
        global _avatar, _top_container, _title, _subtitle
        info, _avatar, _title, _subtitle = user_info_view(page, radius_avatar)
        _top_container = ft.Container(
            width=page.width,  # Dynamic width (80% of the screen width)
            height=page.height * 0.15,  # Dynamic height (40% of the screen height)
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_right,
                end=ft.alignment.top_left,
                colors=["lightblue600", "lightblue900"],
            ),
            border_radius=35,
            animate=ft.animation.Animation(duration=350, curve="decelerate"),
            on_click=_expand_click,
            content=ft.Column(
                alignment="start",
                controls=[info],
            ),
        )
        return _top_container

    def _bottom():
        bottom = ft.Container(
            width=page.width,  # Dynamic width (80% of the screen width)
            height=page.height * 0.10,  # Dynamic height (40% of the screen height)
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_right,
                end=ft.alignment.top_left,
                colors=["lightblue300", "lightblue600"],
            ),
            border_radius=35,
            # animate=ft.animation.Animation(duration=350, curve="decelerate"),
        )
        return bottom

    # Контент страницы
    _c = ft.Container(
        width=page.width,
        height=page.height,
        content=ft.Column(
            width=page.width * 0.95,
            height=page.height,
            controls=[
                _top(),
                ft.Container(height=page.height * 0.7),  # Пустое пространство между верхним и нижним контейнерами
                _bottom()
            ],
        ),
    )
    
    # Добавляем элементы на страницу
    page.add(_c)

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")

# ft.app(main, view=ft.AppView.WEB_BROWSER)
