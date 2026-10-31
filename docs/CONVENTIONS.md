# 规范说明（CONVENTIONS）

> 本仓库 = 孩子的数学「动态图示」集合。每个图 = 一个**离线单文件 HTML**。

## 1. 核心原则

1. **单文件离线**：CSS / JS 全部内联，**禁止任何外部依赖**（无 CDN、无外链字体、无图片外链）。
   - 图标用 emoji 或内联 SVG。
   - 理由：双击即开、可发平板、断网可用、可长期存档。
2. **可交互**：优先用滑块 / 输入框 / 按钮让参数动起来，观察变化（比静态图直观）。
3. **响应式**：适配平板竖屏（孩子多在平板上看）。
4. **给孩子的语言**：字号大、配色清晰、步骤用①②③、避免术语堆砌。

## 2. 目录结构

```
math-visuals/
├── README.md              # 总览 + 图示清单
├── index.html             # 自动生成的导航首页（勿手改，跑 tools/build_index.py 生成）
├── 00-模板/template.html  # 新图从这复制，保证风格统一
├── 01-角/                 # 按「知识点」分文件夹
├── 02-函数/
├── 03-分数与小数/
├── 04-面积与体积/
├── 05-统计与图表/
├── 06-数与运算/
├── 07-应用题/
├── tools/build_index.py   # 扫描全部 html → 生成 index.html
└── docs/CONVENTIONS.md    # 本文件
```

后续按需新增知识点文件夹（三位数字前缀 + 中文名，保持排序）。

## 3. 文件命名

- 规则：`<孩子拼音>-<知识点slug>-<题型>.html`
- 例：`ningmeng-angle-multiples.html`、`ningmeng-angle-a-b-180-360.html`
- **slug 用英文小写 + 连字符**（避免中文文件名的编码坑）。
- 孩子前缀用**拼音**（中文名 → 拼音，如「小明」→ `xiaoming`）；中文名只出现在页面标题与元信息里。
- ⚠️ 本仓库**公开托管**（GitHub Pages）→ 元信息 `child:` 字段、标题、文件名一律用**拼音**，不要写真人中文名。
- 若某个图与特定孩子无关（通用图），可省略孩子前缀。

## 4. 每个 HTML 必带「元信息头」

紧跟在 `<!DOCTYPE html>` 之后，供 `build_index.py` 自动解析：

```html
<!--@visual
title: 角的倍数关系
topic: 角
grade: 小学四年级
child: ningmeng
keywords: 平角,倍数,角
created: 2026-10-31
-->
```

字段说明：

| 字段 | 必填 | 说明 |
|------|------|------|
| title | ✅ | 页面标题（中文，显示在索引里） |
| topic | ✅ | 所属知识点（与文件夹对应） |
| grade |  | 适合年级 |
| child |  | 给哪个孩子（**拼音**，如 ningmeng） |
| keywords |  | 逗号分隔，便于搜索 |
| created | ✅ | 创建日期 YYYY-MM-DD |

## 5. 页面骨架（见 00-模板/template.html）

固定四段：**标题栏 → 交互区（画布/图形）→ 控制区（滑块/输入/按钮）→ 解题思路区**。
- 配色：背景浅色，主色 `#1d3557`，高亮 `#e63946`，强调 `#ffb703`。
- 字体：`"微软雅黑", sans-serif`。
- 圆角卡片 + 轻阴影，风格统一。

## 6. 工作流

1. 从 `00-模板/template.html` 复制一份到对应知识点文件夹。
2. 改文件名 + 元信息头 + 页面内容。
3. 跑 `python3 tools/build_index.py` 重新生成导航页。
4. `git add . && git commit -m "feat: 新增 XX 图示" && git push`。

## 7. 部署（GitHub Pages）

- 本仓库**公开托管**，`main` 分支 push 后由 `.github/workflows/pages.yml` 自动：跑 `build_index.py` → 部署到 Pages。
- 访问地址：`https://s1sunny.github.io/math-visuals/`
- 即：加完图只需 `git push`，线上导航页自动更新。

## 8. 新增知识点分类

在仓库根目录建 `<序号>-<知识点>/`（序号递增），并同步更新 README 的分类表。
