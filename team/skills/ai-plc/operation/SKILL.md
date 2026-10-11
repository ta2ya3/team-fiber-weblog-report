---
name: ai-plc-operation
description: AI-PLC の operation 段。通しで動かし、測り、人が最終確認する
---
# operation
- 入力: Construction の成果物
- 行政がやる: 通しで動かし、測り、人が最終確認する
- 出力: goals/<goal>/04-operation/output.md（末尾に `## 承認` 欄：状態/承認者/日時）
- 司法: `judiciary/check.sh` を走らせ、結果を同じフォルダの judiciary.txt に残す
- 承認ゲート: 人が承認するまで次段に進まない。前提が崩れたら Construction へ Backtrack

## 実行・司法・伝播
1. 通しで実行し、計測値だけを記録
2. `./judiciary/check.sh > goals/<goal>/judiciary.txt`（NG → 該当段へ Backtrack）
3. 伝播: 学びを RULES.md 改正案（立法）／CONSTITUTION.md 改正案（人）／テンプレート・スキル更新に振り分ける
