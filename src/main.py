import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "Kivi Retail TEST"
    page.version = "0.7"
    page.description = "Kivi Retail TEST"
    
    # Загружаем manifest.json для PWA
    page.assets_dir = "assets"  # Путь к папке с ассетами, включая manifest.json и иконки
    page.manifest = "manifest.json" 
    page.theme_mode = ft.ThemeMode.SYSTEM  # Системная тема (светлая/темная)
    page.horizontal_alignment = 'center'  # Выравнивание по центру
    page.vertical_alignment = 'center'  # Выравнивание по центру
    page.adaptive = False # Отключаем адаптивный дизайн
    page.language = "ua"  # Устанавливаем язык страницы
    page.favicon = "favicon.png"  # Устанавливаем иконку страницы
    page.fonts = {"default": "Roboto"}  # Устанавливаем шрифт по умолчанию


    news_list = [
        {"title": "KIVI UA запускает новую линейку телевизоров", "content": "Компания KIVI UA анонсировала новую линейку телевизоров с поддержкой 4K и HDR. Подробнее можно узнать на [официальном сайте](https://www.kivi.ua).", "icon": ft.Icons.TV, "date": "1 марта 2025"},
        {"title": "KIVI UA открывает новый шоурум", "content": "Компания KIVI UA открывает новый шоурум в центре Киева. Адрес шоурума можно найти [здесь](https://www.kivi.ua/showroom).", "icon": ft.Icons.STORE, "date": "28 февраля 2025"},
        {"title": "KIVI UA объявляет о партнерстве с ведущими производителями", "content": "Компания KIVI UA заключила партнерские соглашения с ведущими производителями электроники. Подробности на [сайте](https://www.kivi.ua/partners).", "icon": ft.Icons.HANDSHAKE, "date": "27 февраля 2025"},
        {"title": "KIVI UA проводит благотворительную акцию", "content": "Компания KIVI UA организует благотворительную акцию по сбору средств для детских домов. Узнать больше можно [здесь](https://www.kivi.ua/charity).", "icon": ft.Icons.VOLUNTEER_ACTIVISM, "date": "26 февраля 2025"},
        {"title": "KIVI UA получила награду за инновации", "content": "Компания KIVI UA была удостоена награды за инновационные разработки в области телевизоров. Подробности на [официальном сайте](https://www.kivi.ua/awards).", "icon": ft.Icons.STAR, "date": "25 февраля 2025"},
        {"title": "KIVI UA запускает программу лояльности", "content": "Компания KIVI UA запускает новую программу лояльности для своих клиентов. Узнать больше можно [здесь](https://www.kivi.ua/loyalty).", "icon": ft.Icons.CARD_GIFTCARD, "date": "24 февраля 2025"},
        {"title": "KIVI UA расширяет ассортимент продукции", "content": "Компания KIVI UA расширяет ассортимент своей продукции, добавляя новые модели телевизоров. Подробности на [сайте](https://www.kivi.ua/products).", "icon": ft.Icons.SHOPPING_CART, "date": "23 февраля 2025"},
        {"title": "KIVI UA проводит вебинар по новым технологиям", "content": "Компания KIVI UA организует вебинар, посвященный новым технологиям в телевизорах. Регистрация доступна [здесь](https://www.kivi.ua/webinar).", "icon": ft.Icons.WEB, "date": "22 февраля 2025"},
        {"title": "KIVI UA объявляет о скидках на продукцию", "content": "Компания KIVI UA объявляет о сезонных скидках на свою продукцию. Подробности на [официальном сайте](https://www.kivi.ua/discounts).", "icon": ft.Icons.LOCAL_OFFER, "date": "21 февраля 2025"},
        {"title": "KIVI UA открывает новые вакансии", "content": "Компания KIVI UA объявляет об открытии новых вакансий. Узнать больше можно [здесь](https://www.kivi.ua/careers).", "icon": ft.Icons.WORK, "date": "20 февраля 2025"},
    ]

    def news_feed_view(page, title, content, icon, date):
        container = ft.Container(
            padding=ft.Padding(10, 10, 10, 10),
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            gradient=ft.LinearGradient(
                colors=[ft.Colors.BLUE_200, ft.Colors.BLUE_400],
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
            ),
            # image=ft.DecorationImage(
            # src="news_background.jpg", 
            # fit=ft.ImageFit.COVER, 
            # color_filter=ft.ColorFilter(
            #     blend_mode=ft.BlendMode.COLOR,
            #     color=ft.Colors.BLUE_200
            # )
            # ),  # Добавляем фоновое изображение
            content=ft.Column(
            controls=[
                ft.Row(
                controls=[
                    ft.Icon(icon, size=40, color=ft.Colors.WHITE),
                    ft.Column(
                    controls=[
                        ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, italic=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, expand=True),
                        ft.Text(date, size=12, color=ft.Colors.GREY_300),
                    ],
                    expand=True
                    ),
                ],
                expand=True
                ),
                ft.Markdown(content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
            ],
            expand=True
            ),
            margin=ft.Margin(10, 10, 10, 10),
            animate=ft.Animation(duration=350, curve="decelerate"),
        )

        return container

    def home_page():

        def search_news(e):
            query = e.control.value.lower()
            filtered_news = [news for news in news_list if query in news["title"].lower() or query in news["content"].lower()]
            news_list_view.controls = [news_feed_view(page, news["title"], news["content"], news["icon"], news["date"]) for news in filtered_news]
            news_list_view.update()

        search_input = ft.TextField(
            label="Поиск новостей",
            on_change=search_news,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            border_color=ft.ThemeMode.SYSTEM,
            filled=True,
            fill_color=ft.Colors.with_opacity(0.1, ft.ThemeMode.SYSTEM),
            label_style=ft.TextStyle(color=ft.Colors.BLUE_300),
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            prefix_icon=ft.Icon(ft.Icons.SEARCH, color=ft.ThemeMode.SYSTEM),
        )

        news_controls = [news_feed_view(page, news["title"], news["content"], news["icon"], news["date"]) for news in news_list]

        news_list_view = ft.ListView(
            height=page.height,  # Set the height of the ListView
            controls=news_controls + [ft.Container(height=200)],  # Add spacing at the end
            on_scroll=True,
        )

        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.Animation(duration=250, curve="decelerate"),
            # image=ft.DecorationImage(src="news_background.jpg", fit=ft.ImageFit.COVER),
            # border_radius=ft.BorderRadius(10, 10, 10, 10),
            content=ft.Column(
                controls=[
                    search_input,
                    news_list_view,
                    
                ]
            )
        )

    def search_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.Animation(duration=250, curve="decelerate"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=[
                    ft.Text("Search Page", size=24, weight=ft.FontWeight.BOLD)
                ],  # Add spacing at the end
                on_scroll=True,
            )
        )

    def notifications_page():
        return ft.Container(
            height=0,  # Начальная высота 0
            animate=ft.Animation(duration=250, curve="decelerate"),
            content=ft.ListView(
                height=page.height,  # Set the height of the ListView
                controls=[
                    ft.Text("Notifications Page", size=24, weight=ft.FontWeight.BOLD)
                ],  # Add spacing at the end
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
        bgcolor=ft.Colors.with_opacity(1, ft.ThemeMode.SYSTEM ),
    )

    bottom_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(ft.Icons.HOME, size=30, color=ft.Colors.BLUE_300),
                label="Home"
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(ft.Icons.SEARCH, size=30, color=ft.Colors.BLUE_300),
                label="Search"
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(ft.Icons.NOTIFICATIONS, size=30, color=ft.Colors.BLUE_300),
                label="Notifications"
            ),
        ],
        bgcolor=ft.Colors.with_opacity(1, ft.ThemeMode.SYSTEM ),
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

    # ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)