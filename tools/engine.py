#!/usr/bin/env python3
"""試算用エンジン（作業用コピー）。本物の analyze.py / detection-rules.tsv には触れない。
- base モード: skills/log-analyzer/analyze.py と同一の判定（正規表現は「生の行」に re.search、W4 は時間窓なし・同一IP合計5回以上）。
  → verify_baseline.sh で本物の analyze.py と出力が一致することを確認する。
- 拡張（提案用）: decode=multi（多重URLデコード後にも正規表現を当てる）、W4 時間窓版、W9 低速、W10 分散、W11 総当たり後成功。
使い方: engine.py --input LOG --rules base.tsv [--overlay P1.tsv ...] [--json out.json]
overlay は同じ ID を置換、新しい ID を追加。"#!engine<TAB>key=value" 行でエンジン機能を有効化。"""
import re, sys, json, argparse, collections, datetime
from urllib.parse import unquote

def load_rules(path, rules, flags):
    for l in open(path, encoding="utf-8"):
        l = l.rstrip("\n")
        if l.startswith("#!engine"):
            for kv in l.split("\t")[1:]:
                k, _, v = kv.partition("="); flags[k] = v
            continue
        if not l.strip() or l.startswith("#"): continue
        rid, name, typ, pat = l.split("\t")
        rules[rid] = (rid, name, typ, pat)

LINE = re.compile(r'^(\S+) \S+ (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) ')
def parse(l):
    m = LINE.match(l)
    if not m: return None
    ip, user, ts, req, st = m.groups()
    t = datetime.datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")
    parts = req.split(" ")
    method = parts[0]; path = parts[1] if len(parts) > 1 else ""
    m2 = re.search(r"[?&]username=([^& ]+)", path)
    uname = m2.group(1) if m2 else (user if user != "-" else None)
    return dict(ip=ip, t=t, method=method, path=path, route=path.split("?")[0], status=int(st), user=uname)

def multidecode(s, n=3):
    for _ in range(n):
        d = unquote(s)
        if d == s: break
        s = d
    return s

def run(log, rules, flags):
    hits = []  # (rid, name, line, src, covered_lines)
    recs = [parse(l) for l in log]
    decode = flags.get("decode") == "multi"
    for n, l in enumerate(log, 1):
        ip = l.split()[0]
        dl = multidecode(l) if decode else None
        for rid, name, typ, pat in rules.values():
            if typ != "regex": continue
            if re.search(pat, l) or (decode and dl != l and re.search(pat, dl)):
                hits.append((rid, name, n, ip, [n]))
    # ---- 総当たり系 ----
    w4 = rules.get("W4")
    w4_windowed = w4 is not None and "60秒" in w4[3]
    def is_login(r):  # 本物の analyze.py は '"POST /login' の前方一致（/login-action も含む）
        return r and r["method"] == "POST" and (r["route"] == "/login" if w4_windowed else r["path"].startswith("/login"))
    fails = collections.defaultdict(list)
    for n, r in enumerate(recs, 1):
        if is_login(r) and r["status"] == 401: fails[r["ip"]].append(n)
    bf_groups = {}  # ip -> lines
    def window_groups(ns, sec, minc, minu):
        """同一IPの401列から、sec秒窓で minc回以上かつユーザー名 minu 種以上を満たす行の集合"""
        out = set()
        for i in range(len(ns)):
            j = i
            while j + 1 < len(ns) and (recs[ns[j+1]-1]["t"] - recs[ns[i]-1]["t"]).total_seconds() <= sec: j += 1
            win = ns[i:j+1]
            if len(win) >= minc and len({recs[k-1]["user"] for k in win}) >= minu: out.update(win)
        return sorted(out)
    if w4 is not None:
        for ip, ns in fails.items():
            if w4_windowed:
                g = window_groups(ns, 60, 5, 2)
            else:
                g = ns if len(ns) >= 5 else []
            if g:
                hits.append(("W4", w4[1], g[0], ip + f"（L{g[0]}〜L{g[-1]} で {len(g)}回）", g)); bf_groups[ip] = g
    if "W9" in rules:
        for ip, ns in fails.items():
            g = [k for k in window_groups(ns, 900, 5, 3) if k not in bf_groups.get(ip, [])]
            if g and not bf_groups.get(ip):
                hits.append(("W9", rules["W9"][1], g[0], ip + f"（L{g[0]}〜L{g[-1]} で {len(g)}回）", g)); bf_groups[ip] = g
    if "W10" in rules:
        mm = re.search(r"(\d+)分以内", rules["W10"][3]); wsec = int(mm.group(1)) * 60 if mm else 300
        ev = [(n, recs[n-1]) for ns in fails.values() for n in ns]; ev.sort()
        marked = set()
        for i, (n, r) in enumerate(ev):
            win = [(k, q) for k, q in ev if 0 <= (q["t"] - r["t"]).total_seconds() <= wsec]
            cnt = collections.Counter(q["ip"] for _, q in win)
            single = [(k, q) for k, q in win if cnt[q["ip"]] <= 2 and q["ip"] not in bf_groups]
            if len({q["ip"] for _, q in single}) >= 5 and len({q["user"] for _, q in single}) >= 5:
                marked.update(k for k, _ in single)
        if marked:
            m = sorted(marked)
            ips = sorted({recs[k-1]["ip"] for k in m})
            hits.append(("W10", rules["W10"][1], m[0], f"複数IP {len(ips)}件（L{m[0]}〜L{m[-1]} で {len(m)}回）", m))
    if "W11" in rules:
        for ip, g in bf_groups.items():
            last = recs[g[-1]-1]["t"]
            for n, r in enumerate(recs, 1):
                if n > g[-1] and r and r["ip"] == ip and r["method"] == "POST" and r["route"] == "/login" \
                   and r["status"] in (200, 302) and (r["t"] - last).total_seconds() <= 600:
                    hits.append(("W11", rules["W11"][1], n, ip, [n])); break
    hits.sort(key=lambda h: h[2])
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True); ap.add_argument("--rules", required=True)
    ap.add_argument("--overlay", action="append", default=[]); ap.add_argument("--json")
    a = ap.parse_args()
    rules, flags = collections.OrderedDict(), {}
    load_rules(a.rules, rules, flags)
    for o in a.overlay: load_rules(o, rules, flags)
    log = open(a.input, encoding="utf-8").read().splitlines()
    hits = run(log, rules, flags)
    print(f"# 検知結果（入力 {a.input}、{len(hits)}件、行数 {len(log)}）")
    for rid, name, n, src, _ in hits: print(f"- 検知 [{rid}] {name} / 根拠 L{n} / 送信元 {src}")
    print("\n## ルール別件数")
    for rid, c in sorted(collections.Counter(h[0] for h in hits).items(), key=lambda x: int(x[0][1:])): print(f"- {rid}: {c}")
    if a.json:
        json.dump([dict(rule=h[0], line=h[2], src=h[3], lines=h[4]) for h in hits], open(a.json, "w"), ensure_ascii=False)

if __name__ == "__main__": main()
