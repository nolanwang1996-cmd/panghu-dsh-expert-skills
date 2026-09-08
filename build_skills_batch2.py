#!/usr/bin/env python3
"""Batch 2: work-focused expert skills (office/product/legal/data/writing).

Sources:
- tencent-docx builtin experts (WorkBuddy.app bundle, read-only)
- cb_teams / codebuddy-official marketplace caches (~/.workbuddy, read-only)
Same cleaning contract as batch 1 (build_skills.py).
"""
import os, re, glob, json

SRC = os.path.expanduser('~/.workbuddy/plugins/marketplaces')
DOCX = '/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/builtin-plugins/tencent-docx/experts'
OUT = '/tmp/workbuddy-expert-publish/experts'
os.makedirs(OUT, exist_ok=True)
FM_RE = re.compile(r'\A---\n(.*?)\n---\n', re.S)

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def strip_fm(text):
    m = FM_RE.match(text)
    return text[m.end():].strip() if m else text.strip()

ADAPT = ('> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。'
         '原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。\n')

def emit(skill_id, title, description, sections):
    parts = [f'---\nname: {skill_id}\ndescription: {description}\n---\n', f'# {title}\n', ADAPT]
    for h, t in sections:
        parts.append(f'\n## {h}\n\n{t}\n')
    content = ''.join(parts)
    d = os.path.join(OUT, skill_id)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'SKILL.md'), 'w', encoding='utf-8').write(content)
    return len(content.encode('utf-8'))

def docx_expert(name, label):
    base = os.path.join(DOCX, name)
    secs = [('专家方法论', strip_fm(read(os.path.join(base, 'SKILL.md'))))]
    for ref in sorted(glob.glob(os.path.join(base, 'references', '**', '*.md'), recursive=True)):
        rel = os.path.relpath(ref, os.path.join(base, 'references'))
        secs.append((f'参考：{rel[:-3]}', strip_fm(read(ref))))
    return secs

def agents_sections(base):
    out = []
    for path in sorted(glob.glob(os.path.join(base, 'agents', '*.md'))):
        fm, body = (lambda t: (({}, strip_fm(t))))(read(path))
        name = os.path.splitext(os.path.basename(path))[0]
        out.append((f'成员角色：{name}', body))
    return out

def rules_sections(base):
    return [(f'协作规则：{os.path.basename(p)[:-3]}', strip_fm(read(p)))
            for p in sorted(glob.glob(os.path.join(base, 'rules', '*.md')))]

def subskills(base):
    out = []
    for d in sorted(glob.glob(os.path.join(base, 'skills', '*'))):
        p = os.path.join(d, 'SKILL.md')
        if os.path.exists(p):
            out.append((f'模块：{os.path.basename(d)}', strip_fm(read(p))))
    return out

def commands_sections(base):
    return [(f'操作指引：{os.path.basename(p)[:-3]}', strip_fm(read(p)))
            for p in sorted(glob.glob(os.path.join(base, 'commands', '*.md')))]

BATCH = []

def add(skill_id, title, desc, category, intro, secs):
    BATCH.append(dict(id=skill_id, title=title, description=desc, category=category,
                      intro=intro, sections=secs,
                      license_ref='LicenseRef-WorkBuddy-marketplace-unverified'))

# 1. 工作汇报写作（内置 work-report-expert，4K 单文件）
add('wb-work-report', '工作汇报写作专家',
    '年终总结、述职报告、项目汇报、竞聘演讲、周报月报等职场汇报写作：金字塔原理+STAR 法则，结构清晰、数据有力、亮点突出。',
    '办公协同', '源自 WorkBuddy 内置 work-report-expert。',
    docx_expert('work-report-expert', '工作汇报'))

# 2. 通用写作兜底（7 维质量框架 + 10 文体矩阵）
add('wb-general-writer', '通用写作专家',
    '公文、周报、方案、邮件、文案、新媒体稿件等通用写作：7 维质量评分框架（事实/逻辑/结构/语言/风格/受众/洞察）与 10 种文体适配矩阵。',
    '办公协同', '源自 WorkBuddy 内置 general-writer（含文体矩阵与质量框架 references）。',
    docx_expert('general-writer', '通用写作'))

# 3. 商业文案（AIDA+广告法合规）
add('wb-business-copy', '商业文案专家',
    '品牌文案、营销邮件、产品描述、广告策划、社交媒体内容：AIDA 模型与广告法合规要求下的高转化率文案创作与诊断。',
    '市场营销', '源自 WorkBuddy 内置 business-copy-expert（含各渠道方法论与反模式库）。',
    docx_expert('business-copy-expert', '商业文案'))

# 4. 技术写作
add('wb-tech-writing', '技术写作专家',
    '技术文章、教程、架构解析、源码分析、开源项目文档：基于开发者体验（DX）与技术传播最佳实践的深度技术内容创作。',
    '内容创作', '源自 WorkBuddy 内置 tech-blog-expert。',
    docx_expert('tech-blog-expert', '技术写作'))

# 5. 合同法务
add('wb-legal-contract', '合同法务专家',
    '各类合同/协议/条款的起草与审查：必备条款完整性检查、权利义务对称性审核、高风险点防范，分章 Critic 严格审查模式。',
    '法务合规', '源自 WorkBuddy 内置 legal-contract-expert（含条款库与反模式库）。',
    docx_expert('legal-contract-expert', '合同法务'))

# 6. 产品管理（rules + 10 个子技能）
B = f'{SRC}/cb_teams_marketplace/plugins/product-management'
add('wb-product-management', '产品管理专家',
    '产品全流程工具箱：功能规格、路线图、用户研究综合、竞品分析、指标追踪、干系人沟通、冲刺规划、头脑风暴等 10 个模块。',
    '产品设计', '源自 WorkBuddy 官方市场 product-management 包（rules+skills 全量内联）。',
    rules_sections(B) + subskills(B))

# 7. 需求驱动研发工作流（4 角色 + pilot 指引）
B = f'{SRC}/codebuddy-plugins-official/plugins/requirements-driven-workflow'
add('wb-requirements-workflow', '需求驱动研发工作流',
    '从需求到交付的四角色流程：需求生成、需求编码、需求评审、需求测试，附 pilot 主控指引，保证需求可追溯、实现可验证。',
    '编程工程', '源自 WorkBuddy 官方市场 requirements-driven-workflow 包。',
    agents_sections(B) + commands_sections(B))

# 8. 数据分析（8 个方法论模块）
B = f'{SRC}/cb_teams_marketplace/plugins/data'
add('wb-data-analysis', '数据分析专家',
    '数据分析全流程方法论：数据探索、清洗验证、SQL 查询、统计分析、可视化、交互式仪表盘、分析工作流与上下文提取 8 个模块。',
    '数据处理', '源自 WorkBuddy 官方市场 data 包（rules+skills 全量内联）。',
    rules_sections(B) + subskills(B))

meta = []
for m in BATCH:
    size = emit(m['id'], m['title'], m['description'], m['sections'])
    meta.append({k: m[k] for k in ('id', 'title', 'description', 'category', 'intro', 'license_ref')} | {'bytes': size})
    print(f"{m['id']:24s} {size:7d} bytes  {m['title']}")

json.dump(meta, open('/tmp/workbuddy-expert-publish/manifest-batch2.json', 'w'), ensure_ascii=False, indent=2)
print(f"\ntotal {len(meta)}, max = {max(x['bytes'] for x in meta)} (limit 524288)")
