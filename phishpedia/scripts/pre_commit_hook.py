#!/usr/bin/env python3
import subprocess
import sys  # 引入 sys 模块

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
        print("Modified files:", file=sys.stderr)  # 输出到 stderr
        for file_path in modified_files:
            print(f"- {file_path}", file=sys.stderr)

        folders = get_folders_for_files(modified_files)

        print("\nFolders these files belong to:", file=sys.stderr)
        for folder in folders:
            print(f"- {folder}", file=sys.stderr)
    else:
        print("No modified files.", file=sys.stderr)

if __name__ == "__main__":
    main()
