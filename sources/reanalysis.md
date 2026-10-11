# 再解析レポート（改正ルール採用後）— WebLog解析

- 実施: 2026-10-11 15:16 JST、ta2ya さんの改正案採用（推奨セット）を受けて
- 入力: `/workspace/pseudo-logs/access_log`（2543行、変更なし）
- ルール: `/workspace/weblog-defense-run/trial/adopted/detection-rules.adopted.tsv`（手元のコピー。本物の TSV・analyze.py は変更なし、push なし）
- 実行:
  - `python3 trial/engine.py --input /workspace/pseudo-logs/access_log --rules trial/adopted/detection-rules.adopted.tsv` → `engine_out.txt`（55件、立法の `adopted/detections.txt` と完全一致）
  - 参考: `analyze.py --rules <同TSV>` → `analyze_py_out.txt`（54件）。analyze.py は W4 の60秒窓・W9・W11 に対応していないため、L323–328 を W4 として数え、W11 は出ない。本レポートの数字は engine.py の結果

## 改正前と改正後
| 指標 | 改正前（W1〜W6, analyze.py） | 改正後（engine.py） |
|---|---:|---:|
| 検知件数 | 33 | 55 |
| 期待検知行のカバー（/44） | 33（75.0%） | 43（97.7%） |
| 攻撃行のカバー（/74） | 39 | 52 |
| 攻撃でない行への誤検知（/2469） | 0 | 0 |
| 期待インシデントとの一致（/11） | 7 | 11 |

ルール別件数（改正後）: W1 5、W2 5、W3 5、W4 1、W5 16、W6 12、W7 6、W8 3、W9 1、W11 1

## 新しく拾えた主な攻撃の疑い
- W1: L50（UNION ALL SELECT）、L499（EXTRACTVALUE）
- W5/W6: L135（`/actuator/env`、nuclei の UA）、L246–249（nuclei の UA）
- W7（新設）: L100（FortiWeb）、L217・L219・L220（SharePoint ToolShell）、L248–249（Next.js RSC）
- W8（新設）: L280・L281・L302（多重URLエンコード）
- W9（新設）: L323–328（198.51.100.30、60秒窓の外の低速な総当たり。改正前は W4 に時間窓がなく、期待値とずれていた）
- W11（新設）: L175（8回の失敗の直後のログイン成功）

## 残った課題
- 期待検知行で拾えていないのは L218（SharePoint の `SignOut.aspx`）の1行。単体では正常なアクセスと区別できないため、意図的に対象外
- 検知の表記はすべて「〜の疑い」（R11）
- W4 の60秒窓・W9・W11 を本番で使うには `analyze.py` の改修が必要（人の判断事項）
