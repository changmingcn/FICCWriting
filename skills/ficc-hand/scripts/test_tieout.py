#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_tieout.py: 逐例跑 tieout_probes.json 回归集，走 tieout.py 的命令行，对比预期；全过才退出 0。

用法：
    python3 test_tieout.py                     # 跑同目录 tieout.py，再核 --self-test 与本结果一致
    python3 test_tieout.py --script <tieout.py> # 跑别的版本（如修前），只报结果，不核自检
    python3 test_tieout.py --markdown          # 另打一张“编号｜预期｜实际｜结果”的表

比什么：退出码；未匹配 [类, 词元]；待核词元；写法不认行数；目标行数（预期里有才比）。行号不比。
自检一致：同目录 tieout.py --self-test 必须退出 0、用例数与回归集相同，且本程序全过；三者不一致即失败。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MISS_KINDS = {"日期", "年月", "数", "名称"}


def run_case(script, case, tmp):
    o = os.path.join(tmp, "outline.md")
    with open(o, "w", encoding="utf-8") as f:
        f.write(case["outline"])
    against = case["against"] if isinstance(case["against"], list) else [case["against"]]
    paths = []
    for k, text in enumerate(against):
        p = os.path.join(tmp, f"against{k}.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        paths.append(p)
    r = subprocess.run([sys.executable, "-B", script, "--outline", o, "--against", *paths],
                       capture_output=True, text=True)
    misses, pending, loose, targets = [], [], 0, None
    for line in r.stdout.splitlines():
        cols = line.split("\t")
        if len(cols) == 4 and re.fullmatch(r"L\d+", cols[0]):
            kind, tok = cols[1], cols[2]
            if kind in MISS_KINDS:
                misses.append([kind, tok])
            elif kind == "待核":
                pending.append(tok.split("（")[0])
            elif kind == "未检查":
                loose += 1
        m = re.match(r"查了 (\d+) 行", line)
        if m:
            targets = int(m.group(1))
    return {"exit": r.returncode, "misses": sorted(misses), "pending": sorted(pending),
            "unchecked": loose, "targets": targets, "stderr": r.stderr.strip()}


def diff(exp, got):
    out = []
    if got["exit"] != exp["exit"]:
        out.append(f"退出码 {got['exit']}≠{exp['exit']}")
    if got["misses"] != sorted(exp.get("misses", [])):
        out.append(f"未匹配 {got['misses']}≠{sorted(exp.get('misses', []))}")
    if got["pending"] != sorted(exp.get("pending", [])):
        out.append(f"待核 {got['pending']}≠{sorted(exp.get('pending', []))}")
    if exp.get("unchecked") is not None and got["unchecked"] != exp["unchecked"]:
        out.append(f"写法不认 {got['unchecked']}≠{exp['unchecked']}")
    if exp.get("targets") is not None and got["targets"] != exp["targets"]:
        out.append(f"目标行 {got['targets']}≠{exp['targets']}")
    return out


def brief(r):
    parts = [f"退出{r['exit']}"]
    if r["misses"]:
        parts.append("缺" + "、".join(t for _, t in r["misses"]))
    if r.get("pending"):
        parts.append("待核" + "、".join(r["pending"]))
    if r.get("unchecked"):
        parts.append(f"不认{r['unchecked']}")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--script", default=os.path.join(HERE, "tieout.py"))
    ap.add_argument("--probes", default=os.path.join(HERE, "tieout_probes.json"))
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()
    with open(a.probes, encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    own = os.path.abspath(a.script) == os.path.join(HERE, "tieout.py")
    n_fail, rows = 0, []
    with tempfile.TemporaryDirectory() as tmp:
        for case in cases:
            got = run_case(a.script, case, tmp)
            d = diff(case["expect"], got)
            n_fail += bool(d)
            print(f"{'FAIL' if d else 'PASS'}  {case['id']}: {brief(got)}" + (f"  ｜{'；'.join(d)}" if d else ""))
            rows.append((case["id"], brief(case["expect"]), brief(got), "过" if not d else "不过"))
    print(f"回归集 {len(cases)} 例：通过 {len(cases) - n_fail}，失败 {n_fail}（脚本 {a.script}）")
    ok = n_fail == 0
    if own:
        r = subprocess.run([sys.executable, "-B", a.script, "--self-test"], capture_output=True, text=True)
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()
        m = re.search(r"(\d+) 例，失败 (\d+) 例", last)
        same = (r.returncode == 0) == ok and m is not None and int(m.group(1)) == len(cases) \
            and (int(m.group(2)) == 0) == ok
        print(f"--self-test：退出 {r.returncode}；{last}")
        print("自检与回归集一致" if same else "自检与回归集不一致")
        ok = ok and same
    else:
        print("（--script 指向别的版本：不核自检）")
    if a.markdown:
        print("\n| 编号 | 预期 | 实际 | 结果 |\n|---|---|---|---|")
        for row in rows:
            print("| " + " | ".join(row) + " |")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
