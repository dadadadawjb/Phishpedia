#!/usr/bin/env python3
import subprocess
import sys
import os

def get_modified_files():
    root_dir = '.'
    result = subprocess.run(["git", "diff", "--name-only"], stdout=subprocess.PIPE, text=True, cwd=root_dir)
    modified_files = result.stdout.strip().split('\n')
    return modified_files

def get_folders_for_files(files):
    folders = set()

    for file_path in files:
        # Assuming file paths are relative to the project root
        # folders.add(file_path.split("/")[0])
        folders.add(os.path.dirname(file_path).split("/")[-1])

    return folders

def get_commit_suggestions(modified_files, modified_folders):
    commit_message = []
    if 'configs' in modified_files or 'config' in modified_folders:
        commit_message.append("update configs")
    if 'detectron2_pedia' in modified_files or 'detectron2_pedia' in modified_folders:
        commit_message.append("update detectron2")
    if 'siamese_pedia' in modified_files or 'siamese_pedia' in modified_folders:
        commit_message.append("update siamese")

    return commit_message

def print_commit_info():
    modified_files = get_modified_files()

    if modified_files:
        print("Modified files:", file=sys.stderr)
        for file_path in modified_files:
            print(f"- {file_path}", file=sys.stderr)

        folders = get_folders_for_files(modified_files)

        print("Folders these files belong to:", file=sys.stderr)
        for folder in folders:
            print(f"- {folder}", file=sys.stderr)

        # 生成高层次的 commit message 建议
        commit_suggestions = get_commit_suggestions([os.path.basename(f) for f in modified_files], folders)
        if commit_suggestions:
            print("Commit message suggestions:", file=sys.stderr)
            for suggestion in commit_suggestions:
                print(f"- {suggestion}", file=sys.stderr)
        else:
            print("No high-level commit message suggestions.", file=sys.stderr)
    else:
        print("No modified files.", file=sys.stderr)

if __name__ == "__main__":
    print_commit_info()
