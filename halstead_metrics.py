"""
МЕТРИКИ ХОЛСТЕДА ДЛЯ ОЦЕНКИ СЛОЖНОСТИ КОДА
"""

class HalsteadMetrics:
    def __init__(self):
        self.operators = {
            'уникальные_операторы': ['=', '+', '-', '==', '!=', '>', '<', 'if', 'for', 'while', 'def', 'return', 'import', 'class'],
            'общее_количество_операторов': 45
        }
        
        self.operands = {
            'уникальные_операнды': ['contact_id', 'first_name', 'last_name', 'phone', 'email', 'contacts', 'db_connection', 'search_query', 'result'],
            'общее_количество_операндов': 68
        }
    
    def calculate_metrics(self):
        n1 = len(self.operators['уникальные_операторы'])  # уникальные операторы
        n2 = len(self.operands['уникальные_операнды'])    # уникальные операнды
        N1 = self.operators['общее_количество_операторов'] # общее количество операторов
        N2 = self.operands['общее_количество_операндов']  # общее количество операндов
        
        # Метрики Холстеда
        vocabulary = n1 + n2
        length = N1 + N2
        volume = length * (vocabulary ** 0.5)
        difficulty = (n1 / 2) * (N2 / n2)
        effort = difficulty * volume
        
        return {
            "Словарь программы (n)": vocabulary,
            "Длина программы (N)": length,
            "Объем программы (V)": round(volume, 2),
            "Сложность программы (D)": round(difficulty, 2),
            "Усилия на разработку (E)": round(effort, 2)
        }
    
    def display_metrics(self):
        print("МЕТРИКИ ХОЛСТЕДА")
        print("=" * 30)
        
        print("Операторы:", self.operators['уникальные_операторы'])
        print("Операнды:", self.operands['уникальные_операнды'])
        
        metrics = self.calculate_metrics()
        
        print("\nРАСЧЕТНЫЕ МЕТРИКИ:")
        for metric, value in metrics.items():
            print(f"   {metric}: {value}")

# Рассчитываем и отображаем метрики
halstead = HalsteadMetrics()
halstead.display_metrics()