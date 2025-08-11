import flet as ft
import asyncio

def main(page: ft.Page):
    """
    Головна функція програми KIVI Retail.
    """
    page.title = "Vika AI"
    page.version = "0.7"
    page.description = "Vika AI"

    page.assets_dir = "assets"
    page.manifest = "manifest.json"

    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.adaptive = False
    page.language = "ua"
    page.favicon = "favicon.png"
    page.fonts = {"default": "Roboto"}
    page.padding = 0

    # Загальні дані
    tests_data = [
        {"title": "Знання продукту KIVI TV", "status": "passed", "score": "10/10"},
        {"title": "Техніки продажів", "status": "failed", "score": "4/10"},
        {"title": "Стандарти мерчендайзингу", "status": "assigned"},
        {"title": "Нова лінійка саундбарів", "status": "assigned"},
        {"title": "Робота із запереченнями", "status": "passed", "score": "8/10"},
        {"title": "Ще один тест", "status": "assigned"},
        {"title": "І ще один", "status": "assigned"},
        {"title": "Останній тест", "status": "failed", "score": "2/10"},
        {"title": "Новий пройдений тест 1", "status": "passed", "score": "9/10"},
        {"title": "Новий пройдений тест 2", "status": "passed", "score": "10/10"},
        {"title": "Новий пройдений тест 3", "status": "passed", "score": "7/10"},
        {"title": "Новий пройдений тест 4", "status": "passed", "score": "8/10"},
        {"title": "Новий пройдений тест 5", "status": "passed", "score": "10/10"},
        {"title": "Новий пройдений тест 6", "status": "passed", "score": "9/10"},
        {"title": "Новий пройдений тест 7", "status": "passed", "score": "10/10"},
        {"title": "Новий пройдений тест 8", "status": "passed", "score": "7/10"},
        {"title": "Новий пройдений тест 9", "status": "passed", "score": "8/10"},
        {"title": "Новий пройдений тест 10", "status": "passed", "score": "10/10"},
        {"title": "Новий не пройдений тест 1", "status": "failed", "score": "3/10"},
        {"title": "Новий не пройдений тест 2", "status": "failed", "score": "4/10"},
        {"title": "Новий не пройдений тест 3", "status": "failed", "score": "1/10"},
        {"title": "Новий не пройдений тест 4", "status": "failed", "score": "2/10"},
        # Додано 15 нових навчальних матеріалів для демонстрації прокручування та пошуку
        {"title": "Основи електроніки KIVI", "status": "assigned", "material_status": "learned"},
        {"title": "Маркетингові акції на вересень", "status": "assigned", "material_status": "not_learned"},
        {"title": "Як працювати з CRM-системою", "status": "assigned", "material_status": "learned"},
        {"title": "Просунуті техніки продажів", "status": "assigned", "material_status": "not_learned"},
        {"title": "Презентація нових моделей", "status": "assigned", "material_status": "learned"},
        {"title": "Правила оформлення вітрин", "status": "assigned", "material_status": "not_learned"},
        {"title": "Майстер-клас зі спілкування", "status": "assigned", "material_status": "learned"},
        {"title": "Технічні характеристики ТВ KIVI", "status": "assigned", "material_status": "not_learned"},
        {"title": "Як боротися із запереченнями клієнтів", "status": "assigned", "material_status": "learned"},
        {"title": "Порівняння з конкурентами", "status": "assigned", "material_status": "not_learned"},
        {"title": "Інструкція з налаштування", "status": "assigned", "material_status": "learned"},
        {"title": "Новинки аудіо-техніки KIVI", "status": "assigned", "material_status": "not_learned"},
        {"title": "Історія компанії KIVI", "status": "assigned", "material_status": "learned"},
        {"title": "Особливості виробництва", "status": "assigned", "material_status": "not_learned"},
        {"title": "Секрети успішних продажів", "status": "passed", "score": "10/10"},
    ]

    # Створення Ref-об'єктів для кожної сторінки
    home_view_ref = ft.Ref[ft.Container]()
    search_view_ref = ft.Ref[ft.Container]()
    progress_view_ref = ft.Ref[ft.Container]()
    history_view_ref = ft.Ref[ft.Container]()
    profile_view_ref = ft.Ref[ft.Container]()
    bottom_navigation_bar_ref = ft.Ref[ft.NavigationBar]()

    def create_test_item(test):
        """
        Допоміжна функція для створення картки тесту або навчального матеріалу.
        """
        status_map = {
            "passed": {"icon": ft.Icons.CHECK_CIRCLE, "color": ft.Colors.GREEN, "text": "Пройдено"},
            "failed": {"icon": ft.Icons.CANCEL, "color": ft.Colors.RED, "text": "Не пройдено"},
            "assigned": {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"},
        }

        # Логіка для визначення статусу навчального матеріалу
        if "score" not in test and "material_status" in test:
            material_status = test.get("material_status", "not_learned")
            if material_status == "learned":
                icon = ft.Icons.CHECK_CIRCLE
                color = ft.Colors.GREEN
                text = "Вивчено"
            else:
                icon = ft.Icons.PENDING
                color = ft.Colors.AMBER
                text = "Не вивчено"
            
            return ft.Card(
                elevation=2,
                content=ft.ListTile(
                    leading=ft.Icon(icon, color=color),
                    title=ft.Text(test["title"]),
                    subtitle=ft.Text(f"Статус: {text}"),
                    trailing=ft.Text("", weight=ft.FontWeight.BOLD),
                )
            )

        # Логіка для тестів
        else:
            current_status = status_map.get(test.get("status"), {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"})
            return ft.Card(
                elevation=2,
                content=ft.ListTile(
                    leading=ft.Icon(current_status["icon"], color=current_status["color"]),
                    title=ft.Text(test["title"]),
                    subtitle=ft.Text(f"Статус: {current_status['text']}"),
                    trailing=ft.Text(test.get("score", ""), weight=ft.FontWeight.BOLD),
                )
            )

    def create_progress_bar(title, value, total, color):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(f"{title}"),
                        ft.Text(f"{value}/{total}")
                    ]
                ),
                ft.ProgressBar(value=value/total if total > 0 else 0, color=color, bgcolor=ft.Colors.with_opacity(0.2, color)),
            ]
        )


    def home_page(ref, nav_bar_ref):
        """
        Створює головну сторінку.
        """
        user_info = {"name": "Олександр Риженков", "role": "Промоутер"}

        passed_count = len([t for t in tests_data if t["status"] == "passed"])
        failed_count = len([t for t in tests_data if t["status"] == "failed"])
        assigned_count = len([t for t in tests_data if t["status"] == "assigned"])
        total_tests = len(tests_data)

        user_card = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_GREY_800,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("Вітаємо,", size=16, color=ft.Colors.WHITE70),
                            ft.Text(user_info["name"], size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(user_info["role"], size=16, color=ft.Colors.WHITE70),
                        ]),
                        ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.BLUE_200)
                    ]
                )
            )
        )

        assigned_button_with_badge = ft.Stack(
            [
                ft.ElevatedButton("Призначені", icon=ft.Icons.ASSIGNMENT, width=150),
                ft.Container(
                    content=ft.Text(
                        value=str(assigned_count),
                        size=12,
                        color="white",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=20,
                    height=20,
                    bgcolor="red",
                    shape=ft.BoxShape.CIRCLE,
                    right=0,
                    top=0,
                    visible=assigned_count > 0,
                ),
            ]
        )

        quick_links = ft.Row(
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.ElevatedButton("Навчання", icon=ft.Icons.SCHOOL, width=150),
                ft.ElevatedButton("Всі тести", icon=ft.Icons.QUIZ, width=150),
                assigned_button_with_badge,
            ]
        )

        progress_bars = ft.Column(
            spacing=10,
            controls=[
                create_progress_bar("Пройдено", passed_count, total_tests, ft.Colors.GREEN),
                create_progress_bar("Не пройдено", failed_count, total_tests, ft.Colors.RED),
                create_progress_bar("Призначено", assigned_count, total_tests, ft.Colors.BLUE),
            ]
        )

        chart_container = ft.Card(
            elevation=4,
            content=ft.Container(
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.BLUE_GREY_800,
                content=ft.Column([
                    ft.Text("Прогрес Тестів", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    progress_bars,
                    ft.Container(height=10),
                    ft.Text(f"Усього тестів: {total_tests}", text_align=ft.TextAlign.RIGHT, color=ft.Colors.WHITE70)
                ])
            )
        )

        visible_tests_count = ft.Ref[int]()
        visible_tests_count.current = 2

        filtered_tests = ft.Ref[list]()

        test_list_view = ft.Column(
            spacing=10
        )

        show_all_button = ft.TextButton(
            "Показати все",
        )

        def go_to_history(e):
            nav_bar_ref.current.selected_index = 3
            on_nav_change(ft.ControlEvent(target=nav_bar_ref.current, name='change', data='3', control=nav_bar_ref.current, page=page))

        def go_to_progress(e):
            nav_bar_ref.current.selected_index = 2
            on_nav_change(ft.ControlEvent(target=nav_bar_ref.current, name='change', data='2', control=nav_bar_ref.current, page=page))

        def update_test_list(status_filter="passed"):
            nonlocal show_all_button
           
            filtered_tests.current = [t for t in tests_data if t["status"] == status_filter]

            visible_tests_count.current = 2

            test_list_view.controls = [
                create_test_item(t) for t in filtered_tests.current[:visible_tests_count.current]
            ]

            if status_filter in ["passed", "failed"]:
                show_all_button.on_click = go_to_history
            elif status_filter == "assigned":
                show_all_button.on_click = go_to_progress
            else:
                show_all_button.on_click = None

            show_all_button.visible = len(filtered_tests.current) > 2
            page.update()

        def filter_button_clicked(e):
            status_map = {
                "Пройдені": "passed",
                "Не пройдені": "failed",
                "Призначені": "assigned",
            }
            update_test_list(status_filter=status_map[e.control.text])

        filter_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.ElevatedButton("Пройдені", on_click=filter_button_clicked, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                ft.ElevatedButton("Не пройдені", on_click=filter_button_clicked, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
                ft.ElevatedButton("Призначені", on_click=filter_button_clicked, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))),
            ]
        )

        update_test_list()

        return ft.Container(
            ref=ref,
            expand=True,
            visible=False,
            padding=ft.padding.only(left=15, right=15, top=15),
            content=ft.Column(
                spacing=15,
                controls=[
                    user_card,
                    quick_links,
                    chart_container,
                    filter_buttons,
                    test_list_view,
                    show_all_button,
                ]
            )
        )

    def search_page(ref):
        """
        Сторінка пошуку з полем для введення та списком навчального матеріалу.
        """
        # Фільтруємо всі тести, щоб залишити лише навчальний матеріал (без оцінки)
        educational_materials = [t for t in tests_data if "score" not in t]
        
        # Створюємо Ref для списку, щоб оновлювати його після пошуку
        search_list_view = ft.Ref[ft.Column]()

        def filter_materials(e):
            query = e.control.value.lower()
            filtered_list = [
                create_test_item(t) for t in educational_materials 
                if query in t["title"].lower()
            ]
            search_list_view.current.controls = filtered_list
            page.update()

        return ft.Container(
            ref=ref,
            visible=False,
            expand=True,
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("Навчальний матеріал", size=24, weight=ft.FontWeight.BOLD),
                    ft.TextField(
                        hint_text="Пошук...",
                        prefix_icon=ft.Icons.SEARCH,
                        on_change=filter_materials
                    ),
                    ft.Column(
                        ref=search_list_view,
                        spacing=10,
                        controls=[create_test_item(t) for t in educational_materials],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True
                    )
                ]
            )
        )

    def progress_page(ref):
        """
        Сторінка прогресу з графіком та списком призначених тестів.
        """
        assigned_items = [t for t in tests_data if t.get("status") == "assigned"]
        
        passed_count = len([t for t in tests_data if t["status"] == "passed"])
        failed_count = len([t for t in tests_data if t["status"] == "failed"])
        assigned_count = len([t for t in tests_data if t["status"] == "assigned"])
        total_tests = len(tests_data)

        return ft.Container(
            ref=ref,
            visible=False,
            expand=True,
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Прогрес", size=24, weight=ft.FontWeight.BOLD),
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Column([
                                ft.Text("Прогрес Тестів", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                create_progress_bar("Пройдено", passed_count, total_tests, ft.Colors.GREEN),
                                create_progress_bar("Не пройдено", failed_count, total_tests, ft.Colors.RED),
                                create_progress_bar("Призначено", assigned_count, total_tests, ft.Colors.BLUE),
                                ft.Container(height=10),
                                ft.Text(f"Усього тестів: {total_tests}", text_align=ft.TextAlign.RIGHT, color=ft.Colors.WHITE70)
                            ])
                        )
                    ),
                    ft.Text("Призначені завдання та навчання", size=18, weight=ft.FontWeight.BOLD),
                    ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=[create_test_item(t) for t in assigned_items],
                    )
                ]
            )
        )

    def history_page(ref):
        completed_tests = [t for t in tests_data if t["status"] in ["passed", "failed"]]

        return ft.Container(
            ref=ref,
            visible=False,
            expand=True,
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text("Історія Тестів", size=24, weight=ft.FontWeight.BOLD),
                    ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=[create_test_item(t) for t in completed_tests],
                    )
                ]
            )
        )

    def profile_page(ref):
        """
        Сторінка профілю з інформацією про користувача.
        """
        user_info = {
            "name": "Олександр Риженков",
            "role": "Промоутер",
            "phone": "+380 66 017 5627",
            "email": "oleksandr.ryzhenkov@example.com",
            "about": "Креативний та відповідальний промоутер з досвідом роботи в роздрібній торгівлі."
        }

        return ft.Container(
            ref=ref,
            visible=False,
            expand=True,
            padding=ft.padding.all(15),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Профіль", size=24, weight=ft.FontWeight.BOLD),
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=50, color=ft.Colors.BLUE_200),
                                    ft.Column([
                                        ft.Text(user_info["name"], size=22, weight=ft.FontWeight.BOLD),
                                        ft.Text(user_info["role"], size=16, color=ft.Colors.WHITE70),
                                    ])
                                ], alignment=ft.MainAxisAlignment.START),
                                ft.Divider(height=20, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                                ft.Text("Контактна інформація", size=18, weight=ft.FontWeight.BOLD),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.PHONE),
                                    title=ft.Text(user_info["phone"]),
                                    subtitle=ft.Text("Телефон")
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.EMAIL),
                                    title=ft.Text(user_info["email"]),
                                    subtitle=ft.Text("Електронна пошта")
                                ),
                                ft.Divider(height=20, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                                ft.Text("Про себе", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(user_info["about"]),
                            ])
                        )
                    )
                ]
            )
        )

    def on_nav_change(e):
        selected_index = e.control.selected_index
        views = [
            home_view_ref.current,
            search_view_ref.current,
            progress_view_ref.current,
            history_view_ref.current,
            profile_view_ref.current,
        ]

        for i, view in enumerate(views):
            if view:
                view.visible = (i == selected_index)
        page.update()

    top_appbar = ft.AppBar(
        title=ft.Text(
            "Школа",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREY_400
        ),
        actions=[
            ft.IconButton(
                ft.Icons.INFO,
                style=ft.ButtonStyle(padding=0)
            )
        ],
        bgcolor=ft.Colors.with_opacity(1, ft.ThemeMode.SYSTEM),
    )

    bottom_navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.INDIGO_700,
                icon=ft.Icon(ft.Icons.HOME, size=30, color=ft.Colors.INDIGO_200),
                label="Головна",
                adaptive=True
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.INDIGO_700,
                icon=ft.Icon(ft.Icons.SEARCH, size=30, color=ft.Colors.INDIGO_200),
                label="Пошук",
                adaptive=True
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.INDIGO_700,
                icon=ft.Icon(ft.Icons.GRAPHIC_EQ, size=30, color=ft.Colors.INDIGO_200),
                label="Прогрес",
                adaptive=True
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.INDIGO_700,
                icon=ft.Icon(ft.Icons.HISTORY, size=30, color=ft.Colors.INDIGO_200),
                label="Історія",
                adaptive=True
            ),
            ft.NavigationBarDestination(
                bgcolor=ft.Colors.INDIGO_700,
                icon=ft.Icon(ft.Icons.PERSON, size=30, color=ft.Colors.INDIGO_200),
                label="Профіль",
                adaptive=True
            ),
        ],
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        on_change=on_nav_change,
        selected_index=0,
        ref=bottom_navigation_bar_ref
    )

    page.add(top_appbar)

    main_content_area = ft.Column(expand=True, controls=[
        home_page(home_view_ref, bottom_navigation_bar_ref),
        search_page(search_view_ref),
        progress_page(progress_view_ref),
        history_page(history_view_ref),
        profile_page(profile_view_ref)
    ])
    page.add(main_content_area)
    page.add(bottom_navigation_bar)

    # Встановлення початкової сторінки
    home_view_ref.current.visible = True
    page.update()


if __name__ == "__main__":
    ft.app(main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=9002
     )