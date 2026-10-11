#!/usr/bin/env python3
"""ダミーアクセスログを検知ルール(TSV)で解析し、根拠行番号・ルール番号付きのレポートを出す。外部通信なし。
使い方: analyze.py --input <access.log> [--rules <rules.tsv>]
環境変数 WEBLOG_INPUT / WEBLOG_RULES でも指定可。"""
import re,sys,os,argparse,collections
ap=argparse.ArgumentParser();ap.add_argument("--input",default=os.environ.get("WEBLOG_INPUT"))
ap.add_argument("--rules",default=os.environ.get("WEBLOG_RULES","goals/weblog-defense/rules/detection-rules.tsv"))
a=ap.parse_args()
if not a.input: sys.exit("--input か WEBLOG_INPUT でログを指定してください")
rules=[l.rstrip("\n").split("\t") for l in open(a.rules) if l.strip() and not l.startswith("#")]
log=open(a.input).read().splitlines()
hits=[];fails=collections.defaultdict(list)
for n,l in enumerate(log,1):
    ip=l.split()[0]
    for rid,name,typ,pat in rules:
        if typ=="regex" and re.search(pat,l): hits.append((rid,name,n,ip))
    if '"POST /login' in l and '" 401 ' in l: fails[ip].append(n)
for ip,ns in fails.items():
    if len(ns)>=5: hits.append(("W4","総当たり（ログイン失敗）",ns[0],ip+f"（L{ns[0]}〜L{ns[-1]} で {len(ns)}回）"))
hits.sort(key=lambda h:h[2])
print(f"# 検知結果（入力 {a.input}、{len(hits)}件、行数 {len(log)}）")
for rid,name,n,ip in hits: print(f"- 検知 [{rid}] {name} / 根拠 L{n} / 送信元 {ip}")
print("\n## ルール別件数")
for rid,c in sorted(collections.Counter(h[0] for h in hits).items()): print(f"- {rid}: {c}")
