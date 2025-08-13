import flet as ft

def create_test_item(test):
    """
    Допоміжна функція для створення картки тесту або навчального матеріалу.
    """
    status_map = {
        "passed": {"icon": ft.Icons.CHECK_CIRCLE, "color": ft.Colors.GREEN, "text": "Пройдено"},
        "failed": {"icon": ft.Icons.CANCEL, "color": ft.Colors.RED, "text": "Не пройдено"},
        "assigned": {"icon": ft.Icons.ASSIGNMENT, "color": ft.Colors.BLUE, "text": "Призначено"},
        "learned": {"icon": ft.Icons.CHECK_CIRCLE, "color": ft.Colors.GREEN, "text": "Вивчено"},
        "not_learned": {"icon": ft.Icons.PENDING, "color": ft.Colors.AMBER, "text": "Не вивчено"},
    }



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