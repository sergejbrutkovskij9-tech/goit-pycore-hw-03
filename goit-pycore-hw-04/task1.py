from pathlib import Path

def total_salary(path):
    total = 0
    count = 0
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                name, salary_str = line.split(',')
                total += float(salary_str)
                count += 1
                
        if count == 0:
            return 0, 0
            
        average = total / count
        return total, average

    except FileNotFoundError:
        print(f"Помилка: Файл за шляхом '{path}' не знайдено.")
        return 0, 0
    except ValueError:
        print(f"Помилка: Файл за шляхом '{path}' пошкоджений або має неправильний формат.")
        return 0, 0
total, average = total_salary("HW.6.NEO/salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
