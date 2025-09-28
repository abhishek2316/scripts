import os
import platform
import shutil
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List

def detect_os() -> str:
    return platform.system()


def get_folder_path() -> str:
    folder = Path(input("Enter the folder path: ").strip())
    if not folder.is_dir():
        print("The provided path is not a valid directory.")
        return None
    return folder
    
def scan_folder(folder_path: Path) -> Dict[str, int]:
    extension_count = Counter()

    print(f"Scanning folder: {folder_path}")
    for file in folder_path.iterdir():
        if file.is_file():
            extension = file.suffix.lower().lstrip(".")
            extension_count[extension] += 1

    return dict(extension_count)

def prompt_user_choice(file_counts: Dict[str, int]) -> List[str]:
    print("File types found:")
    for ext, count in file_counts.items():
        print(f".{ext}: {count} files")

    choice = input("Enter the file extension you want to manage like pdf or all(without dot): ").strip().lower()
    if  choice == "all":
        return list(file_counts.keys())
    elif choice in file_counts:
        return [choice]
    else:
        sys.exit("Invalid choice. Exiting.")

def move_files(selected_extensions: List[str], folder_path: Path) -> Dict[str, int]:
    folder_name = folder_path.name
    summary = Counter()

    for ext in selected_extensions:
        target_folder = folder_path / f"{folder_name}_{ext}"
        target_folder.mkdir(exist_ok=True)

        for file in folder_path.glob(f"*.{ext}"):
            destination = target_folder / file.name
            try:
                shutil.move(str(file), str(destination))
                summary[ext] += 1
            except Exception as e:
                print(f"Error moving {file.name}: {e}")

    return dict(summary)


def main() -> None:
    print("Welocome to the File Manager!")
    print(f"Detected Operating System: {detect_os()}")

    folder_path = get_folder_path()
    if not folder_path:
        print("No folder path provided")
        sys.exit(1)
        return
    
    file_counts = scan_folder(folder_path)

    if not file_counts:
        print("No files found in the specified directory.")
        return
    
    selected_extension = prompt_user_choice(file_counts)

    summary = move_files(selected_extension, folder_path)

    print("\nFiles organized successfully!")
    print("Summary:")
    for ext, count in summary.items():
        print(f"  {ext}: {count} files moved")

    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by you.")
        sys.exit(0)
