---
name: ai-plc-construction
description: AI-PLC の construction 段。選ばれた案をタスクに分け、行政が実装する
---
# construction
- 入力: 承認済みの Inception
- 行政がやる: 選ばれた案をタスクに分け、行政が実装する
- 出力: goals/<goal>/03-construction/output.md（末尾に `## 承認` 欄：状態/承認者/日時）
- 司法: `judiciary/check.sh` を走らせ、結果を同じフォルダの judiciary.txt に残す
- 承認ゲート: 人が承認するまで次段に進まない。前提が崩れたら Inception へ Backtrack

## スキル生成の手順
templates/goal/03-construction/output.md の手順 1〜5 に従う。スキルは `skills/<name>/SKILL.md`、RULES.md の条番号を必ず書く。
