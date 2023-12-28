#!/usr/bin/env python3
import subprocess

def get_modified_files():
    result = subprocess.run(["git", "diff", "--name-only", "--cached"], stdout=subprocess.PIPE, text=True)
    modified_files = result.stdout.strip().split('\n')
    return modified_files

def get_folders_for_files(files):
    folders = set()

    for file_path in files:
        # Assuming file paths are relative to the project root
        folders.add(file_path.split("/")[0])

    return folders

def main():
    modified_files = get_modified_files()

    if modified_files:
        print("Modified files:")
        for file_path in modified_files:
            print(f"- {file_path}")

        folders = get_folders_for_files(modified_files)

        print("\nFolders these files belong to:")
        for folder in folders:
            print(f"- {folder}")
    else:
        print("No modified files.")

if __name__ == "__main__":
    main()
