import requests
import urllib.request
import urllib.error
import urllib.parse

ind = "AKfycbyu6UuTGPSgIYEYtylOs4Bkw3t7JxWSnJhQMqv4H3Q72cvdoad3EPIFH5mLyAm0WfKqjA"
# Укажите здесь URL вашего развернутого Google Apps Script API
API_URL = f"https://script.google.com/macros/s/{ind}/exec"


def fetch_data_from_api(request_type, **kwargs):
    # Создаем словарь с обязательным параметром type
    params = {'type': request_type}
    # Добавляем в него все остальные переданные аргументы (например, title)
    params.update(kwargs)

    try:
        # Проверяем наличие интернет-соединения
        urllib.request.urlopen('https://www.google.com', timeout=1)
        # Преобразуем словарь в правильную строку URL-запроса
        query_string = urllib.parse.urlencode(params)
        full_url = f"{API_URL}?{query_string}"
        
        print(f"Запрос к API: {full_url}") # Полезно для отладки
        
        response = requests.get(full_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return {"error": f"Сетевая ошибка: {e}"}
    except urllib.error.URLError as e:
        print(f"Нет интернет-соединения: {e}")
        return {} if data_type == 'user_info' else []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из API: {e}")
        return {} if data_type == 'user_info' else []
    except ValueError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return {} if data_type == 'user_info' else []