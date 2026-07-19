---
name: sha-hao-yong
description: Create a read-only, plain-language HTML installation brief for a candidate Skill or related AI capability asset. Use when the user provides a URL, repository, ZIP, folder, README, plugin, MCP, CLI, app, or installation guide and asks what it does, how hard it is to install or use, what it costs, how much Token or risk it involves, whether it fits a need, or whether it is worth installing. Do not use for security certification or automatic installation.
---

# 啥好用

把候选 Skill 写成一份普通人能看懂的安装前说明书，回答：**这是啥、好用吗、适合吗**。最终交付为单文件 HTML。

默认只读。不安装、不运行陌生代码、不读取凭证、不注册、不付费、不上传、不修改候选对象。

## Reference 路由

- 判断能力来自哪里：读 [complexity-map.md](references/complexity-map.md)。
- 计算任何定量分数：先读 [scoring-rubric.md](references/scoring-rubric.md)，再读对应指标文件。
- 计算安装复杂度：读 [installation-score.md](references/installation-score.md)。
- 计算任务复杂度：读 [task-complexity.md](references/task-complexity.md)。
- 判断 Skill 调用准确性：读 [invocation-accuracy.md](references/invocation-accuracy.md)。
- 计算 Token 消耗：读 [token-score.md](references/token-score.md)。
- 计算风险值：读 [risk-score.md](references/risk-score.md)。
- 计算推荐程度：读 [fit-assessment.md](references/fit-assessment.md)。
- 写用户可见文字：读 [writing-style.md](references/writing-style.md)。
- 输出 HTML：读 [report-template.md](references/report-template.md)，并强制使用 `scripts/render_report.py`。

只读取本次任务需要的 Reference。

## 工作流

### 1. 锁定评估对象

- 明确评估的是单个 Skill、整个仓库、插件、CLI、应用还是产品入口。
- 一个仓库含多个对象时，拆开说明，不把仓库数据直接算到单个 Skill 上。
- 需要向用户显示名称时，只从已提供或可立即看到的信息中取最明确的一项：网页或页面标题、URL 最后一段、文件夹名、文件名、目标文件 YAML 中的 `name`。取不到时显示 `【】`；不为识别名称提前读取正文、依赖或安装说明。

### 2. 选择评估方式

启动后，用户尚未明确选择评估方式时，下一步只显示一道选择题：

- **A：需要结合我的需求评估**
- **B：按一般目标用户进行评估**

支持交互控件时使用可点击的单选题；不支持时显示文字选项，请用户回复 A 或 B。显示后停止，等待用户选择。不得提前读取候选材料、收集证据或开始评估。

- 用户选 B：直接进入第 3 步。根据候选对象的官方定位界定一般目标用户，并在报告中写清判断对象；不再追问需求。
- 用户选 A：使用第 1 步识别的名称，问一个必答开放题：**您希望评估的 Skill 是【目标 Skill 名称】，请问您希望它能帮您做什么？** 显示后停止，等待用户回答；收到回答后立即进入第 3 步，不再追问设备、AI agent、费用、Token、隐私或操作偏好。

用户已在启动消息中明确选择 A 或 B 时，直接进入对应分支，不重复显示第一题。用户选择 A 且已同时写明具体需求时，直接进入第 3 步，不重复提问。不把用户没有提供的环境和偏好当成事实。

### 3. 收集证据

优先检查目标文件、官方文档、安装说明、依赖清单、发布记录、许可证和官方价格。需要判断热度与维护情况时，再查榜单、Stars、Forks、更新时间、Issue、测试和真实案例。

- 使用当前 AI agent 已有的文件读取、网页访问或搜索能力，不要求用户额外安装工具；
- 优先检查用户提供的材料和官方来源；查不到的信息写 `未验证`，不得猜测；
- 无法联网或无法读取链接时，继续评估已有材料；只有无法判断对象是什么时，才请用户补充核心文件；
- 只有找到可核验的公开下载数时，报告才显示“下载量”；没有数值则直接删除该行。
- Stars、Forks 或合集仓库数据不得冒充单个 Skill 的使用效果。
- 仓库公开可读或可下载，不等于免费使用或允许商用；许可证未确认时不得写“核心免费”。
- 价格、兼容性和维护情况查不到时写 `未验证`，不得猜测。

### 4. 回答三问

**这个 Skill 是啥**只回答：

1. 适合什么用户，在什么情况下调用，解决什么问题；
2. 用户要提供什么，Skill 通过什么方式、经过哪些核心步骤完成任务；
3. 最终交付什么结果，结果能否直接使用、修改或核对；
4. 真正干活的是 AI agent、电脑软件、联网服务，还是它们的组合。

**这个 Skill 好用吗**只回答：

1. 公开关注度：可核验的 Stars、Forks、榜单和公开下载量（如有）；
2. 安装复杂度：软件、依赖、账号、Key、权限、系统适配和持续维护；
3. 任务复杂度：输入准备、执行步骤、分支选择、人工确认、返工和故障恢复；
4. Skill 调用准确性：只根据名称、描述和触发规则，判断是否容易漏调用或误调用；
5. 可验证性：文档、维护、更新、Issue、测试和真实案例是否充分；
6. 额外涉及费用：软件订阅、API、联网服务和其他付费点；
7. Token 消耗：完成典型核心任务需要的模型额度；
8. 风险值：涉及的数据、权限、外部操作和潜在损失。

**这个 Skill 适合你吗**只回答：

1. 是否匹配用户想完成的任务和想得到的结果；
2. 哪些场景适合，哪些场景不适合；
3. 是否建议安装。

不得复述前两部分。第一次试用、扩展、复盘和停用方式只放“使用节奏建议”。

### 5. 统一量表

- 安装复杂度：0—10；分数越高，安装和维护越费事。
- 任务复杂度：0—10；分数越高，完成一次典型任务需要的输入、操作、判断和人工处理越多。
- Skill 调用准确性：定性判断为较准确、偏宽、偏窄或无法判断，并写清名称、描述和触发规则如何影响调用。
- Token 消耗：0—10；分数越高，通常越费模型额度。
- 风险值：0—10；分数越高，涉及的数据、权限和外部操作越多。
- 推荐程度：0—10；分数越高，越值得当前用户或报告中写明的人群采用。

允许一位小数。每个分数必须同时写等级、主要原因和判断依据。用户报告不得出现 `S5`、`P1`、`A20`、`F0` 或五项推荐分拆解。

### 6. 输出固定 HTML

先定位当前 `SKILL.md` 所在目录，再调用该目录下的 `scripts/render_report.py`。不要假设用户当前工作目录就是 Skill 目录。

先运行 `init` 生成完整 JSON 骨架，再按 [report-template.md](references/report-template.md) 填写。完成后按 [writing-style.md](references/writing-style.md) 做短句质检。

```bash
<Python命令> <Skill目录>/scripts/render_report.py init <Skill名称> --output-dir <交付目录>
```

填完 JSON 后，一键校验并生成：

```bash
<Python命令> <Skill目录>/scripts/render_report.py build <过程JSON路径>
```

`<Python命令>` 使用设备中真实可用的 Python 3：Windows 常见为 `py -3` 或 `python`，macOS/Linux 常见为 `python3`。Claude Code 可使用 `${CLAUDE_SKILL_DIR}` 定位 Skill；其他 AI agent 直接使用已读取的 `SKILL.md` 所在目录。

`build` 一次列出全部校验问题；通过后自动把 HTML 生成到 `过程文件_CO/` 的上一级目录，并检查固定章节、10 格推荐条、页尾说明、安装准备、渐变和待填写项。只想检查时运行 `<Python命令> <Skill目录>/scripts/render_report.py check <过程JSON路径>`。

脚本只使用 Python 标准库。它固定 JSON 字段、黑曜生漆版式、10 格推荐条、结论卡片和免责声明。

- 禁止直接手写 HTML 或 CSS；
- 禁止渲染后人工修改报告正文；
- 脚本报错时修改 JSON，不得修改脚本绕过检查；
- JSON 由 `init` 放入交付目录下的 `过程文件_CO/`；最终交付只指向 HTML。

## 写作约束

- Skill 定位拆成 3—4 个短句。每句明确使用目标 Skill 名称、用户或你作主语；不用“这是一个”“这是一套”开头。
- 页首 Skill 定位第一句写出目标 Skill 名称；第二、三句再次指代时用“它”；第四句允许重新写出名称作收束。
- 其他卡片或段落第一句写出目标 Skill 名称后，后续再次指代它时用“它”。用户和你仍按原意保留。出现其他可能混淆的对象时，重新写出目标 Skill 名称。
- “适合场景 / 不适合场景”使用平行短语，不套用主语规则，不重复“适合”“不适合”。
- 结论卡片顺序固定为：最终结论、量化分析、适用场景、使用建议。
- 最终结论第一句必须带目标 Skill 名称，例如“auto-tutor 部分匹配你的需求”。
- 按适用用户判断时，改写为“适合这类用户”“部分适合这类用户”或“不适合这类用户”；具体指谁必须在推荐条旁写清楚。
- “这个 Skill 适合你吗”置顶显示匹配结论与安装建议，由渲染器保证两者与总评一致。
- 量化分析只报关键数字；适用场景只写适合谁、做什么、得到什么；使用建议直接写装不装、何时考虑。
- 使用建议与最终结论连用时，最终结论先写出目标 Skill 名称，使用建议用“它”承接；有条件推荐必须在第一句写出具体条件。
- “使用时机、用户提供、任务步骤、额外需要、最后交付”全部使用短句列表，每条不超过 35 个汉字。
- 推荐条分成 10 个等宽色块，由浅到深显示得分；评分说明放在色条下方。
- 以表格、列表和短句为主；同一事实只写一次。
- 用户报告不用“宿主、执行链、静态扫描、证据类型”等内部词。改写为“AI agent、实际步骤、只检查了公开文件、判断依据”。
- 禁止 `multi_agent`、CI、LLM、PR 等未解释缩写；统一使用“AI agent”，不用“多 agent”“子 agent”“AI 编程 agent”。
- 正面陈述已知条件。禁止“不要把……理解成……”“并不是……而是……”等反向教育句式。
- 禁止侧面和迂回表达。能写“它不能完成会议纪要”，就不写“核心工作仍需其他能力完成”。
- 允许少量轻松表达，但费用、风险、隐私和最终结论不用玩笑。
- 不用热度替代效果，不用安装简单替代质量，不用风险低替代安全认证。
- 评分依据不足时给区间或写 `未验证`，不补零，不伪造精确度。

## 边界

- 这是安装前说明书，只提供采用参考，不能替代专业评测，包括代码安全审计、恶意代码检测、软件质量与兼容性测试、隐私合规审查、许可证审查或法律意见。
- 只读检查不得冒充安装实测、兼容性测试、性能测试或长期使用体验。
- 不要求用户在对话中粘贴 API Key、Cookie、Token、密码或其他凭证。
- 报告必须提醒用户：下载、安装、授权、付费、上传、发布或运行自动操作前，自行核对来源、依赖、权限、数据去向、收费和许可证，并优先使用测试环境、最小权限、专用账号和可恢复备份。
- 评分只作采用参考；项目版本、价格、平台规则和依赖更新后应重新评估。
- 来源冲突时并列保留并标 `【待核实】`。
- 页尾必须解释“AI agent”：能够读取 Skill、理解任务，并按规则调用电脑软件或联网服务完成工作的 AI 助手；具体权限取决于产品和用户授权。
