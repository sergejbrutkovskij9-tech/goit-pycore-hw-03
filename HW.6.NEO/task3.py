import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def list_files(startpath, indent=0):
    print(Fore.BLUE + " " * 4 * indent + f"📂 {startpath.name}/")
    for item in startpath.iterdir():
        if item.is_dir():
            list_files(item, indent + 1)
        else:
            print(Fore.GREEN + " " * 4 * (indent + 1) + f"📄 {item.name}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory_path = Path(sys.argv[1])
    else:
        directory_path = Path.cwd()
    if not directory_path.exists():
        print(Fore.RED + f"Помилка: шлях '{directory_path}' не існує.")
        sys.exit(1)
    if not directory_path.is_dir():
        print(Fore.RED + f"Помилка: шлях '{directory_path}' не є директорією.")
        sys.exit(1)
    list_files(directory_path)