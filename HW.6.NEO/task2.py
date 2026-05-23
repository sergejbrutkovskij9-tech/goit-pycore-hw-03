def get_cats_info(path):
    cats_list = []
    
    try:
        
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                cat_id, name, age = line.split(',')
                cat_dict = {
                    "id": cat_id,
                    "name": name,
                    "age": age
                }
                cats_list.append(cat_dict)
                
        return cats_list

    except FileNotFoundError:
        print(f"Помилка: Файл за шляхом '{path}' не знайдено.")
        return []
    except ValueError:
        print(f"Помилка: Файл за шляхом '{path}' містить некоректні дані або пошкоджений.")
        return []
with open("cats_file.txt", "w", encoding="utf-8") as f:
    f.write("60b90c1c13067a15887e1ae1,Tayson,3\n")
    f.write("60b90c2413067a15887e1ae2,Vika,1\n")
    f.write("60b90c2e13067a15887e1ae3,Barsik,2\n")
cats_info = get_cats_info("cats_file.txt")
print(cats_info)

