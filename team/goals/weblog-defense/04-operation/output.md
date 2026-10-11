# 04 Operation
## 実行
- `skills/log-analyzer/analyze.py --input tests/fixtures/mini-access.log` → analysis.md（6件: W1〜W6 各1。動作確認用の最小入力での値）
- デモ本番: Ma-san 側のデモ用ログに `--input <path>` を差し替えて同じ手順
## 司法チェック
- レポート v1 → NG 5件、exit=1（stop-scene-log.txt、v1 は rejected/report.v1.txt）→ v2 → PASS exit=0
- 全体: ../judiciary.txt
## 伝播
- 「検知は根拠行＋ルール番号」「対策は提案のみ・人が承認」を R10〜R12 として RULES.md に追加済み。他のログ種別（認証ログ等）にも同じ型で広げられる
## 発表物
- pitch/slides.md、pitch/voice-script.md、pitch/video-shotlist.md
## 承認（最終確認）
状態: 承認待ち（人の最終確認待ち）
承認者: 未
日時: 
