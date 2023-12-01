#!/bin/bash

# ⚠ USE WITH CAUTION ⚠
# Pre-commit hook that will block commits if they contain passwords, tokens, or other confidential information matched by regex

# ------------------------------------------------------------------------------
# Variables
# ------------------------------------------------------------------------------
# Define list of REGEX to be searched and blocked
regex_list=(
  # block AWS API Keys
  '((?:ASIA|AKIA|AROA|AIDA|AGPA|ANPA|ANVA)([A-Z0-7]{16}))'
  # block slack API token
  'xox[baprs]-([0-9a-zA-Z]{10,48})?'
  # AWS API token
  '^(?i)[A-Za-z0-9\/+=]{40}$'
)

# Concatenate regex_list
separator="|"
regex="$(printf "${separator}%s" "${regex_list[@]}")"
regex="${regex:${#separator}}"

# ------------------------------------------------------------------------------
# Pre-commit hook
# ------------------------------------------------------------------------------
files=$(git diff --cached --name-only)
found=0

for file in $files; do
  # Use extended regex to search for a match in the staged file
  matches=$(git show :$file | grep -nE "(${regex})")

  if [ -n "$matches" ]; then
    echo "Found secrets in file: $file"
    while read -r match; do
      location=$(echo "$match" | awk -F ':' '{print $1}')
      secret=$(echo "$match" | awk -F ':' '{print $2}')
      echo "Line $location: Secret: $secret"
    done <<< "$matches"
    found=1
  fi
done

if [ $found -eq 1 ]; then
  echo "[POLICY BLOCKED] Secrets detected in your commit. Please remove them and try again."
  exit 1
fi

# No secrets detected, allow the commit
exit 0
