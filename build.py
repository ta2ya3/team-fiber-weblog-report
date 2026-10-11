#!/usr/bin/env python3
"""parts/*.md と images/*.svg から README.md（md版）と report.html（人間用）を作る。外部通信なし。"""
import json, re, html, pathlib, markdown
R = pathlib.Path('/workspace/weblog-defense-run/report-parts')
P = pathlib.Path('/workspace/pseudo-logs/scenarios.json')
here = pathlib.Path(__file__).parent

# --- 改善ループ図 ---
steps = [("擬似ログ生成","題材と正解"),("WebLog解析","検知"),("WebLog対策","対策案"),("WebLog司法","審査"),("人 ta2ya","承認"),("WebLog立法","ルール改正案")]
w, bw = 900, 128
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="190" font-family="sans-serif" font-size="13">',
     '<text x="20" y="26" font-size="16" font-weight="bold">改善ループ（Grok Bot 5体＋人）</text>',
     '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#555"/></marker></defs>']
for i,(n,d) in enumerate(steps):
    x = 20 + i*146; col = "#fde68a" if n.startswith("人") else "#dbeafe"
    s.append(f'<rect x="{x}" y="50" width="{bw}" height="56" rx="8" fill="{col}" stroke="#555"/>')
    s.append(f'<text x="{x+bw/2}" y="74" text-anchor="middle" font-weight="bold">{n}</text><text x="{x+bw/2}" y="94" text-anchor="middle">{d}</text>')
    if i < len(steps)-1: s.append(f'<line x1="{x+bw}" y1="78" x2="{x+146}" y2="78" stroke="#555" marker-end="url(#a)"/>')
lx = 20+5*146+bw/2
s.append(f'<path d="M{lx},106 L{lx},150 L{20+146+bw/2},150 L{20+146+bw/2},110" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#a)"/>')
s.append(f'<text x="{(lx+20+146)/2+40}" y="170" text-anchor="middle" fill="#2563eb">人が採用 → 再解析・対策追記・再審査（1周目を実施）</text></svg>')
(here/'images/loop.svg').write_text('\n'.join(s), encoding='utf-8')

# --- シナリオ内訳 ---
sc = json.load(open(P, encoding='utf-8'))
det = sum(1 for x in sc if x['detect'] is True and x.get('type') not in (None,'normal'))
normal = [x for x in sc if x.get('type') in (None,'-','normal')]
miss = len(sc) - det - len(normal)
bars = [("現行ルールで検知される", det, "#16a34a"), ("現行ルールではすり抜ける", miss, "#dc2626"), ("正常（誤検知の確認用）", len(normal), "#9ca3af")]
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="170" font-family="sans-serif" font-size="13">',
     f'<text x="20" y="26" font-size="16" font-weight="bold">擬似ログの18シナリオの内訳（改正前のルール W1〜W6 で判定）</text>']
for i,(n,v,c) in enumerate(bars):
    y = 50 + i*36
    s.append(f'<text x="20" y="{y+14}">{n}</text><rect x="230" y="{y}" width="{v*25}" height="20" fill="{c}"/><text x="{236+v*25}" y="{y+15}">{v}件</text>')
s.append('</svg>')
(here/'images/scenarios.svg').write_text('\n'.join(s), encoding='utf-8')

rows = "\n".join(f"| {x['id']} | {x['name']} | [{'出典'}]({x['source_url']}) | {'検知' if x['detect'] is True else ('正常' if x in normal else 'すり抜け')} |" for x in sc)

def part(p):
    t = (R/p).read_text(encoding='utf-8')
    t = re.sub(r'^#{1,2} ', '### ', t, flags=re.M)  # 見出しを下げる
    t = re.sub(r'!\[([^\]]*)\]\(([^)/]+\.svg)\)', r'![\1](images/\2)', t)
    t = re.sub(r'\n承認: 人の承認が必要（未）\s*$', '\n', t)
    return t

md = f"""# Webアクセスログ攻撃検知・対策提案チーム 成果レポート

- **チーム名:** team_fiber
- **イベント:** Grok Bot Tokyo Hackathon（2026-10-11）
- **参加者:** （あとで追記）
- **成果物:** [kzhr-77/team_fiber（ma-san/weblog-defense ブランチ）](https://github.com/kzhr-77/team_fiber/tree/ma-san/weblog-defense) ／ 擬似ログ・正解データ [ta2ya3/web-attack-pseudo-logs](https://github.com/ta2ya3/web-attack-pseudo-logs)
- **人間用の見やすい版:** `report.html`（ブラウザで開く）

## 1. 要約
Grok Bot 5体が「立法・行政・司法」の三権分立で役割を分け、互いの成果物をチェックしながら Web アクセスログの攻撃検知と対策提案を行いました。最後の判断は人が行います。2025〜2026年に実際にニュースになった攻撃をもとにした擬似ログ（2,543行）で1周回したところ、次のようになりました。

| 指標 | 改正前 | 改正後（人が採用したルール） |
|---|---:|---:|
| 検知件数 | 33 | 55 |
| 正解の検知行のカバー | 33/44（75.0%） | 43/44（97.7%） |
| 想定インシデントとの一致 | 7/11 | 11/11 |
| 攻撃でない行への誤検知 | 0 | 0 |
| 対策案 | 9件 | 13件 |
| 司法の審査 | — | 全成果物 PASS（NG 0件、`check.sh` exit=0） |

改正後の数字は手元のコピーで動かした試算です。本番のルールファイルと `analyze.py` にはまだ反映していません（詳しくは「6. 注意点」を参照）。

![改正前と改正後の検知性能](images/before-after.svg)

## 2. チーム構成と改善ループ
![改善ループ](images/loop.svg)

| Bot | 役割 | 主な成果物 | Skill |
|---|---|---|---|
| 擬似ログ生成 | 実在の攻撃ニュースをもとに、擬似ログ・正解・検知漏れ一覧を作る。全体のとりまとめ | `access_log`, `expected_report.json`, `missed_attacks.md`, 本レポート | `tools/generate_logs.py`（seed を固定して再現できる） |
| WebLog解析（行政） | ルールに当てて攻撃の「疑い」を行番号とルール番号付きで出し、正解と照合する | `analysis.md`, `gap.md`, `reanalysis.md` | `skills/log-analyzer` |
| WebLog対策（行政） | 対策「案」を深刻度順に作る。適用はしない | 対策レポート v1〜v3 | `skills/countermeasure-proposer` |
| WebLog司法 | R10〜R12 と `check.sh` で、根拠のない検知・断定・自動適用を差し戻す | `judiciary.txt` | `judiciary/check.sh`、行番号と数値の全件照合 |
| WebLog立法 | 検知漏れからルールの改正案を作り、効果を試算する | `rule-proposals.md`, 採用ルール | `ai-dev-hotl-governance` |
| 人（ta2ya） | 改正案の採用と、対策の最終承認 | — | — |

## 3. 題材：最新の攻撃ニュースをもとにした擬似ログ
IP アドレスは文書用の範囲だけを使い、攻撃コードは含めていません。ログに残る痕跡だけを再現しています。

![シナリオの内訳](images/scenarios.svg)

| ID | シナリオ | 元ネタ | 改正前のルールでの判定 |
|---|---|---|---|
{rows}

## 4. 解析
{part('analysis/analysis.md')}

## 5. 立法：ルールの改正
{part('legislative/legislative.md')}

## 6. 対策
{part('countermeasure/countermeasure.md')}

## 7. 司法の審査記録
| 対象 | 結果 |
|---|---|
| 対策レポート v1 | PASS（任意の改善点2つ） |
| 対策レポート v2 | PASS |
| 提出下書き v1 | NG 1件（司法の Skill が書かれていない）→ v2 で修正 → PASS |
| 対策レポート v3・再解析・提出下書き v3 | PASS（NG 0件。55件の検知は立法と解析で1行も違わない） |
| 本レポート（README.md・report.html） | PASS（NG 0件。グラフ6枚の数字が元データと一致、HTMLのエスケープとCSPを確認） |

全記録は [`sources/judiciary.txt`](sources/judiciary.txt) にあります。

## 8. 注意点と今後
- 改正後のルールは手元のコピー（[`sources/detection-rules.adopted.tsv`](sources/detection-rules.adopted.tsv)）にだけ反映しています。W4 の60秒窓・W9・W11 は試算エンジンでしか動かないため、本番で使うには `analyze.py` の改修が必要です（今の `analyze.py` では54件になり、W11 は出ません）。
- 対策13件はすべて提案で、設定やサーバーには何も反映していません。

承認: 人の承認が必要（未）
"""
(here/'README.md').write_text(md, encoding='utf-8')

# --- HTML（生HTMLを無効化し、ログ内の文字列は必ずエスケープ） ---
m = markdown.Markdown(extensions=['tables','fenced_code'])
m.preprocessors.deregister('html_block'); m.inlinePatterns.deregister('html')
body = m.convert(md)
def inline_svg(mo):
    return '<figure>' + (here/mo.group(1)).read_text(encoding='utf-8') + '</figure>'
body = re.sub(r'<img alt="[^"]*" src="(images/[^"]+\.svg)"\s*/?>', inline_svg, body)
page = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:;">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>team_fiber Webログ攻撃検知・対策提案 成果レポート</title>
<style>body{{font-family:-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif;max-width:980px;margin:2em auto;padding:0 1em;line-height:1.7;color:#1f2937}}
h1{{border-bottom:4px solid #2563eb;padding-bottom:.3em}}h2{{border-left:6px solid #2563eb;padding-left:.5em;margin-top:2.2em}}
table{{border-collapse:collapse;width:100%;font-size:.92em;margin:1em 0}}th,td{{border:1px solid #d1d5db;padding:.4em .6em;vertical-align:top}}th{{background:#eff6ff}}
tr:nth-child(even) td{{background:#f9fafb}}code{{background:#f3f4f6;padding:.1em .3em;border-radius:4px;font-size:.9em}}
figure{{margin:1.2em 0;overflow-x:auto;background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:.6em}}</style></head><body>
{body}</body></html>"""
(here/'report.html').write_text(page, encoding='utf-8')
print("ok")
