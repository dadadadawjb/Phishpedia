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

        # 生成高层次的 commit message 建议
        commit_suggestions = get_commit_suggestions(modified_files)
        if commit_suggestions:
            print("\nCommit message suggestions:", file=sys.stderr)
            for suggestion in commit_suggestions:
                print(f"- {suggestion}", file=sys.stderr)
        else:
            print("No high-level commit message suggestions.", file=sys.stderr)
    else:
        print("No modified files.", file=sys.stderr)

if __name__ == "__main__":
    main()
