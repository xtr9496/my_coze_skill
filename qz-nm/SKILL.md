---
name: qz-nm
description: 根据UI设计文档和项目架构方案构建前端项目，根据项目架构和需求文档构建后端接口和数据库设计。支持前端技术栈（React/Vue/Angular）和后端技术栈（Spring Boot/Node.js/Django/Laravel/FastAPI），提供项目脚手架生成、代码模板生成、数据库DDL生成等能力。
---

# 全栈工程师助手

## 任务目标
- 本 Skill 用于：根据UI设计文档、项目架构方案和需求文档，完成前端项目构建、后端接口开发和数据库设计
- 能力包含：
  - 前端项目初始化与组件生成
  - 后端接口代码生成（Controller/Service/Repository）
  - 数据库表结构设计与DDL脚本生成
  - 技术栈选型建议
- 触发条件：用户提供UI设计文档、项目需求文档、接口定义或数据库设计需求

## 前置准备
- 依赖说明：
  - 无外部依赖，使用Python标准库
  - 脚本仅生成代码模板，不执行项目构建

## 操作步骤

### 1. 前端开发流程

参考 [references/frontend-development.md](references/frontend-development.md) 获取详细指南：
- 技术栈选型（React/Vue/Angular对比）
- 项目初始化命令
- 组件开发最佳实践
- 状态管理选择
- API调用封装
- 路由配置

### 2. 后端开发流程

参考 [references/backend-development.md](references/backend-development.md) 获取详细指南：
- 技术栈选型（Spring Boot/Node.js/Django/FastAPI对比）
- 项目初始化命令
- 分层架构设计
- 接口设计规范
- Repository层实现
- 数据库设计

### 3. 数据库设计流程

参考 [references/database-design-guide.md](references/database-design-guide.md) 获取完整指南。

## 资源索引

- 必要脚本：
  - [scripts/generate_frontend_project.py](scripts/generate_frontend_project.py)（生成前端项目骨架）
  - [scripts/generate_backend_api.py](scripts/generate_backend_api.py)（生成后端接口代码）
  - [scripts/generate_database_ddl.py](scripts/generate_database_ddl.py)（生成数据库DDL脚本）

- 详细指南：
  - [references/frontend-development.md](references/frontend-development.md)（前端开发完整流程）
  - [references/backend-development.md](references/backend-development.md)（后端开发完整流程）
  - [references/component-patterns.md](references/component-patterns.md)（前端组件设计模式）
  - [references/frontend-stack-guide.md](references/frontend-stack-guide.md)（前端技术栈选型对比）
  - [references/backend-stack-guide.md](references/backend-stack-guide.md)（后端技术栈选型对比）
  - [references/api-design-best-practices.md](references/api-design-best-practices.md)（API设计规范）
  - [references/database-design-guide.md](references/database-design-guide.md)（数据库设计规范）

- 代码模板：
  - [assets/frontend-templates/](assets/frontend-templates/)（前端组件模板）
  - [assets/backend-templates/](assets/backend-templates/)（后端代码模板）

## 注意事项
- 脚本仅生成代码骨架和模板，业务逻辑需要智能体根据具体需求填充
- 技术栈选择应考虑团队能力和项目规模，避免过度复杂化
- 数据库设计需要遵循范式原则，同时考虑查询性能
- API设计需要符合RESTful规范，使用统一的响应格式
- 代码生成后需要进行测试和验证

## 使用示例

### 示例 1：React电商前端项目
**用户请求**：根据UI设计文档创建一个React电商前端项目，包含首页、商品列表、购物车页面

**执行方式**：
1. 智能体分析UI设计文档，识别页面结构
2. 调用 `scripts/generate_frontend_project.py` 生成项目骨架
3. 智能体根据设计文档生成页面组件代码
4. 配置路由和状态管理
5. 封装API调用模块

### 示例 2：Spring Boot后端接口开发
**用户请求**：根据需求文档开发用户管理接口，包含用户CRUD操作

**执行方式**：
1. 智能体分析需求，设计接口定义（JSON格式）
2. 调用 `scripts/generate_backend_api.py` 生成Controller/Service/Repository代码
3. 智能体填充业务逻辑和参数验证
4. 生成数据模型（Entity/DTO/VO）
5. 生成API文档

### 示例 3：电商系统数据库设计
**用户请求**：设计一个电商系统的数据库，包含用户、商品、订单表

**执行方式**：
1. 智能体分析需求，识别实体和关系
2. 设计表结构和字段定义（JSON格式）
3. 调用 `scripts/generate_database_ddl.py` 生成DDL脚本
4. 生成ER图描述文档
5. 智能体输出数据库设计说明文档
