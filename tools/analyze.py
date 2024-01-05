# coding: utf-8
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

def extract_words(commit_id):
    result = {}
    diff_command = "git diff -w -U0 {}^ {}".format(commit_id, commit_id)
    diff_output = os.popen(diff_command).read()

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
                if word not in preserve_words:
                    result[current_file].add(word)
    return result

class RebaseAnalyzer:
    def get_infos(self):
        log_command = 'git log --pretty=format:"%h %ct %s"'
        log_output = os.popen(log_command).read()
        result = []
        pattern = re.compile(r"(\w+) (\d+) (.*)")
        matches = pattern.findall(log_output)
        for match in matches:
            commit_id = match[0]
            commit_time = int(match[1])
            commit_msg = match[2]
            if not commit_msg.startswith('Merge'):
                result.append((commit_id, commit_time, commit_msg))
        return result

    def get_commits_id_little_time_diff(self, infos):
        commits_id = []
        for i in range(len(infos) - 1):
            commit_id, commit_time, commit_msg = infos[i]
            prev_commit_id, prev_commit_time, prev_commit_msg = infos[i+1]
            if commit_time - prev_commit_time >= 0 and commit_time - prev_commit_time < 300:
                commits_id.append(commit_id)
        return commits_id
    
    def get_commits_id_same_commit_msg(self, infos):
        commits_id = []
        for i in range(len(infos) - 1):
            commit_id, commit_time, commit_msg = infos[i]
            prev_commit_id, prev_commit_time, prev_commit_msg = infos[i+1]
            if commit_msg == prev_commit_msg:
                commits_id.append(commit_id)
        return commits_id

    def get_commits_id_same_words(self, infos):
        commits_id = []
        same_words = []
        words = {}
        for i in range(len(infos) - 1):
            commit_id = infos[i][0]
            words[commit_id] = set()
            commit_words = extract_words(commit_id)
            for file in commit_words:
                wordlist = commit_words[file]
                words[commit_id].update(set(wordlist))
        for i in range(len(infos) - 2):
            commit_id = infos[i][0]
            prev_commit_id = infos[i+1][0]
            if words[commit_id] & words[prev_commit_id]:
                commits_id.append(commit_id)
                same_words.append(words[commit_id] & words[prev_commit_id])
                # commits_id.append((commit_id, words[commit_id] & words[prev_commit_id]))
        return commits_id, same_words

    commits_id = []
    same_words = []
    def __init__(self):
        infos = self.get_infos()
        #commits_id_little_time_diff = self.get_commits_id_little_time_diff(infos)
        #self.commits_id.extend(commits_id_little_time_diff)
        commits_id_same_words, self.same_words = self.get_commits_id_same_words(infos)
        self.commits_id.extend(commits_id_same_words)
        


class SplitAnalyzer:
    def get_infos(self):
        log_command = 'git log --shortstat --pretty=format:"%h %s"'
        log_output = os.popen(log_command).read()
        result = []
        pattern = re.compile(r"(\w+) (.*)\n (\d+) files? changed", re.MULTILINE)
        matches = pattern.findall(log_output)
        for match in matches:
            commit_id = match[0]
            commit_msg = match[1]
            files_changed = int(match[2])
            result.append((commit_id, commit_msg, files_changed))
        return result

    def get_commits_id_without_same_words(self, infos):
        result = []
        pairs = []
        for commit_id, commit_msg, files_changed in infos:
            if files_changed > 1 and not commit_msg.startswith('Merge'):
                commit_words = extract_words(commit_id)
                break_flag = 0
                for file1, wordlist1 in commit_words.items():
                    if break_flag:
                        break
                    for file2, wordlist2 in commit_words.items():
                        if break_flag:
                            break
                        if file1 != file2 and not (wordlist1 & wordlist2):
                            #result.append((file1, file2, wordlist1 & wordlist2))
                            result.append(commit_id)
                            pairs.append([file1, file2])
                            break_flag = 1
        return result,pairs

    commits_id = []
    pairs = []
    def __init__(self):
        infos = self.get_infos()
        commits_id_without_same_words, self.pairs = self.get_commits_id_without_same_words(infos)
        self.commits_id.extend(commits_id_without_same_words)
        

rebaseAnalyzer = RebaseAnalyzer()
rebaseCommits = rebaseAnalyzer.commits_id
rebaseWords = rebaseAnalyzer.same_words
splitAnalyzer = SplitAnalyzer()
splitCommits = splitAnalyzer.commits_id
splitPairs = splitAnalyzer.pairs

print("===Split advice===")
print("A total of {} suspicious commits were found:".format(len(splitCommits)))
print("commit ID\tfile1\t\tfile2")
for ID, pair in zip(splitCommits, splitPairs):
    print("{}:\t{}\t{}".format(ID,pair[0],pair[1]))

print("===Rebase advice===")
print("A total of {} suspicious commits were found:".format(len(rebaseCommits)))
print("commit ID\twords")
for ID, words in zip(rebaseCommits, rebaseWords):
    print("{}:\t{}".format(ID,list(words)[:5]))