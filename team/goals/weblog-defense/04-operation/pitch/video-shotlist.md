# 1分の作業動画 撮り順
1. (0-10秒) 立法: rules/detection-rules.tsv（W1〜W6）と RULES.md R10〜R12
2. (10-25秒) 行政: `analyze.py --input <デモ用ログ>` を実行し、検知一覧が出る
3. (25-40秒) レポート v1 → `./judiciary/check.sh` → NG 5件・exit=1
4. (40-52秒) v2 に修正 → 再実行 → PASS exit=0
5. (52-60秒) 承認欄「人の承認が必要（未）」を映して終わる
