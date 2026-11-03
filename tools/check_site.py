"""サイトのデータ（data/*.json）と pdf/ が合っているか確かめる。push の前に実行する。

  python3 tools/check_site.py

- JSON が読めるか
- library.json の PDF が pdf/ にあるか、ファイル名が英数字だけか、ページ数が本当のページ数と同じか（pdfinfo）
- library.json の step が common.json にあるか、file がかぶっていないか
- 生徒の JSON の items が library.json にあるか、sets の id がかぶっていないか、cur（今ここ）が1つ以下か
- now.step・sets の steps が common.json にあるか、days が thu / mon か
- pdf/ にあるのに library.json に書かれていない PDF（警告だけ）
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
err, warn = [], []


def load(name):
    try:
        return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err.append(f"data/{name}.json が読めません: {e}")
        return None


def pages(f):
    try:
        out = subprocess.run(["pdfinfo", str(ROOT / "pdf" / f)], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        return int(m.group(1)) if m else None
    except FileNotFoundError:
        return None


common = load("common") or {}
lib = load("library") or {"items": []}
steps = {st["id"] for u in common.get("units", []) for st in u["steps"]}
allstep = [st["id"] for u in common.get("units", []) for st in u["steps"]]
if len(allstep) != len(set(allstep)):
    err.append("common.json: ステップの id がかぶっています")

files = {}
for it in lib["items"]:
    f = it.get("file", "")
    if f in files:
        err.append(f"library.json: {f} が2回書かれています")
    files[f] = it
    if it.get("step") not in steps:
        err.append(f"library.json {f}: step {it.get('step')!r} が common.json にありません")
    if not re.fullmatch(r"[A-Za-z0-9_.\-]+\.pdf", f):
        err.append(f"library.json: ファイル名は英数字だけにする: {f}")
    if not (ROOT / "pdf" / f).exists():
        err.append(f"library.json: pdf/{f} がありません")
        continue
    n = pages(f)
    if n is not None and n != it.get("pages"):
        err.append(f"library.json: {f} のページ数は {n} です（JSON は {it.get('pages')}）")

for t in common.get("students", []):
    d = load(t)
    if not d:
        continue
    for day in d.get("days", []):
        if day not in ("thu", "mon"):
            err.append(f"{t}.json: days に {day!r} は使えません（thu / mon）")
    if d.get("now") and d["now"].get("step") not in steps:
        err.append(f"{t}.json: now.step {d['now'].get('step')!r} が common.json にありません")
    ids = [s["id"] for s in d["sets"]]
    if len(ids) != len(set(ids)):
        err.append(f"{t}.json: sets の id がかぶっています {ids}")
    curs = [s["id"] for s in d["sets"] if s.get("cur")]
    if len(curs) > 1:
        err.append(f"{t}.json: cur（今ここ）が2つ以上あります {curs}")
    for s in d["sets"]:
        for st in s.get("steps", []):
            if st not in steps:
                err.append(f"{t}.json {s['label']}: step {st!r} が common.json にありません")
        for g in s["groups"]:
            if g["kind"] not in ("thu", "mon", "hw", "teacher"):
                err.append(f"{t}.json {s['label']}: kind {g['kind']!r} は thu / mon / hw / teacher のどれか")
            for r in g["items"]:
                if r["file"] not in files:
                    err.append(f"{t}.json {s['label']} {g['label']}: {r['file']} が library.json にありません")

for p in sorted((ROOT / "pdf").glob("*.pdf")):
    if p.name not in files:
        warn.append(f"pdf/{p.name} は library.json に書かれていません")

for w in warn:
    print("注意:", w)
for e in err:
    print("エラー:", e)
print("OK" if not err else f"{len(err)} 件のエラー")
sys.exit(1 if err else 0)
