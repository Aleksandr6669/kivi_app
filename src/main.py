import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Kivi Retail TEST"
    page.version = "0.0.2"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Системная тема (светлая/темная)
    page.horizontal_alignment = 'center'  # Выравнивание по центру
    page.vertical_alignment = 'center'  # Выравнивание по центру
    page.adaptive = True

    def news_feed_view(page, title, content, icon, date):
        # Пример функции, возвращающей новость о компании КИВИ
        def expand_news(e):
            dialog = ft.AlertDialog(
                title=ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
                content=ft.Markdown(content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                actions=[
                    ft.TextButton("Закрыть", on_click=lambda e: setattr(dialog, 'open', False))
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        return ft.Container(
            padding=ft.Padding(10, 10, 10, 10),
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#333333", "#111111"]
            ),
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.Colors.GREY_400,
                offset=ft.Offset(2, 2)
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, size=40, color=ft.Colors.WHITE),
                            ft.Column(
                                controls=[
                                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                    ft.Text(date, size=14, color=ft.Colors.GREY_300),
                                ]
                            ),
                            ft.IconButton(ft.Icons.EXPAND_MORE, on_click=expand_news, icon_size=24, icon_color=ft.Colors.WHITE)
                        ]
                    ),
                    ft.Markdown(content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                ]
            ),
            margin=ft.Margin(10, 10, 10, 10)
        )

    def home_page():
        news_list = [
            {"title": "Новость 1", "content": "Компания КИВИ запускает новый продукт. Подробнее можно узнать на [официальном сайте](https://www.kivi.com).", "icon": ft.Icons.NEW_LABEL, "date": "26 февраля 2025"},
            {"title": "Новость 2", "content": "Компания КИВИ открывает новый офис. Адрес офиса можно найти [здесь](https://www.kivi.com/office).", "icon": ft.Icons.BUSINESS, "date": "25 февраля 2025"},
            {"title": "Новость 3", "content": "Компания КИВИ объявляет о партнерстве с ведущими компаниями. Подробности на [сайте](https://www.kivi.com/partners).", "icon": ft.Icons.HANDSHAKE, "date": "24 февраля 2025"},
            {"title": "Новость 4", "content": "Компания КИВИ проводит благотворительную акцию. Узнать больше можно [здесь](https://www.kivi.com/charity).", "icon": ft.Icons.VOLUNTEER_ACTIVISM, "date": "23 февраля 2025"},
            {"title": "Новость 5", "content": "Компания КИВИ получила награду за инновации. Подробности на [официальном сайте](https://www.kivi.com/awards).", "icon": ft.Icons.STAR, "date": "22 февраля 2025"},
            {"title": "Новость 6", "content": "Компания КИВИ запускает новую программу лояльности. Узнать больше можно [здесь](https://www.kivi.com/loyalty).", "icon": ft.Icons.CARD_GIFTCARD, "date": "21 февраля 2025"},
            {"title": "Новость 7", "content": "Компания КИВИ расширяет ассортимент продукции. Подробности на [сайте](https://www.kivi.com/products).", "icon": ft.Icons.SHOPPING_CART, "date": "20 февраля 2025"},
            {"title": "Новость 8", "content": "Компания КИВИ проводит вебинар по новым технологиям. Регистрация доступна [здесь](https://www.kivi.com/webinar).", "icon": ft.Icons.WEB, "date": "19 февраля 2025"},
            {"title": "Новость 9", "content": "Компания КИВИ объявляет о скидках на продукцию. Подробности на [официальном сайте](https://www.kivi.com/discounts).", "icon": ft.Icons.LOCAL_OFFER, "date": "18 февраля 2025"},
            {"title": "Новость 10", "content": "Компания КИВИ открывает новые вакансии. Узнать больше можно [здесь](https://www.kivi.com/careers).", "icon": ft.Icons.WORK, "date": "17 февраля 2025"},
        ]

        news_controls = [news_feed_view(page, news["title"], news["content"], news["icon"], news["date"]) for news in news_list]

        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=news_controls + [ft.Container(height=100)],  # Add spacing at the end
                on_scroll=True,
            )
        )

    def search_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=[
                    ft.Text("Search Page", size=24, weight=ft.FontWeight.BOLD)
                ]+ [ft.Container(height=100)],  # Add spacing at the end
                on_scroll=True,
            )
        )

    def notifications_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.animation.Animation(duration=250, curve="ease_in_out"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=[
                    ft.Text("Notifications Page", size=24, weight=ft.FontWeight.BOLD)
                ]+ [ft.Container(height=100)],  # Add spacing at the end
                on_scroll=True,
            )
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
            ft.IconButton(ft.CupertinoIcons.INFO, style=ft.ButtonStyle(padding=0))
        ],
        bgcolor=ft.Colors.with_opacity(0.04, ft.CupertinoColors.SYSTEM_BACKGROUND),
    )

    bottom_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.HOME, size=40), 
                label="Home"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.SEARCH, size=40), 
                label="Search"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.Icons.NOTIFICATIONS, size=40),
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