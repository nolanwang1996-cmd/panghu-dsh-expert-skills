---
name: wb-chat-web
description: 聊天类 Web 应用开发：流式界面、会话管理、消息渲染与多模型接入。
---
# 聊天 Web 应用专家
> **来源与适配说明**：本技能整理自 WorkBuddy 内置/官方市场专家包，单文件合并。原文如引用宿主专属工具或子代理机制，按当前环境等价能力执行即可。

## 协作规则：cbc_sdk_web

# CodeBuddy Agent SDK Web 开发指南

这是一个快速开发指南,帮助你基于模板创建自定义 Web Agent 应用。

**关联技能**: `/init-cbc-sdk-web` - 这是一个本地技能,会从模板目录复制完整的项目结构

## ⚠️ 重要说明

**`/init-cbc-sdk-web` 是一个本地技能(Skill),不是普通的 CLI 命令!**

**这个技能有预置的完整项目模板,必须从模板目录复制,不要从零编写代码!**

### 模板位置

模板文件位于以下位置之一:
1. 已加载的 skill: `~/.codebuddy/skills/init-cbc-sdk-web/templates/`
2. Marketplace plugins: `~/.codebuddy/plugins/marketplaces/*/plugins/codebuddy-chat-web/skills/init-cbc-sdk-web/templates/`
3. 当前工作目录: `.codebuddy/skills/init-cbc-sdk-web/templates/`

### 如何使用模板

**方法 1: 使用复制脚本(推荐)**

在 skill 目录下有一个 `copy-template.sh` 脚本,使用它来复制模板:

```bash
# 找到 skill 目录(会搜索所有可能的位置)
SKILL_DIR=$(find ~/.codebuddy/skills ~/.codebuddy/plugins .codebuddy/skills -path "*/codebuddy-chat-web/skills/init-cbc-sdk-web" -o -name "init-cbc-sdk-web" -type d 2>/dev/null | head -1)

# 使用脚本复制模板
bash "$SKILL_DIR/copy-template.sh" my-agent-app
```

**方法 2: 手动复制**

如果脚本不可用,手动复制模板内容(注意:复制模板**内容**,不是模板目录本身):

```bash
# 找到模板位置(会递归搜索所有可能的目录)
TEMPLATE_DIR=$(find ~/.codebuddy/skills ~/.codebuddy/plugins .codebuddy/skills -path "*/init-cbc-sdk-web/templates" -type d 2>/dev/null | head -1)

# 创建项目目录并复制模板内容
mkdir -p my-agent-app
cp -r "$TEMPLATE_DIR/"* my-agent-app/
```

### 重要提醒

- ❌ **不要**从零开始编写代码
- ❌ **不要**尝试手动创建所有文件
- ✅ **必须**从模板目录复制完整项目
- ✅ **必须**保持模板的完整文件结构

## 推荐工作流程

### 第零步:检查 CodeBuddy Code 是否已安装

在开始之前,必须确保 CodeBuddy Code 已安装:

```bash
# 检查是否已安装
codebuddy --help

# 如果未安装,执行以下命令安装
npm install -g @tencent-ai/codebuddy-code
```

### 第一步:使用模板创建应用

```bash
# 使用技能初始化项目(会从 templates/ 目录复制完整项目)
/init-cbc-sdk-web my-agent-app

# 进入项目目录
cd my-agent-app

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**模板包含的完整文件结构**:
```
my-agent-app/
├── server/              # 后端服务
│   ├── server.ts       # Express + WebSocket 服务器
│   ├── agent.ts        # Agent SDK 封装
│   ├── chat-session.ts # 会话管理
│   ├── store.ts        # 数据存储
│   ├── config.ts       # 配置文件
│   └── types.ts        # 类型定义
├── client/              # 前端应用
│   ├── App.tsx         # 主应用组件
│   ├── components/     # UI 组件
│   └── hooks/          # React Hooks
├── package.json         # 依赖配置
├── tsconfig.json        # TypeScript 配置
├── vite.config.ts       # Vite 配置
├── tailwind.config.js   # Tailwind 配置
└── .env.example         # 环境变量模板
```

### 第二步:根据需求定制应用

在 `server/index.ts` 中修改 `systemPrompt` 来定制你的 Agent:

```typescript
const systemPrompt = `
你是一个 [你的 Agent 角色],专门帮助用户 [主要功能]。

核心能力:
1. [能力描述]
2. [能力描述]
3. [能力描述]

工作方式:
- [工作方式描述]
- [输出格式要求]
`;
```

### 第三步:测试和迭代

1. 在浏览器中访问 http://localhost:3000
2. 测试你的 Agent 功能
3. 根据效果调整 systemPrompt
4. 如需更多功能,参考下方 SDK 文档

### 第四步:遇到问题时查阅文档

**官方文档**(需要深入了解时参考):
- **TypeScript SDK 文档**: https://www.codebuddy.ai/docs/zh/cli/sdk-typescript
- **通用 SDK 文档**: https://www.codebuddy.ai/docs/zh/cli/sdk

---

## 常见定制场景

### 场景 1:修改系统提示词

最简单的定制方式,直接修改 `server/index.ts` 中的 `systemPrompt`:

```typescript
const systemPrompt = `你是一个代码审查助手,帮助开发者提高代码质量。`;
```

### 场景 2:调整 AI 模型

在 `server/index.ts` 中修改模型配置:

```typescript
const config = {
  model: "claude-sonnet-4",  // 或 "claude-opus-4"
  maxTurns: 10,
  cwd: process.cwd()
};
```

### 场景 3:限制工具访问

控制 Agent 可以使用的工具:

```typescript
const config = {
  allowedTools: ["Read", "Grep", "WebSearch"],  // 只允许这些工具
  // ...其他配置
};
```

---

## 快速参考:核心概念

### Query API(单次对话)

```typescript
import { query } from "@tencent-ai/agent-sdk";

const stream = query({
  prompt: "你的问题",
  options: { model: "claude-sonnet-4" }
});

for await (const message of stream) {
  console.log(message);
}
```

### Session API(多轮对话)

```typescript
import { unstable_v2_createSession } from "@tencent-ai/agent-sdk";

const session = await unstable_v2_createSession({
  model: "claude-sonnet-4"
});

await session.sendMessage("第一条消息");
await session.sendMessage("后续消息");
```

### 消息类型

SDK 返回三种消息类型:
- **System**: 会话初始化信息
- **Assistant**: AI 的回复内容
- **Result**: 执行完成的统计信息(耗时、成本)

---

## 配置选项速查表

| 选项 | 说明 | 示例 |
|------|------|------|
| `model` | AI 模型 | `"claude-sonnet-4"` |
| `maxTurns` | 最大对话轮数 | `10` |
| `systemPrompt` | 系统提示词 | `"你是助手"` |
| `allowedTools` | 允许的工具 | `["Read", "Write"]` |
| `cwd` | 工作目录 | `process.cwd()` |

---

## 进阶功能(需要时查阅)

当你需要以下功能时,请查阅官方文档:

### 1. 错误处理
处理 SDK 异常和连接错误

### 2. 权限控制
使用 `canUseTool` 回调精细控制工具访问

### 3. 自定义 Agent
定义专门的子 Agent 处理特定任务

### 4. MCP 服务器
集成自定义工具和功能

### 5. Hook 系统
在工具执行前后插入自定义逻辑

---

## 生产环境建议

### 安全性
- 将 SDK 隔离到独立服务/容器
- 添加用户认证和授权
- 验证和清理用户输入

### 性能
- 使用数据库替代内存存储
- 添加请求限流
- 实现日志和监控

### 配置
- 使用环境变量管理敏感信息
- 设置合适的 CORS 策略
- 配置 HTTPS

---

## 完整文档链接

需要深入了解时,请访问:

- **TypeScript SDK 文档**: https://www.codebuddy.ai/docs/zh/cli/sdk-typescript
- **通用 SDK 文档**: https://www.codebuddy.ai/docs/zh/cli/sdk

文档涵盖:
- 完整 API 参考
- 高级配置选项
- 自定义 Agent 和 MCP 服务器
- Hook 系统详解
- 权限控制机制
- 多 Agent 协作
- Python SDK 使用
- 生产部署指南

## 模块：init-cbc-sdk-web

# init-cbc-sdk-web

Initialize a complete web-based chat application powered by CodeBuddy Agent SDK.

## Description

This skill scaffolds a full-stack chat application with:
- **Backend**: Express server with SSE support and CodeBuddy Agent SDK integration
- **Frontend**: React application with Vite, TypeScript, TDesign React, and Tailwind CSS
- **Real-time Communication**: SSE-based streaming with multi-chat support
- **Database**: SQLite for session and message persistence
- **Modern Stack**: TypeScript, React 18, TDesign React, Express 4, Vite 5

## When to use this skill

Use this skill when you need to:
- Create a new chat application powered by AI agents
- Build a web interface for CodeBuddy Agent SDK
- Set up a starter project for agent-based conversations
- Prototype AI-powered chat features
- Learn how to integrate CodeBuddy Agent SDK in a web application

## How to use this skill

### Interactive Mode
```bash
/init-cbc-sdk-web
```
The skill will ask you for a project name.

### Direct Mode
```bash
/init-cbc-sdk-web my-chat-app
```
Provide the project name directly as an argument.

## Implementation Details

**⚠️ This skill uses a template-based approach - DO NOT write code from scratch!**

When implementing this skill, you MUST use the provided `copy-template.sh` script:

1. **Locate the skill directory**:
   - Check `~/.codebuddy/skills/init-cbc-sdk-web/`
   - Or check `.codebuddy/skills/init-cbc-sdk-web/` in current directory

2. **Use the copy script**:
   ```bash
   bash <skill-directory>/copy-template.sh <project-name>
   ```

3. **The script will**:
   - Copy the complete template from `templates/` directory
   - Update package.json with the project name
   - Display next steps for the user

**DO NOT** manually read and write each template file. The script handles everything.

## What this skill does

1. **Creates project directory** with the specified name
2. **Scaffolds complete application** including:
   - Express backend with REST API and SSE server
   - React frontend with TDesign React UI components
   - TypeScript configuration
   - TDesign React + Tailwind CSS styling
   - SQLite database setup
   - Build and development scripts
3. **Provides ready-to-use code** for:
   - Agent SDK integration (query, unstable_v2_createSession, unstable_v2_authenticate)
   - Chat session management with persistence
   - Real-time message streaming via SSE
   - Multi-chat support with SQLite storage
   - Permission control system
   - Custom agent configuration
   - Theme switching (light/dark)

## Project Structure

```
your-project-name/
├── server/                 # Backend code
│   ├── index.ts           # Express + SSE server
│   ├── index.d.ts         # Type definitions
│   └── db.ts              # SQLite database operations
├── src/                    # Frontend code
│   ├── App.tsx            # Main React app
│   ├── components/        # UI components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ChatMessages.tsx
│   │   ├── ChatInput.tsx
│   │   ├── ToolCallsCollapse.tsx
│   │   ├── AgentConfigDialog.tsx
│   │   ├── PermissionDialog.tsx
│   │   ├── NewChatDialog.tsx
│   │   ├── NewChatView.tsx
│   │   └── SettingsPage.tsx
│   ├── hooks/             # React hooks
│   │   ├── useChat.ts
│   │   ├── useSessions.ts
│   │   ├── useAgents.ts
│   │   ├── useModels.ts
│   │   └── useTheme.ts
│   ├── pages/             # Page components
│   │   └── ChatPage.tsx
│   ├── utils/             # Utilities
│   │   └── iconMap.ts
│   ├── types.ts           # Type definitions
│   ├── config.ts          # Configuration
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── data/                   # Data storage
│   └── chat.db            # SQLite database
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite config
├── tailwind.config.js     # Tailwind config
├── index.html             # HTML template
├── README.md              # Documentation
└── DEVELOPMENT.md         # Development guide
```

## Next Steps

After running this skill:

1. **Navigate to project directory**:
   ```bash
   cd your-project-name
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your `CODEBUDDY_API_KEY`

4. **Start development server**:
   ```bash
   npm run dev
   ```
   This starts both backend (port 3001) and frontend (port 5173)

5. **Open in browser**:
   Navigate to `http://localhost:5173`

## Features

- **Multi-chat support**: Create and manage multiple chat conversations with SQLite persistence
- **Real-time streaming**: See AI responses as they're generated via SSE
- **Tool call visualization**: View when the agent uses tools with expandable details
- **Permission control**: Support for multiple permission modes (default, acceptEdits, plan, bypassPermissions)
- **Custom agents**: Create and manage multiple agent configurations
- **Theme switching**: Support for light/dark themes
- **Session persistence**: Chat history and agent sessions stored in SQLite database
- **Modern UI**: Clean, responsive interface with TDesign React components
- **TypeScript**: Full type safety across frontend and backend

## Keywords

chat, web, agent-sdk, react, express, websocket, typescript, vite, tailwind, ai, assistant, conversation, real-time, streaming

## Requirements

- Node.js 18 or higher
- CodeBuddy API key (get from https://www.codebuddy.cn)
- Modern web browser

## Customization

After initialization, you can customize:
- Agent configurations (system prompt, model, permissions) in Settings page or code
- UI components in `src/components/`
- Styling in `src/index.css`, TDesign theme, and Tailwind config
- Server configuration in `server/index.ts`
- Database schema in `server/db.ts`
- Permission modes and tool allowances in agent settings

## Learn More

- **TypeScript SDK Documentation**: https://www.codebuddy.ai/docs/zh/cli/sdk-typescript
- **General SDK Documentation**: https://www.codebuddy.ai/docs/zh/cli/sdk
- Project README.md for detailed setup instructions
- SDK guide in plugin rules for best practices
