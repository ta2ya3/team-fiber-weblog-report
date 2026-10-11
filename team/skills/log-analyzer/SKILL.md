---
name: log-analyzer
description: Webアクセスログから攻撃の疑いを抽出・分類する（行政）。検知ルールは立法の detection-rules.tsv。
---
# log-analyzer
- 入力: アクセスログ（combined 形式）。`--input <path>` または環境変数 `WEBLOG_INPUT` で差し替え。ルールは `--rules`（既定 goals/weblog-defense/rules/detection-rules.tsv）
- 実行: `skills/log-analyzer/analyze.py --input <path>`（外部通信なし）
- 出力: `- 検知 [W番号] 種類 / 根拠 L行番号 / 送信元` の一覧とルール別件数
- 守ること: RULES.md R10（根拠行とルール番号）、R11（断定しない、「疑い」と書く）。個人情報を出力に転記しない
