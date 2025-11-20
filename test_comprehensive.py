import sys
import os
from predictor import smart_analyze

print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ MODEL...\n")

# --- ТЕСТ-КЕЙС 1: Ошибка Файловой Системы ---
def read_config():
    print("📂 Тест 1: Чтение конфига...")
    # Контекст для модели: пути, режимы, кодировки
    config_path = "/etc/secret_app/config.yaml"
    file_mode = "r"
    encoding_type = "utf-8"
    
    try:
        # Пытаемся открыть несуществующий файл
        with open(config_path, file_mode, encoding=encoding_type) as f:
            data = f.read()
    except Exception:
        smart_analyze(*sys.exc_info())

# --- ТЕСТ-КЕЙС 2: Ошибка Безопасности (Auth) ---
def access_admin_panel(user):
    print("🛡️ Тест 2: Доступ в админку...")
    # Контекст для модели: роли, токены, безопасность
    current_user_role = user['role']
    session_token = user['token']
    required_permission = "superuser"
    
    try:
        if current_user_role != required_permission:
            # Выбрасываем общую ошибку, но контекст подскажет, что это Auth!
            raise PermissionError("Access denied to resource")
    except Exception:
        smart_analyze(*sys.exc_info())

# --- ТЕСТ-КЕЙС 3: Ошибка Логики (для сравнения) ---
def calculate_statistics(data_list):
    print("🧮 Тест 3: Вычисление статистики...")
    # Контекст: списки, числа, итераторы
    total_count = len(data_list)
    factor = 10
    
    try:
        # Ошибка: деление на ноль (если список пуст)
        avg = factor / total_count
    except Exception:
        smart_analyze(*sys.exc_info())

# --- ЗАПУСК ---
if __name__ == "__main__":
    # 1. Вызываем ошибку файла
    read_config()
    
    # 2. Вызываем ошибку безопасности
    guest_user = {'role': 'guest', 'token': 'null'}
    access_admin_panel(guest_user)
    
    # 3. Вызываем ошибку логики
    calculate_statistics([]) # Передаем пустой список