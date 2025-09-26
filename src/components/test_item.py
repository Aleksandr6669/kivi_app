import flet as ft

def create_test_item(test, on_click=None):
    """
    Допоміжна функція для створення картки тесту або навчального матеріалу.
    """
    status_map = {
        "passed": {"icon": ft.Icons.CHECK_CIRCLE, "color": ft.Colors.GREEN, "text": "Пройдено"},
        "failed": {"icon": ft.Icons.CANCEL, "color": ft.Colors.RED, "text": "Не пройдено"},
        "learned": {"icon": ft.Icons.CHECK_CIRCLE, "color": ft.Colors.GREEN, "text": "Вивчено"},
        "not_learned": {"icon": ft.Icons.PENDING, "color": ft.Colors.AMBER, "text": "Не вивчено"},
        "assigned": {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"},
    }

    type_map = {
        "material": {"icon": ft.Icons.MENU_BOOK_OUTLINED, "tooltip": "Матеріал"},
        "test": {"icon": ft.Icons.RULE_OUTLINED, "tooltip": "Тестування"}
    }



    current_status = status_map.get(test.get("status"), {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"})
    type_info = type_map.get(test.get("item_type"), {})

    # ИЗМЕНЕНИЕ 2: Собираем spans для одного Text виджета
    trailing_spans = []
    
    trailing_controls = []
    if type_info:
        trailing_controls.append(ft.Icon(name=type_info.get("icon"), tooltip=type_info.get("tooltip"), color=ft.Colors.BLUE_GREY_400))
    # score = test.get("score")
    percentage_score = test.get("percentage_score")
    if percentage_score is not None:
        percentage_score = int(percentage_score)
    else:
        percentage_score = 0  # Або будь-яке інше значення за замовчуванням
    # if score:
    #     trailing_controls.append(ft.Text(score, weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_GREY_400))
    if percentage_score:
        trailing_controls.append(ft.Text(f"{percentage_score}%", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_GREY_400))

    status_text = f"Статус: {current_status['text']}"

    
    if test.get('item_type') == 'test':
   
        attempts_used = test.get('attempts_used', 0)
        total_attempts = test.get('total_attempts', 0)
        status_text += f" {attempts_used}/{total_attempts}"
    
    return ft.Card(
        elevation=3,
        margin=3,
        content=ft.Container( # Контейнер для отступов и обработки нажатий
            on_click=on_click,
            data=test,
            padding=ft.padding.symmetric(vertical=5, horizontal=10),
            border_radius=ft.border_radius.all(8),
            content=ft.Row( # Главная строка, которая имитирует ListTile
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # 1. Левый элемент (leading)
                    ft.Icon(current_status["icon"], color=current_status["color"], size=28),

                    # 2. Центральная колонка (title + subtitle)
                    # expand=True заставляет эту колонку занять всё доступное место
                    ft.Column(
                        [
                            ft.Text(
                                value=test.get("title", "Без назви"),
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                weight=ft.FontWeight.W_500,
                                size=15
                            ),
                            ft.Text(
                               status_text,
                                color=ft.Colors.BLUE_GREY_400,
                                size=12
                            ),
                        ],
                        spacing=2,
                        expand=True, # <--- ЭТО КЛЮЧЕВОЕ СВОЙСТВО
                    ),

                    # 3. Правый элемент (trailing)
                    ft.Row(
                        controls=trailing_controls,
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                ],
            ),
        ),
    )


