# coding: utf-8
# 导入必要的模块
import os, sys
import re
import difflib

preserve_words = set([
    'False', 'None', 'True', 'and', 'as', 'assert', 'break',
    'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
    'try', 'while', 'with', 'yield'
])

def extract_words(diff_output):
    result = {}
    file_pattern = re.compile(r"diff --git a/(.*) b/(.*)")
    word_pattern = re.compile(r"[a-zA-Z_]\w*")
    current_file = None

    for _line in diff_output.split("\n"):
        line = _line.split("#")[0]
        file_match = file_pattern.match(line)

        if file_match:
            current_file = file_match.group(1)
            result[current_file] = set()

        if len(line) >= 2 and line[0] in '+-' and (line[1].isalnum() or line[1].isspace()):
            words = word_pattern.findall(line)
            for word in words:
                if word not in preserve_words and len(word) > 1:
                    result[current_file].add(word)
    return result



diff_command = "git diff -w -U0 --cached"
diff_output = os.popen(diff_command).read()
current_commit_words = extract_words(diff_output)

diff_command = "git diff -w -U0 HEAD^ HEAD"
diff_output = os.popen(diff_command).read()
previous_commit_words = extract_words(diff_output)


files_compared = {}
files_same_words = []
for file1, wordlist1 in current_commit_words.items():
    for file2, wordlist2 in current_commit_words.items():
        if file1 >= file2:
            continue
        if wordlist1 & wordlist2:
            if file1 not in files_compared:
                files_compared[file1] = {}
            files_compared[file1][file2] = wordlist1 & wordlist2
        else:
            files_same_words.append([file1, file2])


commits_compared = {}
for file1, wordlist1 in current_commit_words.items():
    for file2, wordlist2 in previous_commit_words.items():
        if wordlist1 & wordlist2:
            if file1 not in commits_compared:
                commits_compared[file1] = {}
            commits_compared[file1][file2] = wordlist1 & wordlist2

return_val = 0
if len(files_same_words):
    print("修改涉及多个文件且部分文件不涉及相同词素，请检查是否应该拆分为多个commits")
    print("以下是没有相同词素修改的文件对：")
    for file in files_same_words:
        print(file[0],file[1],sep='\t')
    return_val = 1

if len(commits_compared):
    print("与HEAD-commit的修改涉及相同词素，请检查是否应该 rebase 或 revert:")
    print("Current\tPreviou\tWords")
    for file1 in commits_compared:
        for file2 in commits_compared[file1]:
            print(file1,file2,commits_compared[file1][file2],sep='\t')
    return_val = 1

sys.exit(return_val)