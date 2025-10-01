"""
ТЕСТОВЫЕ СЦЕНАРИИ И ОЦЕНКА КОЛИЧЕСТВА ТЕСТОВ
АИС "Телефонный справочник"
"""

class TestScenarios:
    def __init__(self):
        self.scenarios = [
            {
                "id": "TS001",
                "name": "Добавление нового контакта",
                "steps": [
                    "1. Открыть форму добавления контакта",
                    "2. Заполнить обязательные поля (ФИО, телефон)",
                    "3. Нажать кнопку 'Сохранить'",
                    "4. Проверить, что контакт появился в списке"
                ],
                "expected": "Контакт успешно добавлен в базу"
            },
            {
                "id": "TS002", 
                "name": "Поиск существующего контакта",
                "steps": [
                    "1. Ввести ФИО в поле поиска",
                    "2. Нажать кнопку 'Найти'",
                    "3. Просмотреть результаты поиска"
                ],
                "expected": "В результатах отображается искомый контакт"
            },
            {
                "id": "TS003",
                "name": "Редактирование контакта", 
                "steps": [
                    "1. Выбрать контакт из списка",
                    "2. Нажать кнопку 'Редактировать'",
                    "3. Изменить данные контакта",
                    "4. Сохранить изменения"
                ],
                "expected": "Данные контакта успешно обновлены"
            },
            {
                "id": "TS004",
                "name": "Удаление контакта",
                "steps": [
                    "1. Выбрать контакт из списка", 
                    "2. Нажать кнопку 'Удалить'",
                    "3. Подтвердить удаление",
                    "4. Проверить список контактов"
                ],
                "expected": "Контакт удален из базы данных"
            }
        ]
    
    def calculate_test_count(self):
        # Оценка необходимого количества тестов
        functional_tests = len(self.scenarios)
        boundary_tests = 5  # тесты граничных значений
        negative_tests = 4  # тесты на некорректные данные
        integration_tests = 3  # интеграционные тесты
        
        total = functional_tests + boundary_tests + negative_tests + integration_tests
        return total
    
    def display(self):
        print("ТЕСТОВЫЕ СЦЕНАРИИ")
        print("=" * 30)
        
        for scenario in self.scenarios:
            print(f"\n{scenario['id']}: {scenario['name']}")
            print("Шаги:")
            for step in scenario['steps']:
                print(f"  {step}")
            print(f"Ожидаемый результат: {scenario['expected']}")
        
        total_tests = self.calculate_test_count()
        print(f"\nОЦЕНКА КОЛИЧЕСТВА ТЕСТОВ: {total_tests} тестов")
        print("- Функциональные тесты:", len(self.scenarios))
        print("- Тесты граничных значений: 5")
        print("- Негативные тесты: 4") 
        print("- Интеграционные тесты: 3")

# Создаем и отображаем тестовые сценарии
tests = TestScenarios()
tests.display()