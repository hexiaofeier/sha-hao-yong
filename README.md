# 啥好用 Skill

把候选 Skill 写成一份普通人能看懂的 HTML 安装前说明书，回答三个问题：

- 这个 Skill 是啥；
- 这个 Skill 好用吗；
- 这个 Skill 适合你吗。

它只读检查公开文件和用户提供的材料，不自动安装候选对象，也不替代代码安全审计、隐私合规审查或专业测评。

## 主要评估内容

- Skill 定位、调用时机、输入、任务步骤与最终交付；
- 安装复杂度、任务复杂度与 Skill 调用准确性；
- 公开关注度、额外涉及费用、Token 消耗与风险值；
- 适合场景、不适合场景与安装建议。

最终生成固定版式的单文件 HTML 报告。

## 兼容性

### Codex

把整个仓库放到：

```text
~/.codex/skills/sha-hao-yong/
```

新建会话后，可以直接说“用啥好用评估这个 Skill”，也可以显式调用 `$sha-hao-yong`。

### Claude Code

把整个仓库放到：

```text
~/.claude/skills/sha-hao-yong/
```

Claude Code 会读取同一份 `SKILL.md`。可以直接描述评估需求，也可以输入：

```text
/sha-hao-yong
```

`agents/openai.yaml` 仅提供 Codex 展示信息，Claude Code 会忽略它。核心规则、References 和 Python 渲染脚本由两端共用。

## 安装

### Windows PowerShell

Codex：

```powershell
git clone https://github.com/hexiaofeier/sha-hao-yong.git "$HOME/.codex/skills/sha-hao-yong"
```

Claude Code：

```powershell
git clone https://github.com/hexiaofeier/sha-hao-yong.git "$HOME/.claude/skills/sha-hao-yong"
```

### macOS / Linux

Codex：

```bash
git clone https://github.com/hexiaofeier/sha-hao-yong.git ~/.codex/skills/sha-hao-yong
```

Claude Code：

```bash
git clone https://github.com/hexiaofeier/sha-hao-yong.git ~/.claude/skills/sha-hao-yong
```

## 运行要求

- 能读取 Skill 和访问候选材料的 AI agent；
- Python 3，仅用于校验 JSON 并生成 HTML；
- Python 脚本只使用标准库，不需要额外安装依赖。

## 使用流程

1. 提供候选 Skill 的链接、压缩包、文件夹或 `SKILL.md`；
2. 选择结合个人需求评估，或按一般目标用户评估；
3. AI agent 只读收集证据并完成评估；
4. Skill 生成并校验 HTML 报告。

## 目录结构

```text
sha-hao-yong/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
└── scripts/
    └── render_report.py
```

## 免责声明

“啥好用”只提供安装前的采用参考，不能替代代码安全审计、恶意代码检测、软件质量与兼容性测试、隐私合规审查、许可证审查或法律意见。下载、安装、授权、付费、上传或运行自动操作前，请自行核对来源、依赖、权限、数据去向、收费和许可证。

## License

[MIT License](LICENSE)
