#!/usr/bin/env python3
"""扫描本仓库全部图示 HTML，读取其 <!--@visual ... --> 元信息，生成导航首页 index.html。

用法:
    python3 tools/build_index.py

特性:
- 零第三方依赖（仅标准库）
- 递归扫描，跳过 index.html 自身与 00-模板/ 目录
- 按知识点(topic)分组，卡片式展示，附搜索框与关键词
- 读取每个文件的 title/topic/grade/child/keywords/created
"""
import html
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_RE = re.compile(r"<!--@visual\s*(.*?)-->", re.S)
SKIP_DIRS = {"00-模板", "tools", "docs", ".git"}

FIELDS = ["title", "topic", "grade", "child", "keywords", "created"]


def parse_meta(path):
    try:
        text = open(path, encoding="utf-8").read(4000)
    except OSError:
        return None
    m = META_RE.search(text)
    items = {}
    if m:
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            k, v = line.split(":", 1)
            items[k.strip()] = v.strip()
    if not items.get("title"):
        # 没有元信息头：退回用 <title> 或文件名
        mt = re.search(r"<title>(.*?)</title>", text, re.S)
        items["title"] = mt.group(1).strip() if mt else os.path.splitext(os.path.basename(path))[0]
    return items


def collect():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if not fn.lower().endswith(".html") or fn == "index.html":
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            meta = parse_meta(full) or {}
            meta["_path"] = rel
            meta.setdefault("topic", "未分类")
            meta.setdefault("title", fn)
            entries.append(meta)
    entries.sort(key=lambda e: (e.get("topic", ""), e.get("created", ""), e["title"]))
    return entries


def render(entries):
    groups = {}
    for e in entries:
        groups.setdefault(e.get("topic") or "未分类", []).append(e)

    cards_html = []
    for topic in sorted(groups):
        cards_html.append(f'  <h2 class="topic">{html.escape(topic)}'
                          f'<span class="count">{len(groups[topic])}</span></h2>')
        cards_html.append('  <div class="grid">')
        for e in groups[topic]:
            title = html.escape(e["title"])
            path = html.escape(e["_path"])
            kws = html.escape(e.get("keywords", ""))
            search = html.escape(" ".join([e["title"], topic, e.get("keywords", ""), e.get("child", "")]))
            tagline = []
            if e.get("grade"):
                tagline.append(html.escape(e["grade"]))
            if e.get("child"):
                tagline.append("👦 " + html.escape(e["child"]))
            tag = " · ".join(tagline)
            cards_html.append(
                f'    <a class="card" href="{path}" data-s="{search}">\n'
                f'      <div class="t">{title}</div>\n'
                f'      <div class="m">{tag}</div>\n'
                f'      <div class="k">{kws}</div>\n'
                f'    </a>')
        cards_html.append('  </div>')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>数学图示 · 导航</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: "微软雅黑","PingFang SC",sans-serif; margin:0; padding:24px;
         background:#f4faff; color:#333; }}
  header {{ text-align:center; margin-bottom:8px; }}
  h1 {{ color:#1d3557; margin:0 0 6px; }}
  .lead {{ color:#777; font-size:15px; }}
  #q {{ display:block; margin:18px auto 8px; width:min(560px,90%);
        padding:12px 16px; font-size:17px; border:2px solid #457b9d;
        border-radius:12px; outline:none; }}
  .topic {{ color:#1d3557; border-left:6px solid #ffb703; padding-left:10px;
            margin:26px 4px 10px; font-size:20px; }}
  .count {{ font-size:13px; color:#888; margin-left:8px; }}
  .grid {{ display:grid; gap:14px;
           grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); }}
  .card {{ display:block; text-decoration:none; color:inherit; background:#fff;
           border-radius:14px; padding:16px; box-shadow:0 3px 10px rgba(0,0,0,.08);
           transition:transform .12s, box-shadow .12s; }}
  .card:hover {{ transform:translateY(-3px); box-shadow:0 8px 20px rgba(29,53,87,.18); }}
  .card .t {{ font-size:17px; font-weight:bold; color:#1d3557; margin-bottom:6px; }}
  .card .m {{ font-size:13px; color:#e07a00; margin-bottom:6px; min-height:18px; }}
  .card .k {{ font-size:13px; color:#888; }}
  .empty {{ text-align:center; color:#999; padding:40px; }}
  footer {{ text-align:center; color:#aaa; font-size:12px; margin-top:30px; }}
</style>
</head>
<body>
<header>
  <h1>📐 数学图示</h1>
  <div class="lead">孩子的动态交互图示集合 · 共 {len(entries)} 个</div>
</header>
<input id="q" type="search" placeholder="🔍 搜索：角 / 函数 / 关键词…" oninput="filter(this.value)">
<main id="list">
{chr(10).join(cards_html)}
  <div class="empty" id="empty" style="display:none">没有匹配的图示</div>
</main>
<footer>生成于 {date.today().isoformat()} · 运行 tools/build_index.py 重建</footer>
<script>
function filter(v) {{
  v = (v || "").trim().toLowerCase();
  var shown = 0;
  document.querySelectorAll(".card").forEach(function(c) {{
    var hit = !v || c.getAttribute("data-s").toLowerCase().indexOf(v) >= 0;
    c.style.display = hit ? "" : "none";
    if (hit) shown++;
  }});
  document.querySelectorAll(".topic").forEach(function(h) {{
    var g = h.nextElementSibling, any = false;
    g.querySelectorAll(".card").forEach(function(c) {{
      if (c.style.display !== "none") any = true;
    }});
    h.style.display = any ? "" : "none";
    g.style.display = any ? "" : "none";
  }});
  document.getElementById("empty").style.display = shown ? "none" : "block";
}}
</script>
</body>
</html>
"""


def main():
    entries = collect()
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(entries))
    print(f"[ok] 已生成 {out}（{len(entries)} 个图示）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
