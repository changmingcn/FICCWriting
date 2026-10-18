#!/usr/bin/env python3
"""汉字与英文、数字之间不留空格（用户 2026-10-08 裁定「不留」）。确定性、可重跑、幂等、可自证。

用法：
    python3 cjk_space.py --check <file...>    # 只报每份需改处数，不写；有需改则退出码 1
    python3 cjk_space.py --apply <file...>    # 原位删除并自证；自证不过拒绝写盘，退出码 2
    --include-quotes                           # 连「>」开头的引用行一起改（默认不动：多为作者原文）
    --show N                                   # 每份列出前 N 处上下文（--check 默认 5，--apply 默认 0）
    --near                                     # 另列汉字与 ASCII 符号（% ` * ) 等）之间的空格，只报不改

规则：汉字（U+4E00–U+9FFF）与 ASCII 字母数字之间的半角空格／制表符删掉，两个方向都删；
    数字后紧跟的 % 算数字的一部分，它与后面汉字之间的空格也删（2026-10-08 追加）。
    「2025 年 11 月」→「2025年11月」；「Dealer 只是躺平」→「Dealer只是躺平」；「99% 的时候」→「99%的时候」。
不动：
    围栏代码块（``` 与 ~~~）、行内代码（`…`）、URL、Markdown 链接目标 ](…)、HTML 注释；
    以「>」开头的行（作者原文引用，--include-quotes 才动）；
    两个 ASCII 词之间的空格（Front Run）；表格竖线两侧的空格；汉字与汉字之间；
    汉字与标点、反引号、强调符、前面不是数字的 % 之间（--near 可列出）；全角空格 U+3000；换行。
    受保护片段两侧的空格也不动（URL 后紧贴汉字会被自动链接吞进去）。

自证（照搬 punct_normalize.py「剥掉被改元素后逐字符比对」，三道任一不过即不写盘）：
    一、改前改后各去掉全部空白，逐字符一致——只可能动了空白；
    二、改后文本＝改前文本删去若干半角空格／制表符——只删不加，换行数不变；
    三、受保护的行与片段（引用行、代码、URL、链接目标）改前改后逐字节一致。
"""
import argparse, io, re, sys

HAN, ALNUM = "一-鿿", "A-Za-z0-9"
GAP = re.compile(rf"(?<=[{HAN}])[ \t]+(?=[{ALNUM}])|(?<=[{ALNUM}])[ \t]+(?=[{HAN}])"
                 rf"|(?<=[0-9]%)[ \t]+(?=[{HAN}])")    # 数字后紧跟的 %：「99% 的时候」→「99%的时候」
SYM = r"!-/:-@\[-`{}~"                  # ASCII 符号，不含表格竖线 |
NEAR = re.compile(rf"(?<=[{HAN}])[ \t]+(?=[{SYM}])|(?<=[{SYM}])[ \t]+(?=[{HAN}])")
MDMARK = re.compile(r"[ \t]*(?:#{1,6}|[-*+]|\d+[.)])$")
FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
QUOTE = re.compile(r"^[ \t]*>")
GUARD = re.compile("|".join([
    r"<!--.*?-->",                     # HTML 注释（可跨行）
    r"``[^\n]*?``", r"`[^`\n]*`",      # 行内代码
    r"!?\]\([^)\n]*\)",                # 链接／图片目标
    r"<(?:https?|ftp)://[^>\s]*>",     # 尖括号自动链接
    r"(?:https?|ftp)://\S+",           # 裸 URL
]), re.S)


def _flat(s):
    return re.sub(r"[\x00\n]", " ", s)


def _ctx(s, m, w=8):
    """同一行内的上下文，被删的空白记作 ␣。"""
    a = max(s.rfind("\n", 0, m.start()) + 1, m.start() - w)
    e = s.find("\n", m.end()); e = len(s) if e < 0 else e
    return s[a:m.start()] + "␣" + s[m.end():min(e, m.end() + w)]


def segments(text, include_quotes):
    """按行切成 (可改?, 片段)；围栏代码与引用行整行不可改。"""
    out, buf, fence = [], [], None
    def flush():
        if buf: out.append((True, "".join(buf))); buf.clear()
    for line in text.splitlines(keepends=True):
        if fence:
            out.append((False, line))
            if re.match(rf"^[ \t]{{0,3}}{re.escape(fence[0])}{{{len(fence)},}}[ \t]*$", line.rstrip("\r\n")):
                fence = None
            continue
        m = FENCE.match(line)
        if m:
            flush(); fence = m.group(1); out.append((False, line)); continue
        if not include_quotes and QUOTE.match(line):
            flush(); out.append((False, line)); continue
        buf.append(line)
    flush()
    return out


def convert(text, include_quotes, show=0, near=False):
    """返回 (新文本, 处数, 受保护片段表, 例子, 近似处)。"""
    new, count, guarded, examples, nears = [], 0, [], [], []
    lineno = 1
    for editable, seg in segments(text, include_quotes):
        if not editable:
            guarded.append(seg); new.append(seg); lineno += seg.count("\n"); continue
        spans = []
        def hide(m):
            spans.append(m.group(0)); guarded.append(m.group(0)); return f"\x00{len(spans)-1}\x00"
        masked = GUARD.sub(hide, seg)
        for m in GAP.finditer(masked):
            count += 1
            if len(examples) < show:
                ln = lineno + masked.count("\n", 0, m.start())
                ctx = _ctx(masked, m)
                examples.append(f"L{ln}: {_flat(ctx)}")
        if near:
            gaps = {g.start() for g in GAP.finditer(masked)}
            for m in NEAR.finditer(masked):
                if m.start() in gaps:
                    continue                   # 已归规则（如「99% 的」），不重复列
                if MDMARK.match(masked, masked.rfind("\n", 0, m.start()) + 1, m.start()):
                    continue                   # 「## 」「- 」「1. 」这类 Markdown 结构，不算
                ln = lineno + masked.count("\n", 0, m.start())
                ctx = _ctx(masked, m)
                nears.append(f"L{ln}: {_flat(ctx)}")
        out = GAP.sub("", masked)
        new.append(re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], out))
        lineno += seg.count("\n")
    return "".join(new), count, guarded, examples, nears


def only_deleted_blanks(a, b):
    """b 能否由 a 只删去半角空格／制表符得到。"""
    if a.count("\n") != b.count("\n"):
        return False
    i, n = 0, len(a)
    for ch in b:
        while i < n and a[i] != ch:
            if a[i] not in " \t":
                return False
            i += 1
        if i == n:
            return False
        i += 1
    return all(c in " \t" for c in a[i:])


def run(path, apply_, include_quotes, show, near):
    src = io.open(path, encoding="utf-8", newline="").read()
    name = path.rsplit("/", 1)[-1]
    if "\x00" in src:
        print(f"!! {name}: 含 NUL 字符，跳过"); return 0, False
    new, count, guarded, examples, nears = convert(src, include_quotes, show, near)
    ws = lambda s: re.sub(r"\s+", "", s)
    ok1 = ws(src) == ws(new)
    ok2 = only_deleted_blanks(src, new)
    ok3 = convert(new, include_quotes)[2] == guarded
    ok4 = convert(new, include_quotes)[1] == 0          # 幂等：改后再查为 0
    ok = ok1 and ok2 and ok3 and ok4
    print(f"{'OK' if ok else '!!'} 需改 {count:>4} 处  {name}")
    for e in examples:
        print(f"     {e}")
    if near:
        print(f"     （另有汉字与 ASCII 符号之间的空格 {len(nears)} 处，规则不改，只列出）")
        for e in nears:
            print(f"     ~ {e}")
    if not ok1: print("     ⚠ 自证一失败：去掉全部空白后前后不一致 —— 不写盘")
    if not ok2: print("     ⚠ 自证二失败：改动不只是删去半角空格／制表符 —— 不写盘")
    if not ok3: print("     ⚠ 自证三失败：受保护的行或片段有变化 —— 不写盘")
    if not ok4: print("     ⚠ 幂等失败：改后再查仍有需改处 —— 不写盘")
    if apply_ and count and ok:
        io.open(path, "w", encoding="utf-8", newline="").write(new)
        print(f"     → 已写入（{len(src):,} → {len(new):,} 字符，删去空白 {len(src)-len(new)} 个）"
              f"；自证一二三与幂等均通过")
    return count, ok


def main():
    ap = argparse.ArgumentParser(description="汉字与英文、数字之间不留空格（可自证）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="只报需改处数；有需改则退出码 1")
    g.add_argument("--apply", action="store_true", help="原位改写，自证通过才写盘")
    ap.add_argument("--include-quotes", action="store_true", help="连「>」开头的引用行一起改")
    ap.add_argument("--show", type=int, default=None, help="每份列出前 N 处上下文")
    ap.add_argument("--near", action="store_true", help="另列汉字与 ASCII 符号之间的空格（不改）")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    show = a.show if a.show is not None else (5 if a.check else 0)
    total, bad = 0, 0
    for f in a.files:
        c, ok = run(f, a.apply, a.include_quotes, show, a.near)
        total += c; bad += 0 if ok else 1
    verb = "已改" if a.apply else "需改"
    print(f"\n合计{verb} {total:,} 处；自证失败 {bad} 份")
    if bad:
        sys.exit(2)
    sys.exit(1 if (a.check and total) else 0)


if __name__ == "__main__":
    main()
