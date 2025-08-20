import peewee
import os
import bcrypt
import secrets
import json

# --- НАСТРОЙКА БАЗЫ ДАННЫХ ---
# Определяем путь к базе данных относительно корневой папки проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, "app_data.db")
db = peewee.SqliteDatabase(db_path)

# --- МОДЕЛИ (ОПИСАНИЕ ТАБЛИЦ) ---

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = peewee.CharField(unique=True, index=True)
    password_hash = peewee.CharField()
    role = peewee.CharField(default='user') 
    session_token = peewee.CharField(null=True)

class UserProfile(BaseModel):
    # on_delete='CASCADE' - профиль удалится вместе с пользователем
    user = peewee.ForeignKeyField(User, backref='profile', unique=True, on_delete='CASCADE')
    full_name = peewee.CharField(null=True)
    phone = peewee.CharField(null=True)
    email = peewee.CharField(unique=True, null=True)
    about = peewee.TextField(null=True)


class TestData(BaseModel):
    title = peewee.CharField(unique=True)
    item_type = peewee.CharField() # 'material' или 'test'
    # ... другие поля для самого материала, если нужны ...

class Assignment(BaseModel):
    user = peewee.ForeignKeyField(User, backref='assignments', on_delete='CASCADE')
    test_data = peewee.ForeignKeyField(TestData, backref='assignments', on_delete='CASCADE')
    status = peewee.CharField(default='assigned')
    score = peewee.CharField(null=True)
    class Meta:
        indexes = ((('user', 'test_data'), True),)

class MaterialContent(BaseModel):
    test_data = peewee.ForeignKeyField(TestData, backref='content_steps', on_delete='CASCADE')
    step_number = peewee.IntegerField()
    title = peewee.CharField()
    content_blocks = peewee.TextField() # Храним JSON здесь


class TestQuestion(BaseModel):
    test_data = peewee.ForeignKeyField(TestData, backref='questions', on_delete='CASCADE')
    step_number = peewee.IntegerField()
    question_text = peewee.TextField()
    question_type = peewee.CharField() # 'single_choice' or 'multiple_choice'

class TestAnswer(BaseModel):
    question = peewee.ForeignKeyField(TestQuestion, backref='answers', on_delete='CASCADE')
    answer_text = peewee.TextField()
    is_correct = peewee.BooleanField(default=False)


# --- ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ БАЗОЙ ---

def initialize_database():
    """Создает все таблицы, если их еще нет."""
    try:
        db.connect()
        db.create_tables([User, UserProfile, TestData, Assignment, MaterialContent, TestQuestion, TestAnswer], safe=True)
    finally:
        if not db.is_closed():
            db.close()

def register_user(username, password, role='user'):
    """Регистрирует нового пользователя и создает для него пустой профиль."""
    if not password:
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        db.connect()
        with db.atomic():
            new_user = User.create(
                username=username, 
                password_hash=hashed_password.decode('utf-8'),
                role=role
            )
            UserProfile.create(user=new_user)
        return True
    except peewee.IntegrityError:
        return False
    finally:
        if not db.is_closed():
            db.close()

def login_user(username, password):
    """Проверяет логин/пароль и возвращает токен в случае успеха."""
    try:
        db.connect()
        user = User.get_or_none(User.username == username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            new_token = secrets.token_hex(16)
            user.session_token = new_token
            user.save()
            return new_token
        return None
    finally:
        if not db.is_closed():
            db.close()

def create_or_update_user_profile(username: str, profile_data: dict):
    """Создает или обновляет профиль для указанного пользователя."""
    try:
        db.connect()
        user = User.get_or_none(User.username == username)
        if not user:
            return False

        profile_info = {
            "user": user,
            "full_name": profile_data.get("full_name"),
            "phone": profile_data.get("phone"),
            "email": profile_data.get("email"),
            "about": profile_data.get("about")
        }
        
        update_data = profile_info.copy()
        del update_data["user"]

        UserProfile.insert(profile_info).on_conflict(
            conflict_target=[UserProfile.user],
            update=update_data
        ).execute()
        return True
    except Exception:
        return False
    finally:
        if not db.is_closed():
            db.close()

def get_user_profile(username: str):
    """Возвращает полный профиль (с ролью) для одного пользователя."""
    try:
        db.connect()
        user = User.get_or_none(User.username == username)
        if user:
            role = user.role
            profile_data = {}
            if hasattr(user, 'profile'):
                try:
                    profile = user.profile.get()
                    profile_data = {
                        "full_name": profile.full_name,
                        "phone": profile.phone,
                        "email": profile.email,
                        "about": profile.about
                    }
                except UserProfile.DoesNotExist:
                    pass
            return {"role": role, **profile_data}
        return None
    finally:
        if not db.is_closed():
            db.close()

# --- НОВАЯ ФУНКЦИЯ ---
def get_all_profiles_with_username():
    """
    Возвращает список ВСЕХ профилей, добавляя к каждому 'username' из таблицы User.
    """
    try:
        db.connect()
        query = (UserProfile
                 .select(UserProfile, User.username)
                 .join(User))
        
        profiles_list = list(query.dicts())
        return profiles_list
    except Exception as e:
        print(f"Ошибка при получении профилей: {e}")
        return []
    finally:
        if not db.is_closed():
            db.close()

def add_test_data(data: dict):
    try:
        db.connect()
        TestData.get_or_create(
            title=data.get("title"),
            defaults={"item_type": data.get("item_type")}
        )
    finally:
        if not db.is_closed():
            db.close()


def add_test_question(test_title: str, step_data: dict):
    """
    Добавляет один вопрос с вариантами ответов к существующему тесту.
    """
    try:
        db.connect()
        test = TestData.get_or_none(TestData.title == test_title)
        if not test: return None

        with db.atomic():
            question = TestQuestion.create(
                test_data=test,
                step_number=step_data.get("step_number"),
                question_text=step_data.get("question_text"),
                question_type=step_data.get("question_type")
            )
            
            for answer in step_data.get("answers", []):
                TestAnswer.create(
                    question=question,
                    answer_text=answer.get("answer_text"),
                    is_correct=answer.get("is_correct", False)
                )
            return True
    except Exception as e:
        print(f"Ошибка при добавлении вопроса: {e}")
        return False
    finally:
        if not db.is_closed():
            db.close()

def get_test_questions(test_title: str):
    """
    Возвращает все вопросы и варианты ответов для указанного теста.
    """
    try:
        db.connect()
        test = TestData.get_or_none(TestData.title == test_title)
        if not test: return []

        questions_query = (TestQuestion
                           .select()
                           .where(TestQuestion.test_data == test)
                           .order_by(TestQuestion.step_number))

        result_list = []
        for question in questions_query:
            answers_list = list(question.answers.dicts())
            result_list.append({
                "step_number": question.step_number,
                "question_text": question.question_text,
                "question_type": question.question_type,
                "answers": answers_list
            })
        return result_list
    finally:
        if not db.is_closed():
            db.close()

def update_assignment(username: str, test_title: str, new_data: dict):
    """Обновляет назначение - меняет статус и/или результат."""
    try:
        db.connect()
        # Создаем назначение, если его нет
        user = User.get(User.username == username)
        test_data_item = TestData.get(TestData.title == test_title)
        assignment, created = Assignment.get_or_create(user=user, test_data=test_data_item)
        
        # Обновляем данные
        if "status" in new_data:
            assignment.status = new_data["status"]
        if "score" in new_data:
            assignment.score = new_data["score"]
        assignment.save()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении назначения: {e}")
        return False
    finally:
        if not db.is_closed():
            db.close()

def get_assigned_tests_for_user(username: str):
    try:
        db.connect()
        query = (Assignment
                 .select(User.username.alias('user'), TestData.title, TestData.item_type, Assignment.status, Assignment.score)
                 .join(User).switch(Assignment).join(TestData)
                 .where(User.username == username))
        return list(query.dicts())
    finally:
        if not db.is_closed():
            db.close()

def add_content_step(material_title: str, step_data: dict):
    """Добавляет один шаг с содержимым к существующему материалу."""
    try:
        db.connect()
        material = TestData.get_or_none(TestData.title == material_title)
        if not material: return None
        
        content_json = json.dumps(step_data.get("content_blocks", []), ensure_ascii=False)
        step = MaterialContent.create(
            test_data=material,
            step_number=step_data.get("step_number"),
            title=step_data.get("title"),
            content_blocks=content_json
        )
        return step
    finally:
        if not db.is_closed():
            db.close()

def get_content_for_material(material_title: str):
    """Возвращает все шаги для указанного материала."""
    try:
        db.connect()
        material = TestData.get_or_none(TestData.title == material_title)
        if not material: return []
        
        steps_query = material.content_steps.order_by(MaterialContent.step_number).dicts()
        result_list = []
        for step in steps_query:
            step['content_blocks'] = json.loads(step['content_blocks'])
            result_list.append(step)
        return result_list
    finally:
        if not db.is_closed():
            db.close()


# --- Пример использования ---
if __name__ == '__main__':
    # ВАЖНО: Удалите старый файл app_data.db перед первым запуском,
    # чтобы таблицы создались с новой правильной структурой.
    initialize_database()
    
    # 1. Регистрируем администратора
    register_user("admin", "admin123", role="admin")
    
    # 2. Регистрируем обычного пользователя
    register_user("sasha", "sasha123")
    
    # 3. Создаем профиль для Саши
    profile_dict = {
        "full_name": "Олександр Риженков",
        "phone": "+380 66 017 5627",
        "email": "sasha@example.com",
        "about": "Просто користувач."
    }
    profile_dict_1 = {
        "full_name": "Олександр Риженков",
        "phone": "+380 66 017 5627",
        "email": "sasha@example32423.com",
        "about": "Admin"
    }
    create_or_update_user_profile("sasha", profile_dict)
    create_or_update_user_profile("admin", profile_dict_1)
    
    # 4. Получаем полные данные пользователя
    sasha_data = get_user_profile("sasha")
    data = get_user_profile("admin")

    if sasha_data:
        print("\n--- Данные пользователя 'sasha' ---")
        for key, value in sasha_data.items():
            print(f"  {key}: {value}")
    
    if data:
        print("\n--- Данные пользователя 'admin' ---")
        for key, value in data.items():
            print(f"  {key}: {value}")

    # Все данные из твоего примера
    sample_data = [
        {'user': 'sasha', 'title': 'Лінійка TV 2024', 'status': 'assigned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'Історія компанії', 'status': 'not_learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'KIVI KIDS', 'status': 'not_learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'Знання продукту KIVI TV', 'status': 'assigned_learned', 'score': None, 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Нова лінійка саундбарів та кранштейнів', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Техніки продажів', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'KIVI Plus', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'KIVI Media', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'admin', 'title': 'Єволюція KIVI', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'Єволюція KIVI', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'Лінійка TV 2023', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'KIVI Кріплення', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'HDR and colors FIX Додатковий материал для возвитку', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'admin', 'title': 'Інструкція KIDS TV Додатковий материал для возвитку', 'status': 'learned', 'score': None, 'item_type': 'material'},
        {'user': 'sasha', 'title': 'Тест 1', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 2', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 3', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 4', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 5', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'admin', 'title': 'Тест 6', 'status': 'passed', 'score': '10/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 7', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 8', 'status': 'failed', 'score': '5/10', 'item_type': 'test'},
        {'user': 'admin', 'title': 'Тест 9', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 10', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 11', 'status': 'failed', 'score': '7/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 12', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 13', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 14', 'status': 'failed', 'score': '3/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 15', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 16', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 17', 'status': 'failed', 'score': '4/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 18', 'status': 'passed', 'score': '9/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 19', 'status': 'passed', 'score': '7/7', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 20', 'status': 'passed', 'score': '8/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 21', 'status': 'passed', 'score': '10/10', 'item_type': 'test'},
        {'user': 'sasha', 'title': 'Тест 22', 'status': 'passed', 'score': '9/10', 'item_type': 'test'}
    ]

    # 2. Создаем все уникальные тесты и материалы в библиотеке
    unique_titles = {item['title']: item for item in sample_data}.values()
    for item in unique_titles:
        add_test_data(item)
        
    # 3. Создаем назначения со статусами и результатами для пользователя 'sasha'
    for item in sample_data:
        update_assignment(
            username=item['user'], 
            test_title=item['title'], 
            new_data={"status": item['status'], "score": item['score']}
        )

    print("\n--- Проверка: загружаем назначенные материалы для 'sasha' ---")
    sasha_materials = get_assigned_tests_for_user("sasha")
    for mat in sasha_materials:
        print(f"- {mat['title']} (Тип: {mat['item_type']}, Статус: {mat['status']}, Результат: {mat.get('score')})")

    # --- 4. ПОЛНОЕ СОДЕРЖИМОЕ МАТЕРИАЛОВ ---
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

    # --- 5. ПОЛНОЕ СОДЕРЖИМОЕ ТЕСТОВ ---
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

    # Проверяем, что данные тестов добавлены
    print("\n--- Проверка: загружаем вопросы для 'Техніки продажів' ---")
    sales_questions = get_test_questions("Техніки продажів")
    if sales_questions:
        for q in sales_questions:
            print(f"Вопрос: {q['question_text']} (Тип: {q['question_type']})")
            for a in q['answers']:
                print(f" - Ответ: {a['answer_text']} (Правильный: {a['is_correct']})")
    
    print("\n--- База данных успешно заполнена! ---")