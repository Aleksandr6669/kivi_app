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
        "material": {"type": "Материал"},
        "test": {"type": "Тестування"}
    }



    current_status = status_map.get(test.get("status"), {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"})
    type_info = type_map.get(test.get("item_type"), {})
    return ft.Card(
        elevation=2,
        content=ft.ListTile(
        leading=ft.Icon(current_status["icon"], color=current_status["color"]),
        title=ft.Text(test["title"]),
        subtitle=ft.Text(f"Статус: {current_status['text']}"),
        trailing=ft.Row(
                controls=[
                    # Сначала тип, например "Тест" или "Матеріал"
                    ft.Text(type_info.get("type", ""), weight=ft.FontWeight.NORMAL),
                    # Затем счёт
                    ft.Text(test.get("score", ""), weight=ft.FontWeight.BOLD),
                ],
                spacing=10  # Добавляем немного отступа между элементами
            ),
        data=test,
        on_click=on_click
        ),
    )


