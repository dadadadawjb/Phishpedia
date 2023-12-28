#!/usr/bin/env python3
import subprocess
import sys

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

def get_commit_suggestions(modified_files):
    commit_keywords = {
        'add': ['add', 'new'],
        'update': ['update', 'modify'],
        'delete': ['delete', 'remove']
    }

    file_modifications = {
        'add': [],
        'update': [],
        'delete': []
    }

    for file_path in modified_files:
        # 根据文件路径提取关键字
        keywords = []
        if '/' in file_path:
            keywords = file_path.split('/')[0].split('_')

        # 根据关键字确定修改类型
        modification_type = 'update' if keywords else 'add'

        # 将文件路径添加到相应修改类型的列表中
        file_modifications[modification_type].append(file_path)

    # 生成 commit message
    commit_message = []
    for action, changes in file_modifications.items():
        if changes:
            keywords = commit_keywords.get(action, [])
            commit_message.append(f"{', '.join(keywords)}: {', '.join(changes)}")

    return commit_message

def print_commit_info():
    modified_files = get_modified_files()

    if modified_files:
        print("Modified files:")
        for file_path in modified_files:
            print(f"- {file_path}")

        folders = get_folders_for_files(modified_files)

        print("\nFolders these files belong to:")
        for folder in folders:
            print(f"- {folder}")

        # 生成高层次的 commit message 建议
        commit_suggestions = get_commit_suggestions(modified_files)
        if commit_suggestions:
            print("\nCommit message suggestions:")
            for suggestion in commit_suggestions:
                print(f"- {suggestion}")
        else:
            print("\nNo high-level commit message suggestions.")
    else:
        print("No modified files.")

if __name__ == "__main__":
    print_commit_info()
