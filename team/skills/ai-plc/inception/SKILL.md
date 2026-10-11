---
name: ai-plc-inception
description: AI-PLC の inception 段。候補を評価軸で比較し、推奨案を出す。1案に絞るのは人
---
# inception
- 入力: Collection 出力
- 行政がやる: 候補を評価軸で比較し、推奨案を出す。1案に絞るのは人
- 出力: goals/<goal>/02-inception/output.md（末尾に `## 承認` 欄：状態/承認者/日時）
- 司法: `judiciary/check.sh` を走らせ、結果を同じフォルダの judiciary.txt に残す
- 承認ゲート: 人が承認するまで次段に進まない。前提が崩れたら Collection へ Backtrack
