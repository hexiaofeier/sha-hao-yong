# 啥好用 Skill

告诉你“一个skill适不适合你用”的skill。

## 海选Skill并不是件容易的事

我们经常刷到各类skill榜单和推荐帖，“XX必装skill top10”“github今日最佳的skill没有之一”“三天斩获一千star”……写得天花乱坠。但时间久了，理性的你不免会冒出一个问题：

**“这个 Skill 到底是啥，好用吗，我能用吗？”**

装吧，之前跟着排行榜一个个试 Skill 时，也不是没踩过坑——折腾一晚上，要安各种依赖、要 API Key、要联网……一路十三招装完才发现，嘿，不太用得上，还白费不少 Token。

不装吧，万一错过了一个真正适合自己的好 Skill，怎么办？

“啥好用 Skill”就是干这个的：无论是 GitHub 网址，还是 Skill 压缩包或文件夹，只要你把候选 Skill 丢给它，再告诉它你的需求，它会从里到外扒一遍资料，初步帮你判断一下skill值不值得你装，帮你省点时间和 Token。

---

## 三个直白的问题

1. **这是啥** —— 它到底能干嘛，谁用得上，得给它喂点什么
2. **好用吗** —— 安装麻不麻烦，任务执行麻不麻烦，公开关注度如何，费不费 Token，有没有隐藏收费点，有没有什么风险
3. **适合我吗** —— 适合谁，不适合谁，对照你的真实需求，装还是不装，一句话说清楚

啥好用 skill 会翻看公开网页，或读取你提供的文件和材料，最后生成一份定制化的 **HTML 版 Skill 安装前说明书**。
打开就能看，也能直接分享给其他朋友。

---

## 兼容 Codex 和 Claude Code 

### Codex

丢进去：

```text
~/.codex/skills/sha-hao-yong/
```

新开会话，直接说“用啥好用评估这个 Skill”，或者显式喊它 `$sha-hao-yong`。

### Claude Code

丢进去：

```text
~/.claude/skills/sha-hao-yong/
```

同样可以直接描述你的评估需求，或者输入：

```text
/sha-hao-yong
```

---

## 安装方式

### Windows PowerShell

Codex：

```powershell
New-Item -ItemType Directory -Force "$HOME/.codex/skills" | Out-Null
git clone https://github.com/hexiaofeier/sha-hao-yong.git "$HOME/.codex/skills/sha-hao-yong"
```

Claude Code：

```powershell
New-Item -ItemType Directory -Force "$HOME/.claude/skills" | Out-Null
git clone https://github.com/hexiaofeier/sha-hao-yong.git "$HOME/.claude/skills/sha-hao-yong"
```

### macOS / Linux

Codex：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hexiaofeier/sha-hao-yong.git ~/.codex/skills/sha-hao-yong
```

Claude Code：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/hexiaofeier/sha-hao-yong.git ~/.claude/skills/sha-hao-yong
```

**最简单的，就是把 啥好用 skill 链接发给agent，让它们直接安装就行。**

安装后记得新开一个 Codex 或 Claude Code 会话，让它重新识别 Skill。

---

## 它跑起来很轻

- 一个能读 Skill、能看候选材料的 AI agent，例如 Codex 或 Claude Code
- Python 3——只用来校验 JSON、生成 HTML，跑完你甚至不会意识到它存在
- 不用安装第三方 Python 依赖，渲染脚本全程只用标准库，很干净

---

## 它的使用流程

1. 把候选 Skill 的链接、压缩包、文件夹或 `SKILL.md` 丢给它
2. 选一个模式：
   - 结合你的具体需求评估：很明确自己想干什么时选
   - 按一般目标用户评估：需求还不明确，只想先了解一下时选
3. 它只读翻材料、找证据，不用你一直盯着
4. 校验通过后，自动生成一份 HTML 报告

全程你只需要负责甩链接和 Skill 材料，再回答一两个问题，剩下的它自己跑。

---

## 它的目录

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

---

## 免责声明

“啥好用”给的是**装不装的参考意见**，不是免死金牌。它只能根据当前可读的公开网页、文件和说明作安装前判断，不能替你做代码安全审计、恶意代码检测、软件质量测试、隐私合规审查，也不能签法律文件。

下载、安装、授权、付费、上传或运行自动操作之前，请再核对来源、依赖、权限、数据去向、收费方式和许可证。安装 Skill 的潜在风险，最终仍需要你自己把关哟！

---

## License

[MIT License](LICENSE)——欢迎使用和修改，具体权利与免责边界以许可证为准 😌
