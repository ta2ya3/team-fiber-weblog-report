#!/usr/bin/env bash
# 使い方: bin/new-goal.sh <slug> "<Goal の一文>"
set -eu; cd "$(dirname "$0")/.."; s=$1; g=$2; d=goals/$s
[ -e "$d" ] && { echo "既にある: $d"; exit 1; }
cp -r templates/goal "$d"
sed -i "s|{{GOAL}}|$g|;s|{{DATE}}|$(date +%F)|" "$d/README.md"
echo "作成: $d → 01-collection から書き、./judiciary/check.sh"
