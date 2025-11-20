import random
import sys
import time
from collector import ErrorCollector

# Инициализируем коллектор (он будет писать всё в error_dataset.csv)
# Важно: убедитесь, что в collector.py класс инициализируется как:
# collector = ErrorCollector(save_file='error_dataset.csv')
collector = ErrorCollector(save_file='error_dataset.csv')

# --- Сценарий 1: Ошибки Базы Данных ---
def simulate_db_error():
    ops = ['connect', 'query', 'commit', 'rollback']
    tables = ['users', 'orders', 'logs', 'products']
    hosts = ['192.168.0.1', 'localhost', 'db.prod.internal']
    
    operation = random.choice(ops)
    table = random.choice(tables)
    host = random.choice(hosts)
    timeout_ms = random.randint(1000, 5000)
    
    try:
        # Имитация логики подключения
        if random.random() > 0.5:
            # Тип 1: Connection Refused
            port = random.choice([5432, 3306, 27017])
            raise ConnectionError(f"Failed to connect to {host}:{port} during {operation}")
        else:
            # Тип 2: Timeout (другой контекст переменных!)
            query_time = timeout_ms + 100
            raise TimeoutError(f"Query to table '{table}' timed out after {timeout_ms}ms")
            
    except Exception:
        # Сохраняем с меткой "Database_Error"
        collector.capture_exception(*sys.exc_info(), label="Database_Error")

# --- Сценарий 2: Ошибки Валидации Данных ---
def simulate_validation_error():
    fields = ['email', 'age', 'phone', 'password', 'username']
    bad_inputs = ['', '   ', 'undefined', 'null', 'DROP TABLE']
    
    field = random.choice(fields)
    value = random.choice(bad_inputs) if random.random() > 0.5 else -random.randint(1, 100)
    
    try:
        # Имитация проверки формы
        if isinstance(value, int) and value < 0:
            # Контекст: отрицательное число
            limit = 0
            raise ValueError(f"Field '{field}' cannot be negative: {value}")
        elif isinstance(value, str) and len(value.strip()) == 0:
            # Контекст: пустая строка
            required = True
            raise ValueError(f"Field '{field}' is required but received empty string")
        else:
            raise TypeError(f"Invalid type for {field}: got {type(value)}")
            
    except Exception:
        collector.capture_exception(*sys.exc_info(), label="Validation_Error")

# --- Сценарий 3: Логические Ошибки и Вычисления ---
def simulate_logic_error():
    try:
        scenario = random.choice(['math', 'list', 'dict'])
        
        if scenario == 'math':
            # Деление на ноль
            total = random.randint(100, 5000)
            count = 0 
            # Модель должна увидеть count=0 в переменных
            result = total / count
            
        elif scenario == 'list':
            # Выход за границы массива
            data = [1, 2, 3]
            index = random.randint(5, 20)
            val = data[index]
            
        elif scenario == 'dict':
            # Отсутствующий ключ
            user_data = {'name': 'Alex', 'role': 'admin'}
            key_to_find = 'id_' + str(random.randint(100, 999))
            val = user_data[key_to_find]
            
    except Exception:
        collector.capture_exception(*sys.exc_info(), label="Logic_Calculation_Error")



# ... (импорты и предыдущий код остаются) ...

# --- НОВЫЙ СЦЕНАРИЙ 4: Ошибки Файловой Системы ---
def simulate_file_error():
    paths = ['/var/log/syslog', 'C:/Users/Admin/secret.txt', './config.json']
    modes = ['r', 'w', 'rb']
    encodings = ['utf-8', 'cp1251']
    
    path = random.choice(paths)
    mode = random.choice(modes)
    
    try:
        # Контекст: пути, режимы чтения, кодировки
        current_encoding = random.choice(encodings)
        if random.random() > 0.5:
            raise FileNotFoundError(f"No such file or directory: '{path}'")
        else:
            raise PermissionError(f"Permission denied: '{path}'")
    except Exception:
        # Метка класса: FileSystem_Error
        collector.capture_exception(*sys.exc_info(), label="FileSystem_Error")

# --- НОВЫЙ СЦЕНАРИЙ 5: Ошибки Безопасности/Доступа ---
def simulate_auth_error():
    roles = ['guest', 'anonymous', 'user']
    tokens = ['expired_token_xyz', 'invalid_signature', 'None']
    endpoints = ['/api/v1/admin', '/settings/billing', '/root']
    
    user_role = random.choice(roles)
    auth_token = random.choice(tokens)
    endpoint = random.choice(endpoints)
    
    try:
        # Контекст: роли, токены, защищенные пути
        if user_role == 'guest':
            raise PermissionError(f"User with role '{user_role}' cannot access {endpoint}")
        else:
            # Имитируем кастомную ошибку авторизации
            raise RuntimeError(f"403 Forbidden: Invalid token {auth_token}")
    except Exception:
        # Метка класса: Security_Auth_Error
        collector.capture_exception(*sys.exc_info(), label="Security_Auth_Error")

# --- ОБНОВЛЕННЫЙ ГЛАВНЫЙ ЦИКЛ ---
def generate_dataset(samples=1000):
    print(f"Начинаем генерацию {samples} примеров (включая новые типы)...")
    
    for i in range(samples):
        choice = random.choice([1, 2, 3, 4, 5]) # Теперь 5 вариантов!
        
        if choice == 1: simulate_db_error()
        elif choice == 2: simulate_validation_error()
        elif choice == 3: simulate_logic_error()
        elif choice == 4: simulate_file_error() # Новый
        elif choice == 5: simulate_auth_error() # Новый
            
    print("Готово! Данные обновлены.")

if __name__ == "__main__":
    generate_dataset(5000) # Генерируем чуть больше данных