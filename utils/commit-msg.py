#!/usr/bin/env python2

"""
Git commit hook

Check commit message according to BEURK commit guidelines
"""

import sys
import re

valid_commit_types = ['feat', 'fix', 'docs', 'style', 'refactor',
        'perf', 'test', 'chore', ]
valid_commit_scopes = ['core', 'builder', 'client', ]
commit_file = sys.argv[1]
help_address = 'https://github.com/unix-thrust/beurk/wiki/Commit-Guidelines'

def bad_commit(errmsg):
    sys.stderr.write("\n%s\n" % errmsg)
    sys.stderr.write("\n - Please refer to commit guide: %s\n\n"
            % help_address)
    sys.exit(1)

with open(commit_file) as commit:
    lines = commit.read().splitlines()
    # abracadabra: remove all comments from the list of lines ;)
    lines = [l for l in lines if not l.lstrip().startswith("#")]
    if len(lines) == 0:
        bad_commit("Empty commit message")

    # first line
    line = lines[0]
    if len(line) > 50:
        bad_commit("First commit message line (header) "
                "is exceeding the 50 chars limit")

    m = re.search('^(.*)\((.*)\): (.*)$', line)

    if not m or len(m.groups()) != 3:
        bad_commit("First commit message line (header) "
                "does not follow format: type(scope): message")

    commit_type, commit_scope, commit_message = m.groups()

    if commit_type not in valid_commit_types:
        bad_commit("Commit type not in valid ones: %s"
                % ", ".join(valid_commit_types))

    if commit_scope not in valid_commit_scopes \
            and commit_type not in ["docs", "chore"]:
        bad_commit("Commit scope not in valid ones: %s"
                % ", ".join(valid_commit_scopes))

    if commit_message[0].isupper():
        bad_commit("Commit subject first char not lowercase")

    if commit_message[-1] == '.':
        bad_commit("Commit subject last char (a dot) is not allowed")

    if line != line.strip():
        bad_commit("First commit message line (header) "
                "contains leading or ending spaces")

    if len(lines) > 1 and lines[1]:
        bad_commit("Second commit message line must be empty")

    if len(lines) > 2 and not lines[2].strip():
        bad_commit("Third commit message line (body) must not be empty")

    for l in lines:
        if len(l) > 72:
            bad_commit("Following line is exceeding the "
                    "72 chars limit:\n%s" % l)
