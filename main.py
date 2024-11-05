#main.py
import os
from offsets import apply_offsets
from calc import signal_plot
from filters import data_reading
from ConfigHandling import read_config, write_config



# Функция для навигации по папкам
def navigate_folders():
    current_path = ""
    old_path_usage = False
    noise_path = last_path = 0
    noise_path, last_path = read_config()
    if noise_path == 0 or noise_path is None:
        noise_path = None

    if last_path == 0 or last_path is None:
        old_path_usage = False
    else:
        if input(f"Do you want to use {last_path} as current Path? y/n: ").lower() == 'y':
            if os.path.exists(last_path) and os.path.isdir(last_path):
                current_path = last_path
                old_path_usage = True
        else:
            print("Old path usage is declined")


    while not old_path_usage:
        folder_path = input("Enter Your Start Path: ").strip()
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            current_path = folder_path
            break
        else:
            print(f"Invalid path: {folder_path}. Please try again.\n")

    while True:
        print(f"\nCurrent path: {current_path}")
        items = sorted(os.listdir(current_path))

        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

        print("\nOptions: --Folder [f], --Back [b], --Save [s], --Exit [e]")

        user_input = input("Choose an option (number for selection, or a command): ").strip()

        if user_input.isdigit():
            selection = int(user_input) - 1
            if 0 <= selection < len(items):
                selected_item = items[selection]
                selected_path = os.path.join(current_path, selected_item)

                if os.path.isdir(selected_path):
                    current_path = selected_path
                elif os.path.isfile(selected_path):
                    if selected_item.endswith('.csv'):
                        return selected_path, noise_path  # Возвращаем путь к выбранному файлу
                    else:
                        print("Invalid file type. Please select a .csv file.")
            else:
                print("Invalid selection.")

        elif user_input.lower() == 'f':  # Выбор папки
            if all(os.path.isfile(os.path.join(current_path, item)) for item in items):
                return current_path, noise_path  # Возвращаем путь папки
            else:
                print("You are not in a folder containing only files. Navigate to a folder with files.")

        elif user_input.lower() == 'b':  # Назад
            current_path = os.path.dirname(current_path)

        elif user_input.lower() == 's':  # Сохранить путь
            print(f"Path saved: {current_path}")
            return current_path, noise_path  # Сохраняем путь к текущей папке

        elif user_input.lower() == 'e':  # Выход
            break

        else:
            print("Invalid command.")

def filters():
    print("Expected format: N N (lp hp) -> where N is number. If no N needed, put '-1'")
    user_input = input("Input desired cutoffs: ")

    # Разделяем строку по пробелу
    input_values = user_input.split()

    # Проверяем количество введенных значений
    if len(input_values) != 2:
        print("ERROR: Expected 2 inputs.")
    else:
        try:
            # Преобразуем строки в int и распаковываем в num1 и num2
            num1, num2 = tuple(map(int, input_values))
            print(f"num1: {num1}, num2: {num2}")
            return num1, num2
        except ValueError:
            print("ERROR: One of the inputs is not an Integer.")
            return None, None


# Основная функция
def main():
    while True:
        print("1. Read Data\n2. Crop Data\n3. Apply Filters\n4. About\n5. Exit")
        ans = input()
        if ans == '1':
            file_path = navigate_folders()
            if file_path:
                signal_plot(file_path)
        elif ans == '2':
            file_path = navigate_folders()
            if file_path:
                start_offset = float(input("Enter start offset (seconds): "))
                end_offset = float(input("Enter end offset (seconds): "))
                apply_offsets(file_path, start_offset, end_offset)
        elif ans == '3':
            file_path, noise_path = navigate_folders()
            Num1, Num2 = filters()
            DesiredType = None
            if (Num1 == -1 and Num2 == -1) or Num1 is None or Num2 is None:
                continue
            elif Num1 == -1:
                DesiredType = "HighPass"
            elif Num2 == -1:
                DesiredType = "LowPass"
            else:
                DesiredType = "BandPass"
            print("Choosen Filter Type = " + DesiredType)
            data_reading(file_path, Num1, Num2, DesiredType, noise_path)
        elif ans == '4':
            print("\nMade by Milana K., Kristina M., Artur N., Jeffrey T.\n")
        elif ans == '5':
            break
        elif ans == '9':
            print("Choose a folder with noise samples/1 sample in this folder/file with medium")
            folder = navigate_folders()
            write_config(None, folder)
        else:
            print("Incorrect option, try again.")


if __name__ == "__main__":
    main()
