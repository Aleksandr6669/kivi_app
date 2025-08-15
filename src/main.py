import flet as ft
import asyncio
from views.home_view import HomeView
from views.search_view import SearchView
from views.history_view import HistoryView
from views.profile_view import ProfileView
from views.progress_view import ProgressView
from views.login_view import create_login_view

async def main(page: ft.Page):
    page.title = "Тестування"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.adaptive = True

    async def show_login_view():
        page.controls.clear()

        async def on_login_success():
            await show_main_view()

        login_view = create_login_view(on_login_success=on_login_success)
        page.add(login_view)
        page.update()


    async def show_main_view():
        page.controls.clear()

        home_view = HomeView()
        search_view = SearchView()
        history_view = HistoryView()
        profile_view = ProfileView(on_logout=show_login_view)
        progress_view = ProgressView()

        views = {
            "Головна": home_view,
            "Пошук": search_view,
            "Історія": history_view,
            "Навчання": progress_view,
            "Профіль": profile_view,
        }

        def on_nav_change(e):
            selected_label = views[navigation_bar.destinations[e.control.selected_index].label]
            for view in views.values():
                view.visible = (view == selected_label)
            page.update()

        navigation_bar = ft.NavigationBar(
            selected_index=0,
            on_change=on_nav_change,
            adaptive=False,
            animation_duration=500,
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, selected_icon=ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_400), label="Головна"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, selected_icon=ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE_400), label="Пошук"),
                ft.NavigationBarDestination(icon=ft.Icons.GRAPHIC_EQ, selected_icon=ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.Colors.BLUE_400), label="Навчання"),
                ft.NavigationBarDestination(icon=ft.Icons.HISTORY, selected_icon=ft.Icon(ft.Icons.HISTORY, color=ft.Colors.BLUE_400), label="Історія"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, selected_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400), label="Профіль")
            ]


        )

        page.add(ft.Column([home_view, search_view, history_view, progress_view, profile_view, navigation_bar],
                          expand=True))
        home_view.visible = True
        page.update()

        await asyncio.gather(home_view.initialize_data(),
                             search_view.initialize_data(),
                             history_view.initialize_data(),
                             profile_view.initialize_data(),
                             progress_view.initialize_data())



    await show_login_view()


if __name__ == "__main__":
    # ft.app(main)

    ft.app(main, port=9002, assets_dir='assets', view=ft.WEB_BROWSER)
