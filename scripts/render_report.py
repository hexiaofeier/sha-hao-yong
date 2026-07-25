#!/usr/bin/env python3
import argparse
import copy
import json
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


STYLE_NAME = "白纸墨字"

CSS = """
* { box-sizing: border-box; }
html { background: var(--paper); }
body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.7;
}
a { color: var(--ink); text-decoration-color: var(--line); text-underline-offset: 3px; }
a:hover { text-decoration-color: currentColor; }
.page { width: min(1040px, calc(100% - 36px)); margin: 0 auto; padding: 40px 0 60px; }

.hero { border-top: 2px solid var(--ink); padding: 22px 0 22px; }
.eyebrow { margin: 0 0 10px; font-size: 12px; font-weight: 700; letter-spacing: .16em; color: var(--muted); text-transform: uppercase; }
h1 { margin: 0; font-size: clamp(30px, 5vw, 46px); line-height: 1.2; letter-spacing: -.02em; font-weight: 800; }
.title-red { color: var(--red); }
.title-neutral { color: var(--ink); font-weight: 500; }
.meta { display: flex; flex-wrap: wrap; gap: 6px 20px; margin-top: 14px; font-size: 13px; color: var(--muted); }
.positioning { margin: 22px 0 0; padding: 16px 20px; border-radius: 4px; border-left: 3px solid var(--blue); background: var(--soft); font-size: 16px; font-weight: 400; color: var(--ink); }
.positioning span { display: block; }
.positioning span + span { margin-top: 4px; }

.section { margin-top: 44px; }
.section-title { display: flex; align-items: baseline; gap: 10px; margin: 0 0 16px; font-size: 23px; line-height: 1.3; font-weight: 800; color: var(--ink); }
.section-title .num { font-size: 15px; font-weight: 700; padding: 2px 8px; border-radius: 3px; }
.c-blue .num { background: var(--blue); color: #fff; }
.c-red .num { background: var(--red); color: #fff; }
.c-green .num { background: var(--green); color: var(--ink); }
.c-amber .num { background: var(--amber); color: var(--ink); }

.section-summary { margin: 0 0 16px; padding: 12px 16px; border-left: 3px solid; background: var(--soft); font-weight: 600; font-size: 15px; border-radius: 4px; color: var(--ink); }
.section-summary.c-blue { border-left-color: var(--blue); }
.section-summary.c-green { border-left-color: var(--green); }
.section-summary.c-amber { border-left-color: var(--amber); }
.fit-verdict { color: var(--ink); border-left: 3px solid var(--red); background: var(--soft); padding: 12px 16px; font-weight: 700; font-size: 16px; border-radius: 4px; margin: 0 0 16px; }

.score-head { display: flex; align-items: end; justify-content: space-between; gap: 16px; margin: 20px 0 6px; }
.score-value { font-size: 36px; font-weight: 850; line-height: 1.1; font-variant-numeric: tabular-nums; }
.score-num { color: var(--red); }
.score-label { color: var(--ink); font-weight: 700; }
.score-basis { color: var(--muted); font-size: 13px; text-align: right; max-width: 320px; }
.scale { display: grid; grid-template-columns: repeat(10, 1fr); gap: 3px; margin-top: 14px; height: 16px; }
.scale-segment { min-width: 0; background: var(--soft); border: 1px solid var(--line); overflow: hidden; }
.scale-fill { display: block; height: 100%; background: var(--red); }
.scale-note { margin: 8px 0 0; font-size: 12px; color: var(--muted); }
.scale-explain { display: block; margin-bottom: 2px; font-weight: 700; color: var(--ink); }

.plain-box, .card { border-radius: 4px; border: 1px solid var(--line); border-left-width: 3px; background: #fff; padding: 16px 18px; }
.plain-box h3, .card h3 { margin: 0 0 9px; font-size: 15px; color: var(--ink); font-weight: 800; }
.plain-box ul, .card ul, .card ol { padding-left: 1.1em; color: var(--ink); }
.plain-box li, .card li { color: var(--ink); }

.conclusion-box { margin-top: 20px; border-radius: 4px; border: 1px solid var(--line); border-left: 3px solid var(--blue); background: #fff; padding: 4px 20px; }
.conclusion-block { padding: 16px 0; }
.conclusion-block + .conclusion-block { border-top: 1px dashed var(--line); }
.conclusion-block h3 { margin: 0 0 9px; font-size: 15px; font-weight: 800; color: var(--ink); }
.conclusion-block p { margin: 0; color: var(--ink); }

table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid var(--line); border-radius: 4px; overflow: hidden; }
th, td { padding: 12px 14px; border-top: 1px solid var(--line); border-left: 1px solid var(--line); vertical-align: top; text-align: left; color: var(--ink); }
tr:first-child th, tr:first-child td { border-top: 0; }
th:first-child, td:first-child { border-left: 0; }
th { background: var(--soft); font-size: 16px; font-weight: 800; color: var(--ink); }
td:first-child { font-weight: 700; }
.metric-table th:nth-child(1) { width: 160px; }
.metric-table th:nth-child(2) { width: 240px; }
.metric-table td:nth-child(2) { color: var(--red); font-weight: 700; }
.metric-table td:nth-child(2) .est-note { color: var(--ink); font-weight: 400; }
h3.sub-h { margin: 30px 0 12px; font-size: 17px; color: var(--ink); font-weight: 800; }

ul, ol { margin: 0; padding-left: 1.25em; }
li + li { margin-top: 5px; }

.what-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 4px; }
.what-grid .card { border-left-color: var(--green); }
.what-grid .card h3 { display: flex; align-items: center; gap: 8px; }
.what-grid .card h3 .step-no { display: inline-grid; place-items: center; width: 20px; height: 20px; border-radius: 50%; background: var(--green); color: var(--ink); font-size: 12px; font-weight: 800; flex: 0 0 auto; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 14px 0; }

.steps { counter-reset: step; list-style: none; padding: 0; display: grid; gap: 10px; }
.steps li { display: grid; grid-template-columns: 30px 1fr; gap: 11px; align-items: start; margin: 0; color: var(--ink); }
.steps li::before { counter-increment: step; content: counter(step); display: grid; place-items: center; width: 26px; height: 26px; border-radius: 4px; background: var(--soft); border: 1px solid var(--line); color: var(--ink); font-weight: 800; font-size: 13px; }

details { margin-top: 36px; border: 1px solid var(--line); border-radius: 4px; padding: 12px 16px; }
summary { cursor: pointer; font-size: 16px; font-weight: 700; color: var(--ink); }
summary::marker { color: var(--muted); }
details h3 { color: var(--ink); font-size: 14px; margin: 14px 0 6px; }
details ul { color: var(--muted); }

.notice { margin-top: 34px; padding: 18px 20px; border-radius: 4px; border: 1px solid var(--line); background: var(--soft); }
.notice h2 { margin: 0 0 10px; font-size: 18px; color: var(--ink); }
.notice ul { color: var(--muted); font-size: 12px; }
.notice li + li { margin-top: 7px; }

.footer-line { display: flex; align-items: center; gap: 16px; margin-top: 44px; color: var(--muted); font-size: 12.5px; font-weight: 700; letter-spacing: .06em; white-space: nowrap; }
.footer-line::before, .footer-line::after { content: ""; height: 1px; background: var(--line); flex: 1 1 auto; }

@media (max-width: 760px) {
  .two-col, .what-grid { grid-template-columns: 1fr; }
  .score-head { align-items: start; flex-direction: column; }
  .score-basis { text-align: left; max-width: none; }
  .metric-table th:nth-child(1), .metric-table th:nth-child(2) { width: auto; }
  table { font-size: 13.5px; }
  th, td { padding: 10px; }
}
@media print {
  .page { width: 100%; padding: 0; }
  .section { break-inside: avoid; }
  details { break-inside: avoid; }
  a { text-decoration: none; }
}
"""


def e(value):
    return escape(str(value or "未验证"))


FORBIDDEN_TEXT = (
    "不要把",
    "并不是",
    "装上后，你最多",
    "核心工作仍需其他能力完成",
    "可能会带来一定的",
    "从某种程度上来说",
    "值得注意的是",
    "总体而言",
    "综上所述",
    "赋能",
    "抓手",
    "闭环",
    "multi_agent",
    "多 agent",
    "子 agent",
    "AI 编程 agent",
    "Agent工具",
    "AI 工具",
    "AI工具",
    "Python 数据库",
    "具备一定的",
    "需要一定程度的",
    "在一定程度上",
    "表现良好",
    "可实现",
    "核心路径通常不必",
    "联网必须，Key 可选",
    "按典型目标用户判断",
    "此分数不代表所有人",
    "接受静态、只读的采用评估",
    "目标用户需求",
    "采用代价",
    "证据边界",
    "这是一个",
    "这是一套",
    "有条件安装。",
    "仓库",
    "PDF 路径",
    "Markdown 路径",
    "核心路径",
    "推荐路径",
    "全开路径",
    "一句话：",
)

FORBIDDEN_ABBREVIATIONS = re.compile(r"(?<![A-Za-z])(CI|LLM|PR|repo|TDD|hook|runtime)(?![A-Za-z])", re.IGNORECASE)
PREPARATION_NAMES = [
    "额外软件安装",
    "额外注册/登录的账号",
    "API KEY/联网服务",
    "涉及的数据与隐私",
]

PLACEHOLDER = "【待填写】"
_ISSUE_COLLECTOR = None


class ReportValidationError(ValueError):
    def __init__(self, issues):
        self.issues = list(dict.fromkeys(issues))
        super().__init__("\n".join(self.issues))


def require(condition, message):
    if not condition:
        if _ISSUE_COLLECTOR is not None:
            _ISSUE_COLLECTOR.append(message)
            return False
        raise ValueError(message)
    return True


def require_list(value, name, minimum=2, maximum=4):
    require(isinstance(value, list), f"{name} 必须是列表")
    require(minimum <= len(value) <= maximum, f"{name} 必须有 {minimum}—{maximum} 条")
    require(all(isinstance(item, str) and item.strip() for item in value), f"{name} 不能有空项")


def user_visible_strings(data):
    values = [data["scope"]]
    values.extend(data["positioning"])
    rec = data["recommendation"]
    values.append(rec["basis"])
    values.extend(rec["final_conclusion"])
    values.extend(rec["quantitative_analysis"])
    values.append(rec["use_cases"])
    values.append(rec["advice"])
    what = data["what"]
    values.append(what["summary"])
    for key in ("user_needs", "extra_needs", "output"):
        values.extend(what[key])
    values.extend(what["steps"])
    values.append(data["quality_summary"])
    for row in data.get("metrics", []):
        values.extend([row["name"], row["result"], row["meaning"]])
    values.extend(data.get("strengths", []))
    values.extend(data.get("frictions", []))
    for row in data.get("preparation", []):
        values.extend([row["name"], row["required"], row["impact"]])
    fit = data["fit"]
    values.extend(fit.get("good_for", []))
    values.extend(fit.get("not_for", []))
    values.extend(data.get("usage_rhythm", []))
    values.extend(data.get("unverified", []))
    values.extend(row.get("name", "") for row in data.get("sources", []))
    return values


def _validate_report(data):
    require(data.get("schema_version") == 7, "schema_version 必须是 7")
    for key in ("title", "date", "scope", "positioning", "recommendation", "what", "quality_summary", "metrics", "preparation", "fit", "usage_rhythm", "sources", "unverified"):
        require(key in data, f"缺少字段：{key}")

    require_list(data["positioning"], "positioning", 3, 4)
    display_name = data["title"].split("｜", 1)[0].strip()
    require(bool(display_name), "title 必须以目标 Skill 名称开头")
    require(data["positioning"][0].startswith(display_name), f"定位第一句必须以“{display_name}”开头")
    for index, line in enumerate(data["positioning"]):
        if index in (1, 2):
            require(display_name not in line, f"定位第{index + 1}句再次指代 Skill 时请用“它”，不要重复名称：{line}")
        require(
            display_name in line or line.startswith(("它", "用户", "最终用户", "你", "经评估")),
            f"定位句必须写明主语“{display_name}”“它”“用户”或“你”：{line}",
        )
    rec = data["recommendation"]
    for key in ("score", "label", "basis_type", "basis", "final_conclusion", "quantitative_analysis", "use_cases", "advice"):
        require(key in rec, f"recommendation 缺少字段：{key}")
    require_list(rec["final_conclusion"], "final_conclusion", 2, 4)
    require_list(rec["quantitative_analysis"], "quantitative_analysis", 1, 2)
    require(isinstance(rec["use_cases"], str) and rec["use_cases"].strip(), "use_cases 必须是一句话")
    require(not rec["use_cases"].startswith("一句话"), "适用场景不要用“一句话”这种开头词，直接写判断")
    require(isinstance(rec["advice"], str) and rec["advice"].strip(), "advice 必须是一句话")

    score = float(rec["score"])
    require(0 <= score <= 10, "推荐程度必须在 0—10")
    expected_label = "不推荐" if score < 4 else "谨慎采用" if score < 6 else "有条件推荐" if score < 7.5 else "推荐" if score < 9 else "强推荐"
    require(rec["label"] == expected_label, f"{score:.1f} 分对应的标签应为“{expected_label}”")
    require(rec["basis_type"] in ("personalized", "target"), "basis_type 只能写 personalized 或 target")
    require(isinstance(rec["basis"], str) and 4 <= len(rec["basis"]) <= 50, "basis 必须用 4—50 字写清判断对象或具体依据")
    if rec["basis_type"] == "target":
        require(rec["basis"].startswith("判断对象："), "目标人群判断的 basis 必须以“判断对象：”开头")
    else:
        require(rec["basis"].startswith("根据"), "个性化判断的 basis 必须以“根据”开头")

    if score < 4:
        match_word = "不匹配"
        advice_ok = rec["advice"] == "不建议安装它。"
        advice_rule = "不建议安装它。"
    elif score < 6:
        match_word = "部分匹配"
        advice_ok = rec["advice"] == "建议先试用它，再决定是否安装。"
        advice_rule = "建议先试用它，再决定是否安装。"
    elif score < 7.5:
        match_word = "部分匹配"
        advice_ok = "可以安装它" in rec["advice"] and rec["advice"].startswith(("如果", "满足", "前提是"))
        advice_rule = "写清具体条件，并说明可以安装它"
    else:
        match_word = "匹配"
        advice_ok = rec["advice"] == "建议安装它。"
        advice_rule = "建议安装它。"
    if rec["basis_type"] == "personalized":
        expected_first = f"{display_name} {match_word}你的需求。"
    else:
        target_word = "不适合" if score < 4 else "部分适合" if score < 7.5 else "适合"
        expected_first = f"{display_name} {target_word}这类用户。"
    first = rec["final_conclusion"][0]
    require(first == expected_first, f"{score:.1f} 分的最终结论第一句必须是“{expected_first}”")
    require(rec["use_cases"].startswith(f"{display_name} 适合"), f"适用场景必须以“{display_name} 适合”开头")
    require(advice_ok, f"{score:.1f} 分的使用建议必须{advice_rule}")

    def require_pronoun_chain(lines, label):
        if lines and display_name in lines[0]:
            for line in lines[1:]:
                require(display_name not in line, f"{label}第一句已写出 Skill 名称，后续再次指代时请用“它”：{line}")

    for label, lines in (
        ("最终结论", rec["final_conclusion"]),
        ("好用之处", data.get("strengths", [])),
        ("可能卡住", data.get("frictions", [])),
    ):
        require_pronoun_chain(lines, label)

    for label, lines in (("适合场景", data.get("fit", {}).get("good_for", [])), ("不适合场景", data.get("fit", {}).get("not_for", []))):
        for line in lines:
            require(display_name not in line and "它" not in line and "用户" not in line, f"{label}直接写场景短语，不写主语：{line}")
            require(not line.startswith(("适合", "不适合")), f"{label}不重复栏目名称：{line}")

    conclusion_lines = data["positioning"] + rec["final_conclusion"] + rec["quantitative_analysis"] + [rec["use_cases"], rec["advice"]]
    require(len(conclusion_lines) == len(set(conclusion_lines)), "结论区出现完全重复的句子")
    for line in conclusion_lines:
        require("；" not in line, f"结论区禁止分号长句：{line}")
        require(len(line) <= 70, f"结论区句子过长，请拆句：{line}")

    what = data["what"]
    require(isinstance(what.get("summary"), str) and what["summary"].strip(), "what.summary 必须写明 Skill 身份、用途和核心执行能力")
    require(what["summary"].startswith(display_name), f"what.summary 必须以“{display_name}”开头")
    require_list(what.get("user_needs"), "what.user_needs", 2, 6)
    require_list(what.get("steps"), "what.steps", 3, 5)
    require_list(what.get("extra_needs"), "what.extra_needs", 2, 4)
    require_list(what.get("output"), "what.output", 2, 4)
    for key in ("user_needs", "steps", "extra_needs", "output"):
        for line in what[key]:
            require(len(line) <= 35, f"{key} 单条超过 35 字，请拆短：{line}")
    require(isinstance(data["quality_summary"], str) and data["quality_summary"].strip(), "quality_summary 必须概括完成度、优势和最大门槛")
    completeness_index = data["quality_summary"].find("完整度")
    usability_index = data["quality_summary"].find("好用度")
    require(completeness_index >= 0 and usability_index > completeness_index, "quality_summary 必须按“完整度→好用度→优势和不足哪个权重更大”的顺序写")

    prep_names = [row.get("name") for row in data["preparation"]]
    require(prep_names == PREPARATION_NAMES, "安装准备必须使用固定四项，并保持顺序")
    metric_names = [row.get("name") for row in data["metrics"]]
    for name in ("公开关注度", "安装复杂度", "任务复杂度", "Skill 调用准确性", "额外涉及费用", "Token 消耗", "风险值"):
        require(name in metric_names, f"指标表缺少：{name}")
    task_row = next(row for row in data["metrics"] if row["name"] == "任务复杂度")
    require("基准任务" in task_row["meaning"], "任务复杂度说明必须写明典型核心基准任务")
    invocation_row = next(row for row in data["metrics"] if row["name"] == "Skill 调用准确性")
    require(
        any(label in invocation_row["result"] for label in ("较准确", "偏宽", "偏窄", "无法判断")),
        "Skill 调用准确性只能使用：较准确、偏宽、偏窄或无法判断",
    )
    invocation_text = f"{invocation_row['result']} {invocation_row['meaning']}"
    require(
        all(word in invocation_text for word in ("名称", "描述", "触发规则")),
        "Skill 调用准确性必须写清判断依据：名称、描述和触发规则",
    )
    token_row = next(row for row in data["metrics"] if row["name"] == "Token 消耗")
    require("基准任务" in token_row["meaning"], "Token 消耗说明必须写明典型核心基准任务")

    visible_values = user_visible_strings(data)
    license_unknown = any(
        ("许可证" in value or "使用许可" in value)
        and any(marker in value for marker in ("未验证", "未确认", "未提供", "未找到"))
        for value in visible_values
    )
    fee_row = next(row for row in data["metrics"] if row["name"] == "额外涉及费用")
    fee_text = f"{fee_row['result']} {fee_row['meaning']}"
    if license_unknown:
        require(
            "核心免费" not in fee_text and "无新增费用" not in fee_text,
            "许可证未验证时不得写“核心免费”或“无新增费用”；请分开说明直接费用与使用许可",
        )

    for value in visible_values:
        for forbidden in FORBIDDEN_TEXT:
            require(forbidden not in value, f"用户可见文字含禁用表达“{forbidden}”：{value}")
        require(not FORBIDDEN_ABBREVIATIONS.search(value), f"用户可见文字含未解释缩写：{value}")


def collect_validation_issues(data):
    global _ISSUE_COLLECTOR
    issues = []
    def find_placeholders(value, path="根字段"):
        if isinstance(value, dict):
            for key, item in value.items():
                find_placeholders(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value, 1):
                find_placeholders(item, f"{path}[{index}]")
        elif isinstance(value, str) and PLACEHOLDER in value:
            issues.append(f"{path} 仍有待填写内容")

    find_placeholders(data)
    _ISSUE_COLLECTOR = issues
    try:
        _validate_report(data)
    except (KeyError, TypeError, ValueError, StopIteration) as exc:
        issues.append(f"JSON 结构无法继续检查：{exc}")
    finally:
        _ISSUE_COLLECTOR = None
    return list(dict.fromkeys(issues))


def validate_report(data):
    issues = collect_validation_issues(data)
    if issues:
        raise ReportValidationError(issues)


DEFAULT_PALETTE = {
    "paper": "#FFFFFF",
    "ink": "#17181A",
    "muted": "#676C74",
    "line": "#E3E5E8",
    "soft": "#F5F6F7",
    "red": "#B73F42",
    "blue": "#244C66",
    "amber": "#D6A553",
    "green": "#82B29B",
}

SECTION_COLORS = ["c-blue", "c-green", "c-amber", "c-red", "c-blue"]

_EST_NOTE_RE = re.compile(r"(｜(?:根据|按)[^｜]*)$")


def palette_css():
    palette = DEFAULT_PALETTE
    return """:root {{
  --paper: {paper};
  --ink: {ink};
  --muted: {muted};
  --line: {line};
  --soft: {soft};
  --red: {red};
  --blue: {blue};
  --amber: {amber};
  --green: {green};
}}
""".format(**palette)


def render_scale(score):
    segments = []
    for index in range(10):
        fill = max(0.0, min(1.0, score - index))
        segments.append(f'<span class="scale-segment"><i class="scale-fill" style="width:{fill * 100:.0f}%"></i></span>')
    return "".join(segments)


def render_list(items, ordered=False, css_class=""):
    tag = "ol" if ordered else "ul"
    cls = f' class="{css_class}"' if css_class else ""
    values = items or ["未验证"]
    return f"<{tag}{cls}>" + "".join(f"<li>{e(item)}</li>" for item in values) + f"</{tag}>"


def render_paragraph(value):
    if isinstance(value, list):
        text = "".join(str(item) for item in value if item)
    else:
        text = str(value or "")
    return f"<p>{e(text)}</p>"


def render_metric_result(value):
    text = str(value or "未验证")
    match = _EST_NOTE_RE.search(text)
    if match:
        main = text[:match.start()]
        note = match.group(1)
        return f'{e(main)}<span class="est-note">{e(note)}</span>'
    return e(text)


def render_report(data):
    validate_report(data)
    rec = data["recommendation"]
    what = data["what"]
    fit = data["fit"]
    score = max(0.0, min(10.0, float(rec["score"])))
    scale_html = render_scale(score)
    positioning_html = "".join(f"<span>{e(line)}</span>" for line in data["positioning"])
    conclusion_blocks = [
        ("最终结论", rec["final_conclusion"]),
        ("量化分析", rec["quantitative_analysis"]),
        ("适用场景", rec["use_cases"]),
    ]
    conclusion_html = "".join(
        f'<div class="conclusion-block"><h3>{e(title)}</h3>{render_paragraph(items)}</div>'
        for title, items in conclusion_blocks
    )

    metrics_html = "".join(
        f"<tr><td>{e(row['name'])}</td><td>{render_metric_result(row['result'])}</td><td>{e(row['meaning'])}</td></tr>"
        for row in data.get("metrics", [])
        if not (row.get("name") == "下载量" and not row.get("result"))
    )

    prep_html = "".join(
        f"<tr><td>{e(row['name'])}</td><td>{e(row['required'])}</td><td>{e(row['impact'])}</td></tr>"
        for row in data.get("preparation", [])
    )

    sources_html = "".join(
        f'<li><a href="{e(row["url"])}" target="_blank" rel="noreferrer noopener">{e(row["name"])}</a></li>'
        for row in data.get("sources", [])
    ) or "<li>未列出公开来源</li>"

    unverified_html = render_list(data.get("unverified"))
    fit_verdict = e(rec["final_conclusion"][0] + rec["advice"])

    def section_title(index, text):
        color_class = SECTION_COLORS[index - 1]
        return f'<h2 class="section-title {color_class}"><span class="num">{index}</span>{e(text)}</h2>'

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(data['title'])} · {STYLE_NAME}</title>
  <style>{palette_css()}{CSS}</style>
</head>
<body>
<main class="page">
  <header class="hero">
    <p class="eyebrow">啥好用 · SKILL 安装前说明书</p>
    <h1><span class="title-red">{e(data['title'].split('｜', 1)[0])}</span><span class="title-neutral">｜{e(data['title'].split('｜', 1)[1] if '｜' in data['title'] else '啥好用评估')}</span></h1>
    <div class="meta"><span>评估日期：{e(data['date'])}</span><span>评估范围：{e(data['scope'])}</span></div>
    <div class="positioning">{positioning_html}</div>
  </header>

  <section class="section">
    {section_title(1, "结论概述")}
    <div class="score-head"><div class="score-value"><span class="score-num">{score:.1f}/10</span><span class="score-label">｜{e(rec['label'])}</span></div><div class="score-basis">{e(rec['basis'])}</div></div>
    <div class="scale">{scale_html}</div>
    <p class="scale-note"><span class="scale-explain">分数越高，越值得安装。</span>0—3.9 不推荐｜4.0—5.9 谨慎采用｜6.0—7.4 有条件推荐｜7.5—8.9 推荐｜9.0—10 强推荐</p>
    <div class="conclusion-box">{conclusion_html}</div>
  </section>

  <section class="section">
    {section_title(2, "这个 Skill 是啥")}
    <div class="section-summary c-green">{e(what['summary'])}</div>
    <div class="what-grid">
      <div class="card"><h3><span class="step-no">1</span>用户需求</h3>{render_list(what['user_needs'])}</div>
      <div class="card"><h3><span class="step-no">2</span>任务步骤</h3>{render_list(what.get('steps'), ordered=True)}</div>
      <div class="card"><h3><span class="step-no">3</span>额外需要</h3>{render_list(what['extra_needs'])}</div>
      <div class="card"><h3><span class="step-no">4</span>最后交付</h3>{render_list(what['output'])}</div>
    </div>
  </section>

  <section class="section">
    {section_title(3, "这个 Skill 好用吗")}
    <div class="section-summary c-amber">{e(data['quality_summary'])}</div>
    <div class="two-col">
      <div class="plain-box"><h3>好用之处</h3>{render_list(data.get('strengths'))}</div>
      <div class="plain-box"><h3>可能卡住</h3>{render_list(data.get('frictions'))}</div>
    </div>
    <h3 class="sub-h">指标分析</h3>
    <table class="metric-table"><thead><tr><th>主要指标</th><th>评估结果</th><th>用户影响</th></tr></thead><tbody>{metrics_html}</tbody></table>
    <h3 class="sub-h">安装准备</h3>
    <table><thead><tr><th>前期准备</th><th>是否必须</th><th>用户影响</th></tr></thead><tbody>{prep_html}</tbody></table>
  </section>

  <section class="section">
    {section_title(4, "这个 Skill 适合你吗")}
    <div class="fit-verdict">{fit_verdict}</div>
    <div class="two-col">
      <div class="plain-box"><h3>适合场景</h3>{render_list(fit.get('good_for'))}</div>
      <div class="plain-box"><h3>不适合场景</h3>{render_list(fit.get('not_for'))}</div>
    </div>
  </section>

  <section class="section">
    {section_title(5, "使用节奏建议")}
    {render_list(data.get('usage_rhythm'), ordered=True, css_class='steps')}
  </section>

  <details><summary>来源与尚不能确认的事项</summary><h3>主要来源</h3><ul>{sources_html}</ul><h3>尚不能确认</h3>{unverified_html}</details>

  <aside class="notice">
    <h2>说明</h2>
    <ul>
      <li>本报告中的 AI agent，指能够读取 Skill、理解任务，并按规则调用电脑软件或联网服务完成工作的 AI 助手，例如 Codex、Claude Code、Cursor Agent 等。它能否执行命令、联网或调用工具，取决于具体产品和用户授予的权限。</li>
      <li>除非正文明确标注为本机实测，本报告主要依据公开文件与只读检查完成；正文未记录的安装、运行、长期兼容性、稳定性、价格和输出质量均未验证。</li>
      <li>“啥好用”不能替代专业评测，包括代码安全审计、恶意代码检测、软件质量与兼容性测试、隐私合规审查、许可证审查或法律意见。</li>
      <li>下载或使用前，请核对官方来源、依赖、权限、数据去向、收费和许可证，并注意安全风险。</li>
      <li>请勿在对话或报告中粘贴 API Key、Cookie、Token、密码等凭证；优先使用测试环境、最小权限、专用账号和可恢复备份。</li>
      <li>任何安装、授权、付费、上传、发布或自动操作均须由用户确认。评分只作采用参考；项目更新后应重新评估。</li>
    </ul>
  </aside>

  <div class="footer-line"><span>啥好用skill•盒小Feier</span></div>

</main>
</body>
</html>"""


def write_reports(payload, output):
    if isinstance(payload, dict) and payload.get("palette_variants"):
        base = payload["report"]
        reports = []
        for variant in payload["palette_variants"]:
            report = base.copy()
            report.update({
                "output_name": variant["output_name"],
                "palette_name": variant["palette_name"],
                "palette": variant["palette"],
            })
            reports.append(report)
    else:
        reports = payload if isinstance(payload, list) else [payload]
    output = Path(output)
    if len(reports) == 1 and output.suffix.lower() == ".html":
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_report(reports[0]), encoding="utf-8")
        return [output]

    output.mkdir(parents=True, exist_ok=True)
    written = []
    for report in reports:
        target = output / report["output_name"]
        target.write_text(render_report(report), encoding="utf-8")
        written.append(target)
    return written


def safe_name(value):
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = cleaned.strip(" .-")
    return cleaned or "skill"


def report_skeleton(skill_name):
    name = safe_name(skill_name)
    return {
        "schema_version": 7,
        "output_name": f"{name}_啥好用评估_CO.html",
        "title": f"{name}｜啥好用评估",
        "date": date.today().isoformat(),
        "scope": PLACEHOLDER,
        "positioning": [f"{name} 是{PLACEHOLDER}。", f"它通过{PLACEHOLDER}。", f"最终用户可以得到{PLACEHOLDER}。", f"经评估，{name} 更适合{PLACEHOLDER}。"],
        "recommendation": {
            "score": 5.0,
            "label": "谨慎采用",
            "basis_type": "target",
            "basis": f"判断对象：{PLACEHOLDER}",
            "final_conclusion": [f"{name} 部分适合这类用户。", f"{name} {PLACEHOLDER}。", f"用户需要注意{PLACEHOLDER}。"],
            "quantitative_analysis": [f"这次得分主要由{PLACEHOLDER}这 1—2 个数字决定。"],
            "use_cases": f"{name} 适合{PLACEHOLDER}的用户，用来{PLACEHOLDER}。",
            "advice": "建议先试用它，再决定是否安装。",
        },
        "what": {
            "summary": f"{name} 用{PLACEHOLDER}机制，展开{PLACEHOLDER}的工作，实现{PLACEHOLDER}的效果。",
            "user_needs": [f"用户已有{PLACEHOLDER}", f"用户希望{PLACEHOLDER}"],
            "steps": [f"确认{PLACEHOLDER}", f"处理{PLACEHOLDER}", f"交付{PLACEHOLDER}"],
            "extra_needs": [f"除 AI agent 本身外，用户还需要{PLACEHOLDER}", f"{name} 还会调用{PLACEHOLDER}"],
            "output": [f"用户可以得到{PLACEHOLDER}", f"用户可以继续{PLACEHOLDER}"],
        },
        "quality_summary": f"完整度{PLACEHOLDER}。好用度{PLACEHOLDER}。优势和不足相比，{PLACEHOLDER}的权重更大。",
        "metrics": [
            {"name": "公开关注度", "result": PLACEHOLDER, "meaning": PLACEHOLDER},
            {"name": "安装复杂度", "result": PLACEHOLDER, "meaning": PLACEHOLDER},
            {"name": "任务复杂度", "result": PLACEHOLDER, "meaning": f"基准任务：{PLACEHOLDER}"},
            {"name": "Skill 调用准确性", "result": "无法判断", "meaning": f"名称、描述和触发规则：{PLACEHOLDER}"},
            {"name": "额外涉及费用", "result": PLACEHOLDER, "meaning": PLACEHOLDER},
            {"name": "Token 消耗", "result": PLACEHOLDER, "meaning": f"基准任务：{PLACEHOLDER}"},
            {"name": "风险值", "result": PLACEHOLDER, "meaning": PLACEHOLDER},
        ],
        "strengths": [f"{PLACEHOLDER}。", f"{PLACEHOLDER}优势。"],
        "frictions": [f"{PLACEHOLDER}。", f"{PLACEHOLDER}门槛。"],
        "preparation": [
            {"name": item, "required": PLACEHOLDER, "impact": PLACEHOLDER}
            for item in PREPARATION_NAMES
        ],
        "fit": {
            "good_for": [f"{PLACEHOLDER}", f"{PLACEHOLDER}"],
            "not_for": [f"{PLACEHOLDER}", f"{PLACEHOLDER}"],
        },
        "usage_rhythm": [f"第一次先{PLACEHOLDER}。", f"确认后再{PLACEHOLDER}。", f"出现{PLACEHOLDER}时停用。"],
        "sources": [{"name": PLACEHOLDER, "url": "https://example.com"}],
        "unverified": [f"{PLACEHOLDER}。"],
    }


def load_payload(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"找不到 JSON：{path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 格式错误：第 {exc.lineno} 行，第 {exc.colno} 列，{exc.msg}")


def expand_reports(payload):
    if isinstance(payload, dict) and payload.get("palette_variants"):
        reports = []
        for variant in payload["palette_variants"]:
            report = copy.deepcopy(payload["report"])
            report.update({
                "output_name": variant["output_name"],
                "palette_name": variant["palette_name"],
                "palette": variant["palette"],
            })
            reports.append(report)
        return reports
    return payload if isinstance(payload, list) else [payload]


def payload_issues(payload):
    issues = []
    reports = expand_reports(payload)
    if not reports or not all(isinstance(item, dict) for item in reports):
        return ["JSON 顶层必须是一份报告或报告列表"]
    for index, report in enumerate(reports, 1):
        prefix = f"报告 {index}：" if len(reports) > 1 else ""
        issues.extend(prefix + issue for issue in collect_validation_issues(report))
    return list(dict.fromkeys(issues))


def print_issues(issues):
    print(f"校验未通过，共 {len(issues)} 项：", file=sys.stderr)
    for index, issue in enumerate(issues, 1):
        print(f"{index}. {issue}", file=sys.stderr)


def default_output(input_json, payload):
    reports = expand_reports(payload)
    base = Path(input_json).resolve().parent
    if base.name == "过程文件_CO":
        base = base.parent
    if len(reports) == 1:
        return base / reports[0].get("output_name", "啥好用评估_CO.html")
    return base


def check_html(path):
    html = Path(path).read_text(encoding="utf-8")
    issues = []
    if len(re.findall(r'class="section-title\b', html)) != 5:
        issues.append("HTML 必须包含 5 个固定章节")
    if html.count('class="scale-segment"') != 10:
        issues.append("推荐条必须包含 10 个色块")
    if re.search(r"(?:linear|radial|conic)-gradient", html, re.IGNORECASE):
        issues.append("HTML 禁止使用渐变")
    if PLACEHOLDER in html:
        issues.append("HTML 仍有待填写内容")
    if 'class="notice"' not in html:
        issues.append("HTML 缺少页尾说明")
    if 'class="footer-line"' not in html:
        issues.append("HTML 缺少底部封线")
    if "啥好用skill•盒小Feier" not in html:
        issues.append("HTML 缺少底部固定署名")
    for color in DEFAULT_PALETTE.values():
        if color not in html:
            issues.append(f"HTML 缺少{STYLE_NAME}固定色：{color}")
    for css_class in ("title-red", "title-neutral", "score-num", "score-label", "c-blue", "c-green", "c-amber", "c-red"):
        if css_class not in html:
            issues.append(f"HTML 缺少{STYLE_NAME}分色元素：{css_class}")
    if 'class="conclusion-box"' not in html:
        issues.append("HTML 结论概述必须是单框三段结构")
    if len(re.findall(r'class="card"', html)) != 4:
        issues.append("HTML “这个 Skill 是啥”必须是 4 张信息卡")
    for name in PREPARATION_NAMES:
        if name not in html:
            issues.append(f"HTML 安装准备缺少：{name}")
    return issues


def command_init(args):
    folder = Path(args.output_dir) / f"{safe_name(args.skill_name)}_首次_CO" / "过程文件_CO"
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"{safe_name(args.skill_name)}_啥好用评估_过程_CO.json"
    if target.exists() and not args.force:
        raise ValueError(f"文件已存在：{target}；如需覆盖请加 --force")
    target.write_text(json.dumps(report_skeleton(args.skill_name), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(target.resolve())


def command_check(args):
    payload = load_payload(args.input_json)
    issues = payload_issues(payload)
    if issues:
        print_issues(issues)
        return 1
    print("校验通过")
    return 0


def command_build(args):
    payload = load_payload(args.input_json)
    issues = payload_issues(payload)
    if issues:
        print_issues(issues)
        return 1
    output = Path(args.output) if args.output else default_output(args.input_json, payload)
    written = write_reports(payload, output)
    output_issues = []
    for path in written:
        output_issues.extend(f"{path.name}：{issue}" for issue in check_html(path))
    if output_issues:
        print_issues(output_issues)
        return 1
    for path in written:
        print(path.resolve())
    return 0


def main():
    parser = argparse.ArgumentParser(description="生成、校验和渲染啥好用 HTML 报告。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="生成完整 JSON 骨架")
    init_parser.add_argument("skill_name")
    init_parser.add_argument("--output-dir", default=".")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(handler=command_init)

    check_parser = subparsers.add_parser("check", help="一次列出全部 JSON 校验问题")
    check_parser.add_argument("input_json")
    check_parser.set_defaults(handler=command_check)

    build_parser = subparsers.add_parser("build", help="校验并生成 HTML")
    build_parser.add_argument("input_json")
    build_parser.add_argument("--output")
    build_parser.set_defaults(handler=command_build)

    args = parser.parse_args()
    try:
        return args.handler(args)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
