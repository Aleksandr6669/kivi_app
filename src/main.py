import flet as ft
from routes import route_change
from views.user_info_view import user_info_view

def main(page: ft.Page):
    page.title = "Kivi Retail TEST"
    page.version = "0.0.2"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Системная тема (светлая/темная)
    page.horizontal_alignment = 'center'  # Выравнивание по центру
    page.vertical_alignment = 'center'  # Выравнивание по центру
    page.adaptive = True

    page.appbar = ft.AppBar(
        title=ft.Text("KIVI Retail DEV", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_600),
        actions=[
            ft.IconButton(ft.cupertino_icons.INFO, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )


    
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.EXPLORE,
                label="Explore",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE,
                label="Commute",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Bookmark",
            ),
        ],
    
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED, # Метки отображаются только для выбранного пункта назначения
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )


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
            padding=ft.Padding(left=10, top=10, right=10, bottom=10),
            margin=ft.Margin(left=0, top=0, right=0, bottom=10),
        )
        return _top_container
    
    # Page content
    _c = ft.Container(
        height=page.height,  # Set the height of the container
        content=ft.ListView(
            height=page.height,  # Set the height of the ListView
            controls=[
                _top() for i in range(10)  # Alternate between _top and _bottom
            ]+ [ft.Container(height=100)],  # Add spacing at the end
            on_scroll=True,
        ),
    )
    
    # Добавляем элементы на страницу
    page.add(_c)
    page.add(ft.Container(height=20))

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")

# ft.app(main, view=ft.AppView.WEB_BROWSER)
