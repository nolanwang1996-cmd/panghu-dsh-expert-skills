#!/usr/bin/env python3
"""Build DSH-market SKILL.md files from WorkBuddy local plugin caches.

Read-only on the source side: ~/.workbuddy/plugins/marketplaces/*.
Cleaning contract (per Nolan's tutorial, adapted):
- keep role definitions, capability lists, SOPs verbatim
- strip per-agent frontmatter (tools/color are host-assigned in WorkBuddy)
- no identity-forcing clauses found (checked); nothing to strip there
- host-specific subagent mechanics (TeamCreate/Agent spawn/SendMessage) get a
  single adaptation note instead of fragile prose rewrites
"""
import os, re, glob, json

SRC = os.path.expanduser('~/.workbuddy/plugins/marketplaces')
OUT = '/tmp/workbuddy-expert-publish/experts'
os.makedirs(OUT, exist_ok=True)

FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.S)

def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

def parse_fm(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            v = v.strip().strip('"').strip()
            if v in ('>-', '|-', '>', '|'):
                v = ''
            fm[k.strip()] = v
    return fm, text[m.end():]

def clean_agent_md(path):
    """Return (name, description, body) with frontmatter stripped."""
    fm, body = parse_fm(read(path))
    body = body.strip() + '\n'
    return fm.get('name', os.path.splitext(os.path.basename(path))[0]), fm.get('description', ''), body

ADAPTATION_NOTE = (
    "> **环境适配说明**：本技能源自 WorkBuddy 多智能体专家包，已合并为单文件。"
    "原文中的宿主专属机制（TeamCreate 建团队、Agent 工具 spawn 成员、SendMessage 回传等）"
    "在无子代理能力的环境中，按等价方式执行：**严格按 SOP 阶段顺序，逐个切换到对应成员角色，"
    "以该角色的身份独立产出该阶段的专业结论（不混角色、不跳阶段），全部阶段完成后以主理人视角汇总输出。**\n"
)

def build_skill(skill_id, title, description, sections):
    """sections: list of (heading, text) appended after the header."""
    parts = [f'---\nname: {skill_id}\ndescription: {description}\n---\n',
             f'# {title}\n', ADAPTATION_NOTE]
    for heading, text in sections:
        parts.append(f'\n## {heading}\n\n{text}\n')
    content = ''.join(parts)
    outdir = os.path.join(OUT, skill_id)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, 'SKILL.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    return len(content.encode('utf-8'))

def agents_sections(base, names=None):
    out = []
    for path in sorted(glob.glob(os.path.join(base, 'agents', '*.md'))):
        name, desc, body = clean_agent_md(path)
        if names and name not in names:
            continue
        heading = f'成员角色：{name}'
        if desc:
            heading += f'（{desc[:60]}）'
        out.append((heading, body))
    return out

def rules_sections(base, only=None):
    out = []
    for path in sorted(glob.glob(os.path.join(base, 'rules', '*.md'))):
        base_name = os.path.basename(path)
        if only and base_name not in only:
            continue
        out.append((f'协作规则：{base_name}', read(path).strip()))
    return out

def skill_md_sections(base, sub):
    """Inline a sub-skill's SKILL.md body (frontmatter stripped)."""
    path = os.path.join(base, 'skills', sub, 'SKILL.md')
    if not os.path.exists(path):
        return []
    fm, body = parse_fm(read(path))
    return [(f'分析模块：{sub}（{fm.get("description", "")[:60]}）', body.strip())]

manifest = []

# ---------- 1. A股研究专家团 ----------
B = f'{SRC}/cb_teams_marketplace/plugins/a-share-analysis'
secs = agents_sections(B)
for sub in sorted(os.listdir(os.path.join(B, 'skills'))):
    secs += skill_md_sections(B, sub)
manifest.append(dict(
    id='wb-a-share-research', title='A股研究专家团（WorkBuddy 精选）',
    description='A股研究多角色专家团：个股研报、晨报速览、持仓诊断、行业筛选、资金动向等 7 个专家角色，附 20 个分析模块框架（公司质地打分、估值、财报解读、风格轮动等）。',
    category='投资研究', intro='源自 WorkBuddy 官方插件市场 a-share-analysis 包，7 个研究角色+20 个分析框架模块，已合并为单文件并适配单代理执行。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 2. 美股投资大师圆桌 ----------
B = f'{SRC}/cb_teams_marketplace/plugins/ai-hedge-fund'
secs = agents_sections(B) + rules_sections(B)
manifest.append(dict(
    id='wb-ai-hedge-fund', title='美股投资大师圆桌（WorkBuddy 精选）',
    description='21 位投资大师角色（巴菲特、芒格、达摩达兰、木头姐等）+ 基本面/成长/情绪/新闻分析师，多空辩论式投资分析圆桌，输出结构化交易建议。',
    category='投资研究', intro='源自 WorkBuddy 官方插件市场 ai-hedge-fund 包，21 位大师角色+分析师团队与协作规则，已合并为单文件并适配单代理执行。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 3. 高考志愿规划 ----------
B = f'{SRC}/cb_teams_marketplace/plugins/gaokao-advisor'
secs = agents_sections(B) + skill_md_sections(B, 'gaokao-zhiyuan-assistant')
manifest.append(dict(
    id='wb-gaokao-advisor', title='高考志愿规划专家（WorkBuddy 精选）',
    description='高考志愿填报全流程规划：分数定位、院校专业匹配、冲稳保梯度设计、招生章程风险核对，内含完整志愿助手方法框架。',
    category='教育升学', intro='源自 WorkBuddy 官方插件市场 gaokao-advisor 包（顾问角色+志愿助手框架）；原包联网查询模块依赖其专属搜索工具，已注明按当前环境等价执行。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 4. 深度调研专家 ----------
B = f'{SRC}/cb_teams_marketplace/plugins/deep-research'
secs = agents_sections(B) + rules_sections(B)
manifest.append(dict(
    id='wb-deep-research', title='深度调研专家（WorkBuddy 精选）',
    description='多源信息检索、事实验证、交叉核证与结构化研究报告生成的深度调研方法论，含研究子代理完整工作流与质量规则。',
    category='调研分析', intro='源自 WorkBuddy 官方插件市场 deep-research 包；原包附带微信公众号搜索模块依赖专属 API，未随附。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 5. 表格智能体 ----------
B = f'{SRC}/cb_teams_marketplace/plugins/sheetagent'
secs = agents_sections(B) + skill_md_sections(B, 'excel-generation') + skill_md_sections(B, 'excel-handler')
manifest.append(dict(
    id='wb-sheetagent', title='表格智能体 SheetAgent（WorkBuddy 精选）',
    description='Excel/表格任务智能体：表格创建、公式计算、数据分析、格式化与可视化的方法论与操作框架。',
    category='数据处理', intro='源自 WorkBuddy 官方插件市场 sheetagent 包；原包依赖其内置 MCP 服务器执行实际表格操作，本技能保留方法论框架，实际执行按当前环境可用工具等价完成。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 6. 敏捷开发专家团（BMAD） ----------
B = f'{SRC}/codebuddy-plugins-official/plugins/agent-team-agile-workflow'
secs = agents_sections(B)
manifest.append(dict(
    id='wb-agile-dev-team', title='敏捷开发专家团 BMAD（WorkBuddy 精选）',
    description='7 角色敏捷研发协作团：架构师、开发、产品负责人、项目经理、QA、评审、协调者，覆盖需求到交付的敏捷全流程。',
    category='编程工程', intro='源自 WorkBuddy 官方插件市场 agent-team-agile-workflow 包（BMAD 方法），7 角色完整定义，已合并为单文件并适配单代理执行。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 7. 功能开发三人组 ----------
B = f'{SRC}/codebuddy-plugins-official/plugins/feature-dev'
secs = agents_sections(B) + rules_sections(B)
manifest.append(dict(
    id='wb-feature-dev', title='功能开发三人组（WorkBuddy 精选）',
    description='代码架构师、代码探索者、代码评审者三角色协作的功能开发流程：先理解现状，再设计方案，最后评审把关。',
    category='编程工程', intro='源自 WorkBuddy 官方插件市场 feature-dev 包，3 角色完整定义。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 8. PR 审查工具箱 ----------
B = f'{SRC}/codebuddy-plugins-official/plugins/pr-review-toolkit'
secs = agents_sections(B)
manifest.append(dict(
    id='wb-pr-review-toolkit', title='PR 审查工具箱（WorkBuddy 精选）',
    description='6 个专职审查角色：代码评审、代码简化、注释分析、PR 测试分析、静默失败猎手、类型设计分析，对变更做鹰眼级审查。',
    category='编程工程', intro='源自 WorkBuddy 官方插件市场 pr-review-toolkit 包，6 个审查角色完整定义。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 9. 安全扫描专家团 ----------
B = f'{SRC}/codebuddy-plugins-official/plugins/security-scan'
secs = agents_sections(B) + rules_sections(B)
manifest.append(dict(
    id='wb-security-scan', title='安全扫描专家团（WorkBuddy 精选）',
    description='7 角色安全审计团：漏洞扫描、逻辑扫描、业务逻辑扫描、红队攻击视角、索引器、跨分片扫描与验证器，多视角交叉审计代码安全。',
    category='编程工程', intro='源自 WorkBuddy 官方插件市场 security-scan 包，7 个安全角色完整定义，已合并为单文件并适配单代理执行。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# ---------- 10. 开发必备五件套 ----------
B = f'{SRC}/codebuddy-plugins-official/plugins/development-essentials'
secs = agents_sections(B)
manifest.append(dict(
    id='wb-dev-essentials', title='开发必备五件套（WorkBuddy 精选）',
    description='开发、调试、优化、缺陷修复、修复验证五个日常开发高频角色，覆盖编码-调试-优化-验证闭环。',
    category='编程工程', intro='源自 WorkBuddy 官方插件市场 development-essentials 包，5 个开发角色完整定义。',
    sections=secs, license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

meta = []
for m in manifest:
    size = build_skill(m['id'], m['title'], m['description'], m['sections'])
    meta.append({'id': m['id'], 'title': m['title'], 'category': m['category'],
                 'intro': m['intro'], 'license_ref': m['license_ref'], 'bytes': size})
    print(f"{m['id']:24s} {size:7d} bytes  {m['title']}")

with open('/tmp/workbuddy-expert-publish/manifest.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)
print(f"\ntotal {len(meta)} skills, max bytes = {max(x['bytes'] for x in meta)} (limit 524288)")
