import os
from components.database_manager import (
    initialize_database,
    register_user,
    create_or_update_user_profile,
    add_test_data,
    update_assignment,
    get_assigned_tests_for_user,
    add_content_step,
    add_test_question,
    get_test_questions
)

# Определяем путь к базе данных, если он отличается
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_data_full_example.db")

# --- Пример использования ---
if __name__ == '__main__':
    # Удаляем старый файл базы данных для чистоты эксперимента
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Старая база данных удалена.")

    initialize_database()
    
    # 1. Регистрируем администратора и пользователя
    register_user("admin", "admin123", role="admin")
    register_user("sasha", "sasha123")
    
    # 2. Создаем профили
    profile_dict_sasha = {
        "full_name": "Олександр Риженков",
        "phone": "+380 66 017 5627",
        "email": "sasha@example.com",
        "about": "Просто користувач."
    }
    profile_dict_admin = {
        "full_name": "Олександр Риженков",
        "phone": "+380 66 017 5627",
        "email": "sasha@example32423.com",
        "about": "Admin"
    }
    create_or_update_user_profile("sasha", profile_dict_sasha)
    create_or_update_user_profile("admin", profile_dict_admin)

    # Все данные из твоего примера, обновленные для новых полей
    all_content_data = [
        {'user': 'sasha', 'title': 'Лінійка TV 2024', 'status': 'not_learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Історія компанії', 'status': 'not_learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'KIVI KIDS', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Знання продукту KIVI TV', 'status': 'assigned_learned', 'score': None, 'item_type': 'test', 'related_material_title': 'Історія компанії'},
        {'user': 'sasha', 'title': 'Нова лінійка саундбарів та кранштейнів', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Техніки продажів', 'status': 'assigned_learned', 'score': None, 'item_type': 'test', 'related_material_title': 'Лінійка TV 2024'},
        {'user': 'sasha', 'title': 'KIVI Plus', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'KIVI Media', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'admin', 'title': 'Єволюція KIVI', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Єволюція KIVI', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Лінійка TV 2023', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'KIVI Кріплення', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'HDR and colors FIX Додатковий материал для возвитку', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'admin', 'title': 'Інструкція KIDS TV Додатковий материал для возвитку', 'status': 'learned', 'score': None, 'item_type': 'material', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 1', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 2', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 3', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 4', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 5', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'admin', 'title': 'Тест 6', 'status': 'passed', 'score': '10/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 7', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 8', 'status': 'failed', 'score': '5/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'admin', 'title': 'Тест 9', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 10', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 11', 'status': 'failed', 'score': '7/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 12', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 13', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 14', 'status': 'failed', 'score': '3/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 15', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 16', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 17', 'status': 'failed', 'score': '4/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 18', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 19', 'status': 'passed', 'score': '7/7', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 20', 'status': 'passed', 'score': '8/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 21', 'status': 'passed', 'score': '10/10', 'item_type': 'test', 'related_material_title': None},
        {'user': 'sasha', 'title': 'Тест 22', 'status': 'passed', 'score': '9/10', 'item_type': 'test', 'related_material_title': None}
    ]

    print("\n--- Добавление всех уникальных тестов и материалов ---")
    unique_titles = {item['title']: item for item in all_content_data}.values()
    for item in unique_titles:
        add_test_data(item)
        
    print("\n--- Создание и обновление назначений для всех материалов и тестов ---")
    for item in all_content_data:
        passing_score = 90 if item['item_type'] == 'test' else None
        total_attempts = 3 if item['item_type'] == 'test' else None
        
        update_assignment(
            username=item['user'], 
            test_title=item['title'], 
            new_data={
                "status": item['status'], 
                "score": item['score'],
                "passing_score": passing_score,
                "total_attempts": total_attempts
            }
        )

    print("\n--- Проверка: загружаем начальные назначенные материалы для 'sasha' ---")
    sasha_materials = get_assigned_tests_for_user("sasha")
    for mat in sasha_materials:
        print(f"- {mat['title']} (Тип: {mat['item_type']}, Статус: {mat['status']}, Результат: {mat.get('score')})")

    # --- Добавление содержимого для материалов и тестов ---
    material_contents_data = [
        # Історія компанії
        {
            "material_title": "Історія компанії", "step_number": 1, "title": "Про компанію KIVI",
            "content_blocks": [
                {"type": "text", "value": "# **KIVI** - міжнародна компанія, розробник та виробник смарт-телевізорів. Продукція KIVI продається на європейському та азіатському ринках."},
                {"type": "text", "value": "### Телевізори розробляються міжнародною командою KIVI, а виробництво здійснюється на високотехнологічних заводах у Європі та Азії з міжнародною системою контролю якості. Нашим стратегічним партнером є компанія MTC, один із світових лідерів з виробництва телевізорів. У 2020 році ми стали сертифікованим партнером **Google** та **Netflix**, випустили лінійку телевізорів на базі **Google Android TV 9** та отримали нагороду \"Вибір року 2021\" в Україні."},
                {"type": "text", "value": "## Ми впевнені у нашому продукті. Виробництво здійснюється за міжнародною системою контролю якості та на об'єктах найбільшого у світі контрактного виробника - MTC.\n\n### Телевізори KIVI базуються на програмному забезпеченні із США. Ми постійно оновлюємо програмне забезпечення, додаємо нові функції та можливості. Нам важливо бути на одній хвилі із нашими клієнтами. Наш пріоритет – постійне вдосконалення заради наших клієнтів."}
            ]
        },
        {
            "material_title": "Історія компанії", "step_number": 2, "title": "Головне про KIVI",
            "content_blocks": [
                {"type": "text", "value": "## KIVI – компанія українського походження, заснована в 2016 році. Основний бізнес – розробка та виробництво телевізорів. Бренд зареєстрований в Угорщині, Будапешт."},
                {"type": "text", "value": "## Зараз KIVI — міжнародна компанія з дистрибуцією продукції в Європі та Азії. Відділ R&D знаходиться в Україні та Китаї."},
                {"type": "text", "value": "## Виробництво здійснюється на потужностях найбільшого в світі контрактного виробника – **MTC (Шеньчжень, Китай)**. KIVI використовує комплектуючі провідних виробників Китаю, Японії, Тайваню, Південної Кореї. KIVI має міжнародну систему контролю якості."}
            ]
        },
        {
            "material_title": "Історія компанії", "step_number": 3, "title": "Головне про KIVI",
            "content_blocks": [
                {"type": "text", "value": "## KIVI є сертифікованим партнером Google і Netflix. Стратегічні контент- партнери – Netflix, MEGOGO (регіон СНД). Партнер з хмарних ігор — Boosteroid (один із трьох найбільших постачальників хмарних ігор у Європі). Аудіо партнер — JVC Kenwood."},
                {"type": "text", "value": "## На даний момент KIVI є приватною компанією.\n\n\n## Провідні торгові компанії з різних країн вважають KIVI привабливим брендом з високоякісним продуктом і активно просувають продажі телевізорів KIVI через усі канали продажу - онлайн і офлайн."},
                {"type": "text", "value": "## Загалом KIVI виробила понад 1,5 мільйона телевізорів і неухильно рухається до цілі виробництва 1 мільйона телевізорів на рік, що становить приблизно 0,5% світового ринку."}
            ]
        },
        {
            "material_title": "Історія компанії", "step_number": 4, "title": "Історія компанії",
            "content_blocks": [
                {"type": "text", "value": "## 2021 рік\n## Епоха KIVI MEDIA\n## KIVI отримала 13 мільйонів доларів інвестицій від Shenzhen MTC для розробки продукту і в 2021 році компанія випустила нову лінійку телевізорів із вбудованим додатком KIVI MEDIA з безкоштовними телеканалами, фільмами, хмарними іграми та онлайн-тренуваннями. Звук для нових телевізорів був розроблений спільно з JVC Kenwood, а нові пульти дистанційного керування з функцією покажчика були розроблені спільно з Korean Remote Solution. KIVI вийшов на ринки Грузії, Молдови, Вірменії, Азербайджану.\n## - продано близько 412 000 телевізорів\n## - В команді 300 людей"}
            ]
        },
        {
            "material_title": "Історія компанії", "step_number": 5, "title": "Станом на сьогодні...",
            "content_blocks": [
                {"type": "text", "value": "### - Дизайн: тонка мінімалістична металева підставка, тонкі рамки 2,6 мм навколо дисплея (порівняно з конкурентами в сегменті). Білі телевізори – рідкісний варіант серед конкурентів, особливо для великих діагоналей"},
                {"type": "text", "value": "### - Екран: екрани класу А+ від провідних виробників світу. Телевізори KIVI мають високий рівень яскравості в порівнянні з конкурентами. KIVI надає наступні екранні технології: підвищення якості 4K, підтримка HDR з будь-якого джерела, контроль надконтрастності для налаштування контрастності в окремих частинах екрана тощо."},
                {"type": "text", "value": "### - Звук: розроблений у партнерстві з JVC Kenwood (калібровані динаміки, обробка аудіовиведення в реальному часі за допомогою Dolby DAP, SRC – технологія виведення якості звуку без втрат)"},
                {"type": "text", "value": "### - Дистанційне керування вказівником: створено у співпраці з Remote Solutions (Південна Корея). Ергономіка розроблена на основі досліджень KIVI та Google. Відмінна тактильність, чутливий мікрофон, функція вказівника."}
            ]
        },
        # Лінійка TV 2024
        {
            "material_title": "Лінійка TV 2024", "step_number": 1, "title": "Про нас",
            "content_blocks": [
                {"type": "text", "value": "### **KIVI** — міжнарожна компанія, займається виключно розробкою та виготовленням унікальних смарт-телевізорів."},
                {"type": "text", "value": "## Ключеві партнери KIVI:\n- Google\n- NETFLIX\n- JVC\n- DOLBY DIGITAL\n- AirConsole\n- AMTC\n- MEDIATEK\n- BOOSTEROID\n- Da Vinci\n\n### **1 500 000+** продано ТВ за весь час\n### **20+** Присутність бренду\n### **8 років** у ТВ бізнесі\n\n\n## В 2023 бренд KIVI присутній на 20+ ринках Европи та Азії. Ми продовжуємо активну експансію"}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 2, "title": "Нова лінійка ТВ",
            "content_blocks": [
                {"type": "text", "value": "### У 2024 році KIVI представляє власне бачення еволюції Smart TV як багатофункціонального пристрою."},
                {"type": "image", "value": "https://kivismart.com/themes/kivi/assets/shop/ua/line_2024/H760QB_24/img/design.png"},
                {"type": "text", "value": "## Телевізор — унікальний продукт з точки зору шляху клієнта\n\n- Клієнти шукають ***функції*** , які їм потрібні або які вважаються сучасними/необхідними.\n\n- Клієнти також оцінюють ***якість клієнтської підтримки, умови гарантії*** і т. д.\n\n- ***Впізнаваність бренду*** це не лише репутація продукту а й рівень якості у розумінні клієнта.\n\n- ***Ціна.*** У будь-якого клієна є ліміт, який він готовий витратити на певний продукт.\n\n- Як ви вважаєте, який ***5-й параметр*** використовується як «фільтр» тільки для ТВ- пристрою?"}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 3, "title": "№5 - КІМНАТА",
            "content_blocks": [
                {"type": "text", "value": "- ## **Кожен клієнт наперед знає, в якій кімнаті буде встановлено телевізор.**\n\n- ## **Більшість клієнтів уже знають, чи буде телевізор змонтований на стіні чи стоятиме на ніжках."},
                {"type": "text", "value": "# Нові Кластери Продуктів\n\n## Концепція “Room by Room”"},
                {"type": "image", "value": "https://i.ibb.co/NgbNcCTf/2025-08-16-23-05-10.png"},
                {"type": "text", "value": "В 2023 році ми представляємо нашу нову додаткову лінійку телевізорів, розроблену з особливими, унікальними функціями, щоб задовільнити потреби всіх сімей клієнтів створивши унікальні функції для окремих кімнат."}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 4, "title": "KIVI KidsTV",
            "content_blocks": [
                {"type": "text", "value": "### **флагман 2024**\n# **KIVI KidsTV**\n## **BUILD.PLAY.WATCH**\n\n### Не стримуйте політ фантазії та креативу з нашим найновішим телевізором, розробленим спеціально для дітей ."},
                {"type": "image", "value": "https://i.ibb.co/jPvBLWkf/2025-08-16-23-26-54.png"}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 5, "title": "Дизайну в стилі блоків",
            "content_blocks": [
                {"type": "text", "value": "## Креативна персоналізація завдяки **дизайну в стилі блоків**."},
                {"type": "image", "value": "https://i.ibb.co/DDTqX2B2/2025-08-16-23-30-56.png"},
                {"type": "text", "value": "Дозвольте своїм дітям розкрити їхній творчий потенціал і з легкістю створювати власні унікальні дизайни за допомогою єдиного в своєму роді дизайну телевізора.\n\n## **Задоволення у кожній деталі**"},
                {"type": "image", "value": "https://i.ibb.co/fzWKSkt2/2025-08-16-23-34-16.png"},
                {"type": "text", "value": "## Захисне скло перед екраном\n\n\nЕкран **KidsTV** доповнений міцним загартованим склом, що забезпечує довговічність та безпеку телевізора.\nДля забезпечення безпеки дітей – телевізор можна закріпити на поверхні столу спеціальними стрічками, які входять в комплект, а підставки та кріплення кронштейнів посилені металевою конструкцією."}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 6, "title": "Вмонтований нічник",
            "content_blocks": [
                {"type": "text", "value": "## KidsTV оснащений нічником, щоб ваші діти почувались у безпеці\n\n- Регульована яскравість\n- Керується з ТВ і пульта\n- Може працювати навіть коли ТВ вимкнений\n- Створює затишок"},
                {"type": "text", "value": "Телевізор для дітей, творчості та уяви"},
                {"type": "image", "value": "https://i.ibb.co/3m9QJYwg/2025-08-16-23-40-04.png"}
            ]
        },
        {
            "material_title": "Лінійка TV 2024", "step_number": 7, "title": "Cтруктура нових кластерів",
            "content_blocks": [
                {"type": "image", "value": "https://i.ibb.co/7J9kgLzc/2025-08-16-23-44-27.png"},
                {"type": "image", "value": "https://i.ibb.co/0ydDNgFh/2025-08-16-23-46-25.png"}
            ]
        },
    ]
    
    print("\n--- Добавление пошагового контента ---")
    for content_data in material_contents_data:
        add_content_step(content_data['material_title'], content_data)

    # --- 6. ПОЛНОЕ СОДЕРЖИМОЕ ТЕСТОВ ---
    test_questions_data = [
        # Знання продукту KIVI TV (одиночный выбор)
        {
            "test_title": "Знання продукту KIVI TV", "step_number": 1, 
            "question_text": "У якому році компанія KIVI стала сертифікованим партнером Google та Netflix?",
            "question_type": "single_choice",
            "answers": [
                {"answer_text": "2019", "is_correct": False},
                {"answer_text": "2020", "is_correct": True},
                {"answer_text": "2021", "is_correct": False},
                {"answer_text": "2022", "is_correct": False}
            ]
        },
        {
            "test_title": "Знання продукту KIVI TV", "step_number": 2,
            "question_text": "Який стратегічний партнер KIVI є світовим лідером у виробництві телевізорів?",
            "question_type": "single_choice",
            "answers": [
                {"answer_text": "Samsung", "is_correct": False},
                {"answer_text": "MTC", "is_correct": True},
                {"answer_text": "JVC", "is_correct": False},
                {"answer_text": "LG", "is_correct": False}
            ]
        },
        {
            "test_title": "Знання продукту KIVI TV", "step_number": 3,
            "question_text": "Яка технологія звуку використовується в телевізорах KIVI?",
            "question_type": "single_choice",
            "answers": [
                {"answer_text": "Dolby Vision", "is_correct": False},
                {"answer_text": "HDR10+", "is_correct": False},
                {"answer_text": "Dolby DAP", "is_correct": True},
                {"answer_text": "Ultra Surround", "is_correct": False}
            ]
        },
        {
            "test_title": "Знання продукту KIVI TV", "step_number": 4,
            "question_text": "Яка компанія є партнером KIVI у сфері хмарних ігор?",
            "question_type": "single_choice",
            "answers": [
                {"answer_text": "NVIDIA GeForce Now", "is_correct": False},
                {"answer_text": "Google Stadia", "is_correct": False},
                {"answer_text": "Boosteroid", "is_correct": True},
                {"answer_text": "PlayStation Now", "is_correct": False}
            ]
        },
        {
            "test_title": "Знання продукту KIVI TV", "step_number": 5,
            "question_text": "Яка функція в пульті дистанційного керування KIVI розроблена спільно з Korean Remote Solution?",
            "question_type": "single_choice",
            "answers": [
                {"answer_text": "Вказівник", "is_correct": True},
                {"answer_text": "Голосовий пошук", "is_correct": False},
                {"answer_text": "Вбудований мікрофон", "is_correct": False},
                {"answer_text": "Підсвічування кнопок", "is_correct": False}
            ]
        },
        # Техніки продажів (множественный выбор)
        {
            "test_title": "Техніки продажів", "step_number": 1,
            "question_text": "Які з перелічених питань є етапами продажів?",
            "question_type": "multiple_choice",
            "answers": [
                {"answer_text": "Встановлення контакту", "is_correct": True},
                {"answer_text": "Виявлення потреб", "is_correct": True},
                {"answer_text": "Презентація продукту", "is_correct": True},
                {"answer_text": "Робота з запереченнями", "is_correct": True},
                {"answer_text": "Завершення продажу", "is_correct": True},
                {"answer_text": "Доставка товару", "is_correct": False}
            ]
        },
        {
            "test_title": "Техніки продажів", "step_number": 2,
            "question_text": "Які з цих технік допомагають встановити контакт з клієнтом?",
            "question_type": "multiple_choice",
            "answers": [
                {"answer_text": "Активне слухання", "is_correct": True},
                {"answer_text": "Використання професійного жаргону", "is_correct": False},
                {"answer_text": "Повторення імені клієнта", "is_correct": True},
                {"answer_text": "Задавання закритих питань", "is_correct": False}
            ]
        },
        {
            "test_title": "Техніки продажів", "step_number": 3,
            "question_text": "Які типи питань слід використовувати для виявлення потреб клієнта?",
            "question_type": "multiple_choice",
            "answers": [
                {"answer_text": "Відкриті питання", "is_correct": True},
                {"answer_text": "Запитання, що вимагають відповіді 'так' або 'ні'", "is_correct": False},
                {"answer_text": "Питання, що починаються зі слів 'Чому', 'Як', 'Що'", "is_correct": True},
                {"answer_text": "Прямі питання про бюджет", "is_correct": False}
            ]
        },
        {
            "test_title": "Техніки продажів", "step_number": 4,
            "question_text": "Які є ефективні способи роботи з запереченнями?",
            "question_type": "multiple_choice",
            "answers": [
                {"answer_text": "Промовчати, щоб клієнт сам вирішив", "is_correct": False},
                {"answer_text": "Уточнити заперечення, щоб зрозуміти його причину", "is_correct": True},
                {"answer_text": "Надати додаткову інформацію, що розвіює сумніви", "is_correct": True},
                {"answer_text": "Сперечатися з клієнтом", "is_correct": False}
            ]
        },
        {
            "test_title": "Техніки продажів", "step_number": 5,
            "question_text": "Які з цих дій є частиною завершення продажу?",
            "question_type": "multiple_choice",
            "answers": [
                {"answer_text": "Повторення ключових переваг", "is_correct": True},
                {"answer_text": "Запитання 'Коли ви хочете отримати товар?'", "is_correct": True},
                {"answer_text": "Надання знижки без запиту", "is_correct": False},
                {"answer_text": "Подяка клієнту за угоду", "is_correct": True}
            ]
        },
    ]

    print("\n--- Добавление тестовых вопросов и ответов ---")
    for test_data in test_questions_data:
        add_test_question(test_data['test_title'], test_data)

    print("\n--- Проверка: загружаем вопросы для 'Техніки продажів' ---")
    sales_questions = get_test_questions("Техніки продажів")
    if sales_questions:
        for q in sales_questions:
            print(f"Вопрос: {q['question_text']} (Тип: {q['question_type']})")
            for a in q['answers']:
                print(f" - Ответ: {a['answer_text']} (Правильный: {a['is_correct']})")
    
    print("\n--- База данных успешно заполнена! ---")

    # --- Имитация прохождения материала и проверка обновления статуса теста ---
    print("\n--- Демонстрация автоматического обновления статуса теста ---")
    
    # 1. Проверяем начальные статусы
    print("\nНачальные статусы назначений для 'sasha':")
    initial_assignments = get_assigned_tests_for_user("sasha")
    for a in initial_assignments:
        print(f"- {a['title']}: Статус - {a['status']}")

    # 2. Имитируем прохождение материала "Історія компанії"
    print("\nИмитируем прохождение материала 'Історія компанії'...")
    update_assignment(
        username='sasha',
        test_title='Історія компанії',
        new_data={'status': 'learned'}
    )
    
    # 3. Проверяем конечные статусы
    print("\nКонечные статусы назначений для 'sasha':")
    final_assignments = get_assigned_tests_for_user("sasha")
    for a in final_assignments:
        print(f"- {a['title']}: Статус - {a['status']}")

    print("\n--- Демонстрация завершена. ---")