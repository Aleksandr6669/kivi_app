import peewee
import os
import bcrypt
import secrets
import json
import datetime

# --- НАСТРОЙКА БАЗЫ ДАННЫХ ---
# Определяем путь к базе данных относительно корневой папки проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, "app_data.db")
db = peewee.SqliteDatabase(db_path)

# --- МОДЕЛИ (ОПИСАНИЕ ТАБЛИЦ) ---

class BaseModel(peewee.Model):
    class Meta:
        database = db


class Institution(BaseModel):
    institution_name = peewee.CharField(unique=True, index=True)
    company_name = peewee.CharField(null=True)
    address = peewee.CharField(null=True)
    website = peewee.CharField(null=True)
    logo_url = peewee.CharField(null=True)
    contact_person = peewee.CharField(null=True)
    contact_email = peewee.CharField(null=True)
    contact_phone = peewee.CharField(null=True)
    is_active = peewee.BooleanField(default=True)
    about = peewee.TextField(null=True)


class User(BaseModel):
    username = peewee.CharField(unique=True, index=True)
    password_hash = peewee.CharField()
    role = peewee.CharField(default='user')
    institution = peewee.ForeignKeyField(Institution, backref='users', null=True)
    session_token = peewee.CharField(null=True)


class Device(BaseModel):
    user = peewee.ForeignKeyField(User, backref='devices', on_delete='CASCADE')
    device_id = peewee.CharField()

    class Meta:
        indexes = (
            (('user', 'device_id'), True),
        )

class UserProfile(BaseModel):
    # on_delete='CASCADE' - профиль удалится вместе с пользователем
    user = peewee.ForeignKeyField(User, backref='profile', unique=True, on_delete='CASCADE')
    full_name = peewee.CharField(null=True)
    user_tupe = peewee.CharField(default='student')
    phone = peewee.CharField(null=True)
    email = peewee.CharField(null=True)
    img = peewee.CharField(null=True)
    ava = peewee.CharField(null=True)
    about = peewee.TextField(null=True)


class TestData(BaseModel):
    title = peewee.CharField(unique=True)
    item_type = peewee.CharField() # 'material' or 'test'
    related_material = peewee.ForeignKeyField(
        'self',
        backref='related_tests',
        null=True,
        on_delete='SET NULL'
    )

class Assignment(BaseModel):
    user = peewee.ForeignKeyField(User, backref='assignments', on_delete='CASCADE')
    test_data = peewee.ForeignKeyField(TestData, backref='assignments', on_delete='CASCADE')
    status = peewee.CharField(default='assigned')
    score = peewee.CharField(null=True)
    percentage_score = peewee.FloatField(null=True)
    passing_score = peewee.IntegerField(default=90) 
    total_attempts = peewee.IntegerField(default=3)
    attempts_used = peewee.IntegerField(default=0)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Assignment, self).save(*args, **kwargs)

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
        db.create_tables([User, UserProfile, TestData, Assignment, MaterialContent, TestQuestion, TestAnswer, Device, Institution], safe=True)
    finally:
        if not db.is_closed():
            db.close()

def create_and_assign_institution(username: str, institution_data: dict):
    try:
        db.connect(reuse_if_open=True)
        with db.atomic():
            user = User.get_or_none(User.username == username.lower())
            if not user or user.role != 'admin':
                return False
            if user.institution is not None:
                return False
            institution_name = institution_data.get("institution_name")
            if not institution_name:
                return False
            # Используем универсальную функцию для создания/обновления
            update_institution_details(institution_name, institution_data)
            # Получаем созданное учреждение и привязываем
            new_institution = Institution.get(Institution.institution_name == institution_name)
            user.institution = new_institution
            user.save()
        return True
    except Exception as e:
        return False
    finally:
        if not db.is_closed():
            db.close()

def get_institution_details(institution_name: str):
    """Возвращает детали указанного учебного заведения."""
    try:
        db.connect()
        institution = Institution.get_or_none(Institution.institution_name == institution_name)
        if institution:
            return {
                "company_name": institution.company_name,
                "address": institution.address,
                "website": institution.website,
                "logo_url": institution.logo_url,
                "contact_person": institution.contact_person,
                "contact_email": institution.contact_email,
                "contact_phone": institution.contact_phone,
                "is_active": institution.is_active,
                "about": institution.about
            }
        return None
    finally:
        if not db.is_closed():
            db.close()

def update_institution_details(institution_name: str, data: dict):
    """
    Обновляет информацию об учебном заведении.
    Если заведение с таким названием не существует, оно будет создано.
    """
    try:
        db.connect()

        # Добавляем имя учреждения в основной словарь с данными
        full_data = data.copy()
        full_data['institution_name'] = institution_name

        # Выполняем операцию "создать или обновить"
        (Institution
         .insert(full_data)
         .on_conflict(
             # В случае конфликта по уникальному полю institution_name...
             conflict_target=[Institution.institution_name],
             # ...обновить существующую запись данными из словаря data
             update=data
         )
         .execute())

        return True
    except Exception as e:
        print(f"Ошибка при создании/обновлении учреждения: {e}")
        return False
    finally:
        if not db.is_closed():
            db.close()

def add_test_data_with_relation(data: dict):
    try:
        db.connect()
        # Ищем связанный материал, если он указан
        related_material_item = None
        related_title = data.get("related_material_title")
        if related_title:
            related_material_item = TestData.get_or_none(TestData.title == related_title)

        TestData.get_or_create(
            title=data.get("title"),
            defaults={
                "item_type": data.get("item_type"),
                "related_material": related_material_item
            }
        )
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

def login_user(username, password, device_id=None):
    """Проверяет логин/пароль и возвращает токен в случае успеха."""
    try:
        db.connect()
        user = User.get_or_none(User.username.lower() == username.lower())
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            if device_id:
                Device.get_or_create(user=user, device_id=device_id)
            new_token = secrets.token_hex(16)
            user.session_token = new_token
            user.save()
            return new_token
        return None
    finally:
        if not db.is_closed():
            db.close()

def sravnit_imya_i_id(username, device_id):
    try:
        db.connect()
        device = Device.get_or_none(Device.device_id == device_id)
        if device and device.user.username == username:
            return True
        return False
    
    finally:
        if not db.is_closed():
            db.close()

def update_related_tests_status(material_title, username):
    print(material_title, username)
    try:
        db.connect()
        material = TestData.get_or_none(TestData.title == material_title)
            
        if material:
            related_tests = TestData.select().where(TestData.related_material == material)
            for test_item in related_tests:
                # ИСПРАВЛЕНО: используем test_item вместо related_test
                related_assignment = Assignment.get_or_none(
                    Assignment.user == User.get(User.username == username),
                    Assignment.test_data == test_item
                )
                if related_assignment and related_assignment.status == 'assigned_learned':
                    related_assignment.status = 'assigned'
                    related_assignment.save()
                    print(f"Статус теста '{test_item.title}' обновлен на 'assigned'.")
    except Exception as ex:
        print(f"Ошибка при обновлении связанных тестов: {ex}")
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

        if profile_data.get("password"):
            # Хешируем новый пароль
            hashed_password = bcrypt.hashpw(profile_data["password"].encode('utf-8'), bcrypt.gensalt())
            user.password_hash = hashed_password.decode('utf-8')
            user.save()
            # Удаляем пароль из данных профиля, чтобы не сохранить его в UserProfile
            del profile_data["password"]

        profile_info = {
            "user": user,
            "full_name": profile_data.get("full_name"),
            "phone": profile_data.get("phone"),
            "email": profile_data.get("email"),
            "img": profile_data.get("img"),
            "ava": profile_data.get("ava"),
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

def delete_user_from_db(username: str):
    """
    Видаляє користувача за ім'ям та його пов'язані дані.
    Завдяки `on_delete='CASCADE'` у моделях, пов'язані профілі
    та призначення автоматично видаляються.
    """
    try:
        db.connect()
        user_to_delete = User.get_or_none(User.username == username)
        if user_to_delete:
            user_to_delete.delete_instance(recursive=True, delete_nullable=True)
            return True
        return False
    except Exception as e:
        print(f"Помилка при видаленні користувача: {e}")
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
        # Ищем связанный материал, если он указан
        related_material_item = None
        related_title = data.get("related_material_title")
        if related_title:
            related_material_item = TestData.get_or_none(TestData.title == related_title)
        
        TestData.get_or_create(
            title=data.get("title"),
            defaults={
                "item_type": data.get("item_type"),
                "related_material": related_material_item
            }
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

        # Створюємо або отримуємо існуюче призначення
        assignment, created = Assignment.get_or_create(
            user=user, 
            test_data=test_data_item,
            defaults={
                'passing_score': new_data.get("passing_score", 90),
                'total_attempts': new_data.get("total_attempts", 3),
                'percentage_score': new_data.get("percentage_score", None),
                'updated_at': None 
            }
        )
        
        # Обновляем данные
        if "status" in new_data:
            assignment.status = new_data["status"]
        if "score" in new_data:
            assignment.score = new_data["score"]
        if "percentage_score" in new_data:
            assignment.percentage_score = new_data["percentage_score"]
        if "increment_attempts" in new_data and new_data["increment_attempts"]:
            assignment.attempts_used += 1

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
                 .select(User.username.alias('user'), TestData.title, TestData.item_type, 
                         Assignment.status, Assignment.score, Assignment.percentage_score,  
                         Assignment.passing_score, Assignment.total_attempts, Assignment.attempts_used,
                         Assignment.created_at, Assignment.updated_at) # Добавляем новые поля
                 .join(User).switch(Assignment).join(TestData)
                 .where(User.username == username)
                 # Сортировка: сначала по updated_at, если оно не null, затем по created_at
                 .order_by(
                     peewee.Case(
                         None,
                         [(Assignment.updated_at.is_null(), 1), ],
                         1).asc(),
                     Assignment.updated_at.desc(),
                     Assignment.created_at.desc()
                 ))
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
