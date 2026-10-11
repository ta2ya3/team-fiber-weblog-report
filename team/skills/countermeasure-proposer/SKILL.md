---
name: countermeasure-proposer
description: log-analyzer の検知結果から、WAFルール・設定・レート制限の対策「案」を作る（行政）。適用はしない。
---
# countermeasure-proposer
- 入力: log-analyzer の出力
- 手順: 検知ルール番号ごとに対策案を書く（例: W1/W2→WAF の該当ルール群を検知モードで試す、W3→パス正規化と `..` 拒否、W4→/login にレート制限と一時ロック、W5/W6→機密パスを 404 固定・UA ブロック案）
- 各案に根拠の検知（W番号・L行番号）と副作用（誤検知で正規ユーザーを止める恐れ）を書く
- 出力: `goals/<goal>/04-operation/reports/*.md`。末尾に `承認: 人の承認が必要（未）`
- 守ること: RULES.md R10〜R12。自動適用しない。適用は人が承認後に人の手順で行う
