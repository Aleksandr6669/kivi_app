import requests
import urllib.request
import urllib.error

ind = "AKfycbyu6UuTGPSgIYEYtylOs4Bkw3t7JxWSnJhQMqv4H3Q72cvdoad3EPIFH5mLyAm0WfKqjA"
# Укажите здесь URL вашего развернутого Google Apps Script API
API_URL = f"https://script.google.com/macros/s/{ind}/exec"

def fetch_data_from_api(data_type: str):
    """
    Функция для получения данных из API.
    Args:
        data_type (str): 'user_info' или 'tests_data'.
    Returns:
        dict/list: Полученные данные или пустой объект в случае ошибки.
    """
    try:
        # Проверяем наличие интернет-соединения
        urllib.request.urlopen('https://www.google.com', timeout=1)
        
        response = requests.get(API_URL, params={"type": data_type})
        response.raise_for_status()  # Вызывает исключение для HTTP ошибок
        return response.json()
    except urllib.error.URLError as e:
        print(f"Нет интернет-соединения: {e}")
        return {} if data_type == 'user_info' else []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных из API: {e}")
        return {} if data_type == 'user_info' else []
    except ValueError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return {} if data_type == 'user_info' else []