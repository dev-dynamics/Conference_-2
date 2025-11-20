import sys
import pickle
from collector import ErrorCollector, clean_text

# Загружаем обученную модель
try:
    with open('error_classifier.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None

# Создаем коллектор без режима записи в файл (только захват)
analyzer_collector = ErrorCollector(save_file='dummy.csv')

def smart_analyze(ex_type, ex_value, ex_traceback):
    """
    Функция вызывается внутри except блока для анализа ошибки.
    """
    if not model:
        print("Модель не найдена. Сначала обучите (trainer.py)")
        return

    # 1. Захватываем текст ошибки + переменные
    raw_text = analyzer_collector.capture_exception(ex_type, ex_value, ex_traceback, label=None)
    
    # 2. Чистим
    cleaned_input = clean_text(raw_text)
    
    # 3. Предсказываем
    prediction = model.predict([cleaned_input])[0]
    proba = model.predict_proba([cleaned_input]).max()
    
    # 4. Красивый вывод
    print("\n" + "="*40)
    print("🤖 AI ERROR DIAGNOSTIC REPORT")
    print("="*40)
    print(f"🔴 Original Error: {ex_type.__name__}: {ex_value}")
    print(f"🧠 AI Category:    >> {prediction} <<")
    print(f"📊 Confidence:     {proba:.1%}")
    print(f"💡 Suggestion:     Check issues related to '{prediction}' logic.")
    print("="*40 + "\n")

# --- ТЕСТ: Имитация работы в реальном проекте ---
if __name__ == "__main__":
    print("Запуск приложения...")
    try:
        # Ситуация: Пользователь вводит некорректные данные, переменные сохраняются
        user_limit = 10
        current_val = 15
        
        if current_val > user_limit:
            # Генерируем ошибку, модель должна понять контекст чисел
            raise ValueError("Limit exceeded")
            
    except Exception:
        # Вызов нашего модуля
        smart_analyze(*sys.exc_info())