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

# --- ГЛАВНЫЙ ЦИКЛ ГЕНЕРАЦИИ ---
def generate_dataset(samples=1000):
    print(f"Начинаем генерацию {samples} примеров...")
    
    for i in range(samples):
        # Случайно выбираем тип ошибки, чтобы данные были перемешаны
        choice = random.choice([1, 2, 3])
        
        if choice == 1:
            simulate_db_error()
        elif choice == 2:
            simulate_validation_error()
        elif choice == 3:
            simulate_logic_error()
            
        if i % 100 == 0:
            print(f"Сгенерировано {i} записей...")
            
    print("Готово! Данные сохранены в error_dataset.csv")

if __name__ == "__main__":
    # Генерируем 1000 примеров
    generate_dataset(1000)