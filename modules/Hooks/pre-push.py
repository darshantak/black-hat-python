#!/usr/bin/env python3

import os
import re
import sys,subprocess

SECRETS = [
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",  # Email address
    r"\b[A-Fa-f0-9]{32}\b",  # MD5 hash
    r"\b[A-Fa-f0-9]{40}\b",  # SHA1 hash
    r"\b[A-Fa-f0-9]{64}\b",  # SHA256 hash
    r"\b[A-Fa-f0-9]{128}\b",  # SHA512 hash
    r"\b[A-Za-z0-9]{32}\b",  # Generic 32-character string
    r"\b[A-Za-z0-9]{40}\b",  # Generic 40-character string
    r"\b[A-Za-z0-9]{64}\b",  # Generic 64-character string
    r"\b\d{4}-\d{2}-\d{2}\b",  # Date in YYYY-MM-DD format
    r"\b\d{2}:\d{2}:\d{2}\b",  # Time in HH:MM:SS format
    r"\b\d{4}\d{2}\d{2}\b",  # Date in YYYYMMDD format
    r"\b\d{6}\b",  # Six-digit number
    r"\b\d{8}\b",  # Eight-digit number
    r"\b\d{10}\b",  # Ten-digit number
    r"\b\d{12}\b",  # Twelve-digit number
]

# Define the root path of the Git repository
root_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
print(root_path)
# Define a function to scan a single file for secrets
def scan_file(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
        # print(contents)
        for pattern in SECRETS:
            if re.search(pattern, contents):
                print(f"Potential secret found in {file_path}: {pattern}")
                sys.exit(1)

# Get the list of files that have been changed in the current push
files_changed = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD', 'HEAD^'], universal_newlines=True).splitlines()
print("files changed", files_changed)
# Scan each changed file in the Git repository
for file_path in files_changed:
    print(file_path)
    if file_path.endswith(".py"):
        file_path = os.path.join(root_path, file_path)
        scan_file(file_path)
