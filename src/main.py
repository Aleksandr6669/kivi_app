import flet as ft
import asyncio

def main(page: ft.Page):
    """
    Главная функция приложения KIVI Retail.
    
    Инициализирует и настраивает основной интерфейс приложения, включая:
    - Настройки страницы и PWA
    - Ленту новостей
    - Навигационную панель
    - Поиск по новостям
    
    Args:
        page (ft.Page): Основной объект страницы Flet
    """
    page.title = "Kivi Retail TEST"
    page.version = "0.7"
    page.description = "Kivi Retail TEST"
    
    # Настройки PWA (Progressive Web Application)
    page.assets_dir = "assets"
    page.manifest = "manifest.json" 
    
    # Настройки интерфейса
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.adaptive = False  # Отключаем адаптивный дизайн
    page.language = "ua"
    page.favicon = "favicon.png"
    page.fonts = {"default": "Roboto"}

    # Список новостей компании
    news_list = [
        {"title": "KIVI UA запускає нову лінійку телевізорів", "content": "Компанія KIVI UA анонсувала нову лінійку телевізорів з підтримкою 4K та HDR. Детальніше можна дізнатися на [офіційному сайті](https://www.kivi.ua).", "icon": ft.Icons.TV, "date": "1 березня 2025"},
        {"title": "KIVI UA відкриває новий шоурум", "content": "Компанія KIVI UA відкриває новий шоурум у центрі Києва. Адресу шоуруму можна знайти [тут](https://www.kivi.ua/showroom).", "icon": ft.Icons.STORE, "date": "28 лютого 2025"},
        {"title": "KIVI UA оголошує про партнерство з провідними виробниками", "content": "Компанія KIVI UA уклала партнерські угоди з провідними виробниками електроніки. Подробиці на [сайті](https://www.kivi.ua/partners).", "icon": ft.Icons.HANDSHAKE, "date": "27 лютого 2025"},
        {"title": "KIVI UA проводить благодійну акцію", "content": "Компанія KIVI UA організовує благодійну акцію зі збору коштів для дитячих будинків. Дізнатися більше можна [тут](https://www.kivi.ua/charity).", "icon": ft.Icons.VOLUNTEER_ACTIVISM, "date": "26 лютого 2025"},
        {"title": "KIVI UA отримала нагороду за інновації", "content": "Компанія KIVI UA була удостоєна нагороди за інноваційні розробки в галузі телевізорів. Подробиці на [офіційному сайті](https://www.kivi.ua/awards).", "icon": ft.Icons.STAR, "date": "25 лютого 2025"},
        {"title": "KIVI UA запускає програму лояльності", "content": "Компанія KIVI UA запускає нову програму лояльності для своїх клієнтів. Дізнатися більше можна [тут](https://www.kivi.ua/loyalty).", "icon": ft.Icons.CARD_GIFTCARD, "date": "24 лютого 2025"},
        {"title": "KIVI UA розширює асортимент продукції", "content": "Компанія KIVI UA розширює асортимент своєї продукції, додаючи нові моделі телевізорів. Подробиці на [сайті](https://www.kivi.ua/products).", "icon": ft.Icons.SHOPPING_CART, "date": "23 лютого 2025"},
        {"title": "KIVI UA проводить вебінар з нових технологій", "content": "Компанія KIVI UA організовує вебінар, присвячений новим технологіям у телевізорах. Реєстрація доступна [тут](https://www.kivi.ua/webinar).", "icon": ft.Icons.WEB, "date": "22 лютого 2025"},
        {"title": "KIVI UA оголошує про знижки на продукцію", "content": "Компанія KIVI UA оголошує про сезонні знижки на свою продукцію. Подробиці на [офіційному сайті](https://www.kivi.ua/discounts).", "icon": ft.Icons.LOCAL_OFFER, "date": "21 лютого 2025"},
        {"title": "KIVI UA відкриває нові вакансії", "content": "Компанія KIVI UA оголошує про відкриття нових вакансій. **Дізнатися більше можна** [тут](https://www.kivi.ua/careers).", "icon": ft.Icons.WORK, "date": "20 лютого 2025"},
    ]

    def news_feed_view(page, title, content, icon, date):
        """
        Создает карточку новости с заданным оформлением.
        
        Args:
            page: Объект страницы
            title (str): Заголовок новости
            content (str): Содержание новости в формате Markdown
            icon (ft.Icon): Иконка для новости
            date (str): Дата публикации
            
        Returns:
            ft.Container: Контейнер с оформленной новостью
        """
        container = ft.Container(
            padding=ft.Padding(10, 10, 10, 10),
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            # gradient=ft.LinearGradient(
            #     colors=[ft.Colors.BLUE_200, ft.Colors.BLUE_400],
            #     begin=ft.alignment.top_left,
            #     end=ft.alignment.bottom_right,
            # ),

            image=ft.DecorationImage(
            src="news_background.jpg", 
            fit=ft.ImageFit.COVER, 
            # color_filter=ft.ColorFilter(
            #     blend_mode=ft.BlendMode.COLOR,
            #     color=ft.Colors.BLUE_200
            # )
            ),  # Добавляем фоновое изображение
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
                ft.Container(
                    padding=ft.Padding(10, 10, 10, 10),
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    blur=ft.Blur(sigma_x=20, sigma_y=30, tile_mode=ft.BlurTileMode.CLAMP),
                    content=ft.Markdown(content, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB),
                    ),
                
            ],
            expand=True
            ),
            margin=ft.Margin(10, 10, 10, 10),
            animate=ft.Animation(duration=350, curve="decelerate"),
        )

        return container

    def home_page():
        """
        Создает главную страницу приложения с лентой новостей и поиском.
        
        Returns:
            ft.Container: Контейнер с содержимым главной страницы
        """
        def search_news(e):
            """
            Обработчик поиска по новостям.
            
            Фильтрует новости по введенному тексту в поисковой строке.
            
            Args:
                e: Событие изменения текста в поле поиска
            """
            query = e.control.value.lower()
            filtered_news = [
                news for news in news_list 
                if query in news["title"].lower() or 
                   query in news["content"].lower()
            ]
            news_list_view.controls = [
                news_feed_view(
                    page, 
                    news["title"], 
                    news["content"], 
                    news["icon"], 
                    news["date"]
                ) for news in filtered_news
            ]
            news_list_view.update()

        # Создание поля поиска
        search_input = ft.TextField(
            label="Пошук новин",
            on_change=search_news,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            border_color=ft.ThemeMode.SYSTEM,
            filled=True,
            fill_color=ft.Colors.with_opacity(0.1, ft.ThemeMode.SYSTEM),
            label_style=ft.TextStyle(color=ft.Colors.BLUE_300),
            text_style=ft.TextStyle(color=ft.Colors.WHITE),
            prefix_icon=ft.Icon(ft.Icons.SEARCH, color=ft.ThemeMode.SYSTEM),
        )
        

        # Создание списка новостей
        news_controls = [
            news_feed_view(
                page, 
                news["title"], 
                news["content"], 
                news["icon"], 
                news["date"]
            ) for news in news_list
        ]

        news_list_view = ft.ListView(
            height=page.height,
            controls=news_controls + [ft.Container(height=250)]
        )

        return ft.Container(
            height=0,
            animate=ft.Animation(duration=250, curve="decelerate"),
            content=ft.Column(
                controls=[
                    search_input,
                    news_list_view,
                ]
            )
        )



    def details_page():
        """
        Создает страницу деталей с информацией о продуктах и сервисах.
        
        Returns:
            ft.Container: Контейнер страницы деталей
        """
        # Список продуктов и сервисов
        details_list = [
            {
                "title": "Телевізори KIVI",
                "description": "Сучасні Smart TV з підтримкою 4K HDR",
                "icon": ft.Icons.TV,
                "specs": [
                    "Діагональ: від 32\" до 65\"",
                    "Роздільна здатність: до 4K UHD",
                    "Smart TV на базі Android TV",
                    "Підтримка HDR10+"
                ]
            },
            {
                "title": "Сервісні центри",
                "description": "Мережа авторизованих сервісних центрів",
                "icon": ft.Icons.SUPPORT_AGENT,
                "specs": [
                    "Гарантійне обслуговування",
                    "Післягарантійний ремонт",
                    "Консультації спеціалістів",
                    "Оригінальні запчастини"
                ]
            },
            {
                "title": "Програма лояльності",
                "description": "Спеціальні пропозиції для клієнтів",
                "icon": ft.Icons.CARD_GIFTCARD,
                "specs": [
                    "Бонусна програма",
                    "Спеціальні знижки",
                    "Подарунки до покупок",
                    "Ексклюзивні пропозиції"
                ]
            }
        ]

        def create_detail_card(detail):
            """
            Создает карточку с детальной информацией о продукте или сервисе.
            """
            return ft.Container(
                padding=ft.padding.all(20),
                margin=ft.margin.all(10),
                border_radius=ft.border_radius.all(15),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.colors.BLUE_400, ft.colors.BLUE_900],
                ),
                content=ft.Column([
                    ft.Row([
                        ft.Icon(detail["icon"], size=40, color=ft.colors.WHITE),
                        ft.Text(
                            detail["title"],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE
                        )
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Container(height=10),
                    ft.Text(
                        detail["description"],
                        size=16,
                        color=ft.colors.WHITE70
                    ),
                    ft.Container(height=20),
                    ft.Column([
                        ft.Container(
                            padding=ft.padding.all(10),
                            margin=ft.margin.symmetric(vertical=5),
                            border_radius=ft.border_radius.all(10),
                            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                            content=ft.Text(
                                spec,
                                color=ft.colors.WHITE,
                                size=14
                            )
                        ) for spec in detail["specs"]
                    ])
                ])
            )

        return ft.Container(
            height=0,
            animate=ft.Animation(duration=250, curve="decelerate"),
            content=ft.ListView(
                height=page.height,
                controls=[
                    create_detail_card(detail) 
                    for detail in details_list
                ] + [ft.Container(height=200)]
            )
        )

    def workspace_page():
        """
        Создает рабочее пространство с инструментами и статистикой.
        
        Returns:
            ft.Container: Контейнер рабочего пространства
        """
        # Данные для графиков и статистики
        stats = {
            "daily_sales": 157,
            "monthly_growth": "+12.5%",
            "active_users": 1250,
            "support_tickets": 23
        }

        def create_stat_card(title, value, icon, color):
            """
            Создает карточку со статистикой.
            """
            return ft.Container(
                width=160,
                height=160,
                padding=ft.padding.all(10),
                margin=ft.margin.all(10),
                border_radius=ft.border_radius.all(10),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    colors=[color, ft.colors.with_opacity(0.7, color)]
                ),
                content=ft.Column([
                    ft.Icon(icon, size=40, color=ft.colors.WHITE),
                    ft.Container(height=5),
                    ft.Text(
                        title,
                        size=14,
                        color=ft.colors.WHITE70,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        str(value),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            )

        # Создание панели быстрых действий
        quick_actions = ft.Row([
            ft.ElevatedButton(
                "Звіт залишків",
                icon=ft.icons.ADD_SHOPPING_CART,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE_500
                )
            ),
            ft.ElevatedButton(
                "Звіт продажів",
                icon=ft.icons.ASSESSMENT,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN_500
                )
            ),
            ft.ElevatedButton(
                "Тижневий звіт",
                icon=ft.icons.HELP_OUTLINE,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.ORANGE_500
                )
            )
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        # Создание сетки статистики
        stats_grid = ft.Row([
            create_stat_card(
                "Звіт продажів",
                stats["daily_sales"],
                ft.icons.TRENDING_UP,
                ft.colors.BLUE_500
            ),
            create_stat_card(
                "Місячне зростання",
                stats["monthly_growth"],
                ft.icons.INSERT_CHART,
                ft.colors.GREEN_500
            ),
            create_stat_card(
                "Активні користувачі",
                stats["active_users"],
                ft.icons.PEOPLE,
                ft.colors.PURPLE_500
            ),
            create_stat_card(
                "Запити підтримки",
                stats["support_tickets"],
                ft.icons.SUPPORT,
                ft.colors.ORANGE_500
            )
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Container(
            height=0,
            animate=ft.Animation(duration=250, curve="decelerate"),
            content=ft.Column([
                ft.Container(
                    content=ft.Row(
                        controls=[quick_actions],
                        scroll=ft.ScrollMode.HIDDEN
                    )
                ),
                ft.Container(height=30),
                ft.Container(
                    height=page.height - 100,
                    content=ft.Column(
                        controls=[stats_grid],
                        scroll=ft.ScrollMode.HIDDEN
                    )
                )
            ])
        )

    async def on_nav_change(e):
        """
        Обработчик переключения между страницами в навигационной панели.
        
        Реализует анимированное переключение между страницами путем
        изменения их высоты.
        
        Args:
            e: Событие изменения выбранной вкладки
        """
        selected_index = e.control.selected_index
        for i, container in enumerate(page.controls[1:4]):
            container.height = page.height if i == selected_index else 0
            container.update()

    # Создание верхней панели приложения
    top_appbar = ft.AppBar(
        title=ft.Text(
            "KIVI Retail DEV",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_600
        ),
        actions=[
            ft.IconButton(
                ft.CupertinoIcons.INFO,
                style=ft.ButtonStyle(padding=0)
            )
        ],
        bgcolor=ft.Colors.with_opacity(1, ft.ThemeMode.SYSTEM),
    )

    # Создание нижней навигационной панели
    bottom_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(
                    ft.Icons.NEWSPAPER,
                    size=30,
                    color=ft.Colors.BLUE_300
                ),
                label="Новини"
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(ft.Icons.DETAILS, size=30, color=ft.Colors.BLUE_300),
                label="Деталі"
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.BLUE_500,
                icon=ft.Icon(ft.Icons.WORK, size=30, color=ft.Colors.BLUE_300),
                label="Робочій простір"
            ),
        ],
        bgcolor=ft.Colors.with_opacity(1, ft.ThemeMode.SYSTEM),
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        on_change=on_nav_change
    )

    # Инициализация интерфейса
    page.add(top_appbar)
    page.add(home_page())
    page.add(details_page())
    page.add(workspace_page())
    page.add(bottom_navigation_bar)

    # Установка начальной страницы
    page.controls[1].height = page.height
    page.controls[1].update()

if __name__ == "__main__":
    """
    Точка входа в приложение.
    Запускает приложение с указанной директорией ассетов.
    """
    ft.app(main, assets_dir="assets")

    # Альтернативный запуск в веб-браузере:
    # ft.app(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)