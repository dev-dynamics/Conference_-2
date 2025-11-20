import sys
import traceback
import pandas as pd
import re  # <--- Важно: добавили импорт регулярных выражений

# --- Эту функцию мы добавляем сюда, чтобы она была доступна везде ---
def clean_text(text):
    """
    Препроцессинг: удаляем мусор, оставляем суть.
    Используется и при сборе, и при обучении, и при предсказании.
    """
    text = str(text).lower()
    # Удаляем адреса памяти (напр. 0x7f8b)
    text = re.sub(r'0x[0-9a-f]+', '<ADDR>', text)
    # Удаляем конкретные числа (часто это ID или номера строк)
    text = re.sub(r'\d+', '<NUM>', text)
    # Оставляем буквы, знаки препинания кода (добавили скобки [] для списков)
    text = re.sub(r'[^a-z\s\._\:\=\(\)\[\]]', ' ', text) 
    return text

class ErrorCollector:
    def __init__(self, save_file='error_dataset.csv'):
        self.save_file = save_file
        # Если файла нет, создаем заголовки
        try:
            pd.read_csv(self.save_file)
        except FileNotFoundError:
            pd.DataFrame(columns=['full_text', 'error_type', 'label']).to_csv(self.save_file, index=False)

    def capture_exception(self, ex_type, ex_value, ex_traceback, label=None):
        """
        Перехватывает ошибку, извлекает контекст переменных и сохраняет в датасет.
        """
        # 1. Получаем стандартный текст ошибки
        stack_summary = traceback.extract_tb(ex_traceback)
        error_msg = f"{ex_type.__name__}: {ex_value}"
        
        # 2. ИЗВЛЕЧЕНИЕ КОНТЕКСТА
        locals_context = ""
        try:
            # Получаем последний фрейм (где упало)
            tb_last = ex_traceback
            while tb_last.tb_next:
                tb_last = tb_last.tb_next
            frame = tb_last.tb_frame
            
            # Собираем переменные в строку
            variables = frame.f_locals
            context_items = []
            for k, v in variables.items():
                if not k.startswith('__') and len(str(v)) < 100:
                    context_items.append(f"{k}={v}")
            locals_context = " | Variables: " + ", ".join(context_items)
        except Exception as e:
            locals_context = " | Context unavailable"

        # 3. Формируем полный текст
        full_text_blob = f"{error_msg} \nTrace: {stack_summary} \nContext: {locals_context}"
        
        # Для отладки выводим в консоль (можно закомментировать)
        # print(f"CAPTURED: {full_text_blob[:100]}...")

        # 4. Сохраняем в CSV
        if label:
            new_row = pd.DataFrame([[full_text_blob, ex_type.__name__, label]], 
                                   columns=['full_text', 'error_type', 'label'])
            new_row.to_csv(self.save_file, mode='a', header=False, index=False)
        
        return full_text_blob