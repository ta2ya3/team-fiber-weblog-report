#!/usr/bin/env bash
# 司法（機械チェック）: RULES.md の R1〜R12 を検査。違反があれば exit 1。
set -u; cd "$(dirname "$0")/.."; fail=0
ng(){ echo "NG [$1] $2"; fail=1; }
for g in goals/*/; do
  prev="承認済み"
  for d in "$g"0*-*/; do
    f="$d/output.md"; [ -f "$f" ] || { ng R1 "$f がない"; continue; }
    grep -q '^## 承認' "$f" || ng R1 "$f に承認欄がない"
    st=$(grep -m1 '^状態:' "$f" | sed 's/状態: *//'); ap=$(grep -m1 '^承認者:' "$f" | sed 's/承認者: *//')
    [ -n "$st" ] || ng R1 "$f に状態がない"
    if [ "$st" = "承認済み" ] && echo "$ap" | grep -qiE '^$|AI|bot|grok|未'; then ng R2 "$f 承認者が人でない: '$ap'"; fi
    if [ "$prev" != "承認済み" ] && ! echo "$prev" | grep -q "デモとして" && ! echo "$st" | grep -qE '^(未着手|停止中)'; then ng R4 "$f 前段未承認なのに状態='$st'"; fi
    case "$d" in *01-collection*) grep -qE 'https?://|#[0-9]+' "$f" || ng R5 "$f に出典がない";; esac
    prev="$st"
  done
done
for d in templates/goal/0{1,2,3,4}-*; do grep -q "^## 承認" "$d/output.md" 2>/dev/null || ng R7 "テンプレート $d に承認欄がない"; done
# R9 成果物（行政の出力）の禁止事項
for f in goals/*/03-construction/deliverables/*.md; do [ -f "$f" ] || continue
  grep -nE '安全です|リンクを(押して|クリックして)|パスワードを(入力|教えて)' "$f" && ng R9 "$f 禁止表現（安全の断定／リンク誘導／パスワード要求）"
  grep -q '公式アプリ' "$f" || ng R9 "$f 『公式アプリから確認』の案内がない"
  grep -q '司法チェック: ' "$f" || ng R9 "$f 根拠条番号の欄がない"
done
# R10-R12 Webログ検知レポート
for f in goals/*/04-operation/reports/*.md; do [ -f "$f" ] || continue
  grep -n '^- 検知' "$f" | grep -vE 'L[0-9]+' | grep -vE 'W[0-9]+' >/dev/null; \
  grep -n '^- 検知' "$f" | grep -vE 'L[0-9]+.*|.*L[0-9]+' | sed 's/^/  /' | grep . && ng R10 "$f 根拠の行番号がない検知（誤検知の疑い）"
  grep -n '^- 検知' "$f" | grep -vE 'W[0-9]+' | sed 's/^/  /' | grep . && ng R10 "$f ルール番号がない検知"
  grep -nE '確実に|間違いなく|100 ?%|攻撃者である' "$f" && ng R11 "$f 断定表現"
  grep -niE '適用しました|自動で(適用|反映)|自動反映|\bapply\b|即時適用' "$f" && ng R12 "$f 危険な自動適用の指示"
  grep -q '^承認: 人の承認が必要' "$f" || ng R12 "$f 人の承認欄がない"
done
grep -rnIE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bp]-|AKIA[0-9A-Z]{16}|password\s*=)' --exclude-dir=.git --exclude=check.sh --exclude=RULES.md . && ng R3 "秘密らしき文字列"
[ $fail = 0 ] && echo "PASS 司法チェック（R1〜R12）" ; exit $fail
