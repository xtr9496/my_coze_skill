---
name: fullstack-engineer
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

#### 1.1 技术栈选型
根据项目需求和团队情况选择前端技术栈：
- **React**：组件化强、生态丰富、适合大型应用
- **Vue**：上手简单、文档完善、适合快速开发
- **Angular**：企业级、框架完整、适合大型团队

参考 [references/frontend-stack-guide.md](references/frontend-stack-guide.md)

#### 1.2 项目初始化
调用 `scripts/generate_frontend_project.py` 生成前端项目骨架：

**参数说明**：
- `--project-name`: 项目名称
- `--tech-stack`: 技术栈（react/vue/angular）
- `--output-path`: 输出路径（默认当前目录）

**示例**：
```bash
python scripts/generate_frontend_project.py \
  --project-name my-app \
  --tech-stack react \
  --output-path ./projects
```

#### 1.3 组件开发
根据UI设计文档，智能体分析页面结构：
- 识别页面组件（首页、列表页、详情页等）
- 识别业务组件（按钮、表单、表格等）
- 设计组件层级和状态管理

调用脚本生成组件代码模板，然后由智能体填充业务逻辑。

#### 1.4 路由配置
- 定义路由表
- 配置路由守卫
- 实现页面跳转逻辑

#### 1.5 状态管理
- 选择状态管理方案（Redux/Vuex/Context API）
- 设计状态结构
- 实现状态更新逻辑

#### 1.6 API调用封装
- 封装HTTP请求库（axios/fetch）
- 实现请求拦截和响应拦截
- 统一错误处理

### 2. 后端开发流程

#### 2.1 技术栈选型
根据项目需求选择后端技术栈：
- **Spring Boot**：Java生态、企业级、适合复杂业务
- **Node.js**：JavaScript全栈、高并发、适合实时应用
- **Django**：Python生态、快速开发、适合内容管理
- **Laravel**：PHP生态、开发效率高、适合中小型Web应用
- **FastAPI**：Python生态、高性能、适合API开发和AI/ML应用

参考 [references/backend-stack-guide.md](references/backend-stack-guide.md)

#### 2.2 项目初始化
调用 `scripts/generate_backend_api.py` 生成后端项目骨架：

**参数说明**：
- `--project-path`: 项目路径
- `--tech-stack`: 技术栈（springboot/nodejs/django）
- `--base-package`: 基础包名

**示例**：
```bash
python scripts/generate_backend_api.py \
  --project-path ./backend \
  --tech-stack springboot \
  --base-package com.example.myapp
```

#### 2.3 接口设计
根据需求文档设计RESTful API：
- 定义资源路径（/api/users、/api/orders）
- 定义HTTP方法（GET/POST/PUT/DELETE）
- 定义请求参数和响应格式

参考 [references/api-design-best-practices.md](references/api-design-best-practices.md)

#### 2.4 代码生成
调用脚本生成分层架构代码：
- **Controller层**：处理HTTP请求，参数验证
- **Service层**：业务逻辑处理
- **Repository/DAO层**：数据访问

**接口定义文件格式**（JSON）：
```json
{
  "apis": [
    {
      "name": "UserController",
      "path": "/api/users",
      "methods": [
        {
          "name": "getUsers",
          "httpMethod": "GET",
          "description": "获取用户列表",
          "parameters": [
            {"name": "page", "type": "Integer", "required": false},
            {"name": "size", "type": "Integer", "required": false}
          ],
          "responseType": "List<UserVO>"
        }
      ]
    }
  ]
}
```

#### 2.5 数据模型生成
根据接口定义生成数据模型：
- **Entity**：数据库实体
- **DTO**：数据传输对象
- **VO**：视图对象

### 3. 数据库设计流程

#### 3.1 需求分析
智能体分析需求文档，识别核心实体和关系：
- 用户、订单、商品等业务实体
- 一对一、一对多、多对多关系
- 业务规则和约束

参考 [references/database-design-guide.md](references/database-design-guide.md)

#### 3.2 表结构设计
设计表结构，定义字段：
- 字段名称、类型、长度
- 主键、外键、索引
- 默认值、非空约束、唯一约束

#### 3.3 DDL脚本生成
调用 `scripts/generate_database_ddl.py` 生成SQL脚本：

**参数说明**：
- `--schema-file`: 表结构定义文件（JSON格式）
- `--db-type`: 数据库类型（mysql/postgresql）
- `--output-file`: 输出文件路径

**表结构定义文件格式**（JSON）：
```json
{
  "tables": [
    {
      "name": "users",
      "comment": "用户表",
      "columns": [
        {
          "name": "id",
          "type": "BIGINT",
          "primary": true,
          "autoIncrement": true,
          "comment": "用户ID"
        },
        {
          "name": "username",
          "type": "VARCHAR(50)",
          "notNull": true,
          "unique": true,
          "comment": "用户名"
        },
        {
          "name": "email",
          "type": "VARCHAR(100)",
          "notNull": true,
          "comment": "邮箱"
        },
        {
          "name": "created_at",
          "type": "DATETIME",
          "defaultValue": "CURRENT_TIMESTAMP",
          "comment": "创建时间"
        }
      ],
      "indexes": [
        {
          "name": "idx_email",
          "columns": ["email"],
          "comment": "邮箱索引"
        }
      ]
    }
  ]
}
```

**示例**：
```bash
python scripts/generate_database_ddl.py \
  --schema-file ./database/schema.json \
  --db-type mysql \
  --output-file ./database/schema.sql
```

## 资源索引

- 必要脚本：
  - [scripts/generate_frontend_project.py](scripts/generate_frontend_project.py)（生成前端项目骨架）
  - [scripts/generate_backend_api.py](scripts/generate_backend_api.py)（生成后端接口代码）
  - [scripts/generate_database_ddl.py](scripts/generate_database_ddl.py)（生成数据库DDL脚本）

- 领域参考：
  - [references/frontend-stack-guide.md](references/frontend-stack-guide.md)（前端技术栈选型）
  - [references/backend-stack-guide.md](references/backend-stack-guide.md)（后端技术栈选型）
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
