import os
from offsets import apply_offsets
from calc import signal_plot
from filters import data_reading
from ConfigHandling import read_config, write_config
from audio_visualizer import data_to_audio

def navigate_folders(needed_type):
    config_paths = read_config()
    current_path = config_paths[0 if needed_type == "noise" else 1]
    old_path_usage = input(f"Use saved path ({current_path})? y/n: ").strip().lower() == 'y'

    if old_path_usage and os.path.exists(current_path):
        if current_path.endswith(".csv"):
            return current_path
    else:
        current_path = ""

    while not current_path:
        folder_path = input("Enter your start path: ").strip()
        if os.path.isdir(folder_path):
            current_path = folder_path
        else:
            print(f"Invalid path: {folder_path}. Try again.")

    while True:
        print(f"\nCurrent path: {current_path}")
        items = sorted(os.listdir(current_path))
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item}")

        print("\nOptions: --Folder [f], --Back [b], --Save [s], --Exit [e]")
        user_input = input("Choose an option (number for selection, or a command): ").strip().lower()

        if user_input.isdigit():
            selection = int(user_input) - 1
            if 0 <= selection < len(items):
                selected_item = items[selection]
                selected_path = os.path.join(current_path, selected_item)

                if os.path.isdir(selected_path):
                    current_path = selected_path
                elif selected_item.endswith('.csv'):
                    return selected_path
                else:
                    print("Invalid file type. Please select a .csv file.")
        elif user_input == 'f':
            if all(os.path.isfile(os.path.join(current_path, item)) for item in items):
                return current_path
            print("Navigate to a folder with only files.")
        elif user_input == 'b':
            current_path = os.path.dirname(current_path)
        elif user_input == 's':
            print(f"Path saved: {current_path}")
            return current_path
        elif user_input == 'e':
            break
        else:
            print("Invalid command.")


def filters():
    print("Expected format: N N (lp hp) -> where N is number. If no N needed, put '-1'")
    user_input = input("Input desired cutoffs: ").split()

    if len(user_input) != 2:
        print("ERROR: Expected 2 inputs.")
        return None, None

    try:
        return map(int, user_input)
    except ValueError:
        print("ERROR: Inputs must be integers.")
        return None, None


def main():
    while True:
        print("1. Read Data\n"
              "2. Crop Data\n"
              "3. Apply Filters\n"
              "4. About\n"
              "5. Audio from .CSV\n"
              "6. Exit\n"
              "9. Change Base Values")
        ans = input().strip()

        if ans == '1':
            file_path = navigate_folders("main")
            if file_path:
                signal_plot(file_path, None, None, "plot")

        elif ans == '2':
            file_path = navigate_folders("main")
            if file_path:
                try:
                    start_offset = float(input("Enter start offset (seconds): "))
                    end_offset = float(input("Enter end offset (seconds): "))
                    apply_offsets(file_path, start_offset, end_offset)
                except ValueError:
                    print("ERROR: Offsets must be numeric.")

        elif ans == '3':
            file_path = navigate_folders("main")
            noise_path = navigate_folders("noise")
            if file_path and noise_path:
                num1, num2 = filters()
                if num1 is None or num2 is None:
                    continue

                filter_type = ("HighPass" if num1 == -1 else
                               "LowPass" if num2 == -1 else
                               "BandPass")
                print(f"Chosen Filter Type: {filter_type}")
                data_reading(file_path, num1, num2, filter_type, noise_path)

        elif ans == '4':
            print("\nMade by Milana K., Kristina M., Artur N., Jeffrey T.\n")

        elif ans == '5':
            file_path = navigate_folders("main")
            if file_path:
                data_to_audio(file_path)

        elif ans == '6':
            break

        elif ans == '9':
            folder = navigate_folders("main")
            if folder:
                option = input("Choose a file for:\n1) Noise sample\n2) Wished start point\n")
                if option == '1':
                    write_config(folder, None)
                elif option == '2':
                    write_config(None, folder)
                else:
                    print("Wrong option chosen.")

        else:
            print("Incorrect option. Try again.")


if __name__ == "__main__":
    main()
