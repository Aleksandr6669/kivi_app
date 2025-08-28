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

# Main asynchronous function, which is the entry point for Flet
async def main(page: ft.Page):
    # This function is now async, so we can use `await` directly
    
    # 1. SYNCHRONOUS SETUP: Page and database initialization
    page.title = "Тестування"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.adaptive = True
    page.overlay.append(ft.HapticFeedback())
    initialize_database()

    # 2. DEFINE ASYNCHRONOUS HELPER FUNCTIONS
    
    async def refresh_all_views(source="unknown"):
        """
        A central function to silently refresh all views in the session.
        """
        if hasattr(page, 'views_list'):
            for view in page.views_list:
                if hasattr(view, 'silent_refresh') and callable(getattr(view, 'silent_refresh')):
                    await view.silent_refresh()
    
    page.refresh_all_views = refresh_all_views

    async def show_login_view():
        page.controls.clear()
        if page.views and isinstance(page.views[-1], TestDetailsView):
            page.views.pop()

        async def on_login_success():
            await show_main_view()
        
        login_view = create_login_view(on_login_success=on_login_success)
        
        page.add(login_view)
        page.update()

    async def show_main_view():
        page.controls.clear()
        if page.views and isinstance(page.views[-1], TestDetailsView):
            page.views.pop()

        home_view = HomeView()
        search_view = SearchView()
        history_view = HistoryView()
        profile_view = ProfileView(on_logout=show_login_view)
        progress_view = ProgressView()

        page.views_list = [home_view, search_view, history_view, profile_view, progress_view]

        views = {
            "Головна": home_view,
            "Пошук": search_view,
            "Історія": history_view,
            "Навчання": progress_view,
            "Профіль": profile_view,
        }

        async def on_nav_change(e):
            page.overlay[0].heavy_impact()
            selected_label = views[navigation_bar.destinations[e.control.selected_index].label]

            for view in views.values():
                view.visible = (view == selected_label)

            page.update()

            if hasattr(selected_label, 'refresh_data'):
                await selected_label.refresh_data(None)

        navigation_bar = ft.NavigationBar(
            selected_index=0,
            on_change=on_nav_change,
            animation_duration=500,
            animate_opacity=500,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_400), label="Головна"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, selected_icon=ft.Icon(ft.Icons.YOUTUBE_SEARCHED_FOR_SHARP, color=ft.Colors.BLUE_400), label="Пошук"),
                ft.NavigationBarDestination(icon=ft.Icons.GRAPHIC_EQ, selected_icon=ft.Icon(ft.Icons.GRAPHIC_EQ, color=ft.Colors.BLUE_400), label="Навчання"),
                ft.NavigationBarDestination(icon=ft.Icons.HISTORY, selected_icon=ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF, color=ft.Colors.BLUE_400), label="Історія"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400), label="Профіль")
            ]
        )

        page.add(ft.Column([home_view, search_view, history_view, progress_view, profile_view, navigation_bar],
                          expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,))
        
        home_view.visible = True
        search_view.visible = False
        history_view.visible = False
        progress_view.visible = False
        profile_view.visible = False

        page.update()

        await asyncio.gather(home_view.initialize_data(),
                             search_view.initialize_data(),
                             history_view.initialize_data(),
                             profile_view.initialize_data(),
                             progress_view.initialize_data())
    
    # 3. CORE AUTHENTICATION LOGIC:
    #    This part runs when the app starts.
    saved_username = await page.client_storage.get_async("username")
    if saved_username:
        page.session.set("username", saved_username)
        await show_main_view()
    else:
        await show_login_view()
    
if __name__ == "__main__":
    ft.app(target=main, port=9002, assets_dir='assets', view=ft.WEB_BROWSER)