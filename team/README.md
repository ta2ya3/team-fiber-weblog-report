# team_fiber — AI-PLC × AI三権分立 ハーネス（汎用テンプレート）
Goal を差し替えれば誰でも回せる。AI が発散・収束を回し、判断は人がする。
```
CONSTITUTION.md（憲法・人だけが改正 / .github/CODEOWNERS）
   └ RULES.md（立法 bots/ritsuho.md）
        ├ 行政 bots/gyosei.md ── skills/ai-plc: Collection → Inception → Construction → Operation
        │                         各段末に人の承認ゲート／前提が崩れたら前段へ Backtrack
        └ 司法 bots/shiho.md ── judiciary/check.sh（機械チェック、違反で exit 1）＋ 意味判定
```
## テンプレートの使い方
1. `bin/new-goal.sh <slug> "<Goal の一文>"` → `goals/<slug>/` に4段の雛形ができる
2. 01-collection: 事実を出典付きで書く（出典がないと司法が NG）
3. 02-inception: 候補を評価軸で比較し推奨を書く。選ぶのは人
4. 03-construction: 手順どおりに `skills/<name>/SKILL.md` を作り、成果物を作る
5. 04-operation: 通しで実行 → 計測 → `./judiciary/check.sh > goals/<slug>/judiciary.txt` → 学びを伝播（RULES 改正案／憲法は人へ／テンプレ更新）
6. 各段の `## 承認` は人が `状態: 承認済み`・`承認者: <名前>` にする。AI は承認しない（デモで進める場合は「デモとして自動進行」と明記）

## 構成
- `templates/goal/` 4段の雛形と承認欄　- `skills/ai-plc/` 各段のスキル　- `bin/new-goal.sh`
- `RULES.md` 立法 R1〜R8　- `CONSTITUTION.md` 憲法　- `judiciary/check.sh` 司法　- `bots/` 三権のBot指示文
- 入力例: [goals/hackathon-1600](goals/hackathon-1600)（Inception は人の承認待ち）

AI-PLC: https://github.com/miyatti777/ai-plc （MIT）を参考に書き直し。

## チーム例: Webアクセスログの攻撃検知・対策提案（goals/weblog-defense）
- 立法: `goals/weblog-defense/rules/detection-rules.tsv`（W1 SQLi／W2 XSS／W3 パストラバーサル／W4 総当たり／W5 スキャナ／W6 機密パス）＋ RULES.md R10〜R12
- 行政: `skills/log-analyzer`（抽出・分類）、`skills/countermeasure-proposer`（WAF・設定・レート制限の案）
- 司法: `judiciary/check.sh` が根拠行・ルール番号のない検知、断定、自動適用の指示を exit 1 で差し戻す。対策の適用は人の承認後だけ
- 実行: `skills/log-analyzer/analyze.py --input <ログのパス>`（または `WEBLOG_INPUT=<パス>`）。外部通信なし
- **デモ用ログは別途用意し、パスを差し替えて実行する。** `tests/fixtures/mini-access.log` は動作確認用の最小入力でデモ用ではない
