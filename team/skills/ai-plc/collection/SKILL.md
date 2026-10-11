---
name: ai-plc-collection
description: AI-PLC の collection 段。一次情報（Issue・URL）から困りごとと制約を集め、事実と推測を分ける
---
# collection
- 入力: Goal、Issue
- 行政がやる: 一次情報（Issue・URL）から困りごとと制約を集め、事実と推測を分ける
- 出力: goals/<goal>/01-collection/output.md（末尾に `## 承認` 欄：状態/承認者/日時）
- 司法: `judiciary/check.sh` を走らせ、結果を同じフォルダの judiciary.txt に残す
- 承認ゲート: 人が承認するまで次段に進まない。前提が崩れたら Goal の再定義 へ Backtrack
